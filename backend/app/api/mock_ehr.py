"""Mock EHR API: patient fetch, vitals fetch, lab results fetch. Returns sample responses."""

from datetime import datetime, timezone

from fastapi import APIRouter, Request

from app.agents.wise_adapter import run_wise_agent
from app.core.config import settings
from app.schemas.patient import PatientRead
from app.schemas.vitals import VitalsReading
from app.schemas.lab import LabResultRead

router = APIRouter(tags=["Mock EHR"])

def _default_s18_run_metadata() -> dict:
    metadata = {
        "integration_id": settings.s18_integration_id,
        "workflow_id": settings.s18_workflow_id,
        "contract_version": settings.s18_contract_version,
        "source_system": settings.s18_source_system,
    }
    return {k: v for k, v in metadata.items() if v is not None}


# Per-patient CBC cache: populated by /analyze, consumed by /patients/{id}/labs (S18 EHRDataMinerAgent).
_patient_labs_cache: dict[str, dict] = {}

# CBC payload -> LabResultRead mapping (hemoglobin, wbc, rbc, platelets)
_CBC_TO_LAB = [
    ("hemoglobin", "Hemoglobin", "g/dL"),
    ("wbc", "WBC", "10^3/µL"),
    ("rbc", "RBC", "million/µL"),
    ("platelets", "Platelets", "/µL"),
]


def store_patient_cbc(patient_id: str, payload: dict) -> None:
    """Store CBC payload for a patient so /patients/{id}/labs returns it for S18 EHRDataMinerAgent."""
    if patient_id and isinstance(payload, dict):
        _patient_labs_cache[patient_id] = dict(payload)


def _sample_patient(patient_id: str) -> PatientRead:
    now = datetime.now(timezone.utc)
    return PatientRead(
        id=patient_id,
        external_id=f"ext-{patient_id}",
        created_at=now,
        updated_at=now,
    )


def _sample_vitals(patient_id: str) -> list[VitalsReading]:
    return [
        VitalsReading(
            timestamp=datetime.now(timezone.utc).isoformat(),
            systolic_bp=120,
            diastolic_bp=80,
            temp_c=36.6,
            pulse=72,
            spo2=98.0,
        )
    ]


def _sample_labs(patient_id: str) -> list[LabResultRead]:
    now = datetime.now(timezone.utc)
    return [
        LabResultRead(
            id=f"lab-1-{patient_id}",
            name="Hemoglobin",
            value=14.2,
            unit="g/dL",
            date=now,
        ),
        LabResultRead(
            id=f"lab-2-{patient_id}",
            name="WBC",
            value=7.5,
            unit="10^3/µL",
            date=now,
        ),
    ]


@router.get("/patients/{patient_id}", response_model=PatientRead)
def fetch_patient(patient_id: str) -> PatientRead:
    """Fetch mock patient by ID. Returns sample patient data."""
    return _sample_patient(patient_id)


@router.get("/patients/{patient_id}/vitals", response_model=list[VitalsReading])
def fetch_vitals(patient_id: str) -> list[VitalsReading]:
    """Fetch mock vitals for a patient. Returns sample vitals readings."""
    return _sample_vitals(patient_id)


def _labs_from_cbc_cache(patient_id: str) -> list[LabResultRead] | None:
    """Return labs from cached CBC payload if available."""
    payload = _patient_labs_cache.get(patient_id)
    if not payload:
        return None
    now = datetime.now(timezone.utc)
    rows: list[LabResultRead] = []
    for i, (key, name, unit) in enumerate(_CBC_TO_LAB):
        value = payload.get(key)
        if value is not None:
            try:
                v = float(value)
            except (TypeError, ValueError):
                continue
            rows.append(
                LabResultRead(
                    id=f"lab-{key}-{patient_id}",
                    name=name,
                    value=v,
                    unit=unit,
                    date=now,
                )
            )
    return rows if rows else None


@router.get("/patients/{patient_id}/labs", response_model=list[LabResultRead])
def fetch_labs(patient_id: str, request: Request) -> list[LabResultRead]:
    """Fetch mock lab results for a patient. Returns cached CBC from /analyze when available."""
    cached = _labs_from_cbc_cache(patient_id)
    if cached:
        return cached
    # Skip run_wise_agent when caller is S18 mockehr (avoids nested S18 run)
    if request.headers.get("X-Request-Source") != "s18":
        try:
            run_wise_agent(
                {"event": "mock_ehr_labs_fetch"},
                patient_id,
                db=None,
                run_metadata=_default_s18_run_metadata(),
            )
        except Exception:
            pass
    return _sample_labs(patient_id)
