"""Offline shared-regex behavior and safe-merge tests; no Splunk service required."""
import configparser
import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('merge_redaction', ROOT / 'scripts/merge_redaction_config.py')
merge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(merge)


def expression():
    props = configparser.RawConfigParser(interpolation=None)
    props.optionxform = str
    props.read(ROOT / 'apps/LAB_SIEM/local/props.conf')
    command = props.get('identity', 'SEDCMD-redact_pw')
    parts = re.split(r'(?<!\\)/', command)
    if len(parts) != 4 or parts[0] != 's' or parts[3] != 'g':
        raise ValueError('Expected one global sed substitution.')
    return parts[1].replace(r'\/', '/'), parts[2].replace(r'\/', '/')


class RedactionBehavior(unittest.TestCase):
    def test_dummy_fixtures(self):
        pattern, replacement = expression()
        cases = json.loads((ROOT / 'examples/redaction/cases.json').read_text())
        for case in cases:
            with self.subTest(case=case['name']):
                self.assertEqual(re.sub(pattern, replacement, case['input']), case['expected'])

    def test_reapplying_keeps_same_event(self):
        pattern, replacement = expression()
        raw = 'password=LAB-DUMMY-ONE password=LAB-DUMMY-TWO'
        masked = re.sub(pattern, replacement, raw)
        self.assertEqual(re.sub(pattern, replacement, masked), masked)

    def test_source_type_matches_monitor(self):
        conf = configparser.RawConfigParser(interpolation=None)
        conf.read(ROOT / 'apps/LAB_SIEM/local/inputs.conf')
        stanza = 'monitor:///var/log/siem-lab/identity.log'
        self.assertEqual(conf.get(stanza, 'sourcetype'), 'identity')
        self.assertEqual(conf.get(stanza, 'index'), 'lab')
        self.assertEqual(conf.get(stanza, 'disabled'), '0')


class SafeMerge(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.target = self.root / 'local'
        self.target.mkdir()
        self.snippets = ROOT / 'configs/redaction'
        for name in ('inputs.conf', 'props.conf'):
            (self.target / name).write_text('[existing]\nvalue = keep-me\n')

    def test_preview_does_not_write(self):
        self.assertEqual(len(merge.prepare(self.target, self.snippets)), 2)
        self.assertNotIn('identity', (self.target / 'props.conf').read_text())

    def test_apply_preserves_existing_and_creates_backup(self):
        changes = merge.prepare(self.target, self.snippets)
        backup = merge.apply(changes, self.root / 'backups')
        self.assertIn('[existing]\nvalue = keep-me', (self.target / 'props.conf').read_text())
        self.assertEqual((backup / 'props.conf').read_text(), '[existing]\nvalue = keep-me\n')
        self.assertEqual(merge.prepare(self.target, self.snippets), [])

    def test_conflict_prevents_all_writes(self):
        props = self.target / 'props.conf'
        props.write_text('[identity]\nSEDCMD-redact_pw = wrong\n')
        before = (self.target / 'inputs.conf').read_bytes()
        with self.assertRaises(ValueError):
            merge.prepare(self.target, self.snippets)
        self.assertEqual((self.target / 'inputs.conf').read_bytes(), before)

    def test_duplicate_section_rejected(self):
        (self.target / 'props.conf').write_text('[identity]\na = 1\n[identity]\nb = 2\n')
        with self.assertRaises(configparser.Error):
            merge.prepare(self.target, self.snippets)

    @unittest.skipUnless(hasattr(Path, 'symlink_to'), 'Symlink support unavailable')
    def test_target_symlink_rejected(self):
        target = self.target / 'props.conf'
        outside = self.root / 'outside.conf'
        target.rename(outside)
        target.symlink_to(outside)
        with self.assertRaises(ValueError):
            merge.prepare(self.target, self.snippets)


if __name__ == '__main__':
    unittest.main()
