# Ansible vulnerability patching

This optional automation previews and applies **RHEL 10 operating-system security
updates** and **Windows security/critical updates** in the owned lab. It extends the
[vulnerability-management workflow](../../docs/security-operations/VULNERABILITY_MANAGEMENT.md).
The default is assessment: no packages are installed and no host is rebooted.
Assessment connects to the selected hosts, reads facts/service state, and may
refresh update metadata. It is not a vulnerability scanner.

**Live status: not run.** Syntax and controller-side policy tests are separate
from a successful host patch, functional test, or verified vulnerability fix.
There are no tasks that configure STIG controls, firewalls, Splunk/IdM settings,
authentication, TLS policies or the six lab indexes. OS updates can still affect
those services and their compatibility.

## Scope and defaults

| Area | Behavior |
| --- | --- |
| RHEL-SPLUNK01 / RHEL-IDM01 | RHEL 10 with DNF4 and `python3-dnf`; security-tagged updates to installed packages, honoring the existing repository/release policy |
| WINHUNT01 | Updates from the machine's configured Windows Update/WSUS source; security and critical categories, with optional updates skipped |
| Installation | Needs `patch_mode: apply`, approval, a change ID, recovery confirmation, service names, and `--limit` selecting exactly one host |
| Execution | Serial execution; a failed prerequisite, update, or service check stops the run |
| Reboots | Off by default; `patch_allow_reboot: true` explicitly permits required reboots during an approved apply run |
| Evidence | Private controller-side JSON, outside the repository, directory mode `0700` and file mode `0600` |
| Application upgrades | Splunk/Universal Forwarder packages are excluded from RHEL transactions; product-specific upgrades require verified versions and vendor procedures |

The RHEL task uses `security: true`, `update_only: true`, signature checking and
TLS verification. This does not prove that every CVE is fixed: enabled
repositories need valid advisory metadata, and excludes, release locks,
entitlement, dependencies and installed components affect available fixes.
Normal DNF dependency changes can still occur. Review the proposed transaction.

## 1. Prepare the controller and targets

Run from a **Linux or WSL controller**, using Python 3.12 or newer supported by
the pinned Ansible release. From the repository root:

```bash
python3 -m venv ~/.venvs/tracevector-patching
source ~/.venvs/tracevector-patching/bin/activate
python -m pip install -r automation/ansible/requirements.txt
ansible-galaxy collection install -r automation/ansible/requirements.yml
cd automation/ansible
cp inventory/hosts.yml.example inventory/hosts.local.yml
```

**Command Overview:** Create and activate an isolated controller environment,
install the pinned Python packages and Windows collection, then copy the example
inventory to the ignored local inventory.

**Summary:** `ansible-playbook --version` should identify the installed controller;
`ansible-galaxy collection list ansible.windows` should list the pinned collection.

Edit `inventory/hosts.local.yml` privately. Replace every `REPLACE_` value and
verify the intended host, authorized account and actual service names. The
documented network remains `172.25.250.0/24`: Splunk `.10`, Windows `.20`, and IdM
`.30`. Do not assume that a current VM still has its documented address.

- RHEL needs an existing verified SSH host key, authorized SSH/sudo access,
  `python3-dnf`, working entitled repositories and `dnf needs-restarting -r`.
  The playbook checks these prerequisites rather than installing its own DNF
  bindings or restart-check plugin. Restart-check errors or warnings on stderr
  stop execution for review. Verify the approved RHEL minor-release/EUS
  policy before an update; no release override or repository is created.
- Review `Splunkd.service` and `ipa.service` against the actual unit names and
  running state. Do not remove a required service simply to make a check pass.
- Windows needs existing WinRM HTTPS on port 5986, a matching certificate and
  trusted CA file on the controller, and an authorized local administrator.
  `win_updates` runs as SYSTEM using Windows `runas`. Confirm actual
  `SplunkForwarder` and Sysmon service names. This project does not enable WinRM,
  open a firewall, create an administrator or weaken certificate verification.
- Use SSH keys, `--ask-pass`, `--ask-become-pass`, or approved Ansible Vault
  storage. Keep passwords, CA files, host inventories and completed change
  records outside this public repository.

## 2. Inspect the exact host and preview

For the RHEL Splunk host:

```bash
ansible-playbook playbooks/patch_rhel.yml --limit rhel_splunk01 --list-hosts
ansible-playbook playbooks/patch_rhel.yml --limit rhel_splunk01 --ask-become-pass
```

**Command Overview:** `--list-hosts` lists the target without connecting;
the second command runs the default assessment, using sudo credentials if needed.

**Summary:** Expect a proposed DNF security transaction, service-state checks,
reboot status and a private JSON record. No updates are installed in assessment.

For Windows:

```bash
ansible-playbook playbooks/patch_windows.yml --limit winhunt01 --list-hosts
ansible-playbook playbooks/patch_windows.yml --limit winhunt01 --ask-pass
```

**Command Overview:** Confirm the Windows target, then search its configured
update source without installing updates or rebooting.

**Summary:** Review the returned update titles/KBs, failures and reboot status.
Windows searches and installations can take a long time.

Both playbooks support `--check`. An apply request with `--check` remains a
preview. Controller report files are not written in global check mode, so a
normal default assessment is the preferred way to retain a private record.
An empty update result is not evidence that advisory metadata, inventory,
vulnerability applicability or update coverage is complete.

