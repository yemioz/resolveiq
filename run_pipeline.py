"""
Top-level pipeline entry point.

    python run_pipeline.py --since 2026-08-01

Each stage is a thin wrapper around the corresponding src/ module --
this file should stay orchestration-only. If you're tempted to add
real logic here, it belongs in one of the src/ packages instead.
"""
from __future__ import annotations

import argparse
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("run_pipeline")


def extract(since: datetime):
    # from src.ingestion.socrata_client import SocrataClient
    logger.info("extract(): TODO -- wire up SocrataClient.fetch_all_incremental()")


def validate_raw(records):
    # from src.validation.validators import run_all
    logger.info("validate_raw(): TODO")


def load_postgres(records):
    logger.info("load_postgres(): TODO -- upsert into raw.requests")


def transform():
    logger.info("transform(): TODO -- run sql/staging then sql/analytics transforms")


def validate_analytics():
    logger.info("validate_analytics(): TODO")


def fit_or_update_models():
    # from src.survival.cox_ph import fit_cox_model, check_ph_assumption
    # from src.survival.aft import fit_aft_candidates, select_best_by_aic
    # from src.extremes.gpd_tail_model import fit_gpd_tail
    logger.info("fit_or_update_models(): TODO")


def score_open_cases():
    # from src.scoring.batch_score import score_open_requests
    logger.info("score_open_cases(): TODO")


def store_predictions(scored_df):
    logger.info("store_predictions(): TODO -- write to analytics.model_predictions")


def refresh_power_bi():
    # from src.reporting.powerbi_refresh import get_access_token, trigger_refresh
    logger.info("refresh_power_bi(): TODO -- skip if POWERBI_* env vars are unset")


def run_pipeline(since: datetime) -> None:
    logger.info("Starting pipeline run, since=%s", since.isoformat())
    records = extract(since)
    validate_raw(records)
    load_postgres(records)
    transform()
    validate_analytics()
    fit_or_update_models()
    scored = score_open_cases()
    store_predictions(scored)
    refresh_power_bi()
    logger.info("Pipeline run complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the ResolvIQ pipeline.")
    parser.add_argument(
        "--since",
        type=lambda s: datetime.fromisoformat(s),
        required=True,
        help="Only ingest records updated since this ISO timestamp, e.g. 2026-08-01",
    )
    args = parser.parse_args()
    run_pipeline(args.since)
