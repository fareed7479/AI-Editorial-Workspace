import socket
from types import SimpleNamespace
import pytest
from app.research import canonical_url, validate_public_url, fetch_article
from app.writing import analyze, metrics, decide


def create(client):
    response = client.post("/api/projects", json={"title": "Weekly brief"})
    assert response.status_code == 201
    return response.json()["id"]


def test_complete_persisted_workflow(client):
    pid = create(client)
    assert client.post(f"/api/projects/{pid}/brief").status_code == 422
    for i in range(3):
        response = client.post(f"/api/projects/{pid}/sources", json={"title": f"Report {i}", "url": f"https://example.com/report/{i}", "content": f"Source {i} reports a controlled test of a local model. The result needs independent verification."})
        assert response.status_code == 201
    brief = client.post(f"/api/projects/{pid}/brief").json()["brief"]
    assert len(brief["items"]) == 3
    for item in brief["items"]:
        assert item["what_happened"][0]["url"].startswith("https://")
        assert item["what_happened"][0]["verified"] is False
        assert item["why_it_matters"]["type"] == "analysis"
    text = "We use a small model in order to label documents. The model was tested carefully."
    draft = client.put(f"/api/projects/{pid}/draft", json={"text": text}).json()["draft"]
    result = client.post(f"/api/projects/{pid}/analyze", json={"text": text, "version": draft["version"]})
    assert result.status_code == 200
    draft = result.json()["draft"]
    filler = next(s for s in draft["suggestions"] if s["kind"] == "Filler phrase")
    accepted = client.post(f"/api/projects/{pid}/suggestions/{filler['id']}", json={"action": "accept", "version": draft["version"]}).json()["draft"]
    assert accepted["original"] == text
    assert "in order to" not in accepted["current"]
    assert accepted["version"] == 2
    assert len(accepted["revisions"]) == 1
    assert client.get(f"/api/projects/{pid}").json()["draft"]["current"] == accepted["current"]
    exported = client.get(f"/api/projects/{pid}/export")
    assert exported.status_code == 200 and "## Sources" in exported.text
    assert "Report 2" in exported.text


def test_reject_and_stale_version(client):
    pid = create(client)
    text = "We really need to test this model."
    client.put(f"/api/projects/{pid}/draft", json={"text": text})
    draft = client.post(f"/api/projects/{pid}/analyze", json={"text": text, "version": 1}).json()["draft"]
    sid = draft["suggestions"][0]["id"]
    rejected = client.post(f"/api/projects/{pid}/suggestions/{sid}", json={"action": "reject", "version": 1}).json()["draft"]
    assert rejected["current"] == text
    assert rejected["suggestions"][0]["status"] == "rejected"
    assert client.put(f"/api/projects/{pid}/draft", json={"text": "New text", "version": 99}).status_code == 409
    assert client.post(f"/api/projects/{pid}/suggestions/{sid}", json={"action": "accept", "version": 1}).status_code == 422


def test_duplicates_and_invalidation(client):
    pid = create(client)
    data = {"title": "Original", "url": "https://example.com/report/", "content": "A sufficiently detailed source statement for our research briefing."}
    first = client.post(f"/api/projects/{pid}/sources", json=data).json()
    assert client.post(f"/api/projects/{pid}/sources", json={**data, "url": "https://example.com/report#fragment"}).status_code == 422
    assert client.post(f"/api/projects/{pid}/sources", json={**data, "url": None}).status_code == 422
    source_id = first["sources"][0]["id"]
    assert client.delete(f"/api/projects/{pid}/sources/{source_id}").json()["sources"] == []
    assert client.delete(f"/api/projects/{pid}/sources/{source_id}").status_code == 404


def test_validation(client):
    assert client.post("/api/projects", json={"title": " "}).status_code == 422
    assert client.get("/api/projects/missing").status_code == 404
    pid = create(client)
    for payload in [{"title": "x"}, {"title": "x", "content": "short"}, {"title": "x", "content": "x" * 50, "url": "javascript:alert(1)"}]:
        assert client.post(f"/api/projects/{pid}/sources", json=payload).status_code == 422
    assert client.put(f"/api/projects/{pid}/draft", json={"text": " "}).status_code == 422
    assert client.post(f"/api/projects/{pid}/analyze", json={"text": "text", "version": 1}).status_code == 422


def test_three_checks_and_metrics():
    text = "The model was tested in order to understand how teams can classify documents with a small local system while preserving every qualification about cost and reliability."
    suggestions = analyze(text)
    assert {s["kind"] for s in suggestions} == {"Long sentence", "Filler phrase", "Passive voice candidate"}
    assert metrics("")["words"] == 0
    assert metrics(text)["long_sentences"] == 1


