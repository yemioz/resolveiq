from __future__ import annotations

from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    agency: str
    complaint_type: str
    borough: str | None = None
    intake_channel: str = Field(alias="open_data_channel_type")
    hour_of_day: int = Field(ge=0, le=23)
    day_of_week: str

    model_config = {"populate_by_name": True}


class PredictResponse(BaseModel):
    survival_probability_at_sla: float
    predicted_median_resolution_days: float
    extreme_delay_probability: float
    risk_class: str
    model_version: str


class HealthResponse(BaseModel):
    status: str


class ModelInfoResponse(BaseModel):
    model_version: str
    survival_model_type: str
    sla_default_days: int
