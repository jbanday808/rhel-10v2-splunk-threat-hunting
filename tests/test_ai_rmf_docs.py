"""Offline source-structure checks. These do NOT test an AI model or NIST compliance."""
import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AiRmfDocumentationTests(unittest.TestCase):
    def test_use_case_has_human_review_and_no_autonomy(self):
        data = json.loads(
            (ROOT / "examples/ai-rmf/ai-use-case.example.json").read_text(encoding="utf-8")
        )
        self.assertEqual(data["status"], "proposed_not_deployed")
        self.assertTrue(data["human_review_required"])
        self.assertFalse(data["autonomous_actions_allowed"])
        self.assertFalse(data["external_model_connection_approved"])
        self.assertEqual(data["authorization_to_operate"], "not_granted")
        self.assertEqual(data["fips_199_categorization"], "pending")

    def test_example_risks_are_not_claimed_resolved(self):
        with (ROOT / "examples/ai-rmf/ai-risk-register.example.csv").open(
            encoding="utf-8", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))
        self.assertGreaterEqual(len(rows), 8)
        self.assertEqual(len({row["risk_id"] for row in rows}), len(rows))
        self.assertTrue(all(row["status"] == "Proposed" for row in rows))
        self.assertTrue(all(row["evidence_id"] == "Pending" for row in rows))

    def test_documents_are_present(self):
        docs = [
            "README.md", "IMPLEMENTATION_GUIDE.md", "01-use-case-scope.md",
            "02-system-boundary-and-flow.md", "03-nist-rmf-7-steps.md",
            "04-ai-rmf-core.md", "05-control-crosswalk.md",
            "06-testing-and-assessment.md", "07-monitoring-and-decision.md",
            "08-official-references.md", "09-system-security-plan-template.md",
            "10-poam-template.md", "11-evidence-and-screenshots.md",
        ]
        missing = [name for name in docs if not (ROOT / "docs/ai-rmf" / name).is_file()]
        self.assertFalse(missing, f"Missing documentation: {missing}")

    def test_synthetic_cases_are_not_live_evidence(self):
        payload = json.loads(
            (ROOT / "examples/ai-rmf/synthetic-test-cases.example.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertIn("synthetic", payload["disclaimer"].lower())
        self.assertGreaterEqual(len(payload["test_cases"]), 5)
        self.assertEqual(
            len({case["id"] for case in payload["test_cases"]}),
            len(payload["test_cases"]),
        )


if __name__ == "__main__":
    unittest.main()
