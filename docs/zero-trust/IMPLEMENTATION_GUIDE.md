# Complete Step-by-Step Guide — RHEL 10.2 Splunk Zero Trust Architecture

**Goal:** Build and assess a **DoD-aligned Zero Trust lab extension** in the existing repository `jbanday808/rhel-10v2-splunk-threat-hunting`, focusing on requirements from Booz Allen **ZT Engineer, Lead (R0242994)**: enterprise design, IAM, workload/endpoint defense, microsegmentation, secure communications, multi-vendor integration planning, RMF/STIG, evidence, maintenance and automation.

**Tools:** Windows 11, VMware Workstation Pro, VS Code + Ubuntu WSL, two RHEL 10.2 VMs (Splunk and IdM), one Windows 11 VM, Splunk Enterprise, Sysmon and Universal Forwarder.

**Status:** This is a source-controlled deployment/runbook plan. **No new Zero Trust services are deployed by adding the files to GitHub.** Existing lab service state must be verified individually. The complete NIST / DoD dynamic Zero Trust capabilities are **future work**.

## Phase 1 — Plan, inventory and preserve the lab

### Step 01 — Read and freeze the existing deployment baseline (WSL)

```bash
cd ~/projects/rhel-10v2-splunk-threat-hunting
git status
git remote -v
git fetch origin
git switch --track origin/feature/dod-zero-trust-rhel10v2
code .
```

If the feature branch already exists locally, use `git switch feature/dod-zero-trust-rhel10v2` and then `git pull --ff-only`. Review local changes before switching.

**Command overview:** `git status` checks uncommitted work; `remote -v` identifies GitHub; `fetch` downloads branch metadata; `switch` selects the new review branch; `code .` opens the folder in VS Code WSL.

**Check:** `README.md`, `START_HERE_RHEL10v2.md` and `docs/steps/README.md` are still present, with original 52 steps intact.

### Step 02 — Establish public sources and project scope (WSL)

Read [reference list](12-official-references.md), [DoD pillar mapping](02-dod-seven-pillars.md), [architecture](01-target-architecture.md), and [roles and migration plan](11-migration-and-operations.md). State who approves network changes, whose data is present, what is protected, and what must never be published.

**Exit:** Seven-pillar inventory and initial risk register contain **Proposed/Pending**, not invented pass grades.

### Step 03 — Snapshot each VM and prepare recovery (VMware host and VM consoles)

From VMware Workstation Pro, take identifiable snapshots with each VM in a documented consistent state (use a safe powered-down snapshot for directory/other stateful workloads if required). Record snapshot names **privately**, available console access, last good IP/DNS, and backup restore tests.

On each **RHEL VM console**, collect baseline **without publishing unredacted files**:

```bash
cat /etc/redhat-release
hostnamectl
ip -brief address
nmcli -f NAME,DEVICE,TYPE connection show --active
sestatus
sudo firewall-cmd --get-active-zones
sudo firewall-cmd --list-all
```

**Command overview:** Reports OS, hostname, addresses, connection profiles, SELinux and active firewall rules. Do not change firewalls or NetworkManager while remote without an active console/backout option.

**Exit:** Snapshot and recovery method verified locally; service configurations exported to private encrypted backup.

### Step 04 — Inventory assets and allowed traffic (WSL + VM consoles)

Review [policy matrix](../../configs/zero-trust/allowed-flows.example.json) and [preflight](03-preflight-and-inventory.md). Record the existing VMware NAT network `172.25.250.0/24` and lab hosts:

| Source | Destination | Service | Port | Why |
| --- | --- | --- | --- | --- |
| Windows host management (.1) | RHEL-SPLUNK01 (.10) | HTTPS Splunk Web | TCP 8000 | Analyst/admin browser |
| WINHUNT01 (.20) | RHEL-SPLUNK01 (.10) | Universal Forwarder | TCP 9997 | Windows event ingest |
| RHEL-SPLUNK01 (.10) | RHEL-IDM01 (.30) | LDAPS | TCP 636 | Identity lookup |
| RHEL-SPLUNK01 (.10) | RHEL-IDM01 (.30) | DNS | UDP/TCP 53 | DNS lookup |
| Lab management host(s) | RHEL VMs | SSH | TCP 22 | Authorized console/maintenance |

Other protocols for IdM enrollment, updates and time synchronization must be explicitly discovered and approved before tightening rules. Never block critical DNS, IdM, Kerberos, NTP or repository paths without proving the corresponding dependency is unused.

**Exit:** Verified desired flows, source addresses, service owners and change approvals.

## Phase 2 — Identity and endpoint posture

### Step 05 — Verify IdM accounts and directory groups (RHEL-IDM01)

If IdM is already installed according to the lab [Steps 31–34](../steps/README.md), use the IdM VM console:

```bash
hostnamectl
sudo systemctl status ipa --no-pager
kinit admin
ipa group-show splunk-hunters
ipa group-show splunk-admins
ipa user-show hunter01
kdestroy
```

