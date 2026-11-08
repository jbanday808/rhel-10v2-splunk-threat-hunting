"""Pattern-boundary checks; no Windows simulation or Splunk engine is run."""
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
HUNTS = ROOT / 'hunts/cobalt-strike'


def pattern_from(filename):
    text = (HUNTS / filename).read_text(encoding='utf-8')
    found = re.findall(r'match\(pipe_leaf,\s*"([^"]+)"\)', text)
    if len(found) != 1:
        raise AssertionError(f'Expected one name pattern in {filename}')
    return found[0]


class CobaltPipePatternTests(unittest.TestCase):
    def setUp(self):
        self.pattern = re.compile(pattern_from('01-default-pipe-candidates.spl'))

    def test_positive_names_and_path_formats(self):
        cases = [
            r'\postex_a1b2c3d4', r'\\.\pipe\msagent_aabbccdd',
            'POSTEX_ABCD1234', r'\postex_ssh_1234abcd', r'\MSSE-1234-server',
        ]
        for pipe in cases:
            with self.subTest(pipe=pipe):
                leaf = pipe.rsplit('\\', 1)[-1].lower()
                self.assertIsNotNone(self.pattern.search(leaf))

    def test_benign_and_near_miss_names_do_not_match(self):
        cases = [
            r'\SIEMLabControl_20261107', 'postex_not_hex', 'mypostex_a1b2c3d4',
            'postex_a1b2.exe', 'msagent_', 'MSSE-abc-server', '',
            'postex_abcd_suffix', 'postex_abcd\nother',
        ]
        for pipe in cases:
            with self.subTest(pipe=pipe):
                leaf = pipe.rsplit('\\', 1)[-1].lower()
                self.assertIsNone(self.pattern.search(leaf))

    def test_pattern_and_normalization_are_consistent_across_searches(self):
        expected = pattern_from('01-default-pipe-candidates.spl')
        for name in ('01-default-pipe-candidates.spl', '02-process-context.spl',
                     '03-synthetic-pattern-self-test.spl'):
            with self.subTest(name=name):
                self.assertEqual(pattern_from(name), expected)
                self.assertIn('split(pipe_name,urldecode("%5C"))', (HUNTS / name).read_text())

    def test_telemetry_fragment_collects_both_controls(self):
        fragment = ET.parse(ROOT / 'configs/sysmon/pipe-events.xml.example').getroot()
        self.assertEqual(fragment.tag, 'RuleGroup')
        self.assertEqual(fragment.attrib['groupRelation'], 'or')
        rules = fragment.find('PipeEvent')
        self.assertEqual(rules.attrib['onmatch'], 'include')
        prefixes = [node.text.lower() for node in rules.findall('PipeName')]
        for name in (r'\postex_a1b2c3d4', r'\SIEMLabControl_20261107'):
            self.assertTrue(any(name.lower().startswith(prefix) for prefix in prefixes))

    def test_documented_main_query_matches_search_file(self):
        guide = (ROOT / 'docs/splunk/COBALT_STRIKE_ATOMIC_VALIDATION.md').read_text()
        blocks = re.findall(r'```spl\n(.*?)```', guide, re.S)
        candidate = (HUNTS / '01-default-pipe-candidates.spl').read_text()
        self.assertIn(candidate, blocks)

    def test_process_context_uses_host_and_guid_and_preserves_base_candidates(self):
        context = (HUNTS / '02-process-context.spl').read_text()
        candidate = (HUNTS / '01-default-pipe-candidates.spl').read_text()
        self.assertIn('by host process_guid', context)
        self.assertIn('isnotnull(process_guid)', context)
        self.assertNotIn('isnotnull(process_guid)', candidate)
        self.assertNotIn('by ProcessId', context)


if __name__ == '__main__':
    unittest.main()
