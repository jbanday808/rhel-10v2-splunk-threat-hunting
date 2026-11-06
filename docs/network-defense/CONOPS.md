# Concept of Operations (CONOPS) — Passive Network Security Analytics

**Status:** Draft exercise plan, not an approved operational CONOPS.

## Mission and boundaries

Demonstrate **passive vulnerability analysis**, network baselining, detection engineering and evidence-based investigation within an owned VMware learning lab. No scanning or sensing is authorized beyond explicitly owned synthetic traffic and reviewed capture sources. Do not monitor classified/CUI networks or import protected data.

## Roles and responsibilities

These are proposed functional roles for the authorized lab, not evidence of
staffing, an operational security program, or an Endpoint Security Solution
(ESS) deployment. One person may perform multiple roles where approved
separation-of-duties requirements permit. All activities remain within the
mission and passive-monitoring boundaries above.

| Role | Responsibility |
| --- | --- |
| Lab system owner | Approves VM, capture point, data types, retention and change windows |
| Network engineer | Verifies packets really reach sensor; documents drops, interface and SPAN/TAP dependencies |
| Senior Cybersecurity Analyst | Correlates authorized network, endpoint and identity evidence; validates vulnerability hypotheses with system owners; assesses severity and confidence; reviews detection quality and mentors analysts |
| Threat Hunter | Develops MITRE ATT&CK-aligned hypotheses; establishes baselines and investigates deviations across authorized data; documents benign alternatives, evidence and visibility gaps; hands findings to the SOC and incident owner |
| Senior SOC Analyst | Coordinates assigned shift triage and case prioritization; reviews alert dispositions and evidence timelines; supports analyst handoffs and escalates suspected incidents through approved channels |
| Detection analyst | Validates protocol events, hunts, Suricata rule matches and alert quality |
| Splunk administrator | Creates and maintains approved indexes; manages TLS/forwarder settings, role-based access and retention; reviews parsing and monitors ingestion and search health under authorized change control |
| ESS Administrator | Where ESS is separately deployed and authorized, manages endpoint agents, policies, signatures and telemetry; checks agent health and coordinates findings and proposed endpoint response with the incident owner |
| System Administrator | Maintains authorized RHEL, Windows and IdM systems, accounts, logging, patching and backups; validates host evidence with analysts and implements approved changes and recovery procedures |
| System Engineer | Designs and documents the lab architecture, telemetry flows and optional passive sensor dependencies; coordinates integration, security controls, performance checks and change/rollback plans with system owners and the ISSE |
| ISSO (Information System Security Officer) | Maintains system security documentation, access-review and control evidence, vulnerability records, and plans of action and milestones (POA&Ms); coordinates remediation and reporting with the ISSM and system owner |
| ISSM (Information System Security Manager) | Oversees security governance, incident reporting and corrective-action tracking; reviews risks and coordinates security decisions with the system owner, ISSO and designated authorizing official |
| ISSE (Information System Security Engineer) | Translates security requirements into architecture and control designs; evaluates design risks, recommends secure integrations and validation activities, and advises the ISSO and ISSM |
| Security/compliance reviewer | Reviews CONOPS, risk/800-171 evidence mapping and data protection |
| Incident owner | Confirms anomalies, exposure and root cause with analysts and system owners; authorizes notifications and response where delegated and coordinates with the organization's designated authorities |

Analysts route suspected findings to the Senior SOC Analyst and incident owner;
administrators verify affected systems and make only approved changes. Formal
system authorization and risk acceptance remain with the designated
authorizing official or a formally delegated authority. These role descriptions
do not authorize independent active scanning, inline blocking or automatic
containment.

## Approved workflow

1. Review scope, system inventory and expected protocol/service map.
2. Collect **synthetic offline PCAPs** first; record SHA-256, source, UTC capture period, test case ID and authorization.
3. Decode with TShark/Wireshark, Zeek, Suricata; compare protocol output and known ground truth.
4. Establish baseline by `src/dst/service/protocol/day`. Suggested initial window **7 days** in a live authorized environment; this is not a formal requirement.
5. Review anomalies manually (new DNS patterns, outlier flows, old TLS version, unexpected cleartext, abnormal Suricata alerts).
6. Validate the source data, affected systems and false-positive candidates with the system administrator; never call a network-only inference a confirmed host vulnerability.
7. Escalate confirmed findings through approved incident/vulnerability channels. Keep adversary traffic simulations benign and isolated.
8. Record countermeasures, change approvals, repeat tests and closeout evidence.

## Measures of performance (MOPs) and measures of effectiveness (MOEs)

| Measure | Description | Evidence | Target |
| --- | --- | --- | --- |
| Packet coverage | Authorized flows visible vs expected synthetic flows | PCAP count + ground truth | Owner-defined; Pending |
| Packet drop rate | Lost packets at capture and sensor | Interface/capture counters | Owner-defined; Pending |
| Parsing coverage | Events decoded into Zeek/Suricata metadata | Raw PCAP vs generated logs | Owner-defined; Pending |
| Ingestion latency | Event timestamp to Splunk index arrival | Source log and Splunk metadata | Owner-defined; Pending |
| Detection precision | Validated true alerts / reviewed alerts | Human review with ground truth | Owner-defined; Pending |
| False-positive trend | Benign cases incorrectly alerted | Rule QA notes | Owner-defined; Pending |
| Investigation turnaround | Time to triage and report verified anomaly | Case timeline | Owner-defined; Pending |
| Service availability | Splunk/IdM/Windows services unaffected by sensor | Service baseline & regression | No unapproved outage |

Targets must be agreed with actual lab owners; **do not fabricate performance results**.

## Data protection

- Keep raw PCAPs, full DNS questions, URLs, credentials, SMB content, endpoint binaries and case notes outside public GitHub.
- Public examples use RFC 5737 documentation IPs and `example.test`, never actual CUI or protected identities.
- Prefer metadata (source/destination, TLS certificate attributes, timing, alert signature), with approved field minimization before forwarding.
- Document access control, encryption, time synchronization, retention and disposal.
- Keep sensors read-only/non-inline and prohibit independent active scan, exploitation or automatic containment from alerts.
- Publish only sanitized totals and reproducible synthetic examples after reviewer approval.

## Escalation severity (illustrative only)

**High:** Confirmed data exfiltration indicators or highly credible active exploitation with direct validated corroboration.  
**Medium:** Repeated or correlated suspicious activity needing owner confirmation.  
**Low:** Unexplained outlier with benign explanations or missing context.  
**Informational:** New service/protocol observation during baseline.

No automatic notification is claimed. Use existing organizational reporting requirements and contacts when applicable.
