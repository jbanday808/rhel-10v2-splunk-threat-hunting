# 10 — Positive/Negative Validation and Evidence Guide

**Rule:** A configuration file is NOT proof the control is effective. Capture both successful authorized requests and blocked unauthorized requests, without exposing secrets or private data.

## Lab validation matrix

| ID | Control / pillar | Positive test | Negative test | Status |
| --- | --- | --- | --- | --- |
| ZT-01 | User / ICAM | `hunter01` authenticates to permitted Splunk app | `unmapped01` fails to gain authorized access | Pending |
| ZT-02 | Least privilege | Hunter can query `index=lab` | Hunter cannot access an unrelated unauthorized index or `admin` role | Pending |
| ZT-03 | IdM LDAPS | Verified hostname and trusted CA on TCP 636 | Present wrong CA/hostname in isolated test; handshake fails verification | Pending |
| ZT-04 | Device | WINHUNT01 Defender and firewall statuses observed | Missing/offline Sysmon or forwarder triggers recorded gap | Pending |
| ZT-05 | Network | .20 reaches .10 TCP 9997 | Unauthorized test peer cannot connect to .10 TCP 9997 | Pending |
| ZT-06 | Network | Management host .1 reaches .10 TCP 8000 | Disallowed test source cannot reach .10 TCP 8000 | Pending |
| ZT-07 | Management | Approved access through controlled admin session | Unapproved .10 TCP 8089 remote connection fails | Pending |
| ZT-08 | Data | Six index permissions correctly applied | Hunter cannot bypass Splunk role/index restrictions | Pending |
| ZT-09 | Logging | Windows and RHEL test event ingested with timestamp | Missing source generates an identified coverage gap | Pending |
| ZT-10 | Incident/response | Human-reviewed alert proceeds to documented triage | No auto-containment or account changes from SPL alone | Pending |
| ZT-11 | Recovery | Runtime policy rolled back from VM console | Previously denied service does not silently remain open | Pending |
| ZT-12 | STIG/RMF | Current applicable benchmarks identified; evidence collected | Unsupported “ATO/Target compliant” claims rejected | Pending |

## Actual test record (copy for each test)

```text
Test ID:
Expected result:
Host and tool:
Date/time UTC:
Tester/reviewer:
Command or Splunk search:
Observed behavior:
Result: Pending / Pass / Fail / Not Applicable
Sanitized evidence file:
Findings / exception:
Rollback and retest:
```

## Screenshot names and short Figure captions

| Figure | Suggested name | What it demonstrates |
| --- | --- | --- |
| Figure ZT-01 | `ZT_01_Architecture_Current_vs_Target.png` | Current three-VM design and **proposed** PDP/PEP |
| Figure ZT-02 | `ZT_02_Identity_Groups.png` | Sanitized IdM groups and mapped roles |
| Figure ZT-03 | `ZT_03_LDAPS_Certificate_Validation.png` | Actual CA/hostname verification result |
| Figure ZT-04 | `ZT_04_RHEL_Endpoint_Posture.png` | SELinux, firewall and audit service status |
| Figure ZT-05 | `ZT_05_Windows_Defender_Sysmon.png` | Observed Defender/Sysmon/Forwarder |
| Figure ZT-06 | `ZT_06_Firewall_Allowed_Flows.png` | Firewalld source-limited rules |
| Figure ZT-07 | `ZT_07_Allowed_Denied_Access.png` | Positive and negative connectivity tests |
| Figure ZT-08 | `ZT_08_Splunk_Zero_Trust_Telemetry.png` | Live, sanitized actual index/search results |
| Figure ZT-09 | `ZT_09_Threat_Hunting_Rule.png` | Tested hunting search with evidence |
| Figure ZT-10 | `ZT_10_RMF_STIG_Review.png` | Approved benchmark version and open findings |

**Captions should be one sentence**, such as: “Figure ZT-07: Verified source-specific allow and deny results for Splunk Web and forwarding traffic in the Zero Trust lab.” Only use “Verified” after real tests.

## Public evidence safety

- Screenshot all terminal windows only after hiding credentials, IP details beyond those intentionally public in the sample network, account IDs, private CA material, SSH fingerprints and personal identifiers.
- Keep original unredacted logs, server audit records, backups and reports outside GitHub.
- Associate each claimed result with an evidence ID, host, date and reviewer.
- If a test cannot be run, record **Pending**, not successful.
- Store sanitized findings at [evidence/sanitized/zero-trust-validation.md](../../evidence/sanitized/zero-trust-validation.md).
