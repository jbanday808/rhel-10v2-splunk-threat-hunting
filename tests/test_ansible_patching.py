"""Offline patch-policy regressions. These tests never contact lab systems."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'automation' / 'ansible'
ADJACENT_ANSIBLE = Path(sys.executable).with_name('ansible-playbook')
ANSIBLE = str(ADJACENT_ANSIBLE) if ADJACENT_ANSIBLE.exists() else shutil.which('ansible-playbook')


@unittest.skipUnless(yaml, 'Install automation/ansible/requirements.txt for YAML checks')
class PatchSourceTests(unittest.TestCase):
    def read(self, name):
        return yaml.safe_load((PROJECT / name).read_text())

    def test_inventory_service_scope_is_not_overridden_by_defaults(self):
        defaults = self.read('vars/patch_defaults.yml')
        self.assertNotIn('patch_required_services', defaults)
        inventory = self.read('inventory/hosts.yml.example')['all']['children']
        for group in inventory.values():
            for host in group['hosts'].values():
                self.assertTrue(host['patch_required_services'])
                self.assertTrue(host['ansible_host'].startswith('REPLACE_'))

    def test_both_platforms_enforce_policy_before_gathering_facts(self):
        for name in ('patch_rhel.yml', 'patch_windows.yml'):
            play = self.read('playbooks/' + name)[0]
            self.assertFalse(play['gather_facts'])
            self.assertEqual(play['serial'], 1)
            self.assertTrue(play['any_errors_fatal'])
            self.assertEqual(play['pre_tasks'][0]['ansible.builtin.import_tasks'], '../tasks/guard.yml')

    def test_rhel_security_scope_cannot_disable_signature_or_tls_checks(self):
        tasks = self.read('playbooks/patch_rhel.yml')[0]['tasks']
        task = next(t for t in tasks if 'ansible.builtin.dnf' in t)
        options = task['ansible.builtin.dnf']
        self.assertTrue(options['security'])
        self.assertTrue(options['update_only'])
        self.assertTrue(options['sslverify'])
        self.assertFalse(options['disable_gpg_check'])
        self.assertFalse(options['allowerasing'])
        self.assertFalse(options['allow_downgrade'])
        self.assertIn('splunk*', options['exclude'])
        self.assertIn('not patch_installing', task['check_mode'])

    def test_windows_search_and_reboots_are_conditioned_on_installation(self):
        tasks = self.read('playbooks/patch_windows.yml')[0]['tasks']
        options = next(t['ansible.windows.win_updates'] for t in tasks if 'ansible.windows.win_updates' in t)
        self.assertIn('patch_installing', options['state'])
        self.assertIn('searched', options['state'])
        self.assertIn('patch_installing and patch_allow_reboot', options['reboot'])
        self.assertEqual(options['server_selection'], 'default')
        self.assertTrue(options['skip_optional'])

    def test_evidence_is_private_and_check_mode_does_not_write_it(self):
        tasks = self.read('tasks/report.yml')
        directory = next(t for t in tasks if 'ansible.builtin.file' in t)
        report = next(t for t in tasks if 'ansible.builtin.copy' in t)
        self.assertEqual(directory['ansible.builtin.file']['mode'], '0700')
        self.assertEqual(report['ansible.builtin.copy']['mode'], '0600')
        self.assertTrue(report['no_log'])
        self.assertEqual(report['when'], 'not ansible_check_mode')
        self.assertFalse(self.read('vars/patch_defaults.yml')['patch_allow_reboot'])


@unittest.skipUnless(ANSIBLE and yaml, 'Install automation/ansible/requirements.txt for executable guard tests')
class PatchGuardExecutionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='patch-policy-')
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.inventory = self.directory / 'inventory.yml'
        self.inventory.write_text(json.dumps({'all': {'children': {
            'rhel_patch_targets': {'hosts': {
                'node_a': {'ansible_host': '127.0.0.1'},
                'node_b': {'ansible_host': '127.0.0.1'},
            }},
            'windows_patch_targets': {'hosts': {'windows_stub': {'ansible_host': '127.0.0.1'}}},
        }}}))
        # Only controller-side guard/assert/debug actions execute in this harness.
        self.harness = self.directory / 'guard.yml'
        runtime_vars = yaml.safe_load((PROJECT / 'playbooks/patch_rhel.yml').read_text())[0]['vars'].copy()
        runtime_vars['patch_repository_root'] = str(ROOT)
        self.harness.write_text(json.dumps([{
            'name': 'Exercise the real shared guard without target connections',
            'hosts': 'rhel_patch_targets', 'gather_facts': False,
            'connection': 'local', 'any_errors_fatal': True,
            'vars_files': [str(PROJECT / 'vars/patch_defaults.yml')],
            'vars': runtime_vars,
            'tasks': [
                {'ansible.builtin.import_tasks': str(PROJECT / 'tasks/guard.yml')},
                {'ansible.builtin.debug': {'msg': 'PATCH_GUARD_PASSED'}},
            ],
        }]))

    def run_policy(self, values=None, limit=None, check=False, playbook=None):
        policy = {'patch_report_dir': str(self.directory / 'private-reports')}
        policy.update(values or {})
        data = self.directory / 'vars.json'
        data.write_text(json.dumps(policy))
        args = [ANSIBLE, '-i', str(self.inventory), str(playbook or self.harness), '-e', '@' + str(data)]
        if limit is not None:
            args.extend(['--limit', limit])
        if check:
            args.append('--check')
        env = dict(os.environ, ANSIBLE_CONFIG=str(PROJECT / 'ansible.cfg'), ANSIBLE_NOCOLOR='1')
        result = subprocess.run(args, cwd=self.directory, env=env, capture_output=True, text=True, timeout=45)
        output = result.stdout + result.stderr
        self.assertIn(result.returncode, (0, 2), output)
        return result.returncode, output

    def approved(self):
        return {'patch_mode': 'apply', 'patch_approved': True,
                'patch_change_id': 'SYNTHETIC-TEST-CHANGE', 'patch_recovery_ready': True,
                'patch_required_services': ['synthetic.service']}

    def test_assessment_passes_without_installation_approval(self):
        code, output = self.run_policy()
        self.assertEqual(code, 0, output)
        self.assertIn('PATCH_GUARD_PASSED', output)

    def test_installation_without_approval_is_rejected(self):
        code, output = self.run_policy({'patch_mode': 'apply'}, limit='node_a')
        self.assertNotEqual(code, 0, output)
        self.assertNotIn('PATCH_GUARD_PASSED', output)

    def test_approved_single_host_passes(self):
        code, output = self.run_policy(self.approved(), limit='node_a')
        self.assertEqual(code, 0, output)

    def test_apply_without_limit_is_rejected(self):
        code, output = self.run_policy(self.approved())
        self.assertNotEqual(code, 0, output)

    def test_apply_to_multiple_hosts_is_rejected(self):
        code, output = self.run_policy(self.approved(), limit='rhel_patch_targets')
        self.assertNotEqual(code, 0, output)

    def test_missing_change_id_and_recovery_are_each_rejected(self):
        for override in ({'patch_change_id': ''}, {'patch_recovery_ready': False}, {'patch_required_services': []}):
            with self.subTest(override=override):
                values = self.approved() | override
                code, output = self.run_policy(values, limit='node_a')
                self.assertNotEqual(code, 0, output)

    def test_global_check_mode_stays_a_preview(self):
        code, output = self.run_policy({'patch_mode': 'apply'}, check=True)
        self.assertEqual(code, 0, output)

    def test_invalid_mode_and_boolean_strings_are_rejected(self):
        for values in ({'patch_mode': 'install-everything'}, {'patch_approved': 'false'}):
            with self.subTest(values=values):
                code, output = self.run_policy(values)
                self.assertNotEqual(code, 0, output)

    def test_report_inside_repo_or_through_symlink_is_rejected(self):
        link = self.directory / 'repository-link'
        link.symlink_to(ROOT, target_is_directory=True)
        for dest in (ROOT / 'reports', link / 'reports'):
            with self.subTest(dest=dest):
                code, output = self.run_policy({'patch_report_dir': str(dest)})
                self.assertNotEqual(code, 0, output)

    def test_windows_certificate_bypass_is_rejected_before_remote_facts(self):
        code, output = self.run_policy({
            'ansible_connection': 'winrm', 'ansible_winrm_scheme': 'https',
            'ansible_port': 5986, 'ansible_winrm_server_cert_validation': 'ignore',
        }, limit='windows_stub', playbook=PROJECT / 'playbooks/patch_windows.yml')
        self.assertNotEqual(code, 0, output)
        self.assertIn('Use certificate-verified WinRM HTTPS', output)


if __name__ == '__main__':
    unittest.main()
