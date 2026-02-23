from pathlib import Path
from datetime import datetime, timezone
import re
import pandas as pd

RAW = Path("data/raw")
SILVER = Path("data/silver")

XLSX_NAME = "outpatients_all_attendances_2024_25.xlsx"
HEADER_ROW = 12

ID_COLS = [
    "main_specialty_code",
    "main_specialty_code_description",
]


def snake_case(s: str) -> str:
    s = str(s).strip().lower()
    s = s.replace("&", " and ")
    s = re.sub(r"[^\w]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s


def make_unique(cols):
    seen = {}
    out = []
    for c in cols:
        if c not in seen:
            seen[c] = 0
            out.append(c)
        else:
            seen[c] += 1
            out.append(f"{c}_{seen[c]}")
    return out


def normalise_dashes(s: str) -> str:
    return (
        str(s)
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2212", "-")
        .strip()
    )


def pick_sheet(xls: pd.ExcelFile) -> str:
    for name in xls.sheet_names:
        n = normalise_dashes(name)
        if n.lower() == "all attendances - all":
            return name

    for name in xls.sheet_names:
        n = normalise_dashes(name).lower()
        if ("all attendances" in n) and (n.endswith("all")):
            return name

    raise ValueError(
        f"Could not find the 'All Attendances \u2013 All' sheet. Found: {xls.sheet_names}"
    )


def main():
    SILVER.mkdir(parents=True, exist_ok=True)

    fp = RAW / XLSX_NAME
    if not fp.exists():
        raise FileNotFoundError(f"Missing raw file: {fp}")

    xls = pd.ExcelFile(fp)
    sheet = pick_sheet(xls)
    print(f"Using sheet: {sheet}")

    df = pd.read_excel(fp, sheet_name=sheet, header=HEADER_ROW)

    # Drop fully empty columns
    df = df.dropna(axis=1, how="all")

    # Standardise column names
    cleaned_cols = []
    for i, c in enumerate(df.columns):
        if pd.isna(c) or str(c).strip() == "":
            cleaned_cols.append(f"unnamed_{i}")
        else:
            cleaned_cols.append(snake_case(c))

    df.columns = make_unique(cleaned_cols)

    # Clean string columns
    for c in df.columns:
        if df[c].dtype == "object":
            df[c] = df[c].apply(
                lambda x: x.decode("utf-8") if isinstance(x, (bytes, bytearray)) else x
            )
            df[c] = df[c].astype("string").str.strip()

    # Force ID columns to string
    for c in ID_COLS:
        if c in df.columns:
            df[c] = df[c].astype("string").str.strip()

    # Convert remaining columns to numeric
    for c in df.columns:
        if c not in ID_COLS:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Add lineage
    df["source_file"] = fp.name
    df["load_timestamp"] = datetime.now(timezone.utc).isoformat(timespec="seconds")

    out_path = SILVER / "rtt_provider_all_attendances.parquet"
    df.to_parquet(out_path, index=False)

    print(f"Silver written: {out_path}")
    print(f"Rows={len(df)} | Cols={len(df.columns)}")
    print("Columns:", list(df.columns))


if __name__ == "__main__":
    main()