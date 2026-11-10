# START HERE — RHEL 10.2 Splunk Threat Hunting Lab

**Project:** RHEL 10.2 Splunk Enterprise threat hunting, Windows 11 event collection, and Red Hat Identity Management (IdM) with verified LDAPS.

**Repository:** https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting

> **RHEL 10.2 is the operating-system version.** The repository name uses `10v2`. This file is the starting point for deploying and validating the lab—not a claim that every service or test is already running.

For the **VS Code + WSL on Windows 11** workflow, see [START_HERE_WSL.md](START_HERE_WSL.md). For Windows PowerShell, see [START_HERE_WINDOWS.md](START_HERE_WINDOWS.md).

**Optional RHEL STIG workstream:** [START_HERE_RHEL10v2_STIG.md](START_HERE_RHEL10v2_STIG.md) and the [complete V1R1 OpenSCAP hardening guide](../docs/stig-rhel10/IMPLEMENTATION_GUIDE.md). Assessment-only until you run scans on each VM; do not auto-remediate IdM or Splunk.

**Optional passive network defense workstream:** [Start here](START_HERE_NETWORK_DEFENSE.md) for the tool setup, offline network investigations and CMMC evidence guide.


## 1. Know where to run each task

| Machine | Role | Tasks |
| --- | --- | --- |
| Windows 11 physical host | VMware Workstation Pro | Configure VMnet8 NAT and manage the VMs |
| VS Code connected to Ubuntu WSL | Source-code workspace | Review, test, commit, and push GitHub files |
| `RHEL-SPLUNK01` | RHEL 10.2 Splunk server | Storage, Splunk Enterprise, TLS, Linux logs, searches, dashboards |
| `WINHUNT01` | Windows 11 hunting VM | Windows auditing, Sysmon, Universal Forwarder, harmless test events |
| `RHEL-IDM01` | RHEL 10.2 directory VM | IdM DNS, directory users/groups, LDAP certificate authority |
| Kali Linux (optional) | Analysis VM on VMnet8 | Offline packet and detection-rule exercises; no automatic Splunk feed |
| Splunk Web | Web interface on Splunk VM | Search, add-ons, roles, LDAPS strategy, alerts |

**Important:** WSL is the repository workspace. Do **not** install or initialize the RHEL Splunk server inside WSL, and do not run Windows endpoint-changing scripts on your physical PC.

## 2. Confirm the lab network and system names

| Component | Lab address |
| --- | --- |
| VMware VMnet8 NAT subnet | `172.25.250.0/24` |
| Windows host's VMnet8 adapter | `172.25.250.1` |
| NAT gateway / initial DNS | `172.25.250.2` |
| `splunk01.lab.test` (RHEL-SPLUNK01) | `172.25.250.10` |
| `winhunt01.lab.test` (WINHUNT01) | `172.25.250.20` |
| `idm01.lab.test` (RHEL-IDM01) | `172.25.250.30` |

Use the dedicated VMnet8 network and confirm the addresses are unused before assigning them. After IdM is configured, the Splunk and IdM servers use `172.25.250.30` for DNS. Keep the NAT gateway at `172.25.250.2`.

**Detailed instructions:** [Step 1 — IP plan](../docs/steps/01-confirm-the-ip-address-plan.md), [Step 3 — VM resources](../docs/steps/03-plan-the-vm-resources.md).

## 3. Open your project source in VS Code + WSL

**Run on:** Ubuntu WSL terminal on the Windows 11 physical host.

If the repository has not been cloned:

```bash
mkdir -p "$HOME/projects"
cd "$HOME/projects"
git clone https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting.git
cd rhel-10v2-splunk-threat-hunting
code .
```

If you already have a clean local clone, open it and update it:

```bash
cd "$HOME/projects/rhel-10v2-splunk-threat-hunting"
git status
git pull --ff-only origin main
code .
```

**Command overview:** `git clone` downloads the existing repository; `git status` shows local changes; `git pull --ff-only` updates a clean checkout without creating a merge commit; `code .` opens the current project in VS Code. If `git status` shows changes, review them before pulling.

