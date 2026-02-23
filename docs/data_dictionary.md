# Data Dictionary — NHS Outpatient Attendances Pipeline

## Source Dataset

**File:** `outpatients_all_attendances_2024_25.xlsx`
**Source:** NHS England — Outpatient Appointments Statistics
**Sheet:** All Attendances – All
**Period:** 2024/25 financial year
**Granularity:** One row per main specialty, per reporting period

---

## Silver Table — `rtt_provider_all_attendances.parquet`

This is the single cleaned and standardised output of the Silver layer.
All Gold outputs are derived from this table.

### Dimension Columns

| Column | Type | Description |
|--------|------|-------------|
| `main_specialty_code` | string | NHS national code identifying the clinical specialty (e.g. `100` = General Surgery) |
| `main_specialty_code_description` | string | Human-readable name of the specialty (e.g. `General Surgery`) |

### Age Band Columns (Measures)

Each column represents the total number of outpatient attendances for patients in that age group.

| Column | Age Group |
|--------|-----------|
| `0` | Under 1 year |
| `1_4` | 1 to 4 years |
| `5_9` | 5 to 9 years |
| `10_14` | 10 to 14 years |
| `15` | 15 years |
| `16` | 16 years |
| `17` | 17 years |
| `18` | 18 years |
| `19` | 19 years |
| `20_24` | 20 to 24 years |
| `25_29` | 25 to 29 years |
| `30_34` | 30 to 34 years |
| `35_39` | 35 to 39 years |
| `40_44` | 40 to 44 years |
| `45_49` | 45 to 49 years |
| `50_54` | 50 to 54 years |
| `55_59` | 55 to 59 years |
| `60_64` | 60 to 64 years |
| `65_69` | 65 to 69 years |
| `70_74` | 70 to 74 years |
| `75_79` | 75 to 79 years |
| `80_84` | 80 to 84 years |
| `85_89` | 85 to 89 years |
| `90_120` | 90 years and over |
| `unknown` | Age not recorded |
| `total` | Total attendances across all age groups |

### Lineage Columns

| Column | Type | Description |
|--------|------|-------------|
| `source_file` | string | Name of the source Excel file this row was loaded from |
| `load_timestamp` | string | UTC timestamp of when Silver was last generated (ISO 8601 format) |

---

## Gold Tables

### `attendances_by_specialty.parquet`

| Column | Type | Description |
|--------|------|-------------|
| `main_specialty_code` | string | NHS specialty code |
| `main_specialty_code_description` | string | Specialty name |
| `total_attendances` | float | Total attendances across all age groups for this specialty |

### `attendances_by_age_band.parquet`

| Column | Type | Description |
|--------|------|-------------|
| `age_band` | string | Age band label (matches silver column names) |
| `total_attendances` | float | Total attendances across all specialties for this age group |

### `specialty_share.parquet`

| Column | Type | Description |
|--------|------|-------------|
| `main_specialty_code` | string | NHS specialty code |
| `main_specialty_code_description` | string | Specialty name |
| `total_attendances` | float | Total attendances for this specialty |
| `pct_share` | float | Percentage of grand total (2 decimal places) |
| `cumulative_pct` | float | Running cumulative percentage (useful for Pareto analysis) |
| `rank` | int | Rank by total attendances (1 = highest) |

---

## Key Facts (2024/25)

- **Total specialties:** 90
- **Grand total attendances:** 226,450,306
- **Highest attending age group:** 75–79 years (20.2M attendances)
- **Largest specialty by volume:** Total Activity (113M) — this is an aggregate row in the source data
- **Largest named specialty:** Allied Health Professional (13.6M)