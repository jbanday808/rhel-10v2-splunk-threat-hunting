# Complete 26-Step Guide — RHEL 10.2 STIG V1R1 SCAP Hardening

**Project:** [RHEL 10.2 Splunk Threat Hunting Lab](https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting)  
**Baseline source:** The user-supplied **DISA Red Hat Enterprise Linux 10 STIG SCAP Benchmark V1R1 (SCAP 1.3)**, 396 rules.  
**Targets:** `RHEL-SPLUNK01` (172.25.250.10) and `RHEL-IDM01` (172.25.250.30).  
**Development:** Windows 11, VMware Workstation Pro, Ubuntu WSL and VS Code.  
**Initial status:** Documentation added only. **Live scans/remediations not performed, no formal STIG attestation or ATO.**

This is a **non-destructive, assessment-first** implementation plan. It explains how to install OpenSCAP, securely transfer the supplied benchmark, run a full non-remediating evaluation, inspect failures, protect Splunk/IdM dependencies, apply owner-approved fixes one at a time, rescan, and record evidence. Every command identifies its execution environment. **Never use `--remediate` on a production or complex Splunk/IdM VM without assessed risk, approved change and tested recovery.** This project's scripts never use automatic remediation.

Read [uploaded benchmark metadata](BENCHMARK_METADATA.md), [sensitive configuration risks](01-risk-and-impact.md), and [official references](06-official-references.md) before starting.

## Phase 1 — Preparation, approvals and safe recovery

### Step 01 — Open the original repository (Ubuntu WSL)

```bash
cd ~/projects/rhel-10v2-splunk-threat-hunting
git status
git switch main
git pull --ff-only origin main
code .
```

**Command overview:** `cd` enters the existing project, `git status` shows local edits, `git switch main` selects the approved branch, `git pull --ff-only` safely retrieves merged updates, and `code .` opens VS Code. **If the workstream is still under review**, open its feature branch instead. Save any uncommitted edits before switching.

**Verify:** `start-here/START_HERE_RHEL10v2_STIG.md` and `docs/stig-rhel10/` appear after merge; original 52 steps remain unchanged.

### Step 02 — Review scope, system owners and applicability

Document separately for **RHEL-SPLUNK01** and **RHEL-IDM01**:

- Purpose, installed RHEL minor release, owner and permitted maintenance window.
- Approved DISA benchmark revision, selected full profile and basis for using it.
- Secure source package provenance, checksum and retention.
- Sensitive services: Splunk Web HTTPS 8000, forwarding 9997, LDAPS 636, DNS 53, SSH 22, IdM/Kerberos, storage and backup.
- Who may approve exceptions, review failures, perform remediation and authorize changes.

**Gate:** The selected benchmark is accepted by the actual system owner; **do not** infer DoD classification or formal impact level from an XCCDF profile title.

### Step 03 — Confirm the two RHEL 10.2 VMs from their consoles

On **each RHEL VM console**, run:

```bash
cat /etc/redhat-release
cat /etc/os-release
hostnamectl
uname -r
sudo subscription-manager status || true
sudo dnf repolist --enabled
```

**Command overview:** Shows OS build, kernel, registration status (if configured), and enabled repositories. A failed subscription status requires investigation; it is **not** evidence that RHEL STIG content is unusable.

**Gate:** The target is actually RHEL 10; do **not** apply RHEL 9 profiles to RHEL 10.

### Step 04 — Capture security and service baseline (each RHEL VM)

```bash
getenforce
sudo systemctl is-active firewalld auditd chronyd rsyslog
sudo firewall-cmd --get-active-zones
sudo firewall-cmd --list-all
findmnt --mountpoint /splunkdata || true
df -hT
ip -brief address
sudo ss -lntp
```

**Command overview:** Reads SELinux, firewall/audit/time/logging services, storage, addresses and listeners. `/splunkdata` is specific to RHEL-SPLUNK01; absence on RHEL-IDM01 is expected.

**Gate:** Record actual state and unresolved problems, including whether Splunk or IdM was already functional *before* hardening.

### Step 05 — Back up and plan recovery before any changes

In **VMware Workstation Pro**, create a labeled pre-STIG checkpoint for each owned VM. For directory services, use a consistent backup/snapshot method appropriate to IdM database state. Keep an accessible VM console, last-known-good DNS, and a private encrypted copy of important system configuration. Confirm you can restore the VM and data.

For Splunk, protect `/splunkdata` and installed app configuration. For IdM, protect IPA database, CA, keys and DNS according to Red Hat's IdM backup procedures. **Do not publish backups or secret-bearing files.**

