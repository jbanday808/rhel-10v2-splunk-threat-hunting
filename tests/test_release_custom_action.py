"""Exercise release decisions without creating tags or contacting GitHub."""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/release_custom_action.py'
SPEC = importlib.util.spec_from_file_location('release_custom_action', SCRIPT)
release_action = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release_action)
COMMIT = 'a' * 40
OLDER_COMMIT = 'b' * 40


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / 'scripts').mkdir()
        (self.root / '.github').mkdir()
        (self.root / 'ACTION_VERSION').write_text('1.0.0\n', encoding='utf-8')
        (self.root / '.github/action-release-notes.md').write_text('Source validation action.', encoding='utf-8')
        self.environment = patch.dict(os.environ, {
            'GITHUB_REPOSITORY': release_action.REPOSITORY,
            'GITHUB_REF': 'refs/heads/main',
            'GITHUB_SHA': COMMIT,
            'GITHUB_STEP_SUMMARY': str(self.root / 'summary.md'),
        }, clear=True)
        self.environment.start()
        self.script_path = patch.object(release_action, '__file__', str(self.root / 'scripts/release_custom_action.py'))
        self.script_path.start()
        self.cli = patch.object(release_action, 'gh')
        self.mock_cli = self.cli.start()
        self.addCleanup(self.temporary.cleanup)
        self.addCleanup(self.environment.stop)
        self.addCleanup(self.script_path.stop)
        self.addCleanup(self.cli.stop)

    def test_rejects_other_repository_or_non_main_branch(self):
        for name, value in (
            ('GITHUB_REPOSITORY', 'someone/else'),
            ('GITHUB_REF', 'refs/heads/feature'),
            ('GITHUB_SHA', 'not-a-commit'),
        ):
            with self.subTest(name=name), patch.dict(os.environ, {name: value}):
                with self.assertRaises(ValueError):
                    release_action.main()
        self.mock_cli.assert_not_called()

    def test_rejects_invalid_version_before_network_calls(self):
        for version in ('01.0.0', '1.0', 'v1.0.0', '1.0.0-rc1', '1.0.0\nmalicious'):
            with self.subTest(version=version):
                (self.root / 'ACTION_VERSION').write_text(version, encoding='utf-8')
                with self.assertRaises(ValueError):
                    release_action.main()
        self.mock_cli.assert_not_called()

    def test_existing_version_tag_cannot_be_reassigned(self):
        with patch.object(release_action, 'resolve_tag', return_value=OLDER_COMMIT), \
                patch.object(release_action, 'api') as api:
            with self.assertRaisesRegex(RuntimeError, 'bump ACTION_VERSION'):
                release_action.main()
        api.assert_not_called()
        self.mock_cli.assert_not_called()

    def test_new_release_and_major_tag_use_tested_commit(self):
        url = f'https://github.com/{release_action.REPOSITORY}/releases/tag/v1.0.0'
        with patch.object(release_action, 'resolve_tag', side_effect=[None, COMMIT, None, COMMIT]), \
                patch.object(release_action, 'api', side_effect=[None, {'html_url': url}]):
            self.assertEqual(release_action.main(), 0)
        release_call, major_call = self.mock_cli.call_args_list
        self.assertEqual(release_call.args[:3], ('release', 'create', 'v1.0.0'))
        self.assertIn(COMMIT, release_call.args)
        self.assertIn('ref=refs/tags/v1', major_call.args)
        self.assertIn(f'sha={COMMIT}', major_call.args)
        summary = (self.root / 'summary.md').read_text(encoding='utf-8')
        self.assertIn(url, summary)
        self.assertIn('Marketplace listing is a separate step', summary)

    def test_repeated_published_commit_is_idempotent(self):
        release = {'draft': False, 'prerelease': False, 'html_url': 'https://github.com/example/release'}
        with patch.object(release_action, 'resolve_tag', return_value=COMMIT), \
                patch.object(release_action, 'api', return_value=release):
            self.assertEqual(release_action.main(), 0)
        self.mock_cli.assert_not_called()

    def test_version_bump_updates_only_compatible_major_tag(self):
        (self.root / 'ACTION_VERSION').write_text('1.1.0\n', encoding='utf-8')
        release = {'html_url': 'https://github.com/example/release'}
        with patch.object(release_action, 'resolve_tag', side_effect=[None, COMMIT, OLDER_COMMIT, COMMIT]), \
                patch.object(release_action, 'api', side_effect=[None, release, {'status': 'ahead'}]):
            self.assertEqual(release_action.main(), 0)
        release_call, major_call = self.mock_cli.call_args_list
        self.assertIn('v1.1.0', release_call.args)
        self.assertEqual(major_call.args[:3], ('api', '--method', 'PATCH'))
        self.assertIn(f'repos/{release_action.REPOSITORY}/git/refs/tags/v1', major_call.args)
        self.assertIn(f'sha={COMMIT}', major_call.args)

    def test_old_run_cannot_move_major_tag_backwards_or_diverge(self):
        release = {'draft': False, 'prerelease': False, 'html_url': 'https://github.com/example/release'}
        for status in ('behind', 'diverged', 'unknown'):
            with self.subTest(status=status), \
                    patch.object(release_action, 'resolve_tag', side_effect=[COMMIT, COMMIT, OLDER_COMMIT]), \
                    patch.object(release_action, 'api', side_effect=[release, {'status': status}]):
                with self.assertRaisesRegex(RuntimeError, 'refusing to move it backwards'):
                    release_action.main()
        self.mock_cli.assert_not_called()

    def test_existing_draft_needs_owner_review(self):
        with patch.object(release_action, 'resolve_tag', return_value=COMMIT), \
                patch.object(release_action, 'api', return_value={'draft': True}):
            with self.assertRaisesRegex(RuntimeError, 'owner review'):
                release_action.main()
        self.mock_cli.assert_not_called()

    def test_major_tag_update_failure_is_detected(self):
        release = {'draft': False, 'prerelease': False, 'html_url': 'https://github.com/example/release'}
        with patch.object(release_action, 'resolve_tag', side_effect=[COMMIT, COMMIT, None, OLDER_COMMIT]), \
                patch.object(release_action, 'api', return_value=release):
            with self.assertRaisesRegex(RuntimeError, 'Major version tag verification failed'):
                release_action.main()


class ResolveTagTests(unittest.TestCase):
    def test_missing_tag(self):
        with patch.object(release_action, 'api', return_value=None):
            self.assertIsNone(release_action.resolve_tag('owner/repo', 'v1'))

    def test_annotated_tag_is_peeled_to_commit(self):
        with patch.object(release_action, 'api', side_effect=[
            {'object': {'type': 'tag', 'sha': 'c' * 40}},
            {'object': {'type': 'commit', 'sha': COMMIT}},
        ]):
            self.assertEqual(release_action.resolve_tag('owner/repo', 'v1'), COMMIT)

    def test_non_commit_tag_is_rejected(self):
        with patch.object(release_action, 'api', return_value={'object': {'type': 'tree', 'sha': COMMIT}}):
            with self.assertRaises(RuntimeError):
                release_action.resolve_tag('owner/repo', 'v1')


if __name__ == '__main__':
    unittest.main()
