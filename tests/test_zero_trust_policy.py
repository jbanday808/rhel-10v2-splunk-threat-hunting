"""Offline tests for the proposed Zero Trust flow policy; no networking/deployment."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "configs/zero-trust/allowed-flows.example.json"
MODULE_PATH = ROOT / "scripts/zero-trust/validate_policy.py"
spec = importlib.util.spec_from_file_location("zt_policy_validator", MODULE_PATH)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ZeroTrustPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))

    def test_offline_policy_valid(self):
        self.assertEqual(validator.validate(self.policy), [])

    def test_never_claim_deployed(self):
        bad = copy.deepcopy(self.policy)
        bad["status"] = "fully_deployed"
        self.assertNotEqual(validator.validate(bad), [])

    def test_no_remote_splunk_management_port(self):
        bad = copy.deepcopy(self.policy)
        bad["allowed_flows"][0]["port"] = 8089
        self.assertTrue(any("8089" in x for x in validator.validate(bad)))

    def test_no_conflicting_denied_flows(self):
        bad = copy.deepcopy(self.policy)
        bad["denied_examples"][0]["source"] = "management_host"
        self.assertTrue(any("conflicts" in x for x in validator.validate(bad)))

    def test_duplicate_rule_is_rejected(self):
        bad = copy.deepcopy(self.policy)
        bad["allowed_flows"].append(copy.deepcopy(bad["allowed_flows"][0]))
        self.assertNotEqual(validator.validate(bad), [])

    def test_existing_docs_preserved(self):
        for path in [
            "docs/steps/README.md",
            "apps/LAB_SIEM/local/authorize.conf",
            "start-here/START_HERE_RHEL10v2.md",
            "docs/zero-trust/IMPLEMENTATION_GUIDE.md",
        ]:
            self.assertTrue((ROOT / path).exists(), path)

    def test_complete_pillar_documentation(self):
        data = (ROOT / "docs/zero-trust/02-dod-seven-pillars.md").read_text(encoding="utf-8")
        for pillar in [
            "User", "Device", "Application & Workload", "Data",
            "Network & Environment", "Automation & Orchestration", "Visibility & Analytics",
        ]:
            self.assertIn(pillar, data)


if __name__ == "__main__":
    unittest.main()
