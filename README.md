# NHS Patient Flow Data Pipeline

A reproducible Bronze → Silver → Gold data pipeline for analysing NHS outpatient attendance data.

## Project Summary

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

## Key Outputs

- Total attendances by specialty (90 specialties, 226M attendances)
- Attendances by age band (26 age groups)
- Specialty contribution, ranking, and cumulative share (Pareto analysis)

These outputs are designed to support reporting, dashboards, and policy analysis.

---

## Structure

```
data/raw/       : original source files (not committed)
data/bronze/    : ingested raw file copies
data/silver/    : cleaned, typed, conformed parquet table
data/gold/      : analytics-ready output tables
src/pipelines/  : pipeline scripts
notebooks/      : exploration and checks
docs/           : architecture, data dictionary, design decisions
```

## Quickstart

1. Drop source files into `data/raw/`
2. Run each pipeline layer in order:

```bash
python src/pipelines/run_bronze.py
python src/pipelines/run_silver_rtt_provider.py
python src/pipelines/run_gold_attendances_by_specialty.py
python src/pipelines/run_gold_attendances_by_age_band.py
python src/pipelines/run_gold_specialty_share.py
```

## Principles

- Raw data is never modified
- Every output is reproducible
- Each layer has clear rules and responsibilities
- Silver is built once and reused by all Gold outputs

---

For detailed design decisions, see [docs/architecture.md](docs/architecture.md).
For column definitions, see [docs/data_dictionary.md](docs/data_dictionary.md).