**Gate:** Recovery has been rehearsed or appropriately validated; critical dependencies listed in [01-risk-and-impact.md](01-risk-and-impact.md).

## Phase 2 — Inspect and securely distribute the supplied DISA benchmark

### Step 06 — Keep the downloaded ZIP outside Git (Ubuntu WSL)

Use the **actual downloaded ZIP**. Set the path to your Windows Downloads location (replace the placeholder name):

```bash
STIG_ZIP="/mnt/c/Users/YOUR_WINDOWS_USERNAME/Downloads/U_RHEL_10_V1R1_STIG_SCAP_1-3_Benchmark(1).zip"
test -f "$STIG_ZIP" || { echo "Benchmark ZIP not found"; exit 1; }
mkdir -p "$HOME/stig-private"
chmod 700 "$HOME/stig-private"
cp -- "$STIG_ZIP" "$HOME/stig-private/rhel10-v1r1.zip"
chmod 600 "$HOME/stig-private/rhel10-v1r1.zip"
sha256sum "$HOME/stig-private/rhel10-v1r1.zip"
```

**Command overview:** `test -f` confirms the file, `mkdir` creates a private folder, `cp` copies the original outside the repository, `chmod` restricts local access and `sha256sum` prints the uploaded copy's fingerprint.

**Expected SHA-256 of the uploaded ZIP:**

```text
84d547f9dc099eaeb882c19d49a5b5f2f664f702cad0250d343121ba8689fa7f
```

A mismatch means different bytes: stop to confirm provenance before scanning. This fingerprint identifies the **user-supplied** copy; verify official source authenticity separately.

### Step 07 — Inspect benchmark and export its complete rule inventory (WSL)

```bash
python3 scripts/stig/inspect_benchmark.py \
  "$HOME/stig-private/rhel10-v1r1.zip" \
  --inventory-csv "$HOME/stig-private/rhel10-v1r1-rule-inventory.csv"
```

**Command overview:** Inspects the supplied ZIP's XML **offline** and generates a locally stored inventory of **all 396 rules**, severity, rule IDs, vulnerability IDs and titles. The script never extracts arbitrary ZIP paths, connects to a server, or modifies a VM.

**Expected:** Benchmark version `001.001`, SCAP `1.3`, 396 rules, 28 High / 364 Medium / 4 Low, 11 profiles. Inventory stays outside Git.

### Step 08 — Install OpenSCAP tools (on each RHEL console)

```bash
sudo dnf install -y openscap-scanner scap-security-guide unzip
rpm -q openscap-scanner scap-security-guide
oscap --version
```

**Command overview:** `dnf` installs supported RHEL packages from approved repositories; `rpm -q` reports versions; `oscap --version` verifies the scanner. Installation changes the host's packages but **does not apply any STIG rules**.

If repositories are unavailable, fix registration/network or package access through approved administration before continuing. Do not download random third-party RPMs.

### Step 09 — Transfer ZIP privately to each RHEL host (WSL terminal)

First, on each **RHEL VM console** as `labadmin` (use your actual authorized name):

```bash
mkdir -p "$HOME/stig-transfer"
chmod 700 "$HOME/stig-transfer"
```

From **Ubuntu WSL**:

```bash
scp "$HOME/stig-private/rhel10-v1r1.zip" \
  labadmin@172.25.250.10:~/stig-transfer/rhel10-v1r1.zip
scp "$HOME/stig-private/rhel10-v1r1.zip" \
  labadmin@172.25.250.30:~/stig-transfer/rhel10-v1r1.zip
```

**Command overview:** `scp` transfers the approved archive through SSH into each user's private folder. Verify SSH host fingerprints out-of-band before accepting new keys. Keep the destination outside Git, shared web roots and Splunk monitored input directories.

### Step 10 — Install private read-only scan content (each RHEL console)

On the **RHEL VM**, using the same user as Step 9:

```bash
sha256sum "$HOME/stig-transfer/rhel10-v1r1.zip"
sudo install -d -m 0700 /root/stig-rhel10/v1r1
sudo install -m 0600 "$HOME/stig-transfer/rhel10-v1r1.zip" \
  /root/stig-rhel10/v1r1/source.zip
sudo unzip -p /root/stig-rhel10/v1r1/source.zip \
  U_RHEL_10_V1R1_STIG_SCAP_1-3_Benchmark.xml |
  sudo tee /root/stig-rhel10/v1r1/U_RHEL_10_V1R1_STIG_SCAP_1-3_Benchmark.xml >/dev/null
sudo chmod 600 /root/stig-rhel10/v1r1/U_RHEL_10_V1R1_STIG_SCAP_1-3_Benchmark.xml
sudo sha256sum /root/stig-rhel10/v1r1/U_RHEL_10_V1R1_STIG_SCAP_1-3_Benchmark.xml
```

