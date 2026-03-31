"""Mental health screening input (PHQ-9, GAD-7) for hybrid local + optional S18 reasoning."""

from pydantic import BaseModel, Field, conint, model_validator

Phq9Item = conint(ge=0, le=3)


class MentalHealthInput(BaseModel):
    """
    Structured screening input. Provide PHQ-9 as either nine items (0–3 each) or a total (0–27),
    and/or GAD-7 total (0–21). At least one of PHQ-9 or GAD-7 must be supplied.

    Cutoffs used in scoring follow common PHQ-9 / GAD-7 interpretation (e.g. Kroenke et al.).
    """

    phq9_items: list[Phq9Item] | None = Field(
        None,
        min_length=9,
        max_length=9,
        description="Nine PHQ-9 item scores, each 0–3. Sum defines total.",
    )
    phq9_total: int | None = Field(None, ge=0, le=27, description="PHQ-9 total if items are not sent.")
    gad7_total: int | None = Field(None, ge=0, le=21, description="GAD-7 total score.")

    suicidal_ideation: bool = Field(False, description="Patient-reported suicidal thoughts (item 9 or clinical flag).")
    self_harm_intent: bool = Field(False, description="Intent to self-harm; triggers crisis pathway.")
    concern_text: str | None = Field(None, max_length=4000, description="Optional short context (not used for diagnosis).")

    include_s18: bool = Field(True, description="If true, run optional S18 narrative/context pass after local scoring.")
    fast: bool = Field(
        False,
        description="If true and include_s18, request S18 fast execution mode.",
    )

    @model_validator(mode="after")
    def require_at_least_one_instrument(self) -> "MentalHealthInput":
        has_phq = self.phq9_total is not None or self.phq9_items is not None
        has_gad = self.gad7_total is not None
        if not has_phq and not has_gad:
            raise ValueError("Provide PHQ-9 (phq9_total or phq9_items) and/or gad7_total")
        if self.phq9_items is not None and self.phq9_total is not None:
            raise ValueError("Send either phq9_items or phq9_total, not both")
        return self
