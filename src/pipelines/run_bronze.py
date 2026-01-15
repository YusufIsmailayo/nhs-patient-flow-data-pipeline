from pathlib import Path

RAW = Path("data/raw")
BRONZE = Path("data/bronze")

def main():
    BRONZE.mkdir(parents=True, exist_ok=True)

    files = list(RAW.glob("*"))
    if not files:
        print("No files found in data/raw/")
        return

    print(f"Found {len(files)} raw file(s). Next: read → standardise → write bronze outputs.")
    # TODO: implement: loop files, read, add source_file, standardise columns, save parquet/csv

if __name__ == "__main__":
    main()
