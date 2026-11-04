# RHEL 10.2 STIG SCAP V1R1 — Workstream

**[START HERE](../../START_HERE_RHEL10v2_STIG.md)** · **[Complete 26-Step Guide](IMPLEMENTATION_GUIDE.md)**

| File | Contents |
| --- | --- |
| [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) | 26-step install, assess, review, remediate, rescan, maintain |
| [BENCHMARK_METADATA.md](BENCHMARK_METADATA.md) | Measured ZIP fingerprints, profiles and rule counts |
| [01-risk-and-impact.md](01-risk-and-impact.md) | System dependencies and dangerous configuration categories |
| [02-assessment-triage.md](02-assessment-triage.md) | Pass/fail/error/notapplicable analysis and prioritized findings |
| [03-remediation-and-exceptions.md](03-remediation-and-exceptions.md) | One-rule-at-a-time change method and POA&M |
| [04-evidence-and-poam.md](04-evidence-and-poam.md) | Sanitized evidence and screenshots |
| [05-operations-and-updates.md](05-operations-and-updates.md) | Maintenance, rescans, benchmarks and drift |
| [06-official-references.md](06-official-references.md) | Red Hat, DISA and OpenSCAP citations |
| [../Zero Trust RMF/STIG guide](../zero-trust/09-rmf-stig-ato.md) | Related RMF planning (distinct from scan results) |

## Privacy, scope and integrity

The user-supplied **DISA RHEL 10 V1R1 SCAP 1.3** benchmark is a single source data stream with **396 rules**. We preserve its exact filename and SHA-256 fingerprints in metadata. We do **not** publish the user-provided ZIP/XML or SCAP results, account data, live server configs, keys or credentials.

**Benchmark selection:** The uploaded DISA V1R1 is the basis for the assessment runbook; Red Hat's current vendor SCAP Security Guide for RHEL 10.2 refers to **V1R2**. Choose the officially required benchmark and its exact profile with the system owner. Never present a V1R1 report as a V1R2 result.

**Safety:** No auto-remediation, FIPS mode conversion, firewall reset, partition changes, package removal or service restart is performed by any repository script. Each proposed change needs a documented baseline, impact analysis, VM console, backup and rollback.

**Evidence:** Everything starts **Pending**. Passing GitHub Actions proves source checks, **not** STIG compliance or an ATO.

## Supporting assets

| Artifact | Use |
| --- | --- |
| [inspect_benchmark.py](../../scripts/stig/inspect_benchmark.py) | Inspect supplied ZIP/XML and export a **private local** 396-rule CSV |
| [scan-rhel10-readonly.sh](../../scripts/stig/scan-rhel10-readonly.sh) | Controlled local non-remediating scan; reports private |
| [summarize_results.py](../../scripts/stig/summarize_results.py) | Aggregate real XCCDF results into a **private local** CSV |
| [POA&M example](../../examples/stig-rhel10/poam-example.csv) | Pending example rows only |
| [Evidence template](../../evidence/sanitized/rhel10-stig-validation.md) | Pending; update only after actual scans |
| [Offline unit tests](../../tests/test_stig_rhel10_tools.py) | Script/fixture tests, not live RHEL scans |

## Target hosts

- **RHEL-SPLUNK01**: Splunk app, service, protected TLS, indexes, `/splunkdata`, local audit/logs, verified LDAPS.
- **RHEL-IDM01**: DNS, IdM, Kerberos, LDAP, public CA, server service dependencies.
- **WINHUNT01**: remains outside the RHEL STIG scope.

For RHEL-specific hardening, verify actual software release and dependencies. Scans are host-specific; one host's score cannot stand in for the other.
