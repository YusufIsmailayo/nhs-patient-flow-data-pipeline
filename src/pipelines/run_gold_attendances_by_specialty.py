from pathlib import Path
import pandas as pd

SILVER = Path("data/silver")
GOLD = Path("data/gold")

def main():
    GOLD.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(SILVER / "rtt_provider_all_attendances.parquet")

    # IMPORTANT: pick the correct "total" column
    # We'll detect it safely in case the header names vary.
    possible_total_cols = [c for c in df.columns if c in ["total", "all_ages_total", "all_total"]]
    if not possible_total_cols:
        raise ValueError(f"Can't find a total column. Available columns: {df.columns.tolist()}")
    total_col = possible_total_cols[0]

    gold_df = (
        df
        .groupby(["main_specialty_code", "main_specialty_code_description"], as_index=False)
        .agg(total_attendances=(total_col, "sum"))
        .sort_values("total_attendances", ascending=False)
    )

    out_path = GOLD / "attendances_by_specialty.parquet"
    gold_df.to_parquet(out_path, index=False)

    print(f"Gold written: {out_path}")
    print(gold_df.head(10).to_string(index=False))

if __name__ == "__main__":
    main()
