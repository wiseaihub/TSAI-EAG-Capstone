"""Tests for auth helper endpoints (me + doctor provisioning)."""

from unittest.mock import MagicMock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import auth
from app.core.security import get_current_user
from app.db.session import get_db


def _build_client(db_obj, user=None):
    app = FastAPI()
    app.include_router(auth.router)

    def _db():
        yield db_obj

    app.dependency_overrides[get_db] = _db
    if user is not None:
        app.dependency_overrides[get_current_user] = lambda: user

    return TestClient(app), app


def test_auth_me_returns_role():
    db = MagicMock()
    client, app = _build_client(db, user={"sub": "u1", "email": "x@example.com", "app_role": "doctor"})
    try:
        res = client.get("/auth/me")
        assert res.status_code == 200
        assert res.json()["app_role"] == "doctor"
    finally:
        app.dependency_overrides.clear()


def test_provision_doctor_requires_secret(monkeypatch):
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None
    monkeypatch.setattr(auth.settings, "doctor_provision_secret", "test-secret")
    client, app = _build_client(db, user=None)
    try:
        res = client.post("/auth/provision-doctor", json={"user_id": "abc"})
        assert res.status_code == 403
    finally:
        app.dependency_overrides.clear()


def test_provision_doctor_creates_or_updates(monkeypatch):
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None
    monkeypatch.setattr(auth.settings, "doctor_provision_secret", "test-secret")
    client, app = _build_client(db, user=None)
    try:
        res = client.post(
            "/auth/provision-doctor",
            json={"user_id": "abc"},
            headers={"X-Provision-Secret": "test-secret"},
        )
        assert res.status_code == 200
        body = res.json()
        assert body["user_id"] == "abc"
        assert body["app_role"] == "doctor"
        assert body["status"] == "created"
        assert db.add.called
        assert db.commit.called
    finally:
        app.dependency_overrides.clear()
