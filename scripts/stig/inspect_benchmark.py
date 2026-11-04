#!/usr/bin/env python3
"""Inspect private DISA RHEL 10 STIG SCAP 1.3 ZIP/XML without extracting ZIP paths."""
from __future__ import annotations
import argparse
import csv
import hashlib
import pathlib
import sys
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[2]
XCCDF = "{http://checklists.nist.gov/xccdf/1.2}"
DS = "{http://scap.nist.gov/schema/scap/source/1.2}"
MAX_XML_BYTES = 20 * 1024 * 1024


def load_data(path: pathlib.Path) -> bytes:
    if not path.is_file():
        raise ValueError(f"Input not found: {path}")
    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as archive:
            files = [x for x in archive.infolist() if not x.is_dir()]
            if len(files) != 1 or not files[0].filename.endswith(".xml"):
                raise ValueError("Expected exactly one XML file in archive")
            member = files[0]
            if member.file_size < 1 or member.file_size > MAX_XML_BYTES:
                raise ValueError("Unexpected archive XML size")
            with archive.open(member) as source:
                raw = source.read(MAX_XML_BYTES + 1)
    elif path.suffix.lower() == ".xml":
        if path.stat().st_size > MAX_XML_BYTES:
            raise ValueError("Input XML too large")
        raw = path.read_bytes()
    else:
        raise ValueError("Input must end in .zip or .xml")
    if len(raw) > MAX_XML_BYTES:
        raise ValueError("Input XML exceeds maximum size")
    return raw


def parse_benchmark(data: bytes) -> dict:
    root = ET.fromstring(data)
    if root.tag != DS + "data-stream-collection":
        raise ValueError("Expected SCAP data-stream collection")
    streams = [x for x in root if x.tag == DS + "data-stream"]
    if len(streams) != 1:
        raise ValueError("Expected one SCAP data stream")
    benchmark = next((x for x in root.iter() if x.tag == XCCDF + "Benchmark"), None)
    if benchmark is None:
        raise ValueError("Missing XCCDF Benchmark")
    profiles = []
    for p in benchmark.findall(XCCDF + "Profile"):
        selection = p.findall(XCCDF + "select")
        profiles.append({
            "id": p.get("id", ""),
            "title": p.findtext(XCCDF + "title", default="").strip(),
            "selected": sum(x.get("selected") == "true" for x in selection),
            "excluded": sum(x.get("selected") == "false" for x in selection),
        })
    rules = []
    for group in benchmark.iter(XCCDF + "Group"):
        for rule in group.findall(XCCDF + "Rule"):
            rules.append({
                "version_id": rule.findtext(XCCDF + "version", default="").strip(),
                "v_id": group.get("id", "").removeprefix("xccdf_mil.disa.stig_group_"),
                "sv_id": rule.get("id", "").removeprefix("xccdf_mil.disa.stig_rule_"),
                "severity": rule.get("severity", ""),
                "title": rule.findtext(XCCDF + "title", default="").strip(),
            })
    if not rules or len(rules) != len(list(benchmark.iter(XCCDF + "Rule"))):
        raise ValueError("Missing or structurally unexpected grouped XCCDF rules")
    return {
        "benchmark_id": benchmark.get("id", ""),
        "title": benchmark.findtext(XCCDF + "title", default="").strip(),
        "version": benchmark.findtext(XCCDF + "version", default="").strip(),
        "scap_version": streams[0].get("scap-version"),
        "rule_count": len(rules),
        "severity": dict(Counter(x["severity"] for x in rules)),
        "profiles": profiles,
        "rules": rules,
    }


def private_destination(path: pathlib.Path) -> pathlib.Path:
    result = path.expanduser().resolve()
    if result.is_relative_to(ROOT):
        raise ValueError("Refusing to put private rule inventory in the Git repository")
    result.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=pathlib.Path)
    parser.add_argument("--inventory-csv", type=pathlib.Path)
    args = parser.parse_args()
    try:
        source = args.source.expanduser()
        raw = load_data(source)
        meta = parse_benchmark(raw)
        print("Title:", meta["title"])
        print("Benchmark ID:", meta["benchmark_id"])
        print("Version:", meta["version"], "| SCAP:", meta["scap_version"])
        print("Rules:", meta["rule_count"], "| Severity:", meta["severity"])
        print("Input SHA256:", hashlib.sha256(source.read_bytes()).hexdigest())
        print("XML SHA256:", hashlib.sha256(raw).hexdigest())
        for p in meta["profiles"]:
            print("Profile:", p["id"], "|", p["title"], "| selected:", p["selected"])
        if args.inventory_csv:
            out = private_destination(args.inventory_csv)
            with out.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["version_id", "v_id", "sv_id", "severity", "title"])
                writer.writeheader()
                writer.writerows(meta["rules"])
            out.chmod(0o600)
            print("PRIVATE inventory CSV:", out)
        print("No RHEL host was scanned. No compliance/ATO claim.")
        return 0
    except (OSError, ValueError, ET.ParseError, zipfile.BadZipFile) as exc:
        print("Benchmark inspection failed:", exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
