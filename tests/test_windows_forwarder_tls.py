"""Check that the packaged Windows forwarding example keeps TLS verification on."""

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('lab_validate_project', ROOT / 'scripts/validate_project.py')
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class WindowsForwarderTlsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.checkout = Path(cls.temp.name) / 'project'
        shutil.copytree(ROOT, cls.checkout, ignore=shutil.ignore_patterns('.git', '__pycache__'))
        cls.outputs = cls.checkout / 'apps/LAB_UF_WINDOWS/local/outputs.conf'
        cls.original = cls.outputs.read_text(encoding='utf-8')

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def tearDown(self):
        self.outputs.write_text(self.original, encoding='utf-8')

    def test_packaged_settings_pass_source_validation(self):
        self.assertEqual(VALIDATOR.validate(self.checkout), [])

    def test_disabled_or_missing_tls_controls_fail_source_validation(self):
        cases = (
            ('useSSL = true', 'useSSL = false', 'explicitly enable TLS'),
            ('useSSL = true\n', '', 'explicitly enable TLS'),
            ('sslVerifyServerCert = true', 'sslVerifyServerCert = false', 'verify the receiving certificate'),
            ('sslVerifyServerName = true', 'sslVerifyServerName = false', 'verify the receiving hostname'),
        )
        for before, after, expected in cases:
            with self.subTest(setting=before, replacement=after):
                self.assertEqual(self.original.count(before), 1)
                self.outputs.write_text(self.original.replace(before, after, 1), encoding='utf-8')
                errors = VALIDATOR.validate(self.checkout)
                self.assertTrue(any(expected in error for error in errors), errors)


if __name__ == '__main__':
    unittest.main()
