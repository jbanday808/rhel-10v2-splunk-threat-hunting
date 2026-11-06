# Passive Detection Engineering, Vulnerability Assessment and Incident Triage

## Threat hunting and baseline hypotheses

Use authorized Zeek, Suricata, TShark and Splunk records with documented ground truth.

| Hypothesis | Passive signal | Validate with |
| --- | --- | --- |
| New/unexpected service | Zeek `conn.log` unseen destination port/service | Approved service inventory and administrator |
| Unusual DNS activity | `dns.log` new/rare queried domains, high NXDOMAIN rate | Resolver configuration and endpoint application |
| Potential cleartext risk | HTTP request metadata, Telnet/FTP use, exposed cleartext protocols | Service owner, encryption and access policy |
| Possible obsolete TLS | TLS protocol/version/certificate observation | Validated server configuration and supported clients |
| SMB/RDP connection anomaly | Flow frequency, new sources, repeated failures (if logs available) | Windows/IdM source events and change ticket |
| Signature-driven alert | Suricata `alert.signature_id` and relevant packet context | Rule version, packet completeness and analyst review |
| Suspicious authorized file | YARA match on a collected *permitted* artifact | File hash, analyst classification, trusted tools |
| Portable detection | Sigma rule converted to SPL | Actual mapped fields + synthetic positive and negative tests |

**Passive limitation:** A banner or legacy protocol may indicate exposure, but does not prove host vulnerability, patch state, exploitability or system-level root cause. Escalate to owners for authorized validation; do not conduct active vulnerability probes or exploit tests on live DoD/CUI/third-party networks.

## Anomaly triage playbook

1. **Intake:** Note alert/rule ID, time UTC, source and private evidence URI. Avoid exporting raw packets to GitHub.
2. **Validate:** Confirm actual event exists, sensor saw the right traffic, time is correct, rule enabled and parser fields populated.
3. **Correlate:** Match Zeek UID/5-tuple/protocol time with Suricata flow, Windows/IdM context and approved change logs.
4. **Determine expected behavior:** Compare to defined normal traffic baseline by asset, peer, hour and service.
5. **Investigate:** Analyze harmless samples, role/asset inventory, network topology and configuration; document benign alternatives.
6. **Assess impact:** Affected authorized assets, exposed protocol, recurrence, confidence, false positives, operational effects.
7. **Confirm with owners:** Technical root cause or vulnerability requires authorized administrator configuration evidence and any separately approved scan.
8. **Notify:** Follow documented CONOPS/incident procedure; do not automatically quarantine hosts or modify firewall/IdM.
9. **Remediate and retest:** Approved change with rollback, control revalidation and updated false-positive metrics.
10. **Report:** Executive summary, evidence IDs, impact, recommendation, limitation and owner disposition.

## Splunk exercises

- [01-baseline-service-matrix.spl](../../hunts/network-defense/01-baseline-service-matrix.spl): Count Zeek observed services/ports.
- [02-rare-dns-queries.spl](../../hunts/network-defense/02-rare-dns-queries.spl): Review rare domain activity (actual DNS field mapping required).
- [03-suricata-alert-triage.spl](../../hunts/network-defense/03-suricata-alert-triage.spl): Rank observed IDS alerts.
- [04-network-data-coverage.spl](../../hunts/network-defense/04-network-data-coverage.spl): Source data completeness and last seen.

Do not promote a hunt to a production alert until syntax, ground truth, false-positive rate, index and time span are reviewed.

## Tuning and measurement

Record **expected, observed, confidence, result, false-positive type, analyst, source hash, tool versions, timestamp**, alongside coverage and packet-loss measurements. A detection engine not receiving mirrored traffic can report zero anomalies while the network is unobserved.

**External publication:** Only synthetic/approved sanitized events, never protected traffic or sensitive vulnerability inventories.
