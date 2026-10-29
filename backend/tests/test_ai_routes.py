import json
from uuid import uuid4
import pytest
from test_ai_research import research_output
from test_ai_writing import newsletter
from app.database import Project
from app.main import app
from app.database import get_db


def setup_project(client):
    pid = client.post("/api/projects", json={"title": "AI flow"}).json()["id"]
    for i in range(1, 4):
        response = client.post(f"/api/projects/{pid}/sources", json={"title": f"Source {i}", "url": f"https://example.com/{i}", "content": f"Source {i} reports a controlled local evaluation with 16 GB of memory. The result needs independent review."})
        assert response.status_code == 201
    return pid


def wire_output(client, pid, output):
    ids = [s["id"] for s in client.get(f"/api/projects/{pid}").json()["sources"]]
    text = json.dumps(output)
    for i, sid in enumerate(ids, 1):
        text = text.replace('"s' + str(i) + '"', '"' + sid + '"')
    return json.loads(text)


def fake_stream(output):
    def stream(*args):
        yield {"type": "progress", "characters": 20}
        yield {"type": "result", "value": output, "usage": {"total_token_count": 100}}
    return stream


def events(response):
    assert response.status_code == 200, response.text
    return [json.loads(line) for line in response.text.splitlines()]


def test_generation_disabled_without_key(client):
    pid = setup_project(client)
    result = client.post(f"/api/projects/{pid}/ai/generate", json={"request_id": str(uuid4()), "kind": "brief"})
    assert result.status_code == 503
    assert client.get("/api/ai/config").json()["configured"] is False


def test_research_stream_persists_metadata_and_replays_without_cost(client, monkeypatch):
    import app.ai_routes as routes
    monkeypatch.setenv("GEMINI_API_KEY", "synthetic-test-key")
    pid = setup_project(client)
    monkeypatch.setattr(routes, "iter_gemini", fake_stream(wire_output(client, pid, research_output())))
    payload = {"request_id": str(uuid4()), "kind": "brief"}
    stream = events(client.post(f"/api/projects/{pid}/ai/generate", json=payload))
    assert [e["type"] for e in stream] == ["started", "progress", "complete"]
    assert stream[-1]["project"]["brief"]["method"] == "gemini"
    assert stream[-1]["job"]["usage"]["total_token_count"] == 100
    replay = events(client.post(f"/api/projects/{pid}/ai/generate", json=payload))[-1]
    assert replay["cached"] is True
    assert client.get("/api/ai/usage").json()["requests"] == 1
    assert len(client.get(f"/api/projects/{pid}/ai/jobs").json()) == 1


def test_invalid_evidence_does_not_replace_saved_brief(client, monkeypatch):
    import app.ai_routes as routes
    monkeypatch.setenv("GEMINI_API_KEY", "synthetic-test-key")
    pid = setup_project(client)
    before = client.post(f"/api/projects/{pid}/brief").json()["brief"]
    output = wire_output(client, pid, research_output())
    output["items"][0]["claims"][0]["evidence"][0]["excerpt"] = "Invented source quotation that never occurred."
    monkeypatch.setattr(routes, "iter_gemini", fake_stream(output))
    stream = events(client.post(f"/api/projects/{pid}/ai/generate", json={"request_id": str(uuid4()), "kind": "brief"}))
    assert stream[-1]["type"] == "error"
    assert stream[-1]["code"] == "invalid_evidence"
    assert client.get(f"/api/projects/{pid}").json()["brief"] == before
    assert client.get(f"/api/projects/{pid}/ai/jobs").json()[0]["status"] == "failed"


def test_newsletter_requires_review_and_preserves_original(client, monkeypatch):
    import app.ai_routes as routes
    monkeypatch.setenv("GEMINI_API_KEY", "synthetic-test-key")
    pid = setup_project(client)
    client.post(f"/api/projects/{pid}/brief")
    client.put(f"/api/projects/{pid}/draft", json={"text": "An original draft worth preserving."})
    monkeypatch.setattr(routes, "iter_gemini", fake_stream(wire_output(client, pid, newsletter())))
    result = events(client.post(f"/api/projects/{pid}/ai/generate", json={"request_id": str(uuid4()), "kind": "newsletter", "version": 1}))[-1]
    assert result["project"]["draft"]["current"] == "An original draft worth preserving."
    jid = result["job"]["id"]
    applied = client.post(f"/api/projects/{pid}/ai/jobs/{jid}/apply", json={"version": 1})
    assert applied.status_code == 200
    draft = applied.json()["draft"]
    assert draft["original"] == "An original draft worth preserving."
    assert draft["current"].startswith("# A controlled test")
    assert draft["version"] == 2
    assert client.post(f"/api/projects/{pid}/ai/jobs/{jid}/apply", json={"version": 2}).status_code == 409


