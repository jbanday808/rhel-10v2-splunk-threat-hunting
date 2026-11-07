#!/usr/bin/env python3
"""Create a private text workbook from a local ePO 5.x V3R8 manual XCCDF."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

NAMESPACE = "{http://checklists.nist.gov/xccdf/1.1}"
MAX_INPUT_BYTES = 4 * 1024 * 1024


def require_outside_git(path: Path) -> None:
    for directory in (path, *path.parents):
        if (directory / ".git").exists():
            raise ValueError("Keep source and output outside all Git working trees.")


def text_of(element: ET.Element, path: str, field: str) -> str:
    node = element.find(path)
    text = "".join(node.itertext()).strip() if node is not None else ""
    if not text:
        raise ValueError(f"A rule is missing its {field}.")
    return text


def parse_manual(raw: bytes) -> list[dict[str, str]]:
    if not raw or len(raw) > MAX_INPUT_BYTES:
        raise ValueError("The XML is empty or exceeds the 4 MiB limit.")
    try:
        xml = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("Expected UTF-8 XML.") from exc
    if re.search(r"<!\s*(?:DOCTYPE|ENTITY)\b", xml, re.IGNORECASE):
        raise ValueError("XML document types and entities are not accepted.")

    root = ET.fromstring(xml)
    if root.tag != NAMESPACE + "Benchmark":
        raise ValueError("Expected a manual XCCDF 1.1 Benchmark.")
    title = text_of(root, NAMESPACE + "title", "benchmark title")
    version = text_of(root, NAMESPACE + "version", "benchmark version")
    release = root.find(NAMESPACE + "plain-text[@id='release-info']")
    release_text = "".join(release.itertext()).strip() if release is not None else ""
    if title != "ESS ePO 5.x Security Technical Implementation Guide":
        raise ValueError("The benchmark title does not match ESS ePO 5.x.")
    if version != "3" or not re.search(r"\bRelease:\s*8\b", release_text):
        raise ValueError("Expected Version 3, Release 8.")

    rules = []
    seen = set()
    for group in root.iter(NAMESPACE + "Group"):
        for rule in group.findall(NAMESPACE + "Rule"):
            rule_id = rule.get("id", "").strip()
            group_id = group.get("id", "").strip()
            severity = rule.get("severity", "").strip()
            checks = [
                "".join(check.itertext()).strip()
                for check in rule.findall(NAMESPACE + "check/" + NAMESPACE + "check-content")
                if "".join(check.itertext()).strip()
            ]
            if not rule_id or not group_id or rule_id in seen or not severity or not checks:
                raise ValueError("A rule has missing or duplicated identification or check text.")
            seen.add(rule_id)
            rules.append({
                "group_id": group_id,
                "rule_id": rule_id,
                "version": text_of(rule, NAMESPACE + "version", "version"),
                "title": text_of(rule, NAMESPACE + "title", "title"),
                "severity": severity,
                "check": "\n\n".join(checks),
                "fix": text_of(rule, NAMESPACE + "fixtext", "fix text"),
            })
    if not rules or len(rules) != len(list(root.iter(NAMESPACE + "Rule"))):
        raise ValueError("The manual contains missing or unsupported rule structures.")
    return rules


def render_workbook(rules: list[dict[str, str]]) -> str:
    sections = [
        "CUI - HANDLE ACCORDING TO THE SOURCE AND ORGANIZATION'S APPROVED MARKINGS",
        "ESS ePO 5.x STIG Version 3 Release 8 - Private rule workbook",
        "This working copy contains controlled source text. Apply the source's",
        "category and dissemination markings and use an approved storage location.",
        "The source checklist and authorized assessor determine applicability.",
        "Every rule starts Not Reviewed. Record actual results in STIG Viewer.",
        f"Rules in this source file: {len(rules)}",
        "",
    ]
    for number, rule in enumerate(rules, 1):
        sections.extend([
            "=" * 72,
            f"STEP {number:03d} - {rule['title']}",
            f"Group: {rule['group_id']}",
            f"Rule: {rule['rule_id']}",
            f"Version: {rule['version']}",
            f"Severity: {rule['severity']}",
            "",
            "CHECK - follow the source instructions:",
            rule["check"],
            "",
            "FIX - use only after review and approval:",
            rule["fix"],
            "",
            "Status: Not Reviewed",
            "Evidence / private location:",
            "Owner / change / retest:",
            "",
        ])
    sections.append("CUI - HANDLE ACCORDING TO THE SOURCE AND ORGANIZATION'S APPROVED MARKINGS")
    return "\n".join(sections) + "\n"


def create_workbook(source: Path, output: Path) -> int:
    source = source.expanduser().resolve(strict=True)
    output = output.expanduser()
    if output.is_symlink():
        raise ValueError("The output must not be a symbolic link.")
    output = output.resolve()
    require_outside_git(source.parent)
    require_outside_git(output.parent)
    if not source.is_file() or source.suffix.lower() != ".xml":
        raise ValueError("The source must be an XML file.")
    if output.suffix.lower() != ".txt" or not output.parent.is_dir():
        raise ValueError("Use a .txt output in an existing approved private folder.")
    if source.stat().st_size > MAX_INPUT_BYTES:
        raise ValueError("The input exceeds the 4 MiB limit.")
    with source.open("rb") as stream:
        raw = stream.read(MAX_INPUT_BYTES + 1)
    rules = parse_manual(raw)
    workbook = render_workbook(rules)

    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(output, flags, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(workbook)
    except Exception:
        output.unlink(missing_ok=True)
        raise
    return len(rules)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="Private manual XCCDF XML")
    parser.add_argument("--output", type=Path, required=True, help="New private .txt workbook")
    args = parser.parse_args()
    try:
        count = create_workbook(args.source, args.output)
    except (OSError, ValueError, ET.ParseError) as exc:
        print(f"Workbook not created: {exc}", file=sys.stderr)
        return 1
    print(f"Created private workbook with {count} rule sections.")
    print("Use an approved system and apply the source's handling markings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
