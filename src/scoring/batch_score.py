"""
Batch-scoring utilities for currently open requests.

The scoring workflow combines outputs from:
- the active survival model, including Cox PH or an AFT fallback
- the generalized Pareto model for extreme delays
- the baseline classification model

Predictions are formatted for insertion into
analytics.model_predictions.

The survival prediction function is injected so the scoring pipeline
can use the currently selected survival-model family without
model-specific branching.

Predicted median resolution time is derived from the fitted survival
curve as the time at which the estimated survival probability reaches
0.5.

Extreme-delay probability is evaluated for requests that have crossed
the configured GPD threshold. Requests below that threshold receive a
probability of 0.0.

Risk bands are assigned from configured probability cutoffs and should
be validated against the empirical distribution and operational use of
the model predictions.
"""

from __future__ import annotations

import pandas as pd

from src.config import MODEL


def score_open_requests(
    open_requests: pd.DataFrame,
    survival_model,
    gpd_params: dict,
    baseline_model,
    predict_survival_fn,
    sla_days: int | None = None,
) -> pd.DataFrame:
    """
    Produce one row per open request with survival_probability_at_sla,
    extreme_delay_probability, predicted_median_resolution_days, and
    risk_band.
    """
    raise NotImplementedError
