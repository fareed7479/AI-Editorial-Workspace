"""Opt-in release check against the configured DB; all diagnostic writes roll back.

Run after Alembic. --live-ai makes up to three real billable Gemini requests.
No credentials, source text or generated text are printed.
"""
import argparse
import json
from uuid import uuid4
from fastapi.testclient import TestClient
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.main import app


SOURCES = [
    ("Controlled release note", "Cedar Labs reports a fictional local inference evaluation using 16 GB of memory. The evaluation uses a controlled test workload, not production traffic. The team has not published independent benchmark results. Its release note describes local execution as an option for developers who need to inspect deployment requirements. Availability does not establish suitability for every task. The team says builders should test their own workload before making a deployment decision. Licensing and hardware compatibility still require review. This is synthetic material for software verification, not a real product announcement."),
    ("Controlled engineering report", "A fictional engineering team describes a prototype that runs on a local workstation. The report says response quality depends on the workload and configuration. It provides no production reliability guarantee. Engineers recommend recording memory use, response latency, and failure cases during evaluation. They distinguish a successful demonstration from a supported production deployment. The report does not establish comparative performance against hosted services. Its observations apply only to the prototype discussed here. This synthetic report is supplied solely to verify editorial software behavior and should not be treated as independent corroboration."),
    ("Controlled editorial review", "A fictional editorial review asks readers to separate publisher claims from independent evidence. It notes that local operation can change operational responsibilities, but does not prove better quality or lower overall cost. Editors should retain source attribution, uncertainty, and technical qualifications when summarizing a release. The review recommends a small workload-specific pilot rather than a universal recommendation. It does not provide benchmark numbers or a release date. This is synthetic source material used for a controlled software release check, not current news or a verified factual account."),
]


def verify(live_ai=False):
    required = {"projects", "sources", "drafts", "generation_jobs", "request_quotas"}
    assert required <= set(inspect(engine).get_table_names()), "Missing migrated tables"
    with engine.connect() as connection:
        transaction = connection.begin()
        session = Session(bind=connection, join_transaction_mode="create_savepoint")
        app.dependency_overrides[get_db] = lambda: session
        try:
            with TestClient(app) as client:
                def call(method, url, data=None, status=200):
                    response = client.request(method, "/api" + url, json=data)
                    assert response.status_code == status, f"{method} {url}: HTTP {response.status_code}"
                    return response

                call("GET", "/health")
                project = call("POST", "/projects", {"title": "Release verification (rolled back)"}, 201).json()
                base = "/projects/" + project["id"]
                call("POST", base + "/brief", status=422)
                for title, content in SOURCES:
                    project = call("POST", base + "/sources", {"title": title, "content": content}, 201).json()
                call("POST", base + "/sources", {"title": SOURCES[0][0], "content": SOURCES[0][1]}, 422)
                call("POST", base + "/brief")
                original = "In order to review it, the prototype was tested by the team. The evidence needs independent review."
                project = call("PUT", base + "/draft", {"text": original}).json()
                project = call("POST", base + "/analyze", {"text": original, "version": 1}).json()
                suggestions = project["draft"]["suggestions"]
                assert suggestions, "Expected controlled writing suggestions"
                project = call("POST", base + "/suggestions/" + suggestions[0]["id"], {"action": "reject", "version": 1}).json()
                remaining = next(s for s in project["draft"]["suggestions"] if s["status"] == "pending")
                project = call("POST", base + "/suggestions/" + remaining["id"], {"action": "accept", "version": 1, "replacement": "The team tested the prototype for review."}).json()
                assert project["draft"]["original"] == original
                call("PUT", base + "/draft", {"text": "Stale edit", "version": 1}, 409)
                assert original == call("GET", base).json()["draft"]["original"]
                assert "## Sources" in call("GET", base + "/export").text
                print("RELEASE_CORE_OK: PostgreSQL, sources, brief, editing, decisions, revisions, stale checks, export", flush=True)
                if live_ai:
                    for kind in ("brief", "writing", "newsletter"):
                        version = project["draft"]["version"]
                        payload = {"request_id": str(uuid4()), "kind": kind, "version": None if kind == "brief" else version}
                        response = call("POST", base + "/ai/generate", payload)
                        events = [json.loads(line) for line in response.text.splitlines() if line.strip()]
                        final = events[-1]
                        assert final["type"] == "complete", f"Gemini {kind}: {final.get('code', 'incomplete')}"
                        project = final["project"]
                        replay = call("POST", base + "/ai/generate", payload)
                        assert json.loads(replay.text.splitlines()[-1])["cached"]
                        if kind == "newsletter":
                            assert project["draft"]["current"] != final["job"]["result"]["text"]
                            project = call("POST", base + "/ai/jobs/" + final["job"]["id"] + "/apply", {"version": version}).json()
                            assert project["draft"]["original"] == original
                            assert "## Sources" in call("GET", base + "/export").text
                        print("RELEASE_GEMINI_OK:", kind, "model=" + final["job"]["model"], flush=True)
                call("DELETE", base + "/sources/" + project["sources"][0]["id"])
                assert call("GET", base).json()["brief"] is None
        finally:
            app.dependency_overrides.pop(get_db, None)
            session.close()
            transaction.rollback()
    print("RELEASE_ROLLBACK_OK: diagnostic records and quota changes were not retained", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--live-ai", action="store_true")
    args = parser.parse_args()
    try:
        verify(args.live_ai)
    except Exception as error:
        # Assertion messages contain only operation/status, never secrets/provider bodies.
        print("RELEASE_CHECK_FAILED:", str(error) if isinstance(error, AssertionError) else type(error).__name__, flush=True)
        raise SystemExit(1)

