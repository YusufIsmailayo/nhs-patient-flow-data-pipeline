from pathlib import Path
from datetime import datetime, timezone
import re
import pandas as pd

RAW = Path("data/raw")
SILVER = Path("data/silver")

XLSX_NAME = "outpatients_all_attendances_2024_25.xlsx"

# Your inspection showed headers start on row 12 (0-based)
HEADER_ROW = 12

# Columns that should be treated as identifiers (string-safe)
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
    # normalise various dash characters to a plain hyphen
    return (
        str(s)
        .replace("–", "-")   # en-dash
        .replace("—", "-")   # em-dash
        .replace("−", "-")   # minus
        .strip()
    )

def pick_sheet(xls: pd.ExcelFile) -> str:
    # We want the "All Attendances – All" sheet, regardless of dash type
    candidates = []
    for name in xls.sheet_names:
        n = normalise_dashes(name)
        if n.lower() == "all attendances - all":
            return name
        candidates.append(name)

    # fallback: anything that contains both tokens
    for name in xls.sheet_names:
        n = normalise_dashes(name).lower()
        if ("all attendances" in n) and (n.endswith("all")):
            return name

    raise ValueError(f"Could not find the 'All Attendances – All' sheet. Found: {xls.sheet_names}")

def main():
    SILVER.mkdir(parents=True, exist_ok=True)

    fp = RAW / XLSX_NAME
    if not fp.exists():
        raise FileNotFoundError(f"Missing raw file: {fp}")

    xls = pd.ExcelFile(fp)
    sheet = pick_sheet(xls)
    print(f"Using sheet: {sheet}")
    print(f"All sheets: {xls.sheet_names}")

    # Read the table with correct header row
    df = pd.read_excel(fp, sheet_name=sheet, header=HEADER_ROW)

    # Drop fully empty columns (these often become NaN headers)
    df = df.dropna(axis=1, how="all")

    # Clean / standardise column names (and make unique for Parquet)
    cleaned_cols = []
    for i, c in enumerate(df.columns):
        if pd.isna(c) or str(c).strip() == "":
            cleaned_cols.append(f"unnamed_{i}")
        else:
            cleaned_cols.append(snake_case(c))

    cleaned_cols = make_unique(cleaned_cols)
    df.columns = cleaned_cols

    # Strip whitespace for all object columns, decode bytes if present
    for c in df.columns:
        if df[c].dtype == "object":
            df[c] = df[c].apply(lambda x: x.decode("utf-8") if isinstance(x, (bytes, bytearray)) else x)
            df[c] = df[c].astype("string").str.strip()

    # Force ID columns to string (prevents mixed int/str causing parquet issues)
    for c in ID_COLS:
        if c in df.columns:
            df[c] = df[c].astype("string").str.strip()

    # Convert all non-ID, non-lineage columns to numeric where possible
    for c in df.columns:
        if c not in ID_COLS:
            # try numeric conversion; if it can't convert, it becomes NaN (safe)
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Add lineage
    df["source_file"] = fp.name
    df["load_timestamp"] = datetime.now(timezone.utc).isoformat(timespec="seconds")

    out_path = SILVER / "rtt_provider_all_attendances.parquet"
    df.to_parquet(out_path, index=False)

    print(f"Silver written: {out_path}")
    print(f"Rows={len(df)} | Cols={len(df.columns)}")
    print("First 10 columns:", list(df.columns[:10]))

if __name__ == "__main__":
    main()from pathlib import Path
from datetime import datetime, timezone
import re
import pandas as pd

RAW = Path("data/raw")
SILVER = Path("data/silver")

XLSX_NAME = "outpatients_all_attendances_2024_25.xlsx"
SHEET = "All Attendances - All"

# From inspection (0-based indexing)
HEADER_ROW = 12        # real column headers
BANNER_ROW = 11        # "Age group (years)" row

def snake_case(s: str) -> str:
    s = str(s).strip().lower()
    s = s.replace("&", " and ")
    s = re.sub(r"[^\w]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s

def read_all_attendances_all(fp: Path) -> pd.DataFrame:
    # Read banner row (age-group labels)
    banner = pd.read_excel(
        fp,
        sheet_name=SHEET,
        header=None,
        skiprows=BANNER_ROW,
        nrows=1
    )

    # Read main table
    df = pd.read_excel(
        fp,
        sheet_name=SHEET,
        header=HEADER_ROW
    )

    # Clean column names
    df.columns = [snake_case(c) for c in df.columns]

    # Drop empty rows
    df = df.dropna(how="all")

    return df

def main():
    SILVER.mkdir(parents=True, exist_ok=True)

    fp = RAW / XLSX_NAME
    if not fp.exists():
        raise FileNotFoundError(f"Missing raw file: {fp}")

    df = read_all_attendances_all(fp)

    # Add lineage
    df["source_file"] = fp.name
    df["load_timestamp"] = datetime.now(timezone.utc).isoformat(timespec="seconds")

    out_path = SILVER / "rtt_provider_all_attendances.parquet"
    df.to_parquet(out_path, index=False)

    print(f"Silver written: {out_path}")
    print(f"Rows={len(df)} | Cols={len(df.columns)}")

if __name__ == "__main__":
    main()

