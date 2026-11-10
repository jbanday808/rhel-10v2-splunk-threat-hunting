# Security Operations, Incident Management and Consultant Deliverables

This optional workstream adds repeatable processes for handling threats and vulnerabilities, planning hunts, briefing stakeholders, writing reports, and reviewing forensic evidence with AI assistance. It builds on the existing Splunk, Sysmon, network-analysis and STIG material.

**Status:** proposed procedures and synthetic exercises. They are not an approved organizational incident-response plan, a deployment of Trellix products, or evidence that a customer engagement occurred. The existing lab has no validated Trellix deployment. Obtain the system owner's adoption of roles, response authority, reporting channels and retention rules before operational use. Use only synthetic examples in this public repository.

## Start here

| Task | Procedure | Reusable record |
| --- | --- | --- |
| Handle a suspected incident | [Incident management](INCIDENT_MANAGEMENT.md) | [Incident record](templates/incident-record.md) |
| Manage a vulnerability or misconfiguration | [Vulnerability workflow](VULNERABILITY_MANAGEMENT.md) | [Vulnerability record](templates/vulnerability-record.md) |
| Design and execute a hunt | [Threat-hunting method](THREAT_HUNTING_METHOD.md) | [Detailed plan](templates/threat-hunt-plan.md) |
| Brief leaders and technical teams | [Hunt and stakeholder briefing](templates/hunt-briefing.md) | Six-slide briefing outline and decision log |
| Document investigation results | [Detailed hunt report](templates/threat-hunt-report.md) | Evidence-linked findings, limitations and follow-up |
| Review forensic findings with AI | [AI-assisted forensics](AI_ASSISTED_FORENSICS.md) | [Forensic review record](templates/forensic-review.md) |
| Deliver an engagement and handover | [Engagement workflow](ENGAGEMENT_DELIVERY.md) | [Closeout report](templates/engagement-closeout.md) |
| Practice all workflows | [Synthetic tabletop](TABLETOP_EXERCISE.md) | [Validation template](../../evidence/sanitized/security-operations-validation.md) |

Copy a template into approved private case storage before filling it in. Do not put customer names, accounts, endpoint exports, raw packet captures, passwords, CUI or classified information in this repository. The AI demonstration accepts explicitly labeled synthetic cases only; labels are not a substitute for a human data-release review.

## Relationship to the existing lab

- [Cobalt Strike–associated pipe hunt](../../hunts/cobalt-strike/COBALT_STRIKE_ATOMIC_VALIDATION.md): Validate a named-pipe hypothesis with an upstream Atomic test and separate matching/nonmatching controls. Do not attribute a pipe hit to a tool or a PenTest team without corroboration.
- [Worked passive HTTP case](../network-defense/OFFLINE_HTTP_WALKTHROUGH.md): Compare the baseline and candidate, review packet evidence and correlate synthetic Zeek/Suricata/Splunk data.
- [Arkime playbook](../arkime/HUNTING_PLAYBOOK.md): Establish network baselines and investigate protocol and traffic candidates within actual visibility limits.
- [Windows 11 STIG guidance](../stig-windows11/IMPLEMENTATION_GUIDE.md) and [Defender Firewall STIG guidance](../stig-windows-firewall/IMPLEMENTATION_GUIDE.md): Feed verified applicability and remediation results into the vulnerability process.
- [Existing short hunt report](../reference/hunt-report-template.md): Use for a compact lab record; use the detailed template here for an engagement report.

The six existing Splunk indexes and three core VM roles remain the lab baseline. Optional sensors, licensed Trellix products, cloud AI services, SOAR actions and customer integrations require separate design and validation.

## Capability-to-deliverable map

| Capability | Reviewable evidence in this workstream |
| --- | --- |
| Organizational incident management | Case states, decision authority, severity, communication, escalation and closure criteria |
| Threat and vulnerability analysis | Linked incident/finding records, passive validation, prioritized remediation and retesting |
| Detailed hunting plans and reports | Hypotheses, scope, baseline, telemetry, searches, controls, briefings and end-of-engagement reports |
| Forensic analysis | Evidence register, UTC timeline, chain-of-custody records and reviewed conclusions |
| AI-assisted investigation | Synthetic review packet, referenced response format, structural validation and mandatory human review |
| Product consulting | Product-specific questions, change/rollback and knowledge-transfer planning in the engagement workflow |
| Professional-services delivery | Scope, acceptance criteria, effort/cost tracking, risks, training, handover and billing reconciliation |

## References

- [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final): Current incident-response guidance integrated with CSF 2.0 risk management.
- [NIST SP 800-86](https://csrc.nist.gov/pubs/sp/800/86/final): Forensic techniques within incident response; use alongside current tools and approved collection procedures.
- [NIST AI 600-1](https://doi.org/10.6028/NIST.AI.600-1): Generative AI risk considerations, including unreliable output and data exposure.
- [Trellix product portfolio](https://www.trellix.com/products/): Vendor descriptions; verify actual entitlement, platform and version support.
