import os
from contextlib import asynccontextmanager
from typing import Literal
from fastapi import FastAPI, Depends, HTTPException, Response, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from .database import Base, engine, get_db, Project, Source, Draft
from .research import canonical_url, fetch_article, build_brief
from .writing import analyze, decide, metrics
from .serializers import draft_json, project_json
from .config import get_settings
from .ai_routes import router as ai_router
from .auth import router as auth_router, authenticated


@asynccontextmanager
async def lifespan(app):
    settings = get_settings()
    if settings.cloud and (not settings.database_url.startswith("postgresql+") or len(settings.workspace_password) < 12 or len(settings.session_secret) < 32):
        raise RuntimeError("Hosted workspace requires PostgreSQL and complete access configuration.")
    # Migrations are the deployment path; create_all is only for zero-setup SQLite.
    if engine.url.drivername.startswith("sqlite"):
        Base.metadata.create_all(engine)
    yield


app = FastAPI(title="AI Editorial Workspace", version="1.0.0", lifespan=lifespan)



class ProjectInput(BaseModel):
    title: str = Field(min_length=1, max_length=160)

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value):
        if not value.strip():
            raise ValueError("Title cannot be blank")
        return value.strip()


class SourceInput(BaseModel):
    title: str = Field(min_length=1, max_length=240)
    url: str | None = Field(default=None, max_length=2048)
    content: str = Field(default="", max_length=50000)
    kind: Literal["article", "tweet", "report"] = "article"
    reliability: Literal["primary", "secondary", "unverified"] = "unverified"


class DraftInput(BaseModel):
    text: str = Field(min_length=1, max_length=50000)
    version: int | None = Field(default=None, ge=1)


class DecisionInput(BaseModel):
    action: Literal["accept", "reject"]
    version: int = Field(ge=1)
    replacement: str | None = Field(default=None, max_length=50000)


def find_project(db, project_id):
    project = db.scalars(select(Project).where(Project.id == project_id).with_for_update()).first()
    if project is None:
        raise HTTPException(404, "Project not found")
    return project


def check_version(draft, version):
    if version != draft.version:
        raise HTTPException(409, "Draft changed. Reload the project before editing.")


