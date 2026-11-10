# MITRE ATT&CK threat-hunting workstream

This workstream translates adversary behaviors into hypotheses, telemetry
requirements, investigation pivots, and explicit coverage gaps for the existing
three-VM Splunk lab. It is aligned with endpoint, identity, network, cloud, and
DFIR responsibilities without claiming that all of those sources are deployed.

**Status:** Source-controlled examples only. No hunt, detection, incident, EDR
integration, or cloud-log collection is claimed as observed or validated.

## Start here

1. Read the [technique and telemetry mapping](coverage.md), including the
   difference between candidates, context-only signals, and gaps.
2. Read the [hypothesis-driven hunt playbook](hunt-playbook.md) and
   [role-alignment crosswalk](role-alignment.md).
3. Check source health and choose one search from
   [hunts/mitre-attack](../../hunts/mitre-attack/README.md).
4. Perform only authorized, isolated lab tests; compare expected and actual
   results, and document false positives and missing data.
5. Record a sanitized observation in
   [MITRE hunt validation](../../evidence/sanitized/mitre-attack-validation.md)
   and use the [hunt report template](../reference/hunt-report-template.md).

## Visualize the mapping

Download [navigator-layer.json](navigator-layer.json), then open the official
[ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/) and choose
**Open Existing Layer > Upload from local**. A locally hosted Navigator is also
an option. The file contains only public example descriptions, not hunt results.
Its amber, blue, and gray colors mean candidate, context only, and gap; **none
means a verified detection**. Uncolored techniques are unassessed.

The mapping was checked on 2026-11-05 against
[MITRE ATT&CK Enterprise STIX v20.1](https://github.com/mitre-attack/attack-stix-data/blob/master/enterprise-attack/enterprise-attack-20.1.json).
The Navigator layer identifies the compatible major version `20`; the exact
reviewed STIX release and checksum are recorded in [coverage.md](coverage.md).
Review the mapping when the framework, telemetry, or hunts change.

## What this does not add

The repository does not deploy an EDR/XDR platform, ingest IdM logs, join the
Windows VM to a domain, collect cloud audit logs, or widen the hunter role.
The optional KQL example requires separately authorized Defender XDR telemetry.
No automatic response, alert activation, or changes to live systems are performed.
