"""Offline completeness checks for the user-supplied IAVM notice record."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTICE = ROOT / "docs/iavm/notices/2026-A-1195.md"


class IavmNoticeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = NOTICE.read_text(encoding="utf-8")

    def section(self, name):
        match = re.search(
            rf"^## {re.escape(name)}\n(.*?)(?=^## |\Z)",
            self.text,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(match, f"Missing section: {name}")
        return match.group(1)

    def test_notice_cve_list_is_not_conflated_with_vendor_extras(self):
        expected = {f"CVE-2026-{number}" for number in range(76287, 76299)}
        expected.update({"CVE-2026-76301", "CVE-2026-76302"})
        listed = set(re.findall(r"CVE-2026-\d+", self.section("CVEs")))
        self.assertEqual(listed, expected)
        reconciliation = self.section("Reconciling the notice and vendor advisories")
        for value in ("SVD-2026-1007", "SVD-2026-1008",
                      "CVE-2026-76299", "CVE-2026-76300", "not included"):
            self.assertIn(value, reconciliation)

    def test_notice_fields_and_countermeasure_sections_are_present(self):
        for field in ("Issuing Organization", "Notice Type", "Title", "Notice Number",
                      "Revision Number", "CTO Number",
                      "Severity", "Vendor", "STIG Finding Severity", "Superseded By",
                      "Supersedes", "Known Exploits", "Known DoD Incidents"):
            with self.subTest(field=field):
                self.assertIn(f"| {field} |", self.section("Notice metadata"))
        for heading in ("References", "CVEs", "BIDs", "Timeline Summary",
                        "Revision History", "Executive Summary", "Technical Overview",
                        "Vulnerable Applications/Systems and Countermeasures",
                        "IAVM Scanner"):
            with self.subTest(heading=heading):
                self.section(heading)
        for heading in ("Fix Action", "Note", "Patches", "Temporary Mitigation Strategy",
                        "Vulnerable Applications/Systems with Fixes Available",
                        "Vulnerable Applications/Systems with No Patches Available, but with DCDC or Vendor Temporary Recommended Mitigations Available",
                        "Vulnerable Applications/Systems with No Patch or Temporary Recommended Mitigations Available"):
            with self.subTest(heading=heading):
                self.assertIn(f"### {heading}", self.text)

    def test_notice_bids_timeline_and_revision_match_source(self):
        expected_bids = {
            "228268", "228266", "228264", "228267", "228265", "228263",
            "228270", "228269", "228291", "228290", "228289", "228288",
            "228292", "228293",
        }
        bids = re.findall(r"`(\d{6})`", self.section("BIDs"))
        self.assertEqual(len(bids), len(expected_bids))
        self.assertEqual(set(bids), expected_bids)
        timeline = self.section("Timeline Summary")
        for field, date in (
            ("Release Date", "22 Oct 2026"),
            ("Acknowledge Date", "27 Oct 2026"),
            ("First Report Date", "01 Nov 2026"),
            ("CDR Override Mitigation Date", "12 Nov 2026"),
        ):
            self.assertIn(f"| {field} | {date} |", timeline)
        self.assertIn(
            "| `0.0` | 22 Oct 2026 | Initial Release | Not supplied | Not supplied |",
            self.section("Revision History"),
        )

    def test_fixed_versions_and_additional_actions_are_documented(self):
        for version in ("10.4.4", "10.2.8", "10.0.11", "9.4.16",
                        "3.10.12", "3.9.26", "3.8.73"):
            with self.subTest(version=version):
                self.assertIn(f"`{version}`", self.text)
        self.assertIn("Enterprise upgrade alone", self.text)
        self.assertIn("CVE-2026-76290", self.text)
        self.assertIn("ACAS | N/A", self.text)
        self.assertIn("MDE | N/A", self.text)
        for row in (
            "| 10.4 | 10.4.0-10.4.3 | `10.4.4` |",
            "| 10.2 | 10.2.0-10.2.7 | `10.2.8` |",
            "| 10.0 | 10.0.0-10.0.10 | `10.0.11` |",
            "| 9.4 | 9.4.0-9.4.15 | `9.4.16` |",
        ):
            self.assertIn(row, self.text)

    def test_relative_document_links_exist(self):
        paths = (
            ROOT / "README.md",
            ROOT / "docs/iavm/README.md",
            NOTICE,
            ROOT / "evidence/sanitized/iavm-2026-a-1195-validation.md",
        )
        for path in paths:
            for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                if link.startswith(("https://", "http://", "#", "mailto:")):
                    continue
                with self.subTest(document=path.name, link=link):
                    self.assertTrue((path.parent / link.split("#", 1)[0]).exists())


if __name__ == "__main__":
    unittest.main()
