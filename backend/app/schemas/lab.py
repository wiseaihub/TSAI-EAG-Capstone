"""Lab result schema for mock EHR API."""

from datetime import datetime
from pydantic import BaseModel, Field


class LabResultRead(BaseModel):
    """Single lab result for API response."""

    id: str = Field(..., description="Lab result identifier")
    name: str = Field(..., description="Lab test name (e.g. Hemoglobin, WBC)")
    value: float = Field(..., description="Numeric result value")
    unit: str = Field(..., description="Unit of measurement (e.g. g/dL)")
    date: datetime = Field(..., description="Date/time of the lab")
