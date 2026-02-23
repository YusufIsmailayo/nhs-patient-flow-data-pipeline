from pathlib import Path
import pandas as pd

SILVER = Path("data/silver")
GOLD = Path("data/gold")


def main():
    GOLD.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(SILVER / "rtt_provider_all_attendances.parquet")

    # Detect total column
    possible_total_cols = [c for c in df.columns if c in ["total", "all_ages_total", "all_total"]]
    if not possible_total_cols:
        # Fallback: sum all numeric columns that aren't ID or lineage
        non_measure_cols = [
            "main_specialty_code",
            "main_specialty_code_description",
            "source_file",
            "load_timestamp",
        ]
        measure_cols = [c for c in df.columns if c not in non_measure_cols]
        df["_total"] = df[measure_cols].sum(axis=1)
        total_col = "_total"
        print("No explicit total column found — computed row total from all measure columns.")
    else:
        total_col = possible_total_cols[0]
        print(f"Using total column: {total_col}")

    gold_df = (
        df.groupby(
            ["main_specialty_code", "main_specialty_code_description"], as_index=False
        )
        .agg(total_attendances=(total_col, "sum"))
        .sort_values("total_attendances", ascending=False)
        .reset_index(drop=True)
    )

    # Add share and cumulative share
    grand_total = gold_df["total_attendances"].sum()
    gold_df["pct_share"] = (gold_df["total_attendances"] / grand_total * 100).round(2)
    gold_df["cumulative_pct"] = gold_df["pct_share"].cumsum().round(2)
    gold_df["rank"] = gold_df["total_attendances"].rank(ascending=False, method="min").astype(int)

    out_path = GOLD / "specialty_share.parquet"
    gold_df.to_parquet(out_path, index=False)

    print(f"\nGold written: {out_path}")
    print(gold_df.head(15).to_string(index=False))
    print(f"\nTotal specialties: {len(gold_df)}")
    print(f"Grand total attendances: {grand_total:,.0f}")


if __name__ == "__main__":
    main()