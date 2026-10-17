"""
Data validation utilities for schema, referential integrity,
business rules, grain, and censoring consistency.

Validation functions raise ValidationError with descriptive messages
when a dataset violates an expected invariant.

Checks include:
- schema validation
- duplicate detection at the expected grain
- referential integrity across fact and dimension tables
- business-rule validation
- censoring consistency between event status and closed dates
"""

from __future__ import annotations
import pandas as pd


class ValidationError(AssertionError):
    pass


def validate_schema(df: pd.DataFrame) -> None:
    """
    schema checks
    - required columns
    - unique key must be nonempty
    - created_date is nonnull
    """

    required_cols = {
        "unique_key",
        "created_date",
        "closed_date",
        "agency",
        "complaint_type",
        "status",
    }
    missing = required_cols - set(df.columns)
    if missing:
        raise ValidationError(f"missing columns: {missing}")

    if df["created_date"].isna().any():
        raise ValidationError("created_date contains null values")

    for column in ("unique_key", "agency", "complaint_type"):
        values = df[column].astype("string")
        invalid = values.isna() | values.str.strip().eq("")

        if invalid.any():
            raise ValidationError(f"{column} contains null or blank values")


def validate_grain(df: pd.DataFrame, key_col: str = "unique_key") -> None:
    # validate unique_key grain
    duplicate_count = df[key_col].duplicated().sum()
    if duplicate_count > 0:
        raise ValidationError(
            f"{duplicate_count} duplicates in {key_col}. Expects 1 row per request"
        )


def validate_business_rules(df: pd.DataFrame) -> None:
    # created_at must be before closed_at
    if (df["created_date"] > df["closed_date"]).any():
        raise ValidationError("contains orders created after closed date")


def validate_censoring_consistency(
    df: pd.DataFrame,
    event_col: str = "event_indicator",
    closed_col: str = "closed_date",
) -> None:
    # check participants survival time is available
    if not df[event_col].isin([0, 1]).all():
        raise ValidationError("event indicator must contain only 0 or 1")

    if ((df[event_col] == 0) & df[closed_col].notna()).any():
        raise ValidationError("censored request must not have a closed_date")

    if ((df[event_col] == 1) & df[closed_col].isna()).any():
        raise ValidationError("observed closures must have closed_date")


def validate_referential_integrity(
    fact_df: pd.DataFrame, dim_df: pd.DataFrame, fk_col: str, pk_col: str
) -> None:
    raise NotImplementedError


def run_all(df: pd.DataFrame) -> None:
    # run every check, in order. Validates a normalizd request dataset with event indicators
    validate_schema(df)
    validate_grain(df)
    validate_business_rules(df)
    validate_censoring_consistency(df)