@app.get("/api/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "mode": "gemini-enabled" if get_settings().gemini_api_key else "deterministic", "version": "1.0.0"}


@app.get("/api/projects")
def list_projects(db: Session = Depends(get_db)):
    return [{"id": p.id, "title": p.title, "source_count": len(p.sources)} for p in db.scalars(select(Project).order_by(Project.created_at.desc()))]


@app.post("/api/projects", status_code=201)
def create_project(data: ProjectInput, db: Session = Depends(get_db)):
    project = Project(title=data.title)
    db.add(project)
    db.commit()
    return project_json(project)


@app.get("/api/projects/{project_id}")
def get_project(project_id: str, db: Session = Depends(get_db)):
    return project_json(find_project(db, project_id))


@app.post("/api/projects/{project_id}/sources", status_code=201)
def add_source(project_id: str, data: SourceInput, db: Session = Depends(get_db)):
    project = find_project(db, project_id)
    if len(project.sources) >= 20:
        raise HTTPException(422, "A project supports at most 20 sources.")
    try:
        url = canonical_url(data.url) if data.url else None
        content, title = data.content.strip(), data.title.strip()
        if not title:
            raise ValueError("Provide a source title.")
        if not content:
            if not url:
                raise ValueError("Paste source content or supply a public URL.")
            imported = fetch_article(url)
            content = imported["content"]
        if len(content) < 40:
            raise ValueError("Include at least 40 characters of source content.")
        if any((url and canonical_url(s.url) == url) or s.content.strip() == content for s in project.sources):
            raise ValueError("This source is already in the project.")
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    project.sources.append(Source(title=title, url=url, content=content, kind=data.kind, reliability=data.reliability))
    project.brief = None
    db.commit()
    return project_json(project)


@app.delete("/api/projects/{project_id}/sources/{source_id}")
def remove_source(project_id: str, source_id: str, db: Session = Depends(get_db)):
    project = find_project(db, project_id)
    source = next((s for s in project.sources if s.id == source_id), None)
    if source is None:
        raise HTTPException(404, "Source not found")
    project.sources.remove(source)
    project.brief = None
    db.commit()
    return project_json(project)


@app.post("/api/projects/{project_id}/brief")
def generate_brief(project_id: str, db: Session = Depends(get_db)):
    project = find_project(db, project_id)
    try:
        project.brief = build_brief(project.sources)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    db.commit()
    return project_json(project)


@app.put("/api/projects/{project_id}/draft")
def save_draft(project_id: str, data: DraftInput, db: Session = Depends(get_db)):
    project = find_project(db, project_id)
    if not data.text.strip():
        raise HTTPException(422, "Draft cannot be empty.")
    if project.draft is None:
        project.draft = Draft(original=data.text, current=data.text, suggestions=[], revisions=[])
    else:
        check_version(project.draft, data.version)
        draft = project.draft
        if draft.current != data.text:
            draft.revisions = [*draft.revisions, {"version": draft.version, "text": draft.current, "reason": "Manual edit"}]
            draft.current = data.text
            draft.version += 1
            draft.suggestions = []
    db.commit()
    return project_json(project)


@app.post("/api/projects/{project_id}/analyze")
def analyze_draft(project_id: str, data: DraftInput, db: Session = Depends(get_db)):
    project = find_project(db, project_id)
    if project.draft is None:
        raise HTTPException(422, "Save a draft first.")
    check_version(project.draft, data.version)
    if data.text != project.draft.current:
        raise HTTPException(409, "Save your draft before running checks.")
    project.draft.suggestions = analyze(project.draft.current)
    db.commit()
    return project_json(project)


@app.post("/api/projects/{project_id}/suggestions/{suggestion_id}")
def resolve_suggestion(project_id: str, suggestion_id: str, data: DecisionInput, db: Session = Depends(get_db)):
    project = find_project(db, project_id)
    if project.draft is None:
        raise HTTPException(422, "Save a draft first.")
    check_version(project.draft, data.version)
    try:
        decide(project.draft, suggestion_id, data.action, data.replacement)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    db.commit()
    return project_json(project)


@app.get("/api/projects/{project_id}/export")
def export_project(project_id: str, db: Session = Depends(get_db)):
    project = find_project(db, project_id)
    body = "# " + project.title + "\n\n" + (project.draft.current if project.draft else "") + "\n\n## Sources\n"
    for i, source in enumerate(project.sources, 1):
        body += f"\n{i}. {source.title} — {source.url or 'Pasted text (no public URL)'} [{source.reliability}]\n"
    return Response(body, media_type="text/markdown", headers={"Content-Disposition": 'attachment; filename="editorial.md"'})


app.include_router(ai_router)


@app.middleware("http")
async def protect_workspace(request: Request, call_next):
    settings = get_settings()
    if settings.cloud and (not settings.database_url.startswith("postgresql+") or len(settings.workspace_password) < 12 or len(settings.session_secret) < 32):
        return JSONResponse({"detail": "Hosted workspace configuration is incomplete."}, status_code=503)
    public = {"/api/health", "/api/auth/session", "/api/auth/login"}
    origin = request.headers.get("origin")
    if request.method not in ("GET", "HEAD", "OPTIONS") and origin:
        own_origin = str(request.base_url).rstrip("/")
        if origin not in settings.cors_origins and origin != own_origin:
            return JSONResponse({"detail": "This request origin is not allowed."}, status_code=403)
    if request.method != "OPTIONS" and request.url.path not in public:
        if (request.url.path.startswith("/api/") or request.url.path in ("/docs", "/openapi.json")) and not authenticated(request, settings):
            return JSONResponse({"detail": "Sign in to the workspace to continue."}, status_code=401)
    response = await call_next(request)
    if request.url.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-store"
    return response

app.include_router(auth_router)

app.add_middleware(CORSMiddleware, allow_origins=list(get_settings().cors_origins), allow_credentials=True, allow_methods=["GET", "POST", "PUT", "DELETE"], allow_headers=["Content-Type"])
