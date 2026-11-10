"""Offline source tests. No RHEL host scan, STIG deployment or government compliance claim."""
import importlib.util
import re
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def import_tool(path, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


inspector = import_tool("scripts/stig/inspect_benchmark.py", "stig_inspector")
summarizer = import_tool("scripts/stig/summarize_results.py", "stig_results")
SCAP_XML = b"""<?xml version="1.0"?>
<ds:data-stream-collection xmlns:ds="http://scap.nist.gov/schema/scap/source/1.2"
 xmlns:x="http://checklists.nist.gov/xccdf/1.2">
 <ds:data-stream scap-version="1.3"/>
 <x:Benchmark id="benchmark-fixture">
  <x:title>Test only</x:title><x:version>001.001</x:version>
  <x:Profile id="fixture"><x:title>Test profile</x:title>
   <x:select idref="test-rule" selected="true"/>
  </x:Profile>
  <x:Group id="xccdf_mil.disa.stig_group_V-001">
   <x:Rule id="xccdf_mil.disa.stig_rule_SV-001_rule" severity="medium">
    <x:title>Test fixture</x:title><x:version>RHEL-10-TEST</x:version>
   </x:Rule>
  </x:Group>
 </x:Benchmark>
</ds:data-stream-collection>"""
RESULT_XML = b"""<?xml version="1.0"?>
<x:Benchmark xmlns:x="http://checklists.nist.gov/xccdf/1.2">
 <x:TestResult id="fixture">
  <x:rule-result idref="rule-1"><x:result>fail</x:result></x:rule-result>
  <x:rule-result idref="rule-2"><x:result>notapplicable</x:result></x:rule-result>
 </x:TestResult>
</x:Benchmark>"""


class StigRhel10ToolsTests(unittest.TestCase):
    def test_inspector_extracts_rule_and_profile(self):
        meta = inspector.parse_benchmark(SCAP_XML)
        self.assertEqual(meta["rule_count"], 1)
        self.assertEqual(meta["severity"], {"medium": 1})
        self.assertEqual(meta["version"], "001.001")
        self.assertEqual(meta["scap_version"], "1.3")
        self.assertEqual(meta["rules"][0]["v_id"], "V-001")
        self.assertEqual(meta["profiles"][0]["selected"], 1)

    def test_zip_is_read_without_extracting(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "source.zip"
            with zipfile.ZipFile(path, "w") as z:
                z.writestr("data.xml", SCAP_XML)
            self.assertEqual(inspector.load_data(path), SCAP_XML)
            self.assertFalse((Path(tmp) / "data.xml").exists())

    def test_zip_with_extra_members_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "source.zip"
            with zipfile.ZipFile(path, "w") as z:
                z.writestr("data.xml", SCAP_XML)
                z.writestr("unexpected.xml", SCAP_XML)
            with self.assertRaises(ValueError):
                inspector.load_data(path)

    def test_bad_benchmark_refused(self):
        with self.assertRaises(ValueError):
            inspector.parse_benchmark(b"<unexpected/>")

    def test_result_states_are_separate(self):
        rows, runs = summarizer.parse_results(RESULT_XML)
        self.assertEqual(runs, 1)
        self.assertEqual({x["result"] for x in rows}, {"fail", "notapplicable"})

    def test_empty_report_not_treated_as_pass(self):
        with self.assertRaises(ValueError):
            summarizer.parse_results(b"<root/>")

    def test_scan_wrapper_never_automatically_remediates(self):
        content = (ROOT / "scripts/stig/scan-rhel10-readonly.sh").read_text()
        self.assertNotIn("--remediate", content)
        self.assertIn("oscap xccdf eval", content)
        self.assertIn("--results-arf", content)

    def test_preserves_lab_and_new_stig_docs(self):
        for path in (
            "README.md",
            "start-here/START_HERE_RHEL10v2.md",
            "start-here/START_HERE_RHEL10v2_STIG.md",
            "docs/zero-trust/09-rmf-stig-ato.md",
            "docs/stig-rhel10/IMPLEMENTATION_GUIDE.md",
            "apps/LAB_SIEM/local/authorize.conf",
        ):
            self.assertTrue((ROOT / path).is_file(), path)

    def test_restored_stig_docs_relative_links_exist(self):
        docs = [
            ROOT / "docs/stig-rhel10/IMPLEMENTATION_GUIDE.md",
            ROOT / "docs/zero-trust/09-rmf-stig-ato.md",
            ROOT / "docs/zero-trust/06-network-microsegmentation.md",
        ]
        docs.extend((ROOT / "docs/stig-rhel10").glob("*.md"))
        for doc in sorted(set(docs)):
            text = doc.read_text(encoding="utf-8")
            for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                if link.startswith(("https://", "http://", "#", "mailto:")):
                    continue
                with self.subTest(document=doc.relative_to(ROOT), link=link):
                    target = link.split("#", 1)[0]
                    self.assertTrue((doc.parent / target).exists())


if __name__ == "__main__":
    unittest.main()
