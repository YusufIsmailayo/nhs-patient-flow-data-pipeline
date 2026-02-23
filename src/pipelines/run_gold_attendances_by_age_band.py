from pathlib import Path
import pandas as pd

SILVER = Path("data/silver")
GOLD = Path("data/gold")


def main():
    GOLD.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(SILVER / "rtt_provider_all_attendances.parquet")

    print("Available columns:", df.columns.tolist())

    # Detect age band columns — they follow a numeric pattern like "0_4", "5_9", "85_plus" etc.
    # They are everything that is NOT an ID column or lineage column
    non_age_cols = [
        "main_specialty_code",
        "main_specialty_code_description",
        "source_file",
        "load_timestamp",
    ]

    age_band_cols = [c for c in df.columns if c not in non_age_cols]

    if not age_band_cols:
        raise ValueError("No age band columns detected. Check silver column names.")

    print(f"Detected {len(age_band_cols)} age band column(s): {age_band_cols}")

    # Sum each age band across all specialties
    age_totals = df[age_band_cols].sum().reset_index()
    age_totals.columns = ["age_band", "total_attendances"]
    age_totals = age_totals.sort_values("total_attendances", ascending=False)

    out_path = GOLD / "attendances_by_age_band.parquet"
    age_totals.to_parquet(out_path, index=False)

    print(f"\nGold written: {out_path}")
    print(age_totals.to_string(index=False))


if __name__ == "__main__":
    main()