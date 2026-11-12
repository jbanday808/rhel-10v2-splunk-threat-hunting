# START HERE — RHEL 10.2 STIG Hardening, SCAP Assessment and Evidence

**Benchmark:** DISA Red Hat Enterprise Linux 10 STIG SCAP Benchmark, Version 1 Release 1 (SCAP 1.3).  
**Target:** RHEL-SPLUNK01 (172.25.250.10) and RHEL-IDM01 (172.25.250.30) in the VMware homelab.  
**State:** Runbooks, offline validators and evidence templates only. **No live STIG scans, remediations, ATO or compliance approvals are claimed.**

## Read the complete implementation guide

**[Full Installation, Configuration, STIG Assessment, Remediation, Rescan and Maintenance Guide](../docs/stig-rhel10/IMPLEMENTATION_GUIDE.md)**

Start with [benchmark metadata and exact source fingerprint](../docs/stig-rhel10/BENCHMARK_METADATA.md), then follow the implementation guide in order.

## Scope and important warnings

- The uploaded V1R1 ZIP contains **one XML SCAP 1.3 data stream**, **396 XCCDF rules**: **28 high (CAT I)**, **364 medium (CAT II)**, **4 low (CAT III)**, plus **11 XCCDF profiles** (nine mission/sensitivity profiles and two special profiles).
- The source ZIP and original XML are **not committed to public GitHub**. They remain with the user and on privately controlled VMs.
- SCAP benchmark V1R1 is distinct from Red Hat's **RHEL 10.2 vendor-provided STIG profile**, which Red Hat documents as aligned with V1R2. Do not mix results or assert equivalent rule coverage. Follow an actual system owner's baseline decision.
- **Never run indiscriminate remediation**, move mounted Splunk storage, or restrict SSH/IdM networking without a snapshot, console access and tested recovery.
- **Do not enable FIPS in-place on RHEL 10:** post-installation enablement is unsupported. If required, plan a separately approved replacement installation with FIPS enabled during installation; follow the [FIPS inspection and planning guidance](../docs/stig-rhel10/03-remediation-and-exceptions.md#example-3--fips-mode-requires-a-separate-architecture-plan).
- Select an explicit **full-assessment** benchmark profile using `oscap info`. A limited “CAT I Only” profile is **not** a complete assessment. A profile name such as `MAC-3_Public` does not formally categorize the system.
- This is educational guidance; passing an OpenSCAP assessment does **not** by itself grant STIG compliance, RMF authorization, or DoD ATO.

## Existing lab, preserved

| VM | Network | Security-sensitive functions |
| --- | --- | --- |
| RHEL-SPLUNK01 | 172.25.250.10 | Splunk Enterprise, /splunkdata, TCP 8000, 9997, LDAPS client, audit + rsyslog |
| RHEL-IDM01 | 172.25.250.30 | Identity Management, DNS, LDAP/LDAPS, Kerberos, CA, directory and time dependencies |
| WINHUNT01 | 172.25.250.20 | Windows/Sysmon forwarding source; **not a RHEL STIG target** |
| VMware host | VMnet8 172.25.250.1 | Console, backup and management path |

**Original configuration and 52 deployment steps are untouched.**

## Quick commands after reviewing the guide

On each RHEL VM console, after private backup, verify:

```bash
cat /etc/redhat-release
sudo dnf install -y openscap-scanner scap-security-guide unzip
oscap --version
sudo oscap info /root/stig-rhel10/v1r1/U_RHEL_10_V1R1_STIG_SCAP_1-3_Benchmark.xml
```

**Command overview:** Shows installed RHEL version, installs trusted RHEL scanner packages, checks OpenSCAP, and lists profiles in your privately installed uploaded DISA benchmark. The last command requires following the **private transfer** steps first.

Run only a **read-only scan** with the reviewed [assessment wrapper](../scripts/stig/scan-rhel10-readonly.sh), using an **explicitly selected** full-assessment profile. Raw reports remain under private root-only storage, not GitHub.

## Documentation and source navigation

- [STIG workstream README](../docs/stig-rhel10/README.md)
- [Benchmark provenance and all profiles](../docs/stig-rhel10/BENCHMARK_METADATA.md)
- [Splunk and IdM change-risk checklist](../docs/stig-rhel10/01-risk-and-impact.md)
- [How to review OpenSCAP results](../docs/stig-rhel10/02-assessment-triage.md)
- [Controlled remediation and exceptions](../docs/stig-rhel10/03-remediation-and-exceptions.md)
- [Evidence and POA&M plan](../docs/stig-rhel10/04-evidence-and-poam.md)
- [Operations and baseline updates](../docs/stig-rhel10/05-operations-and-updates.md)
- [Official DISA and Red Hat references](../docs/stig-rhel10/06-official-references.md)
- [Sanitized validation log](../evidence/sanitized/rhel10-stig-validation.md)
- [Local benchmark metadata inventory tool](../scripts/stig/inspect_benchmark.py)
- [Offline result summarizer](../scripts/stig/summarize_results.py)
- [Private full assessment wrapper](../scripts/stig/scan-rhel10-readonly.sh)

**Only sanitized findings and project-owned scripts/templates belong in this public repository.**
