# 08 — Continuous Monitoring, Splunk Hunts and Reviewed Automation

## Purpose

Demonstrate the DoD **Visibility & Analytics** pillar with Splunk searches, while keeping **Automation & Orchestration** safe and reviewable. Searches complement existing [13 lab hunts](../../hunts/); an SPL file alone is **not** evidence that its detection has fired.

## Deployment workflow

1. Confirm actual events are arriving in each expected index using the existing data health search.
2. Open Splunk Search in the approved lab browser.
3. Copy one search from [hunts/zero-trust](../../hunts/zero-trust/README.md) and run in a controlled test window.
4. Review time field, source names and event-code conventions of the installed add-ons; update SPL to match observed data.
5. Compare results with a synthetic test activity and ground-truth record.
6. Review any false positives; only then save a search or create a scheduled alert as a separate approved change.
7. Route detections to human investigation and case review; **do not** auto-block accounts, quarantine hosts or modify IdM based solely on SPL matches.
8. Log alert ownership, severity, false positive rate, data coverage, run date and recovery.

## Example data coverage search

```spl
(index=win_security OR index=win_system OR index=powershell OR index=sysmon OR index=linux OR index=lab) earliest=-24h
| stats count latest(_time) as last_event by index host sourcetype
| eval last_seen=strftime(last_event,"%Y-%m-%d %H:%M:%S")
| fields index host sourcetype count last_seen
```

**Explanation:** Counts collected events by index/host/sourcetype over 24 hours, showing the last arrival. It does **not** prove endpoint compliance or a complete log collection policy.

## Example failed-logon search

```spl
index=win_security (EventCode=4625 OR EventID=4625) earliest=-24h
| stats count by host user
| sort -count
```

**Explanation:** Lists observed failed Windows sign-in events by host and user. Field extraction may differ; inspect raw sanitized example event before trusting the query. A failed sign-in is not automatically a threat or an identity-policy violation.

## Source-controlled policies

- `configs/zero-trust/allowed-flows.example.json` is a **design specification**, not an automatically deployable firewall configuration.
- `scripts/zero-trust/validate_policy.py` validates the policy **offline**.
- GitHub Actions should run tests with `contents: read`, no secrets, no self-hosted runners and no access to private VMnet8.
- Enforce change review by a real person before any firewall or IdM modification.
- Optional future SOAR/ZTNA requires separate signed off architecture, least privilege, incident escalation and independent testing.

## Monitoring plan (example cadence, not a mandatory DoD schedule)

- Daily during exercises: endpoint log ingestion, authentication errors, TLS failures, Splunk process health.
- Weekly: review exceptions, open firewalld rules, index roles, patch posture and source gap reports.
- Monthly: review model/policy inventory, vendor versions, open risks, STIG findings, recovery tests and approved overrides.
- On significant change: re-run positive/negative access tests and document any denied legitimate service.

**Status:** Monitoring instructions, not evidence of continuous operational monitoring.
