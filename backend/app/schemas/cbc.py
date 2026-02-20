from pydantic import BaseModel, Field


class DifferentialCounts(BaseModel):
    """WBC differential (counts or %). Units: 10^9/L for counts."""

    neutrophils: float | None = Field(None, example=4.2, description="Neutrophils (10^9/L or %)")
    lymphocytes: float | None = Field(None, example=2.0, description="Lymphocytes")
    monocytes: float | None = Field(None, example=0.5, description="Monocytes")
    eosinophils: float | None = Field(None, example=0.2, description="Eosinophils")
    basophils: float | None = Field(None, example=0.05, description="Basophils")


class CBCInput(BaseModel):
    """Complete Blood Count input (Hb, WBC, RBC, platelets, differential)."""

    hemoglobin: float = Field(..., example=13.5, description="Hb (g/dL)")
    wbc: float = Field(..., example=7000, description="WBC (per µL)")
    rbc: float = Field(..., example=4.5, description="RBC (million/µL)")
    platelets: float = Field(..., example=250000, description="Platelets (per µL)")
    differential: DifferentialCounts | None = Field(None, description="WBC differential counts")


class CBCOutput(BaseModel):
    risk_level: str
    flags: list[str]
    confidence: float
