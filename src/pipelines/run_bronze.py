from pathlib import Path
import shutil
from datetime import datetime, timezone

RAW = Path("data/raw")
BRONZE = Path("data/bronze")


def main():
    BRONZE.mkdir(parents=True, exist_ok=True)

    files = list(RAW.glob("*"))
    if not files:
        print("No files found in data/raw/")
        return

    print(f"Found {len(files)} raw file(s). Copying to bronze...")

    for src in files:
        if src.is_file():
            dst = BRONZE / src.name
            shutil.copy2(src, dst)
            print(f"  Copied: {src.name} → data/bronze/{src.name}")

    print(f"\nBronze complete. {len(files)} file(s) preserved in data/bronze/")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat(timespec='seconds')}")


if __name__ == "__main__":
    main()