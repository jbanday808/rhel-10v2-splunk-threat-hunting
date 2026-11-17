"""Exercise the action boundary, outputs, and trusted validator loading."""
from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('source_check_action', ROOT / 'scripts/run_source_check_action.py')
action = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(action)


class SourceCheckActionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.target = self.workspace / 'lab with spaces'
        self.target.mkdir()
        self.environment = {
            'GITHUB_WORKSPACE': str(self.workspace),
            'SOURCE_CHECK_PATH': self.target.name,
            'SOURCE_CHECK_VERIFY_MANIFEST': 'false',
            'GITHUB_OUTPUT': str(self.workspace / 'output'),
            'GITHUB_STEP_SUMMARY': str(self.workspace / 'summary'),
        }

    def run_action(self, validator=None):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            result = action.main(self.environment, validator)
        return result, stdout.getvalue() + stderr.getvalue()

    def test_success_outputs_and_manifest_option(self):
        self.environment['SOURCE_CHECK_VERIFY_MANIFEST'] = 'true'
        check = Mock(return_value=[])
        result, logs = self.run_action(check)
        self.assertEqual(result, 0)
        check.assert_called_once_with(self.target.resolve(), True)
        self.assertEqual((self.workspace / 'output').read_text(), 'result=passed\nerror-count=0\n')
        self.assertIn('Errors: **0**', (self.workspace / 'summary').read_text())
        self.assertIn('unverified', logs)

    def test_failure_does_not_emit_untrusted_diagnostics(self):
        payload = 'bad file\n::warning::injected\nprivate-value'
        result, logs = self.run_action(Mock(return_value=[payload, 'second error']))
        self.assertEqual(result, 1)
        self.assertEqual((self.workspace / 'output').read_text(), 'result=failed\nerror-count=2\n')
        summary = (self.workspace / 'summary').read_text()
        self.assertNotIn('private-value', logs + summary)
        self.assertNotIn('::warning::', logs + summary)
        self.assertIn('Errors: **2**', summary)

    def test_invalid_boolean_fails_without_calling_validator(self):
        self.environment['SOURCE_CHECK_VERIFY_MANIFEST'] = 'yes'
        check = Mock(return_value=[])
        result, _ = self.run_action(check)
        self.assertEqual(result, 1)
        check.assert_not_called()
        self.assertIn('error-count=1', (self.workspace / 'output').read_text())

    def test_path_outside_workspace_is_rejected(self):
        self.environment['SOURCE_CHECK_PATH'] = '..'
        check = Mock(return_value=[])
        result, _ = self.run_action(check)
        self.assertEqual(result, 1)
        check.assert_not_called()

    def test_missing_path_and_file_path_are_rejected(self):
        for value in ('missing', '', 'line\nbreak'):
            with self.subTest(value=value):
                self.environment['SOURCE_CHECK_PATH'] = value
                check = Mock(return_value=[])
                self.assertEqual(self.run_action(check)[0], 1)
                check.assert_not_called()
        (self.target / 'file').write_text('example')
        with self.assertRaises(ValueError):
            action.target_directory(str(self.workspace), str(self.target / 'file'))

    def test_outside_symlink_is_rejected(self):
        try:
            (self.target / 'outside').symlink_to(self.workspace / 'output')
        except OSError:
            self.skipTest('Symbolic-link creation is unavailable on this runner.')
        check = Mock(return_value=[])
        self.assertEqual(self.run_action(check)[0], 1)
        check.assert_not_called()

    def test_bundled_validator_rejects_incomplete_source(self):
        # A target-side Python file must be inspected as data, never imported.
        (self.target / 'validate_project.py').write_text('raise RuntimeError("must not execute")\n')
        result, logs = self.run_action()
        self.assertEqual(result, 1)
        self.assertIn('Source validation failed', logs)
        self.assertNotIn('must not execute', logs)

    def test_bundled_validator_accepts_repository_source(self):
        self.environment['GITHUB_WORKSPACE'] = str(ROOT)
        self.environment['SOURCE_CHECK_PATH'] = '.'
        self.assertEqual(self.run_action()[0], 0)

    def test_validator_read_error_fails_with_outputs(self):
        result, logs = self.run_action(Mock(side_effect=OSError('private filename')))
        self.assertEqual(result, 1)
        self.assertNotIn('private filename', logs)
        self.assertIn('result=failed', (self.workspace / 'output').read_text())

    def test_unexpected_validator_error_fails_with_outputs(self):
        result, logs = self.run_action(Mock(side_effect=AttributeError('private source text')))
        self.assertEqual(result, 1)
        self.assertNotIn('private source text', logs)
        self.assertIn('error-count=1', (self.workspace / 'output').read_text())

    def test_invalid_output_path_fails_action(self):
        self.environment['GITHUB_OUTPUT'] = str(self.workspace / 'missing' / 'output')
        self.assertEqual(self.run_action(Mock(return_value=[]))[0], 1)


if __name__ == '__main__':
    unittest.main()
