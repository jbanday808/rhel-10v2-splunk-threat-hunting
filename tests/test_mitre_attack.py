"""Offline consistency checks; these do not execute searches or validate a lab."""

import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAYER = ROOT / "docs/mitre-attack/navigator-layer.json"
COVERAGE = ROOT / "docs/mitre-attack/coverage.md"
HUNTS = ROOT / "hunts/mitre-attack"

# Active Enterprise ATT&CK v20.1 identifiers reviewed in the mapping.
EXPECTED = {
    "T1059.001": "Candidate",
    "T1136.001": "Candidate",
    "T1098.007": "Candidate",
    "T1053.005": "Candidate",
    "T1547.001": "Candidate",
    "T1685.005": "Candidate",
    "T1110.001": "Candidate",
    "T1110.003": "Candidate",
    "T1078": "Context only",
    "T1071.001": "Context only",
    "T1071.004": "Context only",
    "T1021.004": "Context only",
    "T1566.001": "Gap",
    "T1136.003": "Gap",
    "T1098.003": "Gap",
    "T1003.001": "Gap",
    "T1047": "Gap",
    "T1021.002": "Gap",
    "T1685.006": "Gap",
    "T1005": "Gap",
    "T1041": "Gap",
    "T1486": "Gap",
}
COLORS = {
    "Candidate": "#f6c65b",
    "Context only": "#85bfe7",
    "Gap": "#cbd0d5",
}
REFERENCE = {
    "T1059.001": ("PowerShell", {"Execution"}),
    "T1136.001": ("Local Account", {"Persistence"}),
    "T1098.007": ("Additional Local or Domain Groups", {"Persistence", "Privilege Escalation"}),
    "T1053.005": ("Scheduled Task", {"Execution", "Persistence", "Privilege Escalation"}),
    "T1547.001": ("Registry Run Keys / Startup Folder", {"Persistence", "Privilege Escalation"}),
    "T1685.005": ("Clear Windows Event Logs", {"Defense Impairment"}),
    "T1110.001": ("Password Guessing", {"Credential Access"}),
    "T1110.003": ("Password Spraying", {"Credential Access"}),
    "T1078": ("Valid Accounts", {"Initial Access", "Persistence", "Privilege Escalation", "Stealth"}),
    "T1071.001": ("Web Protocols", {"Command and Control"}),
    "T1071.004": ("DNS", {"Command and Control"}),
    "T1021.004": ("SSH", {"Lateral Movement"}),
    "T1566.001": ("Spearphishing Attachment", {"Initial Access"}),
    "T1136.003": ("Cloud Account", {"Persistence"}),
    "T1098.003": ("Additional Cloud Roles", {"Persistence", "Privilege Escalation"}),
    "T1003.001": ("LSASS Memory", {"Credential Access"}),
    "T1047": ("Windows Management Instrumentation", {"Execution"}),
    "T1021.002": ("SMB/Windows Admin Shares", {"Lateral Movement"}),
    "T1685.006": ("Clear Linux or Mac System Logs", {"Defense Impairment"}),
    "T1005": ("Data from Local System", {"Collection"}),
    "T1041": ("Exfiltration Over C2 Channel", {"Exfiltration"}),
    "T1486": ("Data Encrypted for Impact", {"Impact"}),
}


class MitreAttackMappingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.layer = json.loads(LAYER.read_text(encoding="utf-8"))
        cls.coverage = COVERAGE.read_text(encoding="utf-8")

    def test_navigator_version_and_unique_techniques(self):
        self.assertEqual(self.layer["domain"], "enterprise-attack")
        self.assertEqual(self.layer["versions"]["attack"], "20")
        self.assertEqual(self.layer["versions"]["layer"], "4.5")
        techniques = self.layer["techniques"]
        ids = [item["techniqueID"] for item in techniques]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), set(EXPECTED))
        self.assertEqual({item["color"] for item in self.layer["legendItems"]},
                         set(COLORS.values()))

    def test_statuses_colors_and_search_paths(self):
        for item in self.layer["techniques"]:
            with self.subTest(technique=item["techniqueID"]):
                technique = item["techniqueID"]
                metadata = {entry["name"]: entry["value"] for entry in item["metadata"]}
                status = EXPECTED[technique]
                self.assertEqual(metadata.get("Status"), status)
                self.assertEqual(item["color"], COLORS[status])
                self.assertIn(f"[{technique} ", self.coverage)
                if status != "Gap":
                    path = (ROOT / metadata["Search"]).resolve()
                    self.assertTrue(path.is_relative_to(HUNTS.resolve()))
                    self.assertTrue(path.is_file())
                    self.assertEqual(path.suffix, ".spl")
                else:
                    self.assertNotIn("Search", metadata)

    def test_coverage_rows_match_reviewed_names_tactics_and_statuses(self):
        pattern = (
            r"^\| \[(T\d{4}(?:\.\d{3})?) ([^]]+)\]\(([^)]+)\)"
            r" — ([^|]+) \|.*\| (Candidate|Context only|Gap) \|$"
        )
        rows = re.findall(pattern, self.coverage, flags=re.MULTILINE)
        self.assertEqual(len(rows), len(EXPECTED))
        self.assertEqual({row[0] for row in rows}, set(EXPECTED))
        self.assertEqual(set(REFERENCE), set(EXPECTED))
        for technique, name, url, tactics, status in rows:
            with self.subTest(technique=technique):
                expected_name, expected_tactics = REFERENCE[technique]
                self.assertEqual(name, expected_name)
                self.assertEqual({tactic.strip() for tactic in tactics.split(",")},
                                 expected_tactics)
                self.assertEqual(status, EXPECTED[technique])
                self.assertEqual(
                    url,
                    "https://attack.mitre.org/techniques/"
                    + technique.replace(".", "/") + "/",
                )

    def test_spl_queries_have_index_time_and_question(self):
        searches = sorted(HUNTS.glob("*.spl"))
        self.assertEqual(len(searches), 11)
        for path in searches:
            with self.subTest(search=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertRegex(text, r"\bindex=(?:sysmon|win_security|win_system|powershell|linux)\b")
                self.assertRegex(text, r"\bearliest=-\d+[hd]\b")
                self.assertIn("```Question:", text)

    def test_documented_relative_links_exist(self):
        docs = [
            ROOT / "README.md",
            ROOT / "docs/mitre-attack/README.md",
            COVERAGE,
            ROOT / "docs/mitre-attack/hunt-playbook.md",
            ROOT / "docs/mitre-attack/role-alignment.md",
            HUNTS / "README.md",
            ROOT / "evidence/sanitized/mitre-attack-validation.md",
        ]
        for doc in docs:
            text = doc.read_text(encoding="utf-8")
            for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                if link.startswith(("https://", "http://", "#", "mailto:")):
                    continue
                with self.subTest(document=doc.name, link=link):
                    target = link.split("#", 1)[0]
                    self.assertTrue((doc.parent / target).exists())

    def test_optional_kql_is_explicitly_separate_and_uses_process_identity(self):
        text = (HUNTS / "optional-defender-powershell-network.kql").read_text(
            encoding="utf-8"
        )
        self.assertIn("Requires separately deployed Defender for Endpoint", text)
        for field in ("DeviceProcessEvents", "DeviceNetworkEvents", "DeviceId",
                      "ProcessId", "ProcessCreationTime", "InitiatingProcessId",
                      "InitiatingProcessCreationTime"):
            self.assertIn(field, text)

    def test_account_group_search_filters_each_addition_to_window(self):
        text = (HUNTS / "03-account-to-group.spl").read_text(encoding="utf-8")
        self.assertIn("coalesce(TargetSid,Target_Sid)", text)
        self.assertIn("coalesce(MemberSid,Member_Sid)", text)
        self.assertIn("last(created_time) as created_at", text)
        self.assertIn("_time-created_at<=3600", text)
        self.assertLess(text.index("| streamstats"), text.index("| where event_code=4732"))
        self.assertLess(text.index("| where event_code=4732"), text.index("| table"))

    def test_project_validator_checks_spl_and_kql_text(self):
        spec = importlib.util.spec_from_file_location(
            "lab_validate_project", ROOT / "scripts/validate_project.py"
        )
        validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validator)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in validator.REQUIRED:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / name, target)
            steps = root / "docs/steps"
            steps.mkdir(parents=True, exist_ok=True)
            for number in range(1, 53):
                (steps / f"{number:02d}-fixture.md").write_text("", encoding="utf-8")
            marker = "-" * 5 + "BEGIN " + "PRIVATE KEY" + "-" * 5
            for extension in ("spl", "kql"):
                (root / f"hunts/fixture.{extension}").write_text(marker, encoding="utf-8")
            errors = validator.validate(root)
            for extension in ("spl", "kql"):
                self.assertIn(f"Private key material: hunts/fixture.{extension}", errors)

    def test_publication_preflight_scans_kql(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / "tools").mkdir()
            shutil.copyfile(ROOT / "tools/publication_preflight.py",
                            root / "tools/publication_preflight.py")
            (root / "hunts").mkdir()
            query = root / "hunts/fixture.kql"
            query.write_text("DeviceProcessEvents | take 1\n", encoding="utf-8")
            command = [sys.executable, str(root / "tools/publication_preflight.py")]
            clean = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(clean.returncode, 0, clean.stdout + clean.stderr)
            fake_token = "gh" + "p_" + "Z" * 36
            query.write_text(fake_token, encoding="utf-8")
            flagged = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertNotEqual(flagged.returncode, 0)
            self.assertIn("GitHub token-shaped value: hunts/fixture.kql", flagged.stdout)


if __name__ == "__main__":
    unittest.main()
