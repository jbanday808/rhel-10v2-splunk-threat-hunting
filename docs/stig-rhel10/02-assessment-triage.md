# 02 — Understand SCAP Results and Prioritize Findings

**Use the exact user-provided V1R1 XML** and a full benchmark profile from [metadata](BENCHMARK_METADATA.md). A partial CAT-I-only scan is not a full assessment.

## Scan outputs

The [scan wrapper](../../scripts/stig/scan-rhel10-readonly.sh) writes these **private, root-only files** under a timestamped folder:

- `results.xml` — XCCDF rule results. Primary input to the included result summarizer.
- `results-arf.xml` — Asset Reporting Format result stream for detailed export/processing.
- `report.html` — OpenSCAP visual findings report; private only.
- `scan.log` — stdout/stderr, including incomplete/error details. Treat as sensitive.
- `source-sha256.txt`, `host-identity.txt` — source and host metadata; private only.

## Typical XCCDF outcomes

| Outcome | Meaning and next action |
| --- | --- |
| `pass` | Test matched specified expected state **for this one rule**; independently verify operational effects. |
| `fail` | Rule condition failed; record and assess control gap, not an automatic change command. |
| `error` | Evaluation failed; investigate test/tool/permissions before scoring the control. |
| `unknown` | Indeterminate; not a pass. Investigate content and environment. |
| `notapplicable` | Rule appears outside detected platform/applicability; manually verify applicability assumptions. |
| `notchecked` | Not tested by the tool; requires manual or additional evidence. |
| `notselected` | Out of the chosen profile; not assessed. |
| `informational` | Informational result; not equivalent to an assessed pass. |
| `fixed` | Automated remediation changed state; **this repository scan wrapper never runs automated remediation**. Investigate if encountered from another tool. |

OpenSCAP `xccdf eval` exit code **2** can mean the scan completed with failed checks. An unexpected process error is separate from a noncompliant finding. Review `scan.log` and confirm the output files exist.

## Read and summarize actual results (on the RHEL VM)

```bash
sudo python3 /path/to/repository/scripts/stig/summarize_results.py \
  /root/stig-rhel10/reports/YOUR_SCAN_ID/results.xml \
  --csv /root/stig-rhel10/reports/YOUR_SCAN_ID/rule-results.csv
```

The result CSV includes full `idref` rule IDs and result values. Match them to V1R1 catalog `SV-`, `V-` and `RHEL-10-` identifiers from the local [benchmark inventory tool](../../scripts/stig/inspect_benchmark.py). Both inventories should remain private on a host or analyst workstation.

## Triage in a fixed sequence

1. Confirm the **host and profile**; wrong host or only CAT-I profile invalidates conclusions.
2. Separate **error/unknown/notchecked** from actual failures; re-run/repair scanner if needed.
3. Prioritize **CAT I** failures, then CAT II and CAT III, considering real exploitation potential and system role.
4. Review **applicability**. Some requirements apply only when a service is installed or according to system owner policy.
5. Assess the **functional risk** to Splunk indexes, LDAP, IdM, DNS, Kerberos, storage, TLS, SELinux, SSH and availability.
6. Assign owner, approved change ticket, backup ID, rollback test and target date.
7. Make one reviewed change or one tightly related change set; then perform functional regression.
8. Re-scan **the same source/profile** and compare rule outcomes; record unresolved findings.
9. Escalate policy exceptions and compensating controls to the authorized reviewer; never silently relabel fail as N/A.

## Two separate evaluation sources

**1. User-supplied official DISA V1R1 package** has `xccdf_mil.disa.stig_profile_MAC-...` profiles and 396 rules.

**2. Red Hat's vendor `scap-security-guide` package** uses a different stream and `xccdf_org.ssgproject.content_profile_stig`; Red Hat documentation refers to RHEL 10.2 V1R2 content. Run separate scans and reports if both baselines are approved. Do not combine rule counts, severity, scored percentages or profile IDs.

## Reporting quality

Always retain benchmark version, scanner build, OS minor version, asset, profile, UTC time, tool exit code, observed total result count and limitations. Passing automated checks is **not** evidence that all STIG controls were satisfied; some need manual assessment or independent review.
