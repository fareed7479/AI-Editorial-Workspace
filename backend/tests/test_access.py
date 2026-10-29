def test_workspace_opens_without_login_even_with_legacy_secrets(client, monkeypatch):
    monkeypatch.setenv("WORKSPACE_PASSWORD", "ignored-legacy-password")
    monkeypatch.setenv("SESSION_SECRET", "ignored-legacy-secret")
    assert client.get("/api/projects").status_code == 200
    assert client.post("/api/projects", json={"title": "Direct workspace"}).status_code == 201
    assert client.post("/api/auth/login", json={"password": "unused"}).status_code == 404


def test_untrusted_write_origin_is_blocked(client):
    response = client.post("/api/projects", json={"title": "Blocked"}, headers={"Origin": "https://attacker.example"})
    assert response.status_code == 403


def test_cloud_still_requires_postgresql(client, monkeypatch):
    monkeypatch.setenv("VERCEL", "1")
    monkeypatch.setenv("DATABASE_URL", "sqlite://")
    assert client.get("/api/projects").status_code == 503
