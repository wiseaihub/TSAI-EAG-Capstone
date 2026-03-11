"""Mock EHR API: patient fetch, vitals fetch, lab results fetch. Returns sample responses."""

from datetime import datetime, timezone

from fastapi import APIRouter

from app.agents.wise_adapter import run_wise_agent
from app.schemas.patient import PatientRead
from app.schemas.vitals import VitalsReading
from app.schemas.lab import LabResultRead

router = APIRouter(tags=["Mock EHR"])


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


@router.get("/patients/{patient_id}/labs", response_model=list[LabResultRead])
def fetch_labs(patient_id: str) -> list[LabResultRead]:
    """Fetch mock lab results for a patient. Returns sample lab results."""
    # Best effort side-effect: trigger WISE adapter for mock EHR lab fetches.
    # This keeps the mock response stable even if the adapter runtime is down.
    try:
        run_wise_agent({"event": "mock_ehr_labs_fetch"}, patient_id, db=None)
    except Exception:
        pass
    return _sample_labs(patient_id)
