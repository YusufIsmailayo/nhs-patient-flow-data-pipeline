# NHS Patient Flow Data Pipeline — Architecture

## Overview
I built a simple but production-aligned data pipeline using a Bronze → Silver → Gold
layered architecture to process NHS outpatient attendance data.

The goal is to:
- Preserve raw data safely
- Standardise and validate it for reuse
- Produce clean, business-ready aggregates for analysis

---

## Data Layers

### Bronze — Raw ingestion
**Purpose:** Protect the original data exactly as received.

- Files are ingested without modification
- Original structure, headers, and values are preserved
- No cleaning, renaming, or aggregation is allowed

**Why this matters:**  
Bronze allows me to reprocess data safely if logic changes later.

**Typical formats:** Excel, CSV  
**Location:** `data/raw/`

---

### Silver — Standardised analytical layer
**Purpose:** Prepare data for analysis and reuse.

In this layer, I:
- Identify the correct worksheet safely
- Fix headers and remove empty columns
- Standardise column names to `snake_case`
- Enforce consistent data types
- Ensure unique column names (required for Parquet)
- Add lineage metadata (`source_file`, `load_timestamp`)

**What is allowed here:**
- Cleaning
- Type enforcement
- Schema consistency

**What is forbidden here:**
- Business logic
- Aggregations
- KPIs

**Format:** Parquet  
**Location:** `data/silver/`

---

### Gold — Business logic & KPIs
**Purpose:** Produce stakeholder-ready metrics.

In this project, I aggregate outpatient attendances by:
- Main specialty code
- Main specialty description

This produces a table at the grain:
> **One row per specialty**

**What is allowed here:**
- Grouping
- Aggregation
- Sorting
- KPI definitions

**What is forbidden here:**
- Cleaning
- Schema fixing
- Guessing column meanings

**Format:** Parquet  
**Location:** `data/gold/`

---

## Pipeline Execution Order

1. Bronze (manual ingestion)
2. Silver:
   ```bash
   python src/pipelines/run_silver_rtt_provider.py
