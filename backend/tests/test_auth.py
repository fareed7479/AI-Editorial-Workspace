from app.auth import COOKIE


def protected(monkeypatch):
    monkeypatch.setenv("WORKSPACE_PASSWORD", "synthetic-workspace-password")
    monkeypatch.setenv("SESSION_SECRET", "synthetic-session-secret-with-enough-length")


def test_workspace_requires_signed_session(client, monkeypatch):
    protected(monkeypatch)
    assert client.get("/api/projects").status_code == 401
    assert client.get("/api/auth/session").json()["authenticated"] is False
    assert client.post("/api/auth/login", json={"password": "wrong"}).status_code == 401
    response = client.post("/api/auth/login", json={"password": "synthetic-workspace-password"})
    assert response.status_code == 200
    assert "httponly" in response.headers["set-cookie"].lower()
    assert client.get("/api/projects").status_code == 200
    assert client.post("/api/auth/logout").status_code == 200
    assert client.get("/api/projects").status_code == 401


def test_forged_session_and_untrusted_origin_are_blocked(client, monkeypatch):
    protected(monkeypatch)
    client.cookies.set(COOKIE, "forged-session")
    assert client.get("/api/projects").status_code == 401
    assert client.post("/api/auth/login", json={"password": "synthetic-workspace-password"}, headers={"Origin": "https://attacker.example"}).status_code == 403


def test_cloud_configuration_fails_closed(client, monkeypatch):
    monkeypatch.setenv("VERCEL", "1")
    monkeypatch.setenv("DATABASE_URL", "sqlite://")
    assert client.get("/api/projects").status_code == 503


def test_password_rotation_invalidates_session(client, monkeypatch):
    protected(monkeypatch)
    client.post("/api/auth/login", json={"password": "synthetic-workspace-password"})
    monkeypatch.setenv("WORKSPACE_PASSWORD", "new-synthetic-workspace-password")
    assert client.get("/api/projects").status_code == 401