**Command overview:** Confirms archive identity, creates a root-only content directory, saves the source ZIP, extracts only the **named XML** to a root-only file and computes the XML fingerprint. The extraction command intentionally avoids unpacking any arbitrary paths.

**Expected XML SHA-256:** `47d7a6c9fb544a510a69b871422adfc4967ddd53f2c35e669c1fcbb029f29c93`.

If the check fails or `unzip` reports errors, **do not** scan the file. Remove the old unneeded transfer copy after verifying the private root copy.

### Step 11 — Confirm the source data stream and profiles (each RHEL VM)

```bash
sudo oscap info \
  /root/stig-rhel10/v1r1/U_RHEL_10_V1R1_STIG_SCAP_1-3_Benchmark.xml
```

**Command overview:** Lists the **actual benchmark name and selectable XCCDF profiles**. Find the `xccdf_mil.disa.stig_profile_MAC-*` profiles described in [BENCHMARK_METADATA.md](BENCHMARK_METADATA.md).

Do not mix this DISA benchmark profile with Red Hat's separate vendor profile `xccdf_org.ssgproject.content_profile_stig`. Red Hat's vendor content for RHEL 10.2 may reflect **V1R2**, not the uploaded V1R1.

### Step 12 — Select and document a complete assessment profile

For an **unclassified educational example only**, a complete profile present in the uploaded benchmark is:

```bash
PROFILE="xccdf_mil.disa.stig_profile_MAC-3_Public"
printf 'Selected educational example profile: %s\n' "$PROFILE"
```

**Command overview:** Sets a shell variable for a profile that selects all **396 rules** in this uploaded content. Selecting it is **not** formal FIPS 199, mission-assurance or DoD classification. An authorized organization must determine its actual profile. Do not use the `CAT_I_Only` profile to claim a full STIG assessment.

## Phase 3 — Conduct an initial non-remediating audit

### Step 13 — Create a root-only assessment location (each RHEL VM)

```bash
sudo install -d -m 0700 /root/stig-rhel10/reports
sudo ls -ld /root/stig-rhel10/reports
```

**Command overview:** Creates a restricted location for scan results, ARF, HTML and logs. These often contain hostnames, local configuration and user information.

### Step 14 — Run the uploaded DISA V1R1 benchmark in assessment-only mode

Use the repository-supplied scan wrapper from the checked-out project on the **RHEL VM**, or run its exact equivalent manually. First copy only the reviewed script to an approved local path or clone your existing repository on the RHEL VM according to your source-management procedure.

**If the project checkout is present on the RHEL VM:**

```bash
cd /path/to/rhel-10v2-splunk-threat-hunting
sudo bash scripts/stig/scan-rhel10-readonly.sh \
  /root/stig-rhel10/v1r1/U_RHEL_10_V1R1_STIG_SCAP_1-3_Benchmark.xml \
  xccdf_mil.disa.stig_profile_MAC-3_Public
```

**If the project exists only in WSL**, first review and transfer the standalone script using SSH/SCP into a root-controlled directory, then run that script from the RHEL VM. **Never attempt to assess a RHEL VM by running the WSL commands on your Windows host.**

The wrapper executes a **non-remediating** OpenSCAP `xccdf eval` and writes private `results.xml`, `results-arf.xml`, `report.html` and `scan.log` files under a timestamped directory. No `--remediate` switch is accepted.

**Command overview:** `bash` executes the reviewed assessment wrapper; `sudo` permits reading protected local configuration; first positional argument is the private benchmark XML; second is the explicitly chosen profile.

**Interpretation:** OpenSCAP may return **2** when a scan completes but finds noncompliant checks; the wrapper treats that as **scan completed with findings**, not a successful hardening result. Other unexpected exit codes require investigation.

### Step 15 — Record host, profile, time, tool and content versions

Within the private report folder, record:

- Host / purpose, `/etc/redhat-release`, RPM versions and installed kernel.
- Scanner version (`oscap --version`).
- Full benchmark filename and both expected SHA-256 hashes.
- Full profile ID and approval rationale.
- Scan start/finish UTC, exit code, and locations of source results.
- Important scan limitations: missing packages, unscanned mounts, non-applicable checks, or errors.