## 4. Build or verify RHEL-SPLUNK01

**Run on:** RHEL-SPLUNK01 console, not WSL.

Follow the deployment instructions **in order**:

1. [Steps 4–7 — Download, install, network, and prepare RHEL 10.2](../docs/steps/README.md). Use publisher-verified installers, keep SELinux Enforcing, and verify time synchronization.
2. [Steps 8–12 — Project source, Splunk app settings, Windows forwarder settings, and Sysmon rules](../docs/steps/README.md). The source files are **already in this repository**; review them instead of rebuilding or overwriting the latest versions.
3. [Step 13 — Splunk account and separate XFS storage](../docs/steps/13-create-the-service-account-and-prepare-storage.md). Never format a disk that already contains data or is mounted.
4. [Steps 14–15 — Install Splunk Enterprise and create private lab certificates](../docs/steps/README.md). Certificates and private keys must be generated and protected on lab machines.
5. [Steps 16–20 — Configure Linux logging, deploy the app, set up systemd/firewall, and install supported add-ons](../docs/steps/README.md).

### Verify the operating system

```bash
cat /etc/redhat-release
hostnamectl
ip -brief address
getenforce
chronyc tracking
```

**Command overview:** These report the RHEL version, hostname, IP address, SELinux mode, and clock synchronization. Confirm RHEL 10.2, `splunk01.lab.test`, `172.25.250.10`, and `Enforcing` before proceeding.

### Verify existing storage and Splunk service

Run **only after** Splunk installation and storage setup:

```bash
findmnt --mountpoint /splunkdata
df -h /splunkdata
sudo systemctl status Splunkd.service --no-pager -l
sudo -u splunk /opt/splunk/bin/splunk btool check
```

**Command overview:** `findmnt` checks the data mount, `df` shows space, `systemctl status` checks the service, and `btool check` verifies Splunk configuration syntax. These commands do **not** repair or reformat storage.

For the full RHEL source and helper scripts, see [scripts/rhel/README.md](../scripts/rhel/README.md), [verify-server.sh](../scripts/rhel/verify-server.sh), and [configure-linux-logging.sh](../scripts/rhel/configure-linux-logging.sh). Review scripts before running them; some make system changes.

## 5. Set up WINHUNT01 and confirm event forwarding

**Run on:** WINHUNT01, not on the Windows physical host.

Follow [Steps 21–27](../docs/steps/README.md) for the Windows 11 VM, Windows auditing, Sysmon, the Splunk Universal Forwarder, TLS certificates, and collection checks.

The documented Windows helper scripts are under [scripts/windows/](../scripts/windows/). Configure the official Sysmon and Splunk installer versions separately. Windows sends telemetry to `splunk01.lab.test:9997` over verified TLS.

In Splunk Web (on the private lab), run a source-health search:

```spl
(index=win_security OR index=win_system OR index=powershell OR index=sysmon OR index=linux OR index=lab) earliest=-24h
| stats count by index host sourcetype
```

Expected result: Actual event counts for the sources you have configured. A file existing on GitHub is **not** proof that Windows data is arriving.

## 6. Run safe threat-hunting exercises

Follow [Steps 28–30](../docs/steps/README.md): generate controlled lab activity, run SPL searches, then configure the lab dashboard and limited analyst role.

