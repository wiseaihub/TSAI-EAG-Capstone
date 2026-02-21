from datetime import datetime
from pydantic import BaseModel, Field


class PatientBase(BaseModel):
    external_id: str = Field(..., description="External/system patient identifier")


class PatientCreate(PatientBase):
    pass


class PatientRead(PatientBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EncounterBase(BaseModel):
    patient_id: str
    encounter_type: str | None = None
    started_at: datetime
    ended_at: datetime | None = None


class EncounterCreate(EncounterBase):
    pass


class EncounterRead(EncounterBase):
    id: str

    class Config:
        from_attributes = True
