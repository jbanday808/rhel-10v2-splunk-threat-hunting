"""Exercise private ePO workbook safeguards using synthetic XML only."""

import importlib.util
import os
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "epo_workbook", ROOT / "scripts/stig-epo/build_private_workbook.py"
)
workbook = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(workbook)


def fixture(release="8"):
    return f"""<?xml version="1.0"?>
<Benchmark xmlns="http://checklists.nist.gov/xccdf/1.1">
  <title>ESS ePO 5.x Security Technical Implementation Guide</title>
  <version>3</version>
  <plain-text id="release-info">Release: {release}</plain-text>
  <Group id="SYNTHETIC-GROUP">
    <Rule id="SYNTHETIC-RULE" severity="medium">
      <version>TEST-1</version>
      <title>Synthetic test title</title>
      <fixtext>Apply the harmless test setting.</fixtext>
      <check><check-content>Review the harmless test setting.</check-content></check>
    </Rule>
  </Group>
</Benchmark>
""".encode("utf-8")


class PrivateWorkbookTests(unittest.TestCase):
    def test_writes_synthetic_rule_and_starts_unreviewed(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source.xml"
            output = Path(tmp) / "workbook.txt"
            source.write_bytes(fixture())
            self.assertEqual(workbook.create_workbook(source, output), 1)
            result = output.read_text(encoding="utf-8")
            self.assertIn("SYNTHETIC-RULE", result)
            self.assertIn("Review the harmless test setting.", result)
            self.assertIn("Apply the harmless test setting.", result)
            self.assertIn("Status: Not Reviewed", result)
            if os.name == "posix":
                self.assertEqual(output.stat().st_mode & 0o777, 0o600)

    def test_refuses_existing_output_and_keeps_original(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source.xml"
            output = Path(tmp) / "workbook.txt"
            source.write_bytes(fixture())
            output.write_text("existing", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                workbook.create_workbook(source, output)
            self.assertEqual(output.read_text(encoding="utf-8"), "existing")

    def test_rejects_different_release_and_external_entities(self):
        with self.assertRaises(ValueError):
            workbook.parse_manual(fixture(release="7"))
        with self.assertRaises(ValueError):
            workbook.parse_manual(b'<!DOCTYPE x [<!ENTITY a "test">]>' + fixture())
        with self.assertRaises(ValueError):
            workbook.parse_manual(fixture().decode("utf-8").encode("utf-16"))

    def test_rejects_incomplete_rule(self):
        broken = fixture().replace(b"<fixtext>Apply the harmless test setting.</fixtext>", b"")
        with self.assertRaises(ValueError):
            workbook.parse_manual(broken)

    def test_rejects_git_checkout_for_source_or_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            checkout = root / "checkout"
            checkout.mkdir()
            (checkout / ".git").mkdir()
            private_source = root / "source.xml"
            private_source.write_bytes(fixture())
            with self.assertRaises(ValueError):
                workbook.create_workbook(private_source, checkout / "workbook.txt")
            source_in_checkout = checkout / "source.xml"
            source_in_checkout.write_bytes(fixture())
            with self.assertRaises(ValueError):
                workbook.create_workbook(source_in_checkout, root / "workbook.txt")
            self.assertFalse((checkout / "workbook.txt").exists())
            self.assertFalse((root / "workbook.txt").exists())

    @unittest.skipUnless(hasattr(os, "symlink"), "Symbolic links unavailable")
    def test_rejects_dangling_output_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.xml"
            source.write_bytes(fixture())
            target = root / "target.txt"
            link = root / "workbook.txt"
            try:
                link.symlink_to(target)
            except OSError:
                self.skipTest("Symbolic-link creation is not permitted")
            with self.assertRaises(ValueError):
                workbook.create_workbook(source, link)
            self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