## 3. Review and authorize one change

Copy `vars/change.yml.example` to an approved **private location outside Git**.
Set `patch_approved: true`, the actual `patch_change_id`, and
`patch_recovery_ready: true` only after the system owner authorizes the change.
Use real YAML booleans, not quoted strings. Retain the approved target, finding,
maintenance window, compatibility review, backup and recovery procedure there.

Optionally narrow `patch_rhel_packages` to reviewed package names, or
`patch_windows_accept_list` to reviewed KBs/titles. Windows accept/reject lists
use the module's regular-expression matching and still honor the selected
categories. Definition updates are permitted only if explicitly added to
`patch_windows_categories`; upgrade/feature categories are rejected.

Do not use this OS workflow to close the [Splunk IAVM notice](../../docs/iavm/README.md).
Enterprise and Universal Forwarder upgrades need their actual installed version,
applicability, trusted installer/hash, backup and release-specific upgrade plan.

## 4. Apply the reviewed change

Example for one RHEL host, after replacing the private path:

```bash
ansible-playbook playbooks/patch_rhel.yml --limit rhel_splunk01 --extra-vars @/absolute/private/change.yml --ask-become-pass
```

**Command Overview:** Load the private approved change and apply its scoped
security transaction to the single named RHEL host.

**Summary:** A successful package task is an implementation result, not a closed
vulnerability. An outstanding reboot keeps an apply run incomplete.

For Windows, use `playbooks/patch_windows.yml`, `--limit winhunt01`, and
`--ask-pass` with the same private change-file pattern. A multi-host limit is
rejected for installation. Repeat assessment and owner review for the next host.

If `patch_allow_reboot` stays false, no reboot is requested by these playbooks.
Package installation scripts can still restart services; schedule an appropriate
maintenance window. If rebooting is explicitly permitted, RHEL may reboot once;
the Windows update module can reboot multiple times to finish its update cycles.

## 5. Verify, retain evidence and recover if necessary

Default private report location on the controller:
`~/.local/state/tracevector/patching/<host-alias>-<run-id>.json`.
Reports contain update and target information; do not commit or share them
without review. A custom `patch_report_dir` must be absolute and resolve outside
this repository, including when it contains a symlink. A report is written only
when execution reaches the reporting stage; retain early failure output in
approved private case storage as well.

1. Rerun assessment after the update/reboot. Record actual versions, remaining
   updates, outstanding restart requirements and errors. Review affected
   services that need a restart even when the reboot hint is clear.
2. Independently retest the original vulnerability using the applicable vendor
   advisory and approved assessment method. RPM backports and Windows update
   supersedence require product-specific interpretation.
3. Verify fresh events in Splunk and the forwarding path. For IdM, check DNS,
   Kerberos, directory/authentication behavior and certificate-verified LDAPS.
   A running service alone does not verify those functions.
4. Add sanitized evidence references and the owner's disposition to the
   [vulnerability record](../../docs/security-operations/templates/vulnerability-record.md).
   Keep unresolved findings open; do not turn a patch-job result into a STIG pass.
5. On failure, stop and inspect actual state. The automation does not perform an
   automatic downgrade, `dnf history undo`, service restart or backup restore.
   Use the reviewed recovery plan and VM console; repeat verification after
   recovery. Retain the failed transaction and do not proceed to another host.

The policy guards prevent common accidental runs; they are not an authorization
system against an operator who edits playbooks or bypasses tasks. Do not skip the
guards with tags or `--start-at-task`.

## Source validation and live acceptance

```bash
ansible-playbook -i inventory/hosts.local.yml --syntax-check playbooks/patch_rhel.yml
ansible-playbook -i inventory/hosts.local.yml --syntax-check playbooks/patch_windows.yml
```

**Command Overview:** Parse both playbooks and resolve their modules without
connecting to the inventory hosts.

**Summary:** Each command should exit successfully. Syntax checks do not test
remote DNF/WinRM behavior, entitlement, installation, reboots or health checks.

The repository CI installs the pinned dependencies, checks syntax using a
placeholder inventory, and executes `tests/test_ansible_patching.py` offline.
The guard tests use controller-only actions and synthetic inventory aliases;
they do not connect to lab hosts. Complete the pending
[live acceptance record](../../evidence/sanitized/ansible-patching-validation.md)
after an authorized lab run and independent review.

Source checks completed November 11, 2026 (Hawaii): Python 3.12.14,
ansible-core 2.20.11, and ansible.windows 3.9.2; both playbook syntax checks,
project source validation and publication preflight passed. The repository suite
ran 100 tests: 99 passed and one offline Suricata replay was skipped because the
engine was unavailable. All 15 patch-policy tests passed. No live inventory was
used, and no target was patched or rebooted by these checks.

## References

- [Ansible DNF module](https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/dnf_module.html): This reference explains security filtering, installed-package updates and check mode.
- [Ansible Windows Update module](https://docs.ansible.com/projects/ansible/latest/collections/ansible/windows/win_updates_module.html): This reference explains update categories, search mode, configured update sources and reboot behavior.
- [DNF needs-restarting](https://dnf-plugins-core.readthedocs.io/en/latest/needs_restarting.html): This reference explains restart inspection and reboot-hint exit codes.
- [Repository publication guidance](../../docs/reference/security-and-sanitization.md): This checklist explains how to review evidence before publication.
