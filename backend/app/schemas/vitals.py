from typing import Optional

from pydantic import BaseModel, Field


class VitalsInput(BaseModel):
    """Vitals: core set plus extended vitals from UI."""

    # Core vitals (existing)
    systolic_bp: int = Field(..., ge=0, example=120, description="Systolic BP (mmHg)")
    diastolic_bp: int = Field(..., ge=0, example=80, description="Diastolic BP (mmHg)")
    temp_c: float = Field(..., example=36.6, description="Body temperature (°C)")
    pulse: int = Field(..., ge=0, example=72, description="Heart rate (bpm)")
    spo2: float = Field(..., ge=0, le=100, example=98.0, description="Oxygen saturation SpO2 (%)")

    # Additional vitals from UI (optional)
    height_cm: Optional[float] = Field(
        None, ge=0, description="Height (cm)"
    )
    weight_kg: Optional[float] = Field(
        None, ge=0, description="Weight (kg)"
    )
    head_circumference_cm: Optional[float] = Field(
        None, ge=0, description="Head circumference (cm)"
    )
    respiratory_rate: Optional[int] = Field(
        None, ge=0, description="Respiratory rate (breaths per minute)"
    )
    blood_sugar_before_meal_mgdl: Optional[float] = Field(
        None, ge=0, description="Blood sugar level before meal (mg/dL)"
    )
    blood_sugar_after_meal_mgdl: Optional[float] = Field(
        None, ge=0, description="Blood sugar level after meal (mg/dL)"
    )


class VitalsOutput(BaseModel):
    """Vitals analysis result."""

    risk_level: str
    flags: list[str]
    confidence: float


class VitalsReading(BaseModel):
    """Single vitals reading for fetch/display."""

    timestamp: str = Field(..., description="ISO datetime of reading")

    # Core vitals (existing)
    systolic_bp: int = Field(..., ge=0, description="Systolic BP (mmHg)")
    diastolic_bp: int = Field(..., ge=0, description="Diastolic BP (mmHg)")
    temp_c: float = Field(..., description="Body temperature (°C)")
    pulse: int = Field(..., ge=0, description="Heart rate (bpm)")
    spo2: float = Field(..., ge=0, le=100, description="Oxygen saturation SpO2 (%)")

    # Additional vitals from UI (optional)
    height_cm: Optional[float] = Field(
        None, ge=0, description="Height (cm)"
    )
    weight_kg: Optional[float] = Field(
        None, ge=0, description="Weight (kg)"
    )
    head_circumference_cm: Optional[float] = Field(
        None, ge=0, description="Head circumference (cm)"
    )
    respiratory_rate: Optional[int] = Field(
        None, ge=0, description="Respiratory rate (breaths per minute)"
    )
    blood_sugar_before_meal_mgdl: Optional[float] = Field(
        None, ge=0, description="Blood sugar level before meal (mg/dL)"
    )
    blood_sugar_after_meal_mgdl: Optional[float] = Field(
        None, ge=0, description="Blood sugar level after meal (mg/dL)"
    )
