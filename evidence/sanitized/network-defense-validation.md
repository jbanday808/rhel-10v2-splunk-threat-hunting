# Network Defense Lab — Sanitized Validation (Work in Progress)

**Repository content:** Prepared. **Sensor deployment:** Not verified. **Live captures:** None performed here. **CMMC assessment or certification:** Not claimed.

| ID | Milestone | Current status | Actual evidence |
| --- | --- | --- | --- |
| NET-01 | Approved CONOPS and boundaries | Pending | TBD |
| NET-02 | RHEL-SENSOR01 OS, resources, snapshot and isolation | Pending | TBD |
| NET-03 | Synthetic DNS PCAP generation and hash | Pending | TBD |
| NET-04 | TShark/Wireshark correct DNS decoding | Pending | TBD |
| NET-05 | Zeek offline PCAP parsing / JSON events | Pending | TBD |
| NET-06 | Suricata config + EVE + benign IDS rule match | Pending | TBD |
| NET-07 | YARA benign positive and negative control | Pending | TBD |
| NET-08 | Sigma backend and converted SPL review | Pending | TBD |
| NET-09 | New indexes, UF TLS and firewall source allowlist | Pending | TBD |
| NET-10 | Splunk parsing, timestamp and RBAC verification | Pending | TBD |
| NET-11 | Baseline coverage, anomalies and measured drops | Pending | TBD |
| NET-12 | Case report and owner root-cause review | Pending | TBD |
| NET-13 | CMMC Level 2 sample mapping | Documentation only | No assessment |
| NET-14 | Existing Splunk, Windows and IdM regression | Pending | TBD |

## Zeek deployment acceptance

Follow [Step 28 of the Zeek deployment guide](../../docs/network-defense/ZEEK_DEPLOYMENT.md#step-28-record-acceptance-evidence) for the observation required at each milestone. The new guide and configuration examples do not change the deployment statuses above.

| Zeek-specific check | Current status | Actual evidence |
| --- | --- | --- |
| Approved image digest, actual version, and policy parse | Pending | TBD |
| Sensor offline DNS fixture and missing-file negative test | Pending | TBD |
| Authorized mirror, interface/filter, and bidirectional visibility | Pending | TBD |
| Quadlet start/stop, preserved run directories, and approved boot behavior | Pending | TBD |
| Synthetic Splunk event count, timestamp accuracy, and JSON fields | Pending | TBD |
| Optional UF service identity, staging, verified TLS, and RBAC negative test | Pending | TBD |
| Retention/loss monitoring, rollback, and core-lab regression | Pending | TBD |

## Observed synthetic replay

These checks ran on a separate Linux validation host on November 5, 2026 (Hawaii time). They cover the repository fixtures. The VM milestones above track your own environment.

| Check | Observed result |
| --- | --- |
| TShark 4.4.18 and dpkt 1.9.8 | The DNS fixture decoded as one query. The HTTP fixtures had 33 baseline and 22 investigation packets. The candidate HTTP request appeared in frame 17. Fixed timestamps reproduced identical capture hashes. |
| Zeek 9.0.1 | The baseline produced 6 connection, 3 DNS and 3 HTTP rows. The investigation produced 4 connection, 2 DNS and 2 HTTP rows. The candidate connection's Community ID and tuple matched the Suricata alert. |
| Suricata 7.0.10 | The DNS fixture fired SID `1000001` once. HTTP SID `1001001` fired zero times on baseline and once on investigation. A private path-only rule fired once on baseline and twice on investigation, including the two approved-host requests. |
| YARA 4.5.2 | The HTTP candidate matched both inert markers. The one-marker control did not match. |
| Sigma CLI 4.0.0 and Splunk backend 3.0.0 | The DNS rule produced a native Zeek `query` filter. The Windows rule produced a process-creation filter using `EventCode`, `Image` and `CommandLine`. |
| Splunk upload preparation | The local preparation commands produced 16 normalized fixture rows and one candidate correlation by run, tuple, Community ID and time. Splunk indexing and Windows event verification remain Pending. |

Reproduce the HTTP replay with the [worked case](../../docs/network-defense/OFFLINE_HTTP_WALKTHROUGH.md). Store generated evidence privately. Record live results against the corresponding milestone after testing in the actual lab.
