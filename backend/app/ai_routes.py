import hashlib
import json
from contextlib import closing
from datetime import datetime, timezone
from typing import Literal
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .config import get_settings
from .database import get_db, Project, Draft, GenerationJob
from .serializers import project_json
from .limits import reserve_request, day_key, used_requests
from .gemini import AIError, iter_gemini
from .ai_editorial import SCHEMAS, CONVERTERS, make_prompt
from .writing import analyze

router = APIRouter(prefix="/api")


class GenerationInput(BaseModel):
    request_id: UUID
    kind: Literal["brief", "writing", "newsletter"]
    version: int | None = Field(default=None, ge=1)


class ApplyInput(BaseModel):
    version: int | None = Field(default=None, ge=1)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def project_for_update(db, project_id):
    project = db.scalars(select(Project).where(Project.id == project_id).with_for_update()).first()
    if project is None:
        raise HTTPException(404, "Project not found")
    return project


def snapshot_project(project, kind):
    sources = [{"id": s.id, "source_number": i, "title": s.title, "url": s.url, "content": s.content,
                "kind": s.kind, "reliability": s.reliability} for i, s in enumerate(project.sources, 1)]
    return {"sources": sources, "draft_text": project.draft.current if project.draft and kind != "brief" else "",
            "brief": project.brief if kind == "newsletter" else None}


def input_fingerprint(project, kind):
    version = project.draft.version if project.draft and kind != "brief" else None
    return digest({"kind": kind, "snapshot": snapshot_project(project, kind), "version": version})


def job_json(job, include_result=True):
    result = {"id": job.id, "kind": job.kind, "status": job.status, "provider": job.provider, "model": job.model,
              "created_at": job.created_at.isoformat(), "finished_at": job.finished_at.isoformat() if job.finished_at else None,
              "draft_version": job.draft_version, "usage": job.usage, "error_code": job.error_code}
    if include_result:
        result["result"] = job.result
    return result


def ndjson(event):
    return json.dumps(event, ensure_ascii=False) + "\n"


def replay(job, project):
    if job.status in ("complete", "applied"):
        event = {"type": "complete", "job": job_json(job), "project": project_json(project), "cached": True}
        return StreamingResponse(iter([ndjson(event)]), media_type="application/x-ndjson", headers={"Cache-Control": "no-store"})
    if job.status == "running":
        raise HTTPException(409, "This request is already running. Check its saved status before retrying.")
    raise HTTPException(409, "This request failed or was cancelled. Start a new request to retry.")


@router.get("/ai/config")
def ai_config():
    settings = get_settings()
    return {"configured": bool(settings.gemini_api_key), "provider": "gemini", "model": settings.gemini_model,
            "daily_request_limit": settings.ai_daily_request_limit, "max_input_chars": settings.ai_max_input_chars,
            "max_output_tokens": settings.ai_max_output_tokens, "stream": "validated-progress"}


@router.get("/ai/usage")
def ai_usage(db: Session = Depends(get_db)):
    limit = get_settings().ai_daily_request_limit
    used = used_requests(db)
    return {"date": day_key()[3:], "requests": used, "limit": limit, "remaining": max(0, limit - used),
            "note": "Request cap, not a currency budget. Failed provider attempts count; cached replays do not."}


@router.get("/projects/{project_id}/ai/jobs")
def list_jobs(project_id: str, db: Session = Depends(get_db)):
    project_for_update(db, project_id)
    jobs = db.scalars(select(GenerationJob).where(GenerationJob.project_id == project_id).order_by(GenerationJob.created_at.desc()).limit(10))
    return [job_json(job) for job in jobs]


@router.get("/projects/{project_id}/ai/jobs/{job_id}")
def get_job(project_id: str, job_id: str, db: Session = Depends(get_db)):
    job = db.get(GenerationJob, job_id)
    if job is None or job.project_id != project_id:
        raise HTTPException(404, "Generation request not found")
    return job_json(job)