**Command overview:** `systemctl status ipa` checks IdM status (service names may vary by installed IdM version); `kinit` prompts for a Kerberos credential; `ipa group-show` and `ipa user-show` inspect identities; `kdestroy` clears the ticket cache. Run these only with a test identity you are authorized to use. If a specific systemd `ipa` service does not exist, use `ipactl status` and inspect installed unit names rather than assuming a failure.

**Exit:** Groups exist; only intended members are included; no broad `ipausers` mapping to Splunk admin.

### Step 06 — Verify encrypted LDAP and least-privilege roles (RHEL-SPLUNK01)

Use the existing [certificate trust procedure](../steps/35-configure-splunk-dns-and-trust-the-directory-certificate.md) and [LDAPS verification procedure](../steps/36-verify-ldaps-before-enabling-directory-sign-in.md). After installing only the **verified public CA**:

```bash
getent hosts idm01.lab.test
sudo -u splunk openssl s_client \
  -connect idm01.lab.test:636 \
  -servername idm01.lab.test \
  -CAfile /opt/splunk/etc/auth/ldap/idm-ca.pem \
  -verify_hostname idm01.lab.test \
  -verify_return_error </dev/null
sudo -u splunk /opt/splunk/bin/splunk btool authorize list role_lab_hunter --debug
```

**Command overview:** `getent` checks DNS; `s_client` verifies certificate chain/hostname; `btool` shows effective Splunk role settings. Never use `TLS_REQCERT never` or `curl -k` to bypass TLS errors.

**Exit:** Successful certificate validation and observed `lab_hunter` limited to six lab indexes; Splunk native administrator retained as emergency recovery.

### Step 07 — Document MFA/conditional access gaps (design review)

**Do not claim MFA is enforced.** Splunk's native LDAP group binding is not equivalent to phishing-resistant MFA and device-risk-aware authorization. Record a **future** design using an approved identity provider with SAML/OIDC or supported Splunk authentication integration, MFA, device compliance and session risk evaluation; check exact installed Splunk version and IdP support first. Document emergency-admin recovery and denial behavior for untrusted devices.

**Exit:** `MFA/continuous-device-posture = Not implemented`, unless separately proven.

### Step 08 — Verify RHEL/Windows endpoint security (both VMs)

**RHEL-SPLUNK01 / RHEL-IDM01, consoles:**

```bash
getenforce
sudo systemctl is-active firewalld
sudo systemctl is-active auditd
sudo dnf check-update --security || true
```

**WINHUNT01, PowerShell launched as appropriate to read status:**

```powershell
Get-MpComputerStatus | Select-Object AntivirusEnabled,RealTimeProtectionEnabled
Get-NetFirewallProfile | Select-Object Name,Enabled,DefaultInboundAction
Get-Service SplunkForwarder -ErrorAction SilentlyContinue
Get-WinEvent -LogName 'Microsoft-Windows-Sysmon/Operational' -MaxEvents 3 -ErrorAction SilentlyContinue
```

**Command overview:** `getenforce` checks SELinux; `firewalld`/`auditd` checks services; `dnf check-update --security` lists available fixes (it does not install); PowerShell checks anti-malware, firewalls, forwarder, and collected Sysmon events.

**Exit:** Actual observed posture recorded, gaps open. Do not install unapproved agents or globally disable protections to simplify the lab.

## Phase 3 — Segmentation and workload protection

### Step 09 — Read the effective firewall policy before modifying it

At **RHEL-SPLUNK01 VM console**:

```bash
sudo firewall-cmd --get-active-zones
sudo firewall-cmd --zone=siem-lab --list-all
sudo firewall-cmd --zone=siem-lab --list-rich-rules
sudo ss -lntp
```

**Command overview:** Shows the active zone, rich rules and listeners. If `siem-lab` is not attached to the VM's connection, stop and reconcile with [original Step 18](../steps/18-configure-the-rhel-firewall.md).

**Exit:** Network policy change checklist and management console access are confirmed.

### Step 10 — Narrow network flows, one service at a time

Follow [06-network-microsegmentation.md](06-network-microsegmentation.md) exactly. Use **runtime-only** source-limited rich rules first; perform positive and negative tests; review broad open services/ports; only then make reviewed changes permanent. Preserve the current SSH management path and allow RHEL-SPLUNK01 outbound DNS/LDAPS; do not assume host firewalls replace microsegmentation across VLANs.

**Exit:** WINHUNT01 can reach 9997, approved browser can reach 8000, approved LDAPS works, non-authorized paths are denied. Record packet-level evidence and firewall logs where safe.

### Step 11 — Enforce protected application and data access

In **Splunk Web** confirm `splunk-hunters → lab_hunter`, `splunk-admins → admin`, no broad implicit mapping. On the server, inspect **effective** `authorize.conf`, TLS settings, index permissions and log retention. Keep the admin role for only explicitly approved administrators. See [07-app-data-security.md](07-app-data-security.md).

**Exit:** Positive hunter access, negative unmapped user test, unauthorized index denied; observations recorded.

### Step 12 — Validate secure endpoint telemetry

