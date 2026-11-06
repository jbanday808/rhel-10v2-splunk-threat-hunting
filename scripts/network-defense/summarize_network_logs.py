#!/usr/bin/env python3
"""Print only aggregate counts from small PRIVATE newline JSON logs, no sensitive fields."""
from __future__ import annotations
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

MAX_BYTES = 25 * 1024 * 1024
MAX_LINE = 1024 * 1024


def summarize(path: Path, kind: str) -> dict:
    if not path.is_file() or path.stat().st_size > MAX_BYTES:
        raise ValueError("Missing log or exceeds private 25 MiB demo size limit")
    counters: Counter[str] = Counter()
    invalid = 0
    with path.open(encoding="utf-8") as source:
        for line in source:
            if len(line) > MAX_LINE:
                invalid += 1
                continue
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                if not isinstance(data, dict):
                    raise ValueError("Not an object")
            except (ValueError, json.JSONDecodeError):
                invalid += 1
                continue
            label = "zeek-json" if kind == "zeek" else str(data.get("event_type", "unknown"))[:80]
            counters[label] += 1
    return {"events": sum(counters.values()), "invalid": invalid, "types": dict(counters)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--type", choices=["zeek", "suricata"], required=True)
    args = parser.parse_args()
    try:
        stats = summarize(args.path.expanduser(), args.type)
        print("Events:", stats["events"], "invalid/oversize:", stats["invalid"])
        for kind, total in sorted(stats["types"].items()):
            print(kind, total)
        print("Counts only; no raw DNS, addresses, URLs, credentials or alert text printed.")
        return 0
    except (OSError, ValueError, UnicodeError) as exc:
        print("Summary failed:", exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
