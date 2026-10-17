"""
FastAPI inference service for serving model predictions and metadata.

The service exposes:
- /predict for inference requests
- /health for service health checks
- /model-info for information about the active model artifacts

Serialized model artifacts are loaded at application startup once
fitted survival and extreme-value models are available.
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException

from src.api.schemas import (
    HealthResponse,
    ModelInfoResponse,
    PredictRequest,
    PredictResponse,
)
from src.config import MODEL

app = FastAPI(title="ResolvIQ", version=MODEL.version)

# TODO: load real artifacts at startup, e.g.:
# survival_model = joblib.load("artifacts/cox_model.pkl")
# gpd_params = json.load(open("artifacts/gpd_params.json"))
survival_model = None
gpd_params = None


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/model-info", response_model=ModelInfoResponse)
def model_info() -> ModelInfoResponse:
    return ModelInfoResponse(
        model_version=MODEL.version,
        survival_model_type="cox_ph",  # TODO: reflect actual production model (cox_ph vs aft fallback)
        sla_default_days=MODEL.sla_default_days,
    )


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    if survival_model is None:
        raise HTTPException(
            status_code=503,
            detail="No model artifact loaded yet -- train and serialize a model first.",
        )
    # TODO: build a single-row feature frame from `request`, run it
    # through the same point-in-time feature pipeline used in
    # training, and call src.survival.cox_ph.predict_survival_at (or
    # the AFT equivalent).
    raise NotImplementedError