@router.post("/projects/{project_id}/ai/generate")
def generate(project_id: str, data: GenerationInput, db: Session = Depends(get_db)):
    project = project_for_update(db, project_id)
    existing = db.get(GenerationJob, str(data.request_id))
    if existing:
        if existing.project_id != project_id or existing.kind != data.kind:
            raise HTTPException(409, "Request ID belongs to another operation.")
        if data.kind != "brief" and data.version != existing.draft_version:
            raise HTTPException(409, "Request ID was submitted for a different draft version.")
        if existing.status != "applied" and input_fingerprint(project, data.kind) != existing.fingerprint:
            raise HTTPException(409, "The inputs changed since this request. Start a fresh request.")
        # A replay never reapplies an old result or consumes another provider call.
        return replay(existing, project)
    settings = get_settings()
    if not settings.gemini_api_key:
        raise HTTPException(503, "Gemini is not configured. Add GEMINI_API_KEY to the backend environment.")
    if data.kind in ("brief", "newsletter") and len(project.sources) < 3:
        raise HTTPException(422, "Gemini research and newsletters require at least three sources.")
    if data.kind == "newsletter" and not project.brief:
        raise HTTPException(422, "Build a research brief before generating a newsletter.")
    if data.kind != "brief":
        version = project.draft.version if project.draft else None
        if data.version != version:
            raise HTTPException(409, "Draft changed. Reload the project before generating.")
        if data.kind == "writing" and not project.draft:
            raise HTTPException(422, "Save a draft before requesting Gemini writing suggestions.")
    snapshot = snapshot_project(project, data.kind)
    prompt = make_prompt(data.kind, snapshot)
    if len(prompt) > settings.ai_max_input_chars:
        raise HTTPException(422, "AI input limit exceeded. Shorten the source text or draft.")
    job = GenerationJob(id=str(data.request_id), project_id=project.id, kind=data.kind, status="running",
        fingerprint=input_fingerprint(project, data.kind), source_fingerprint=digest(snapshot["sources"]),
        draft_version=project.draft.version if project.draft and data.kind != "brief" else None,
        model=settings.gemini_model, usage={})
    try:
        reserve_request(db, day_key(), settings.ai_daily_request_limit)
        db.add(job)
        db.commit()
    except AIError as error:
        raise HTTPException(error.status, {"code": error.code, "message": error.message}) from None
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Request was already submitted. Check its saved status.") from None

    def events():
        finished = False
        try:
            yield ndjson({"type": "started", "job_id": job.id, "model": settings.gemini_model})
            with closing(iter_gemini(prompt, SCHEMAS[data.kind])) as stream:
                for event in stream:
                    if event["type"] == "progress":
                        yield ndjson(event)
                        continue
                    result = CONVERTERS[data.kind](event["value"], snapshot)
                    db.expire_all()
                    current = project_for_update(db, project_id)
                    active_job = db.get(GenerationJob, job.id)
                    if input_fingerprint(current, data.kind) != active_job.fingerprint:
                        raise AIError("stale_generation", "The sources, brief or draft changed during generation. Nothing was applied.", 409)
                    active_job.usage = event.get("usage", {})
                    active_job.result = result
                    active_job.status = "complete"
                    active_job.finished_at = datetime.now(timezone.utc)
                    metadata = {"job_id": active_job.id, "provider": "gemini", "model": active_job.model,
                                "generated_at": active_job.finished_at.isoformat(), "usage": active_job.usage}
                    if data.kind == "brief":
                        current.brief = {**result, "generation": metadata}
                    elif data.kind == "writing":
                        current.draft.suggestions = [*analyze(current.draft.current), *result["suggestions"]]
                    db.commit()
                    finished = True
                    yield ndjson({"type": "complete", "job": job_json(active_job), "project": project_json(current)})
                    return
            if not finished:
                raise AIError("empty_response", "Gemini returned no complete result. Nothing was applied.")
        except AIError as error:
            db.rollback()
            failed = db.get(GenerationJob, str(data.request_id))
            failed.status, failed.error_code = "failed", error.code
            failed.finished_at = datetime.now(timezone.utc)
            db.commit()
            finished = True
            yield ndjson({"type": "error", "code": error.code, "message": error.message})
        except Exception:
            db.rollback()
            failed = db.get(GenerationJob, str(data.request_id))
            if failed:
                failed.status, failed.error_code = "failed", "generation_failed"
                failed.finished_at = datetime.now(timezone.utc)
                db.commit()
            finished = True
            yield ndjson({"type": "error", "code": "generation_failed", "message": "Generation could not be saved. Check request history before retrying."})
        finally:
            if not finished:
                db.rollback()
                cancelled = db.get(GenerationJob, str(data.request_id))
                if cancelled and cancelled.status == "running":
                    cancelled.status, cancelled.error_code = "cancelled", "cancelled"
                    cancelled.finished_at = datetime.now(timezone.utc)
                    db.commit()
    return StreamingResponse(events(), media_type="application/x-ndjson", headers={"Cache-Control": "no-store", "X-Accel-Buffering": "no"})


@router.post("/projects/{project_id}/ai/jobs/{job_id}/apply")
def apply_newsletter(project_id: str, job_id: str, data: ApplyInput, db: Session = Depends(get_db)):
    project = project_for_update(db, project_id)
    job = db.get(GenerationJob, job_id)
    if job is None or job.project_id != project_id or job.kind != "newsletter":
        raise HTTPException(404, "Newsletter generation not found")
    if job.status != "complete" or not job.result:
        raise HTTPException(409, "This newsletter is unavailable or was already applied.")
    version = project.draft.version if project.draft else None
    if data.version != version or input_fingerprint(project, "newsletter") != job.fingerprint:
        raise HTTPException(409, "The project changed after generation. Create a fresh newsletter before applying.")
    text = job.result["text"]
    if project.draft:
        draft = project.draft
        draft.revisions = [*draft.revisions, {"version": draft.version, "text": draft.current, "reason": "Reviewed Gemini newsletter"}]
        draft.current, draft.suggestions = text, []
        draft.version += 1
    else:
        project.draft = Draft(original=text, current=text, suggestions=[], revisions=[])
    job.status = "applied"
    db.commit()
    return project_json(project)