From WINHUNT01, confirm Universal Forwarder service and verified TLS configuration; from Splunk Web, confirm actual events. Do not count `inputs.conf` or `outputs.conf` source files as evidence of collection.

In Splunk Search (authorized lab, **not WSL**):

```spl
(index=win_security OR index=win_system OR index=powershell OR index=sysmon OR index=linux OR index=lab) earliest=-24h
| stats count by index host sourcetype
```

**Exit:** Actual event totals, indexing latency and missing sources documented.

## Phase 4 — Continuous monitoring and security governance

### Step 13 — Deploy **read-only SPL hunts** and record incident workflow

Read [08-siem-and-automation.md](08-siem-and-automation.md) and [example hunts](../../hunts/zero-trust/README.md). Test failed sign-ins, audit gaps, least privilege violations and Windows telemetry with **authorized synthetic** activity. Keep automatic containment and IdM changes **disabled**.

**Exit:** Evidence-based search results and analyst-review workflow tested; no unobserved success claims.

### Step 14 — Apply RMF and STIG assessment planning

Follow [09-rmf-stig-ato.md](09-rmf-stig-ato.md): PREPARE → CATEGORIZE → SELECT → IMPLEMENT → ASSESS → AUTHORIZE → MONITOR. Select the actual applicable STIG/SRG version and benchmark from DISA; verify any OpenSCAP content exists for installed RHEL 10.2. Do **not** apply auto-remediation blindly to Splunk/IdM. These documents are **not** a federal ATO or DoD Target Level certificate.

**Exit:** Draft SSP, control allocation, scan records, POA&M and formal decision status clearly labeled.

### Step 15 — Create a system-migration plan

Map perimeter-based rules to resource-based access: identify one protected resource at a time, deploy parallel policy, observe, test and only then remove broad access. See [11-migration-and-operations.md](11-migration-and-operations.md). Document vendors as **reference options**, not installed platforms.

### Step 16 — Document automation with change review

In WSL, validate a **non-deploying example flow matrix**:

```bash
python3 scripts/zero-trust/validate_policy.py configs/zero-trust/allowed-flows.example.json
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/validate_project.py
python3 tools/publication_preflight.py
```

**Command overview:** Validates example policy syntax and lab paths, runs offline tests, checks original project files and scans for common public-repository risks. These checks do **not** configure firewalls or demonstrate live Zero Trust compliance.

### Step 17 — Conduct verification with both allow and deny tests

Use [10-verification-and-evidence.md](10-verification-and-evidence.md) to capture evidence for identity/role authorization, transport encryption, connectivity, endpoint health, audit visibility and recovery. For each test, record observed outcome, timestamp, tester, test host, expected behavior, actual behavior and sanitized screenshot.

**Exit:** Results are **Pass / Fail / Pending / Not Applicable** based on actual observations.

### Step 18 — Test backup/recovery and failure handling

Practice authorized rollback of one **runtime-only** network rule from the VM console and demonstrate recovery of Splunk access. Do not run destructive tests against production data. Backups contain private configuration; store them only in encrypted private locations.

### Step 19 — Review portfolio evidence and scope claims

Before publication, strip credentials, SSH fingerprints, internal IDs beyond approved lab examples, raw security logs and private key material. All capability claims must distinguish **Configured**, **Tested**, **Planned** and **Not implemented**. See [10-verification-and-evidence.md](10-verification-and-evidence.md).

### Step 20 — Review and merge your GitHub changes

In WSL:

```bash
git status
git diff --check
git log -3 --oneline
```

Review the GitHub pull request and its source-check workflow. After approval/merge into `main`:

```bash
git switch main
git pull --ff-only origin main
```

**Command overview:** `git diff` checks whitespace; `git log` displays recent commits; `git pull --ff-only` obtains the merged repository changes.

## Final architecture milestones

| Capability | Existing source/plan | Evidence that must still be collected |
| --- | --- | --- |
| IAM | IdM groups, Splunk RBAC and LDAPS documentation | Users/groups verified, allow/deny role tests |
| Devices | Sysmon, auditd, SELinux, Defender references | Collected posture + actual telemetry |
| Applications/workloads | Splunk app and six index configs | Role/capability and integrity checks |
| Data | TLS and secret-handling policies | Certificate, retention, access-denial results |
| Network | VMnet8 plus rich-rule source allowlists | Positive/negative port reachability |
| Automation | Source-controlled example policy | Review/audit trail; no unapproved changes |
| Visibility/analytics | Existing 13 hunts + new ZT searches | Actual search returns and test outcomes |
| Dynamic ZTNA/PDP + device-conditional MFA | **Future architecture only** | Architecture approval, product integration, test results |
| DoD Target / ATO / STIG compliance | **No claim** | Full organizational capability and RMF assessment |

## References and boundary notice

Read [official source links](12-official-references.md). This project uses public sources only; no classified material, real DoD networks or contractor proprietary architectures should be added. Static allowlists, directory group mapping and log collection provide useful foundations but are **not equal to fully implemented DoD Target-Level Zero Trust**.