For the optional Kali VM, follow [Step 28.16](../docs/steps/28-generate-harmless-hunting-activity.md#step-2816--optional-kali-linux-analysis-workstation) and the [full Kali workstation guide](../docs/network-defense/KALI_DEPLOYMENT.md) for private synthetic PCAP analysis. Record only results you actually observe; VMnet8 alone does not mirror other VMs' traffic.

Start with [`hunts/00-data-health.spl`](../hunts/00-data-health.spl). Continue through the [hunting-search folder](../hunts/) for PowerShell, account changes, failed logons, tasks, process/network activity, Linux logging, and custom fields.

**Important:** A matching event identifies something to investigate. It does not establish that an attack occurred. Remove the disposable Windows account and scheduled task after testing, following [Step 46](../docs/steps/46-remove-the-test-objects.md).

## 7. Configure and test RHEL-IDM01 + LDAPS

Follow [Steps 31–44](../docs/steps/README.md) to configure IdM DNS, create the separate lookup identity, install the public directory CA certificate on Splunk, and verify TLS and directory lookup.

- Use `idm01.lab.test:636` for verified LDAPS.
- Map `splunk-hunters` to `lab_hunter` and `splunk-admins` to `admin`.
- Preserve the native Splunk administrator account for recovery.
- Test permitted access, denied access, and group removal; record actual results.

Safe source examples: [`docs/reference/ldap-authentication.conf.example`](../docs/reference/ldap-authentication.conf.example) and [`docs/reference/ldap-client.conf.example`](../docs/reference/ldap-client.conf.example). **Never upload the live `authentication.conf` or its bind password.**

## 8. Alerts, backup, final checks, and optional labs

Follow [Steps 45–49](../docs/steps/README.md) to enable and test the encoded-PowerShell alert, clean up test objects, create a protected backup, and verify startup after reboot.

The [backup script](../scripts/rhel/backup-config.sh) briefly stops Splunk and saves private configuration. Run it only during planned lab downtime; keep backup archives outside GitHub. Do not treat a successful backup as proof of successful recovery until tested on an isolated clone.

Optional exercises are linked in [the seven appendices](../docs/appendices/README.md): pipeline processing, local data integrity, Azure OIDC, NGINX, Windows ZIP handling, password redaction, and HEC. Optional workflows must be explicitly configured; their presence does not mean they have run.

## 9. Record results and publish updates

- Record observed outcomes in [`evidence/sanitized/validation.md`](../evidence/sanitized/validation.md) and [`evidence/sanitized/ldap-validation.md`](../evidence/sanitized/ldap-validation.md). Leave untested checks **Pending**.
- Update [`docs/reference/versions.md`](../docs/reference/versions.md) with the exact installed builds.
- Add reviewed screenshots using [the screenshot guidance](../docs/reference/screenshot-naming.md); the existing [screenshots](../screenshots/) are source evidence, not automatic validation.
- Review [SECURITY.md](../SECURITY.md) before committing anything to this **public** repository.

**Run on:** VS Code WSL terminal, from the repository root:

```bash
python3 scripts/validate_project.py
python3 -B -m unittest discover -s tests -v
python3 tools/publication_preflight.py
git status
```

**Command overview:** The validator checks project structure; `unittest` executes offline tests; the publication preflight checks for common public-repository risks; `git status` shows unpublished changes. None of these replaces live Splunk, Windows, or IdM testing.

To publish *reviewed* changes, use [the WSL GitHub guide](../docs/reference/WSL_VSCODE_GITHUB_UPLOAD_GUIDE.md) and preserve the existing Git history and MIT `LICENSE`.

## 10. Full documentation

- [Complete 52-step deployment index](../docs/steps/README.md)
- [Deployment order](../docs/reference/deployment-order.md)
- [Complete lab guide (Markdown)](../docs/reference/RHEL_10_2_Splunk_Complete_Guide_with_LDAP.md)
- [Installed software and vendor download sources](../docs/reference/downloads.md)
- [Architecture](../docs/reference/architecture.md)
- [VS Code + WSL start guide](START_HERE_WSL.md)

**Optional Zero Trust extension:** [START_HERE_ZERO_TRUST.md](START_HERE_ZERO_TRUST.md) and [complete zero-trust implementation guide](../docs/zero-trust/IMPLEMENTATION_GUIDE.md) describe additional resource-level identity, network, telemetry and RMF controls. These are separate from the original lab deployment and are WIP.

**Security:** Keep passwords, tokens, private keys, installation packages, raw logs, and backups out of Git. If real passwords shown in older source instructions were ever used, rotate them. Review historical documentation and screenshots before making additional public commits.