**Gate:** Actual `results.xml` and `report.html` exist in root-only storage and the OpenSCAP log was reviewed. **Do not equate an exit code 0 with all rules passed.**

### Step 16 — Summarize results into a private finding inventory

On the **RHEL VM**, for the timestamped directory displayed by the scan wrapper:

```bash
sudo python3 /path/to/rhel-10v2-splunk-threat-hunting/scripts/stig/summarize_results.py \
  /root/stig-rhel10/reports/REPLACE_WITH_SCAN_TIMESTAMP/results.xml \
  --csv /root/stig-rhel10/reports/REPLACE_WITH_SCAN_TIMESTAMP/rule-results.csv
```

**Command overview:** Parses the XCCDF result document and reports counts for `pass`, `fail`, `error`, `unknown`, `notapplicable` and other states. A record of `notapplicable` must be reviewed; `error` / `unknown` are not passes. It also generates a private CSV of individual rule results. Replace the timestamp placeholder with the actual folder reported in Step 14.

### Step 17 — Review the private HTML report and prioritize findings

**At the VM console or through an approved encrypted private transfer**, review `report.html`. Check every high/CAT I finding first, then medium/CAT II and low/CAT III. Prioritize **real** exposure, business impact and compensating controls, not simply a severity number.

Cross-reference the exact `SV-...` rule, `V-...` vulnerability ID, `RHEL-10-...` version, test outcome and host. Use [triage guidance](02-assessment-triage.md).

**Gate:** Each failure has an owner, reason, proposed fix, safe test and rollback, or a documented exception review—not just an unexplained “Failed”.

## Phase 4 — Controlled remediation and functional regression

### Step 18 — Analyze Splunk and IdM compatibility **before** changing a rule

Use [01-risk-and-impact.md](01-risk-and-impact.md) and [03-remediation-and-exceptions.md](03-remediation-and-exceptions.md). Especially check:

- FIPS mode/cryptographic algorithms and TLS keys, SSH / certificates.
- `gssproxy` and IPA/Kerberos dependencies on **RHEL-IDM01**.
- `/splunkdata`, `/var/log`, `/var/log/audit` and index mounts.
- SELinux labels for the Splunk service and custom log inputs.
- `firewalld` allowlists for 22/8000/9997/636/53 and IdM/CA/Kerberos.
- `rsyslog` remote forwarding, audit logging and Splunk inputs.
- Password/account policy, service accounts and authorized admins.
- `chronyd`, DNS and certificate time validity.

**Stop gate:** If a rule breaks storage, authentication, DNS, event forwarding, recoverability or scanner reliability, do **not** apply it without explicit risk/owner review.

### Step 19 — Create one change ticket and a private backup for each proposed fix

Record exact `V-` / `SV-` / `RHEL-10-` identifiers, system, current state, recommended fix from the **actual benchmark**, risk, assigned owner, approved commands, snapshot ID, maintenance window, functional test, revert plan and retest date.

Use the [POA&M example](../../examples/stig-rhel10/poam-example.csv) as a **template**, not a list of real findings. Exceptions must reflect a documented review, not a silent skipped rule.

### Step 20 — Apply only reviewed, reversible changes (VM console)

A low-risk *example*, **only if this exact benchmark rule failed and has been reviewed**, is the debug-shell service. First inspect:

```bash
systemctl is-enabled debug-shell.service || true
systemctl is-active debug-shell.service || true
```

If present, confirmed unnecessary, and approved:

```bash
sudo systemctl mask --now debug-shell.service
systemctl is-enabled debug-shell.service
```

**Command overview:** Checks whether the debug shell is enabled or running; `mask --now` blocks starting it and stops it if active; the final command verifies state. This corresponds to uploaded **RHEL-10-700970 (V-280094)**; a disabled/absent service may already be safe. Do **not** use this one example as evidence that the other **395** checks were remediated.

**Backout:** If masking interfered with an approved dependency, restore the documented pre-change state through the VM console after change-owner review; never unmask silently.

### Step 21 — Run Splunk/IdM service health and security regression tests

On **RHEL-SPLUNK01** (commands are read-only):

```bash
sudo systemctl status Splunkd.service --no-pager -l
findmnt --mountpoint /splunkdata
df -hT /splunkdata
getenforce
sudo firewall-cmd --get-active-zones
sudo ss -lntp
```

On **RHEL-IDM01**:

