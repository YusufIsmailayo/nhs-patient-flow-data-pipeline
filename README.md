# NHS Outpatient Patient Flow Pipeline — 226 Million Records

A production-style medallion architecture pipeline processing NHS outpatient 

attendance data across England. Covers **226 million+ attendances** across 

**152 NHS Trusts** and **90 specialties**.

---

## The Problem

NHS outpatient data is published monthly by NHS England but arrives in raw, 

inconsistent formats that require significant engineering to make useful. 

This pipeline automates that entire process — from raw ingestion to 

analytics-ready outputs — using a Bronze → Silver → Gold medallion architecture.

---

## Key Findings

| Metric | Value |

|--------|-------|

| Total attendances processed | 226,287,000+ |

| NHS Trusts covered | 152 |

| Specialties analysed | 90 |

| Top specialty by volume | General Medicine |

| Age groups tracked | 26 |

---

## Medium Article

Full analysis and findings published in **Towards Artificial Intelligence**:

👉 [I Processed 226 Million NHS Patient Records — Here's What I Found](https://medium.com/towards-artificial-intelligence/i-processed-226-million-nhs-patient-records-heres-what-i-found-c35455d3c5f1)

---

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

----

---

## Related Work

- **Project 2:** [NHS RTT Incomplete Pathways Pipeline — 14 million patient pathways](https://github.com/YusufIsmailayo/nhs-rtt-incomplete-pathways-pipeline)
- **Published in Towards Artificial Intelligence:** [The NHS Postcode Lottery Is Real — I Built a Pipeline to Measure It](https://medium.com/towards-artificial-intelligence/the-nhs-postcode-lottery-is-real-i-built-a-pipeline-to-measure-it-04b343f7953e)

---

*Built by [Yusuf Ismail](https://github.com/YusufIsmailayo) — Data Engineer focused on NHS pipelines and public sector analytics.*
