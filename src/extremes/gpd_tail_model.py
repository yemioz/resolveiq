"""
Extreme value theory utilities for modeling unusually long resolution
times with a peaks-over-threshold Generalized Pareto Distribution (GPD).

The workflow supports:
- computing mean excess values across candidate thresholds
- fitting a GPD to exceedances above a selected threshold
- estimating conditional exceedance probabilities for extreme delays

Mean excess values are intended for exploratory threshold selection
and diagnostic plotting.

GPD fitting is performed on exceedances measured relative to the
selected threshold. The fit should require a sufficient number of
exceedances to support a stable estimate and should fail explicitly
when the available tail sample is inadequate.

Exceedance probabilities are reported on the original duration scale
while accounting for the GPD's excess-over-threshold parameterization.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import genpareto


def mean_excess_values(durations: pd.Series, thresholds: np.ndarray) -> pd.DataFrame:
    """Mean-excess-plot data for a range of candidate thresholds."""
    raise NotImplementedError


def fit_gpd_tail(durations: pd.Series, threshold: float) -> dict:
    """Fit a GPD to exceedances over `threshold`."""
    raise NotImplementedError


def prob_exceeds(gpd_params: dict, value: float) -> float:
    """P(duration > value | duration > threshold), from the fitted GPD."""
    raise NotImplementedError
