# 09 — NIST RMF, DISA STIG, Security Controls and ATO Planning

**Scope:** Public learning lab. This document is not a System Security Plan approved by a federal organization, and it does **not** grant an Authorization to Operate (ATO).

## NIST RMF seven-step sequence (SP 800-37 Rev. 2)

| Step | Action for this lab | Evidence / actual status |
| --- | --- | --- |
| **PREPARE** | Document purpose, responsible users, boundaries, assets, architecture and recovery. | Lab inventory and stakeholder list — planning |
| **CATEGORIZE** | Identify information types and CIA impact; apply FIPS 199 only when an organization authorizes the categorization. | **Not formally categorized** |
| **SELECT** | Determine applicable controls from SP 800-53 and SP 800-53B, tailoring and inheritance after categorization. | Illustrative mapping only |
| **IMPLEMENT** | Configure least privilege, TLS, zoning, patches, audit logging, backups. | Source controls documented; live evidence pending |
| **ASSESS** | Execute examine/interview/test assessment procedures with independent review. | Not independently assessed |
| **AUTHORIZE** | Obtain the actual authorizing official's documented risk decision if applicable. | **NO ATO / not authorized** |
| **MONITOR** | Record metrics, risks, changes and periodic verification. | Template provided; live monitoring unverified |

## Illustrative NIST SP 800-53 control mapping

| Control | Relevant Zero Trust action | Example lab artifact | Status |
| --- | --- | --- | --- |
| **AC-2** Account Management | Approved user inventory and lifecycle | IdM account inventory, offboarding test | Proposed |
| **AC-3** Access Enforcement | Splunk authorized index access | `lab_hunter` role allow/deny | Proposed |
| **AC-6** Least Privilege | Minimal analyst privilege | `authorize.conf` review | Proposed |
| **IA-2** Identification & Authentication | Protected human identity entry | LDAP/SSO/MFA review | Partial design, MFA absent |
| **CM-2** Baseline Configuration | Version and drift inventory | Git commits, docs/versions.md | Documentation |
| **CM-6** Configuration Settings | Secure configuration design | Firewall/LDAP policy | Proposed |
| **AU-2** Event Logging | Relevant auth/network events | Splunk collection matrix | Pending test |
| **AU-12** Audit Record Generation | Actual event recording | Synthetic test event/search | Pending test |
| **SC-8** Transmission Confidentiality & Integrity | TLS 9997, HTTPS 8000, LDAPS 636 | Certificate chain verification | Pending test |
| **SC-7** Boundary Protection | Host-specific allowlists | firewalld rules and packet tests | Pending test |
| **SI-2** Flaw Remediation | Maintain RHEL/Windows and Splunk | Patch inventory and change ticket | Pending |
| **SI-4** System Monitoring | SIEM correlation | SPL searches and investigations | Pending |
| **CA-7** Continuous Monitoring | Repeated compliance / exposure review | Monitoring cadence and evidence | Planned |
| **IR-4** Incident Handling | Controlled human triage and response | Incident exercise | Planned |

**This is an illustrative mapping, NOT a selected or assessed baseline.** Authoritative control wording and enhancement applicability must be checked in the current NIST catalog and your system’s actual approved requirements.

## DISA STIG and OpenSCAP procedure (RHEL 10.2)

1. Open the official [DISA STIG library](https://public.cyber.mil/stigs/downloads/) and identify the **correct current published benchmark** for each OS and product. Do **not** assume a RHEL 10 STIG exists or use a RHEL 9 STIG as if it covers RHEL 10.
2. Check whether validated machine-readable content (XCCDF/SCAP) exists and corresponds to installed RHEL 10.2.
3. Save the benchmark to a **private** lab directory. Review each finding for application dependencies (IdM, SELinux policies, Splunk listeners, audit, FIPS) and documented applicability.
4. On the appropriate RHEL VM, optionally install/check the official scanner after authorization:

```bash
rpm -q openscap-scanner scap-security-guide
oscap --version
oscap info /path/to/verified-official-datastream.xml
```

5. Choose the actual approved benchmark profile ID from `oscap info`; **never invent one**. If authorized, run an **assessment only**, not remediation:

```bash
sudo oscap xccdf eval \
  --profile 'PROFILE_ID_FROM_OSCAP_INFO' \
  --results /root/private-scan-results.xml \
  --report /root/private-scan-report.html \
  /path/to/verified-official-datastream.xml
```

6. Keep raw reports in **private** storage. Extract non-sensitive findings into a POA&M with control owner, impact, planned action, exception, timestamp and recheck.
7. Test changes on VM snapshots first. Never mass-remediate or overwrite a production Splunk/IdM host.

**Command overview:** `rpm -q` checks installed RPMs; `oscap info` shows available profiles; `oscap xccdf eval` performs a scan without `--remediate`. The paths/profile are intentional placeholders and **must** be replaced after verifying actual content.

## SSP / POA&M fields

- System name, owner, mission, authorized users, boundaries and interconnections.
- Actual asset/security categorization (when approved), controls and inheritance.
- Observed implementation and evidence ID for each control.
- Gap, severity, owner, target date, compensating control, exception and retest.
- Actual decision authority and status. Never fabricate a signed ATO.

See [Zero Trust risk register](../../examples/zero-trust/risk-register.example.csv), [verification evidence template](../../evidence/sanitized/zero-trust-validation.md) and [NIST AI RMF workstream](../ai-rmf/README.md) **only if that separate draft branch is later merged**.

## DoD Zero Trust Target guidance

The publicly available DoD Zero Trust Strategy defines capability and activity targets, but compliance depends on component-level implementation, independent evidence and organizational governance, not a portfolio checklist. This repository claims **alignment for educational demonstration**, not formal DoD Target maturity.
