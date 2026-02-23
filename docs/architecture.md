# NHS Patient Flow Data Pipeline — Architecture

## Overview

A simple but robust Bronze → Silver → Gold data pipeline to process NHS outpatient attendance data.

The pipeline is designed to preserve raw data, standardise it once, and support multiple business-ready outputs.

**Guiding principles:**
- Raw data is never modified
- Silver is reusable and schema-safe
- Gold answers specific business questions

---

## Data Layers

### 🥉 Bronze — Raw Ingestion

**Purpose:** Preserve source data exactly as received.

- Copies raw Excel files from `data/raw/` to `data/bronze/`
- No cleaning, renaming, or type coercion
- Acts as a forensic copy of the source
- Hidden files (e.g. `.gitkeep`) are automatically skipped

**What is allowed:** file copying, folder organisation, basic inspection

**What is forbidden:** renaming columns, type conversion, aggregation

**Location:** `data/bronze/`

---

### 🥈 Silver — Standardised Analytical Dataset

**Purpose:** Prepare data once so it can support multiple analyses.

In Silver, the pipeline:
- Detects and selects the correct worksheet safely (handles encoding differences in sheet names)
- Removes empty columns
- Standardises column names to snake_case
- Enforces consistent data types
- Adds lineage metadata (`source_file`, `load_timestamp`)

Silver produces a single, reusable Parquet file.

**What is allowed:** cleaning, standardisation, type coercion, column renaming, metadata columns

**What is forbidden:** business logic, aggregations, KPI calculations

**Output:** `data/silver/rtt_provider_all_attendances.parquet`

---

### 🥇 Gold — Business-Focused Outputs

**Purpose:** Answer specific business questions clearly and safely.

Each Gold script:
- Reads from Silver only
- Produces ONE business output
- Writes ONE Parquet file

Gold outputs are fully independent of each other.

**What is allowed:** aggregations, ranking, percentages, sorting and filtering for insight

**What is forbidden:** data cleaning, schema fixes, editing raw values

**Current Gold outputs:**

| Script | Output | Business Question |
|--------|--------|-------------------|
| `run_gold_attendances_by_specialty.py` | `attendances_by_specialty.parquet` | Which specialties have the highest attendance volumes? |
| `run_gold_attendances_by_age_band.py` | `attendances_by_age_band.parquet` | Which age groups attend most frequently? |
| `run_gold_specialty_share.py` | `specialty_share.parquet` | What is each specialty's share and cumulative contribution to total activity? |

**Location:** `data/gold/`

---

## Execution Model

Each layer is executed manually and independently, in order:

```bash
# Step 1 — Bronze: copy raw files to bronze
python src/pipelines/run_bronze.py

# Step 2 — Silver: clean and standardise (run once)
python src/pipelines/run_silver_rtt_provider.py

# Step 3 — Gold: run each output independently
python src/pipelines/run_gold_attendances_by_specialty.py
python src/pipelines/run_gold_attendances_by_age_band.py
python src/pipelines/run_gold_specialty_share.py
```

Silver only needs to be re-run if the source data changes. Gold scripts can be re-run independently at any time.