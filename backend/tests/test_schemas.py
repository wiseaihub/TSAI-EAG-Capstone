"""Tests for Pydantic schemas (CBC, vitals, patient, encounter)."""

import pytest
from app.schemas.cbc import CBCInput, CBCOutput, DifferentialCounts
from app.schemas.vitals import VitalsInput, VitalsOutput
from app.schemas.patient import PatientCreate, EncounterCreate


def test_cbc_input():
    data = CBCInput(hemoglobin=13.5, wbc=7000, rbc=4.5, platelets=250000)
    assert data.hemoglobin == 13.5
    assert data.rbc == 4.5
    assert data.differential is None


def test_cbc_input_with_differential():
    diff = DifferentialCounts(neutrophils=4.2, lymphocytes=2.0)
    data = CBCInput(hemoglobin=12, wbc=6000, rbc=4.2, platelets=200000, differential=diff)
    assert data.differential.neutrophils == 4.2


def test_vitals_input():
    v = VitalsInput(systolic_bp=120, diastolic_bp=80, temp_c=36.6, pulse=72, spo2=98.0)
    assert v.systolic_bp == 120
    assert v.spo2 == 98.0


def test_patient_encounter_schemas():
    from datetime import datetime
    p = PatientCreate(external_id="EXT-001")
    assert p.external_id == "EXT-001"
    e = EncounterCreate(
        patient_id="pid-1",
        encounter_type="outpatient",
        started_at=datetime.utcnow(),
    )
    assert e.patient_id == "pid-1"
    assert e.encounter_type == "outpatient"
