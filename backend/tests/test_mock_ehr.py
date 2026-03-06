"""Tests for mock EHR API endpoints (patient, vitals, lab fetch)."""

import pytest
from fastapi.testclient import TestClient

from app.api.mock_ehr import router as mock_ehr_router
from fastapi import FastAPI

# Minimal app with only mock EHR router - no DB/auth deps
app = FastAPI()
app.include_router(mock_ehr_router)
client = TestClient(app)


def test_fetch_patient():
    """GET /patients/{patient_id} returns sample patient data."""
    r = client.get("/patients/patient-123")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == "patient-123"
    assert data["external_id"] == "ext-patient-123"
    assert "created_at" in data
    assert "updated_at" in data


def test_fetch_vitals():
    """GET /patients/{patient_id}/vitals returns sample vitals readings."""
    r = client.get("/patients/patient-456/vitals")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    v = data[0]
    assert v["systolic_bp"] == 120
    assert v["diastolic_bp"] == 80
    assert v["temp_c"] == 36.6
    assert v["pulse"] == 72
    assert v["spo2"] == 98.0
    assert "timestamp" in v


def test_fetch_labs():
    """GET /patients/{patient_id}/labs returns sample lab results."""
    r = client.get("/patients/patient-789/labs")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    names = [item["name"] for item in data]
    assert "Hemoglobin" in names
    assert "WBC" in names
    for item in data:
        assert "id" in item
        assert "name" in item
        assert "value" in item
        assert "unit" in item
        assert "date" in item