def test_newsletter_cannot_apply_after_manual_edit(client, monkeypatch):
    import app.ai_routes as routes
    monkeypatch.setenv("GEMINI_API_KEY", "synthetic-test-key")
    pid = setup_project(client)
    client.post(f"/api/projects/{pid}/brief")
    monkeypatch.setattr(routes, "iter_gemini", fake_stream(wire_output(client, pid, newsletter())))
    job = events(client.post(f"/api/projects/{pid}/ai/generate", json={"request_id": str(uuid4()), "kind": "newsletter"}))[-1]["job"]
    client.put(f"/api/projects/{pid}/draft", json={"text": "New manual text."})
    assert client.post(f"/api/projects/{pid}/ai/jobs/{job['id']}/apply", json={"version": 1}).status_code == 409


def test_request_limit_is_persisted(client, monkeypatch):
    import app.ai_routes as routes
    monkeypatch.setenv("GEMINI_API_KEY", "synthetic-test-key")
    monkeypatch.setenv("AI_DAILY_REQUEST_LIMIT", "1")
    pid = setup_project(client)
    monkeypatch.setattr(routes, "iter_gemini", fake_stream(wire_output(client, pid, research_output())))
    events(client.post(f"/api/projects/{pid}/ai/generate", json={"request_id": str(uuid4()), "kind": "brief"}))
    assert client.post(f"/api/projects/{pid}/ai/generate", json={"request_id": str(uuid4()), "kind": "brief"}).status_code == 429


def test_source_change_during_stream_discards_result(client, monkeypatch):
    import app.ai_routes as routes
    monkeypatch.setenv("GEMINI_API_KEY", "synthetic-test-key")
    pid = setup_project(client)
    output = wire_output(client, pid, research_output())
    def stream(*args):
        dependency = app.dependency_overrides[get_db]()
        db = next(dependency)
        project = db.get(Project, pid)
        project.sources[0].content = "Changed source content with enough text for a new interpretation."
        db.commit()
        dependency.close()
        yield {"type": "result", "value": output, "usage": {}}
    monkeypatch.setattr(routes, "iter_gemini", stream)
    result = events(client.post(f"/api/projects/{pid}/ai/generate", json={"request_id": str(uuid4()), "kind": "brief"}))[-1]
    assert result["code"] == "stale_generation"
    assert client.get(f"/api/projects/{pid}").json()["brief"] is None


def test_writing_suggestions_remain_individually_reviewable(client, monkeypatch):
    import app.ai_routes as routes
    monkeypatch.setenv("GEMINI_API_KEY", "synthetic-test-key")
    pid = setup_project(client)
    original = "We use 16 GB in order to test the model."
    client.put(f"/api/projects/{pid}/draft", json={"text": original})
    output = {"summary": "One clarity improvement.", "suggestions": [{"kind": "Clarity", "passage": original, "replacement": "We use 16 GB to test the model.", "explanation": "Remove filler while preserving the number.", "occurrence": 0}]}
    monkeypatch.setattr(routes, "iter_gemini", fake_stream(output))
    complete = events(client.post(f"/api/projects/{pid}/ai/generate", json={"request_id": str(uuid4()), "kind": "writing", "version": 1}))[-1]
    draft = complete["project"]["draft"]
    assert draft["current"] == original
    ai = next(s for s in draft["suggestions"] if s.get("provider") == "gemini")
    accepted = client.post(f"/api/projects/{pid}/suggestions/{ai['id']}", json={"action": "accept", "version": 1}).json()["draft"]
    assert accepted["original"] == original
    assert accepted["current"] == "We use 16 GB to test the model."
