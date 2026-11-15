# Check the evidence before promising a hunt

Use this checklist before a customer or lab investigation. It turns “we have logs” into a reviewable answer about **which records exist, who owns them, and what period they cover**. This public file is a blank planning aid. Keep completed answers, customer system names, sample events, access details, and retention settings in an approved private case location.

## 1. Agree on the question and access

| Decision | Private answer |
| --- | --- |
| One security question to investigate | Pending |
| Decision maker and source owners | Pending |
| Approved systems, accounts, and UTC window | Pending |
| Excluded systems and records | Pending |
| Permitted read-only search or harmless test | Pending |
| Evidence storage, sharing, and deletion rules | Pending |

Do not expand the search or run a test without the authorized owner's approval. A missing record can mean that collection, access, or retention was incomplete; it does not mean nothing happened.

## 2. Check each possible source

The **repository status** column describes source files, not a live customer's coverage. Mark actual availability only after a permitted source-health check. Leave irrelevant sources out of the case instead of implying that all are required.

| Possible source | Repository status | Private readiness checks |
| --- | --- | --- |
| RHEL local syslog → `linux` | [Local file route and two harmless markers](SYSLOG_HUNTING_GUIDE.md) are documented. | Confirm installed rule, recent marker, file input, host, event time, and search retention. |
| Windows Security → `win_security` | Forwarder and hunt examples are documented; delivery needs separate observation. | Confirm event IDs needed for the question, host/account fields, recent events, and indexing delay. |
| Windows System → `win_system` | A core index, with collection instructions in the lab. | Confirm provider and event ID together; one event number can have different meanings. |
| Sysmon → `sysmon` | Example configuration and process/network searches exist. | Confirm which event types are enabled, process identity fields, exclusions, and last event time. |
| PowerShell → `powershell` | Script-logging examples and hunts exist. | Confirm permitted logging, event contents, encoding, time coverage, and privacy handling. |
| Lab markers → `lab` | Core index for lab checks. | Confirm a marker's purpose; a delivered marker proves a path, not threat detection. |
| IdM server authentication | No validated IdM log stream into the six indexes. | Ask the identity owner whether separate records are available, accessible, and in scope. |
| Zeek, Wireshark, Suricata, Arkime | Optional network tools and synthetic capture guidance. | Verify sensor placement, packet visibility, capture period, packet loss, and permission. |
| AWS CloudTrail | [Worked cloud examples](AWS_ACCOUNT_CREATION_HUNT.md) are read-only plans; no Splunk feed is configured here. | Confirm account and Region coverage, event type, owner, retention, and approved console access. |
| Microsoft Entra sign-in/audit | [Worked sign-in example](AZURE_ENTRA_SIGN_IN_HUNT.md) is a read-only plan; no Splunk feed is configured here. | Confirm tenant, log type, role, retention, time zone, and export permission. |
| Trellix product records | The presentation is educational; no Trellix product is validated in this lab. | Verify actual product, license, version, supported platform, integration, owner, and data fields. |

For each source selected, privately record **owner, last observed event, earliest available event, retention, access role, expected fields, collection gap, and how time zones are handled**. Verify a small original event before relying on a dashboard or parsed field. The [tools and cloud overview](../reference/tools-and-cloud.md) explains what each tool can contribute; the [hunt plan](templates/threat-hunt-plan.md) records the approved scope.

## 3. Decide whether the hunt can answer the question

- **Ready:** The approved source covers the time and system, required fields are present, and a benign comparison is available. Record the check and proceed with a scoped search.
- **Limited:** Some clues exist, but a source, field, time period, or owner confirmation is missing. Narrow the question and state the limit in the [hunt report](templates/threat-hunt-report.md).
- **Not ready:** The needed records cannot be found or accessed. Report a visibility gap and ask the owner to decide whether collection should be improved; do not claim a negative hunt result.

**Plain-language update:** “We can review the records that are available for this period. We will also tell you where the records are incomplete, so a missing clue is not mistaken for proof that nothing happened.”
