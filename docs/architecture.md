# NHS Patient Flow Data Pipeline — Architecture

## Overview
I built a simple but robust Bronze → Silver → Gold data pipeline to process NHS outpatient attendance data.
The pipeline is designed to preserve raw data, standardise it once, and support multiple business-ready outputs.

The guiding principles are:
- Raw data is never modified
- Silver is reusable and schema-safe
- Gold answers specific business questions

---

## Data Layers

### 🥉 Bronze — Raw Ingestion
**Purpose:** Preserve source data exactly as received.

- Stores raw Excel files
- No cleaning, renaming, or type coercion
- Acts as a forensic copy of the source

**What is allowed:**
- File copying
- Folder organisation
- Basic inspection

**What is forbidden:**
- Renaming columns
- Type conversion
- Aggregation

**Location:** data/raw/
data/bronze/

---

### 🥈 Silver — Standardised Analytical Dataset
**Purpose:** Prepare data once so it can support multiple analyses.

In Silver, I:
- Select the correct worksheet safely
- Remove empty columns
- Standardise column names
- Enforce consistent data types
- Add lineage metadata

Silver produces a single, reusable Parquet file.

**What is allowed:**
- Cleaning and standardisation
- Type coercion
- Column renaming
- Metadata columns (source file, load timestamp)

**What is forbidden:**
- Business logic
- Aggregations
- KPI calculations

**Output:** data/silver/rtt_provider_all_attendances.parquet
---

### 🥇 Gold — Business-Focused Outputs
**Purpose:** Answer specific business questions clearly and safely.

Each Gold script:
- Reads from Silver
- Produces ONE business output
- Writes ONE Parquet file

Gold outputs are independent of each other.

**What is allowed:**
- Aggregations
- Ranking
- Percentages
- Sorting and filtering for insight

**What is forbidden:**
- Data cleaning
- Schema fixes
- Editing raw values

**Current Gold Outputs:**
- Attendances by specialty
- Attendances by age band
- Specialty share and cumulative contribution

**Location:** data/gold/

---

## Execution Model

Each layer is executed manually and independently:

```bash
# Run Silver once
python src/pipelines/run_silver_rtt_provider.py

# Run Gold outputs independently
python src/pipelines/run_gold_attendances_by_specialty.py
python src/pipelines/run_gold_attendances_by_age_band.py
python src/pipelines/run_gold_specialty_share.py