```bash
sudo ipactl status
getent hosts splunk01.lab.test
sudo firewall-cmd --get-active-zones
```

On **RHEL-SPLUNK01**, if the public trusted IdM CA is installed:

```bash
sudo -u splunk openssl s_client \
  -connect idm01.lab.test:636 \
  -servername idm01.lab.test \
  -CAfile /opt/splunk/etc/auth/ldap/idm-ca.pem \
  -verify_hostname idm01.lab.test -verify_return_error </dev/null
```

**Command overview:** Checks services, Splunk data mount, SELinux/firewall, directory status, DNS and authenticated TLS. Add an **actual Splunk query** verifying current Windows/Linux events and an authorized/unauthorized role test. A passing scan with broken application function is **not an acceptable deployment result**.

### Step 22 — Restore service immediately if an approved fix causes an outage

Use the **VM console**, documented known-good snapshot/config backup and host-specific rollback. If an on-the-fly firewall change blocks a connection and permanent rules have not been modified, follow the existing [firewall recovery guide](../zero-trust/06-network-microsegmentation.md). Verify both successful authorized access and denied unauthorized access after recovery.

For storage, SELinux/FIPS, or IdM changes, use the approved component recovery procedure; **do not** blindly disable SELinux, flush all firewall rules, revoke certificate checks, reformat drives, or remove whole authentication packages.

**Record:** Incident, rollback, actual observed impact, owner and decision.

## Phase 5 — Reassess, report and maintain

### Step 23 — Perform the post-change full benchmark scan

Repeat Step 14 using the **same V1R1 XML, chosen full profile, host and documented tool version**. Use a new timestamped report directory. Compare actual rule IDs/states rather than just numeric score. Report improvements, regressions and unresolved failures.

Do **not** mark a failed requirement “Not Applicable” just because it is inconvenient. Confirm N/A criteria in the underlying rule and obtain the appropriate review.

### Step 24 — Produce a sanitized POA&M and evidence package

Update [evidence/sanitized/rhel10-stig-validation.md](../../evidence/sanitized/rhel10-stig-validation.md), the private full results, and [POA&M template](../../examples/stig-rhel10/poam-example.csv). Include actual failed IDs, severity, evidence pointers, ownership, target, compensating safeguards, observed retest and decision.

**Never publish:** raw ARF/XML/HTML, privileged shell history with secrets, IdM databases, CA keys, login events with real identities, full system inventories, logs with credentials or private backups.

### Step 25 — Establish ongoing STIG maintenance and change control

Use [maintenance guide](05-operations-and-updates.md). Define review cadence, check official DISA/Red Hat updates, monitor security patches and drift, retest on Splunk/IdM updates, patching, new packages, certificate replacement, firewall changes and role changes. Record both **V1R1 and any future V1R2** decisions separately. Never assume a newer guide has identical rule IDs or that data can be combined into one score.

### Step 26 — Validate project source and publish approved documentation

From **Ubuntu WSL**:

```bash
cd ~/projects/rhel-10v2-splunk-threat-hunting
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/validate_project.py
python3 tools/publication_preflight.py
git status
git diff --check
```

**Command overview:** Runs offline repository checks, scans for source/package issues, checks the current working tree and verifies changed line formatting. **These are NOT live OpenSCAP scans.**

Review any GitHub pull request and GitHub Actions source tests before merging. Public docs should describe actual accomplishments precisely: **benchmark inspected**, **scanner procedure documented**, **scans Pending** until executed. **Never claim “STIG-compliant” or “ATO granted” solely from source files or scanner reports.**

## Summary and expected outcomes

| Deliverable | Completion criterion | Current project status |
| --- | --- | --- |
| Benchmark provenance and version | User copy identified; approved content confirmed | Uploaded copy metadata verified; official source authentication by owner pending |
| Scanner installation | Actual `oscap --version` on each RHEL VM | Pending |
| Initial full audit | Private XML/ARF/HTML from both hosts | Pending |
| Detailed findings and risk | Each relevant rule assessed and owner assigned | Pending |
| Controlled remediation | Approved change + observed regression tests | Pending |
| Rescan and evidence | Actual pass/fail/N/A trends + private report | Pending |
| Formal system compliance / ATO | Appropriate organizational assessment and authorization | **Not claimed** |

**References:** [Official resources](06-official-references.md) · [Benchmark metadata](BENCHMARK_METADATA.md) · [RHEL 10.2 STIG quick start](../../start-here/START_HERE_RHEL10v2_STIG.md).
