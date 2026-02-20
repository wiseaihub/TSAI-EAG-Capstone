from pydantic import BaseModel, Field

class CBCInput(BaseModel):
    hemoglobin: float = Field(..., example=13.5)
    wbc: float = Field(..., example=7000)
    platelets: float = Field(..., example=250000)


class CBCOutput(BaseModel):
    risk_level: str
    flags: list[str]
    confidence: float
