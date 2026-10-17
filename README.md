# ResolvIQ

A resolution-risk analytics platform for municipal 311 service requests: live incremental ingestion, a PostgreSQL warehouse, survival-analysis and extreme-value modeling of resolution time, a capacity-constrained triage decision layer, a Power BI dashboard, and a FastAPI inference service.

## Status

Repo scaffold — directory structure, config, schemas, and API are in place. The learning-bearing logic (ingestion pagination, validation, survival models, EVT tail model, classifier baseline, batch scoring, Power BI refresh) is intentionally left as `NotImplementedError` stubs in `src/`, with docstrings specifying the contract each function must satisfy. A working reference implementation of each lives in `reference/` — see `reference/README.md` for how that folder is meant to be used.

Workflow: implement a function in `src/`, run the relevant test in `tests/`, iterate until it passes, and only consult `reference/` if genuinely stuck — then rewrite your own version rather than copying it in.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # then fill in real values
```

Bring up a local Postgres (schemas load automatically from `sql/ddl/` on first start):

```bash
docker compose -f docker/docker-compose.yml up -d postgres
```

Run tests:

```bash
pytest
```

Run the API locally:

```bash
uvicorn src.api.main:app --reload
```

## A note on the live data source

Ingestion (`src/ingestion/socrata_client.py`) makes outbound HTTP requests to a city open-data domain and will not run inside network-restricted environments. Run ingestion from a normal development machine or CI runner with outbound internet access.

## Repository layout

```
resolviq/
├── sql/ddl/          raw / staging / analytics schema definitions
├── src/
│   ├── ingestion/    live Socrata API client (incremental pull)
│   ├── validation/   schema, grain, referential, censoring-consistency checks
│   ├── features/     point-in-time feature engineering
│   ├── survival/     Kaplan-Meier, Cox PH, AFT fallback
│   ├── extremes/     GPD tail-risk model
│   ├── classification/  logistic regression comparison baseline
│   ├── scoring/      batch scoring of open requests
│   ├── reporting/    Power BI REST API refresh trigger
│   └── api/          FastAPI inference service
├── tests/            unit, data-quality, statistical, and API tests
├── notebooks/        EDA and experiments only -- not where pipeline logic lives
├── docker/           Dockerfile + docker-compose for local Postgres/API
└── run_pipeline.py   orchestration entry point
```

See `docs/` (or the original project spec) for the full business framing, decision-layer design, and Power BI page layout.