def test_overlaps_and_offset_shifts():
    text = "We really try in order to learn."
    draft = SimpleNamespace(current=text, original=text, suggestions=analyze(text), revisions=[], version=1)
    first = draft.suggestions[0]
    decide(draft, first["id"], "accept")
    second = next(s for s in draft.suggestions if s["status"] == "pending")
    decide(draft, second["id"], "accept")
    assert draft.current == "We try to learn."
    text = "The model was tested in order to understand how teams can classify documents with a small local system while preserving every qualification about cost and reliability."
    draft = SimpleNamespace(current=text, suggestions=analyze(text), revisions=[], version=1)
    filler = next(s for s in draft.suggestions if s["kind"] == "Filler phrase")
    decide(draft, filler["id"], "accept")
    assert all(s["status"] == "stale" for s in draft.suggestions if s["id"] != filler["id"])


def test_passive_requires_human_rewrite():
    draft = SimpleNamespace(current="The model was tested.", suggestions=analyze("The model was tested."), revisions=[], version=1)
    with pytest.raises(ValueError, match="reviewed rewrite"):
        decide(draft, draft.suggestions[0]["id"], "accept")
    decide(draft, draft.suggestions[0]["id"], "accept", "The team tested the model.")
    assert draft.current == "The team tested the model."


@pytest.mark.parametrize("url", ["file:///etc/passwd", "http://user:pass@example.com", "http://example.com:8080"])
def test_bad_url_syntax(url):
    with pytest.raises(ValueError):
        canonical_url(url)


@pytest.mark.parametrize("address", ["127.0.0.1", "10.0.0.1", "169.254.169.254", "::1"])
def test_private_hosts(monkeypatch, address):
    monkeypatch.setattr(socket, "getaddrinfo", lambda *a, **k: [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (address, 80))])
    with pytest.raises(ValueError, match="blocked"):
        validate_public_url("http://internal.example")


def test_fetch_redirect_rejected(monkeypatch):
    from contextlib import contextmanager
    import app.research as research
    monkeypatch.setattr(research, "validate_public_url", lambda url: None)
    class Client:
        def __init__(self, **kwargs):
            assert kwargs["follow_redirects"] is False
        def __enter__(self): return self
        def __exit__(self, *args): pass
        @contextmanager
        def stream(self, *args, **kwargs):
            yield SimpleNamespace(status_code=302)
    monkeypatch.setattr(research.httpx, "Client", Client)
    with pytest.raises(ValueError, match="Redirects"):
        fetch_article("https://example.com")


def test_speculation_and_topic_prompts():
    from app.research import build_brief
    sources = [SimpleNamespace(id=str(i), title=f"Source {i}", url=f"https://example.com/{i}", reliability="unverified", content="A new local model may reduce infrastructure costs for some teams. The publisher released weights for evaluation on laptop hardware.") for i in range(3)]
    brief = build_brief(sources)
    assert any(e["type"] == "speculation" for e in brief["items"][0]["what_happened"])
    assert "local execution" in brief["items"][0]["why_it_matters"]["text"]
    assert "toad" not in [s["passage"] for s in analyze("We ask in order toad to proceed.")]
    assert not any(s["passage"] == "in order to" for s in analyze("We ask in order toad to proceed."))


@pytest.mark.parametrize("content_type,body,error", [
    ("application/json", b'{}', "Only HTML"),
    ("text/plain", b'x' * 2_000_001, "2 MB"),
    ("text/html", b'<p>short</p>', "Not enough"),
    ("text/html", b'<html><title>Article</title><body><p>A detailed report describes a controlled evaluation of a local model and its practical limitations.</p></body></html>', None),
], ids=["unsupported-type", "oversize", "short-content", "valid-html"])
def test_import_content_limits(monkeypatch, content_type, body, error):
    from contextlib import contextmanager
    import httpx
    import app.research as research
    monkeypatch.setattr(research, "validate_public_url", lambda url: None)
    class Client:
        def __init__(self, **kwargs): pass
        def __enter__(self): return self
        def __exit__(self, *args): pass
        @contextmanager
        def stream(self, *args, **kwargs):
            yield httpx.Response(200, headers={"content-type": content_type}, content=body, request=httpx.Request("GET", "https://example.com"))
    monkeypatch.setattr(research.httpx, "Client", Client)
    if error:
        with pytest.raises(ValueError, match=error):
            fetch_article("https://example.com")
    else:
        result = fetch_article("https://example.com")
        assert result["title"] == "Article"
        assert "controlled evaluation" in result["content"]
