# ResolveIQ Development Guidelines

## Project Architecture

ResolveIQ follows this general flow:

raw -> staging -> analytics -> features -> models -> scoring -> API/reporting

Preserve separation between these layers.

## Development Environment

Use Docker for the project runtime.

Run tests with:

docker compose -f docker/docker-compose.yml exec app pytest

Run linting with:

docker compose -f docker/docker-compose.yml exec app ruff check .

Do not install project dependencies directly into the host environment unless necessary for development tooling.

## Data Engineering

- Preserve raw source data in the raw layer.
- Perform cleaning and normalization in staging.
- Keep business-ready tables in analytics.
- Maintain clearly defined table grain.
- Validate referential integrity and business rules.
- Keep incremental ingestion deterministic and replayable.

## Feature Engineering

All predictive features must satisfy:

feature_information_timestamp <= prediction_timestamp

Do not use information that would not have been available at prediction time.

Historical aggregates must exclude the current observation when appropriate.

## Survival Analysis

The survival workflow includes:

- Kaplan-Meier estimation
- Cox proportional-hazards modeling
- proportional-hazards diagnostics
- accelerated failure time models as an alternative when PH assumptions are inappropriate

Do not assume the proportional-hazards assumption holds without checking it.

## Extreme Value Modeling

Extreme resolution delays are modeled using a peaks-over-threshold Generalized Pareto Distribution.

Threshold selection and tail-model assumptions should be justified using diagnostics and sufficient tail observations.

## Classification

The logistic regression model is a baseline comparison model rather than the primary modeling approach.

Be explicit about unresolved or censored observations when constructing classification targets.

## Testing

Run relevant tests after modifying code.

Before considering a change complete, run the full test suite when practical.

Do not modify tests merely to make failing implementation code pass unless the existing test is demonstrably incorrect.

## Code Changes

- Prefer small, testable functions.
- Preserve existing public interfaces unless there is a clear reason to change them.
- Avoid unnecessary abstractions.
- Do not silently change statistical assumptions.
- Do not introduce target leakage.
- Keep SQL, Python, and API behavior consistent with documented data contracts.

## Git

Keep commits focused and descriptive.

Do not commit:
- `.env`
- credentials
- API keys
- local model artifacts
- large raw datasets
- temporary notebooks or scratch files