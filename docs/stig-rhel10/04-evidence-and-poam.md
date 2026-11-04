# 04 — Scan Evidence, Screenshots and POA&M

## Private evidence requirements

The assessment wrapper stores `results.xml`, `results-arf.xml`, `report.html`, `scan.log` and source/host metadata under `/root/stig-rhel10/reports/SCAN_TIMESTAMP/` on each RHEL VM. This directory is root-only. Do **not** upload raw reports, source benchmark, ZIP, system inventory with real identifiers or screenshots containing private attributes to public GitHub.

For **each host** preserve privately:

- RHEL release and scanner RPM/version.
- User-supplied DISA package checksum and approved baseline revision.
- Full XCCDF profile ID and reason/approval.
- Scan date/time (UTC), tool exit status, rule-result counts and exceptions.
- OpenSCAP logs, full scan report, checks used, remediation changes and actual retest.
- Service regression: Splunk forwarding/searches/index mount and IdM LDAP/Kerberos/DNS/time.
- Signed review/decision record appropriate to the organization (if applicable).

## Suggested screenshots (capture only after actually performing each action)

| Figure | Suggested sanitized name | Evidence |
| --- | --- | --- |
| Figure STIG-01 | `STIG_01_RHEL10_2_Version.png` | Actual RHEL release and kernel |
| Figure STIG-02 | `STIG_02_OpenSCAP_Package_Versions.png` | Installed OpenSCAP scanner version |
| Figure STIG-03 | `STIG_03_DISA_V1R1_Profiles.png` | `oscap info` benchmark and approved profile |
| Figure STIG-04 | `STIG_04_PreScan_Private_Summary.png` | Redacted initial rule-result totals |
| Figure STIG-05 | `STIG_05_CAT_I_Findings_Review.png` | Sanitized high-risk findings; no leaked host data |
| Figure STIG-06 | `STIG_06_Splunk_Service_Regression.png` | Observed index mount, service state and secure forwarding |
| Figure STIG-07 | `STIG_07_IdM_Service_Regression.png` | Observed IPA, DNS, Kerberos, verified LDAPS |
| Figure STIG-08 | `STIG_08_Approved_Remediation.png` | One documented change + verification |
| Figure STIG-09 | `STIG_09_PostScan_Comparison.png` | Actual repeat assessment and trend |
| Figure STIG-10 | `STIG_10_POAM_and_Exception_Status.png` | Open findings and validated decision state |

**Figure caption example:** “Figure STIG-09: V1R1 baseline and post-change OpenSCAP results for the RHEL 10.2 lab, with unresolved findings retained.”

## Sanitized public status

Update [validation template](../../evidence/sanitized/rhel10-stig-validation.md) only with actual non-sensitive results. Keep `Pending` for unperformed tests; document failures and limitations. A successful local syntax test does not become a STIG Pass.

## POA&M template fields

| Field | Meaning |
| --- | --- |
| Finding and V-ID / SV-ID | Identifier from actual scan |
| Host | Splunk or IdM VM; redacted externally if required |
| CAT | Baseline severity |
| Observed result | `fail`, `error`, `unknown`, `notchecked`, etc. |
| Impact / dependencies | Actual security and service risks |
| Proposed mitigation | Exact reviewed change and rollback |
| Interim control | Monitored compensating safeguard |
| Owner / target date | Actual accountable resource and deadline |
| Exception / risk acceptance | Proper reviewer and signed decision |
| Retest | Actual timestamp, scanner, benchmark, profile and outcome |
| Evidence pointer | Private internal path or sanitized ID |

Do not publish sensitive vulnerability inventories or host-specific evidence if the systems are not designated for public portfolio use.
