# NHS Patient Flow Data Pipeline

A reproducible Bronze → Silver → Gold data pipeline for analysing NHS patient flow datasets.


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

- ## Project Summary

This project demonstrates how I design and implement a layered data pipeline
to transform raw NHS outpatient attendance data into reusable analytical datasets
and business-ready insights.

The pipeline follows a Bronze → Silver → Gold pattern commonly used in
production data engineering environments.

## What This Project Shows

- How I protect raw data integrity
- How I standardise data once for reuse
- How I separate data preparation from business logic
- How I produce multiple Gold outputs from a single Silver dataset

- ## Key Outputs

- Total attendances by specialty
- Attendances by age band
- Specialty contribution, ranking, and cumulative share

These outputs are designed to support reporting, dashboards, and policy analysis.

For detailed design decisions, see [docs/architecture.md](docs/architecture.md).