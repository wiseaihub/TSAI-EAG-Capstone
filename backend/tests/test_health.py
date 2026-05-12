"""GET /health including optional Railway deploy metadata."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_base():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "poll_timeout_seconds" in body


def test_health_includes_deploy_when_railway_git_env_set(monkeypatch):
    monkeypatch.setenv("RAILWAY_GIT_COMMIT_SHA", "abc123deadbeef")
    monkeypatch.setenv("RAILWAY_GIT_BRANCH", "main")
    monkeypatch.setenv("RAILWAY_GIT_COMMIT_MESSAGE", "Merge pull request #224")
    r = client.get("/health")
    assert r.status_code == 200
    deploy = r.json()["deploy"]
    assert deploy["git_sha"] == "abc123deadbeef"
    assert deploy["git_branch"] == "main"
    assert deploy["git_commit_message"] == "Merge pull request #224"
