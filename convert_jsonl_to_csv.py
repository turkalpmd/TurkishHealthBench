"""Convert a JSONL file to CSV.

Usage:
- No arguments: converts every `.jsonl` in `/home/ubuntu/TurkishHealthBench/jsonldata`
  to CSVs in `/home/ubuntu/TurkishHealthBench/csvdata`.
- With arguments: `python convert_jsonl_to_csv.py input.jsonl output.csv`

Notes:
- All keys across records are collected to form the CSV header.
- Nested structures (dict/list) are JSON-encoded in the CSV cell.
"""

import csv
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set


def load_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def collect_keys(records: Iterable[Dict[str, Any]]) -> List[str]:
    keys: Set[str] = set()
    for record in records:
        keys.update(record.keys())
    return sorted(keys)


def normalize_value(value: Any) -> Any:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return value


def write_csv(records: List[Dict[str, Any]], header: List[str], out_path: Path) -> None:
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for record in records:
            row = {key: normalize_value(record.get(key, "")) for key in header}
            writer.writerow(row)


def convert_file(in_path: Path, out_path: Path) -> None:
    records = list(load_jsonl(in_path))
    header = collect_keys(records)
    write_csv(records, header, out_path)
    print(f"→ {in_path.name} -> {out_path.name} ({len(records)} rows, {len(header)} cols)")


def convert_directory(
    src_dir: Path = Path("/home/ubuntu/TurkishHealthBench/jsonldata"),
    dst_dir: Path = Path("/home/ubuntu/TurkishHealthBench/csvdata"),
) -> None:
    if not src_dir.exists():
        print(f"Source directory not found: {src_dir}", file=sys.stderr)
        sys.exit(1)
    dst_dir.mkdir(parents=True, exist_ok=True)

    jsonl_files = sorted(p for p in src_dir.iterdir() if p.suffix.lower() == ".jsonl")
    if not jsonl_files:
        print(f"No .jsonl files found in {src_dir}")
        return

    for jsonl_path in jsonl_files:
        out_path = dst_dir / f"{jsonl_path.stem}.csv"
        convert_file(jsonl_path, out_path)


def main() -> None:
    # No args: batch-convert default directory.
    if len(sys.argv) == 1:
        convert_directory()
        return

    # Two args: single file mode.
    if len(sys.argv) == 3:
        in_path = Path(sys.argv[1]).expanduser().resolve()
        out_path = Path(sys.argv[2]).expanduser().resolve()

        if not in_path.exists():
            print(f"Input not found: {in_path}", file=sys.stderr)
            sys.exit(1)

        convert_file(in_path, out_path)
        return

    print("Usage: python convert_jsonl_to_csv.py input.jsonl output.csv", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()