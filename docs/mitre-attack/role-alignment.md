# Threat-hunter role alignment

This crosswalk relates the requested threat-hunting responsibilities to project
artifacts and identifies what would require additional platforms or real
experience. It is not a claim that the lab has been deployed or that any
individual has particular years of experience or certifications.

| Responsibility | Project artifact | Boundary / next step |
| --- | --- | --- |
| Build proactive hypotheses from intelligence, incidents, and visibility gaps | [Hunt playbook, sections 1-3](hunt-playbook.md) and [ATT&CK mapping](coverage.md) | Choose and cite the actual intelligence or incident; the example is not an attributed intrusion. |
| Map behaviors to tactics, techniques, telemetry, findings, and gaps | [Coverage table](coverage.md) and [Navigator layer](navigator-layer.json) | Candidates and context require real evidence; gaps and unassessed techniques are not coverage. |
| Analyze process lineage, script execution, tasks, registry, and account activity | [Endpoint and identity searches](../../hunts/mitre-attack/README.md) | Fields, event collection, and the narrowly filtered Sysmon rules must be verified. |
| Investigate authentication anomalies and privilege changes | [Failures before success](../../hunts/mitre-attack/02-failures-before-success.spl), [multi-account failures](../../hunts/mitre-attack/07-multiple-account-failures.spl), and [account/group correlation](../../hunts/mitre-attack/03-account-to-group.spl) | Thresholds are illustrative; failed logons alone do not prove credential abuse. |
| Pivot across endpoints, networks, identity, and time | [Process/network](../../hunts/mitre-attack/01-process-network.spl), [DNS](../../hunts/mitre-attack/08-powershell-dns-context.spl), [SSH](../../hunts/mitre-attack/09-linux-ssh-context.spl), and [timeline](../../hunts/mitre-attack/11-investigation-timeline.spl) | The lab has one Windows endpoint, limited network events, and no ingested IdM log stream; a timeline does not establish causality. |
| Work across SIEM and EDR/XDR query languages | SPL hunts and [optional Defender XDR KQL](../../hunts/mitre-attack/optional-defender-powershell-network.kql) | Defender is not deployed by this lab. CrowdStrike, SentinelOne, Cortex XDR, and other products require separately authorized integrations, schemas, and tested queries. |
| Baseline activity and find uncommon patterns | [Rare parent/child](../../hunts/mitre-attack/10-rare-parent-child.spl) and [baseline guidance](hunt-playbook.md#2-establish-telemetry-and-a-baseline) | A seven-day, one-host lab sample and an illustrative threshold are not an enterprise baseline. |
| Investigate cloud and identity-based activity | [Prioritized cloud and identity gaps](coverage.md#prioritized-gaps-from-the-threat-hunter-role) | Azure OIDC example workflows are not cloud audit collection; IdM logs are not automatically ingested. |
| Reconstruct timelines, preserve evidence, and escalate to IR | [Timeline](../../hunts/mitre-attack/11-investigation-timeline.spl), [DFIR handoff](hunt-playbook.md#5-document-escalate-and-improve), and [report template](../reference/hunt-report-template.md) | Follow the organization's actual chain-of-custody, authority, legal, and escalation procedures. |
| Turn findings into improved detection opportunities | [Query validation and promotion](hunt-playbook.md#4-validate-the-query-not-just-its-appearance) and [validation record](../../evidence/sanitized/mitre-attack-validation.md) | No alert is automatically enabled or response action taken. Tune, test, approve, and assign an owner first. |
