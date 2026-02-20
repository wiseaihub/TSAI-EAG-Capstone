from pydantic import BaseModel, Field


class VitalsInput(BaseModel):
    """Vitals: BP, temp, pulse, SpO2."""

    systolic_bp: int = Field(..., ge=0, example=120, description="Systolic BP (mmHg)")
    diastolic_bp: int = Field(..., ge=0, example=80, description="Diastolic BP (mmHg)")
    temp_c: float = Field(..., example=36.6, description="Temperature (°C)")
    pulse: int = Field(..., ge=0, example=72, description="Heart rate (bpm)")
    spo2: float = Field(..., ge=0, le=100, example=98.0, description="SpO2 (%)")


class VitalsOutput(BaseModel):
    """Vitals analysis result."""

    risk_level: str
    flags: list[str]
    confidence: float
