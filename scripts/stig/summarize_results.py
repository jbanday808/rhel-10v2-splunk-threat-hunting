#!/usr/bin/env python3
"""Summarize PRIVATE OpenSCAP XCCDF results; cannot assess STIG compliance alone."""
from __future__ import annotations
import argparse
import csv
import pathlib
import sys
import xml.etree.ElementTree as ET
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[2]
XCCDF = "{http://checklists.nist.gov/xccdf/1.2}"


def parse_results(raw: bytes) -> tuple[list[dict], int]:
    root = ET.fromstring(raw)
    containers = list(root.iter(XCCDF + "TestResult"))
    rows = []
    for container in containers:
        for rule in container.findall(XCCDF + "rule-result"):
            rows.append({
                "rule_id": rule.get("idref", ""),
                "result": rule.findtext(XCCDF + "result", default="unknown").strip(),
            })
    if not rows:
        for rule in root.iter(XCCDF + "rule-result"):
            rows.append({
                "rule_id": rule.get("idref", ""),
                "result": rule.findtext(XCCDF + "result", default="unknown").strip(),
            })
    if not rows:
        raise ValueError("No XCCDF rule results found (use --results XML)")
    return rows, len(containers)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=pathlib.Path)
    parser.add_argument("--csv", type=pathlib.Path, help="Private output outside Git")
    args = parser.parse_args()
    try:
        rows, tests = parse_results(args.results.expanduser().read_bytes())
        print("XCCDF rule outcomes:", len(rows), "| TestResult containers:", tests)
        for state, count in sorted(Counter(x["result"] for x in rows).items()):
            print(f"  {state}: {count}")
        if tests > 1:
            print("WARNING: Multiple TestResult containers; do not treat as single-host score.")
        if args.csv:
            out = args.csv.expanduser().resolve()
            if out.is_relative_to(ROOT):
                raise ValueError("Refusing to write private scan results into public repository")
            out.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            with out.open("w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["rule_id", "result"])
                writer.writeheader()
                writer.writerows(rows)
            out.chmod(0o600)
            print("PRIVATE CSV:", out)
        print("Interpretation, applicability, exceptions and compliance require human review.")
        return 0
    except (OSError, ValueError, ET.ParseError) as exc:
        print("Result summarization failed:", exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
