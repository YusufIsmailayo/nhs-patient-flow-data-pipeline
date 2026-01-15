# NHS Patient Flow Data Pipeline

A reproducible data pipeline (Bronze → Silver → Gold) for NHS patient flow datasets.

## Structure
- `data/raw/`   : original source files (not committed)
- `data/bronze/`: ingested/standardised extracts
- `data/silver/`: cleaned, typed, conformed tables
- `data/gold/`  : analytics-ready marts
- `src/`        : pipeline code
- `notebooks/`  : exploration + checks
- `docs/`       : notes, data dictionary, decisions

## Quickstart
1. Create a virtual environment (optional)
2. Drop source files into `data/raw/`
3. Run pipelines from `src/pipelines/`

## Principles
- Raw data never edited
- Every output is reproducible
- Each layer has clear rules and validation checks
