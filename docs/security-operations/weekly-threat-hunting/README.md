# Weekly APT Threat Hunting and Incident Response Guides

Use these guides to turn verified public APT reporting into bounded hunts, coordinated incident response and testable mitigation/prevention work for the RHEL and Splunk lab. The content is educational and proposed; it does not establish that an attack occurred in the lab or that optional integrations are installed.

## Start here

| Need | Guide |
| --- | --- |
| Read the latest edition | [November 11 2026 initial edition](2026-11-11.md) |
| Follow the complete six-phase response | [APT incident response playbook](../APT_INCIDENT_RESPONSE_PLAYBOOK.md) |
| Run bounded candidate searches and harmless controls | [Hunt queries and validation](HUNT_QUERIES.md) |
| Assign real people and contact paths privately | [Empty private contact roster example](../../reference/incident-response-contact-roster.md.example) |
| Use the existing incident/hunt reporting process | [Security operations](../README.md) |

## Schedule and publication

An active Codex schedule starts preparation **every Friday at 5:00 AM Hawaii Standard Time**, using `Pacific/Honolulu` (UTC-10). The first scheduled start is **November 13, 2026 at 05:00 HST / 15:00 UTC**. Research, verification and publication take place after the scheduled start; 05:00 is not a guaranteed completion time. The November 11 edition is an initial publication, not a completed scheduled Friday run.

The recurring task researches primary reporting from the preceding seven days, distinguishes report dates from attack dates and state-linked activity from cybercrime, and labels older context. It publishes a dated edition here and updates the latest link and archive. Repeated runs for one HST date reconcile the existing edition. Scheduling is managed in Codex, rather than by a repository GitHub Actions publishing workflow. Execution depends on the scheduled task's available tools and connected GitHub access; a blocked publication is reported instead of claimed complete.

Every edition includes prioritized intelligence, lab applicability, telemetry prerequisites, bounded searches and controls, roles/authority, severity and acknowledgment fallback, zero-day/critical-incident contacts, and detailed steps for Detection; Detection and Analysis (Identification); Containment; Eradication; Recovery; and Post-Incident Activity (Lessons Learned). Immediate mitigations, durable prevention, verification and rollback considerations are part of every edition.

Real incidents escalate immediately through the organization's approved private contacts. A weekly documentation task neither monitors the live environment continuously nor replaces on-call incident response. Do not publish real incidents, names, internal contact details, raw evidence, secrets or undisclosed exploit details here.

## Edition archive

| HST edition date | Scope |
| --- | --- |
| [2026-11-11](2026-11-11.md) | Initial edition: recent state-linked investigations, current Linux persistence/exposed-secret reporting, six-phase response, escalation, mitigations and prevention |

## Publication checks

Read the current repository instructions and [sanitization checklist](../../reference/security-and-sanitization.md). Preserve the core VM roles and six indexes. Run source validation, the existing test suite and publication preflight before completing publication. If a local operating-system limitation prevents a required test, use an appropriate supported test environment and retain the result; do not silently suppress the test or claim it passed.

Read back the committed edition and navigation after publication. Record live hunt or response results only after they actually occur and only in approved private storage. A query example or green source check is not evidence of live detection coverage.
