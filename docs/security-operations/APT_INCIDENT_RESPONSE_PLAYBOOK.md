# APT Threat Hunting and Incident Response Playbook

Use this playbook to investigate suspected advanced persistent threat activity, coordinate the people needed to respond, remove the attacker's access, and restore trusted service. Begin with the current [weekly intelligence and hunts](weekly-threat-hunting/README.md). The six phases below follow the requested operational sequence; investigation, containment, and evidence collection can overlap when delay would increase harm.

**Adoption status:** proposed procedures for this educational lab. The organization must assign decision authority, approve response targets, and maintain a private on-call roster before operational use. These procedures do not grant authority to isolate systems, change accounts, notify third parties, or disclose a vulnerability. Existing delegated emergency authority can permit immediate action; record the authority used.

[NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) integrates incident response with CSF 2.0 risk management. The six phase names here are this repository's working arrangement, not a claim that NIST prescribes this exact sequence or the proposed response times. Keep preparation and prevention active throughout the lifecycle.

## First actions for a critical incident

1. **Protect people and essential services.** Notify the safety/operations lead immediately if a cyber event could affect physical safety. Follow the established emergency path; safety takes priority over evidence acquisition.
2. **Open a private incident record and page the SOC lead and incident commander.** Record discovery time in UTC, reporter, affected service, observed behavior, and the strongest evidence reference. Use the escalation table below without waiting for attribution or a CVE.
3. **Use a trusted communication channel.** If corporate identity, email, or collaboration services may be compromised, switch to the prearranged independent bridge and independently verify participants.
4. **Stop ongoing harm within delegated authority.** Request or execute narrowly scoped isolation, account/session restriction, or service withdrawal as the approved runbook permits. Confirm the actual effect and preserve management/recovery access.
5. **Preserve the evidence that can be collected safely.** Assign a forensic owner. Avoid rebooting, wiping, deleting logs, running untrusted samples, or making broad configuration changes before an acquisition decision. Do not delay urgent containment for a long export.
6. **Give the next update time.** State known impact, unknown scope, actions and owners, decisions needed, and the next checkpoint. Notify leadership and legal/privacy in parallel for P1 events.

## People, roles, and responsibilities

Use named primary and backup people in approved private storage. A small lab may combine roles, but record both the executor and the person accountable for consequential decisions.

| Role or person to assign | Responsibilities | Authority and required handoff |
| --- | --- | --- |
| Reporter / help desk | Receive reports, capture contact and discovery time, preserve the original report, warn against further interaction with suspicious content | Route urgent reports to the duty SOC; do not forward malware broadly or investigate beyond assigned scope |
| SOC analyst, Tier 1 | Validate signal and telemetry, open case, assess initial severity, preserve query and event references | Page Tier 2/SOC lead when the signal is credible, scope is unclear, or a trigger below is met |
| Threat hunter / SOC Tier 2 | Test hypotheses, correlate hosts/identities/network activity, scope exposure and compromise, assess alternatives | Recommend declaration and containment; transfer evidence and confidence to the incident commander |
| Incident commander / IR lead | Own incident declaration, objectives, priorities, workstream assignments, decisions, update cadence, and phase transitions | Direct response under delegated policy; escalate mission impact and decisions outside authority to the CISO/system owner |
| Forensic lead / evidence custodian | Plan volatile and persistent acquisition, preserve originals, hash evidence, maintain custody and UTC timeline | Approve collection methods and document unavoidable evidence changes; hand evidence to authorized investigators |
| Threat intelligence analyst | Verify reports, affected versions, actor assessments, exploit status, indicators and ATT&CK mappings | Separate vendor observations from local findings; coordinate sensitive intelligence through the IR lead |
| Splunk / detection engineer | Confirm ingestion, timestamps, parsing, permissions and retention; preserve searches; improve and test detection logic | Change searches/collection only through approved change control; do not claim a query proves coverage |
| RHEL / application administrator | Assess packages, services, persistence and application state; execute approved isolation, rebuild and patch actions | Preserve current state and rollback evidence; prove effective remediation and service health |
| Windows / endpoint administrator | Collect authorized endpoint artifacts, isolate with approved tools, remediate persistence and rebuild endpoints | Verify the intended device and isolation effect; preserve EDR/management access and document results |
| Identity / IdM / cloud administrator | Scope privileged identity exposure, revoke sessions/credentials where supported, remove unauthorized trust and grants | Coordinate service-account dependencies and recovery identities; verify restriction instead of assuming reset equals revocation |
| Network / firewall administrator | Apply precise segmentation, DNS, proxy and egress controls; preserve connection evidence | Validate allowed management and business paths; record rule scope, expiry, owner and rollback |
| Vulnerability / PSIRT liaison | Confirm product applicability, open vendor security/support cases, track workarounds and fixed versions | Route suspected novel vulnerabilities privately; keep a vulnerability record linked to the incident |
| System / service owner and recovery lead | Identify business impact, dependencies, RTO/RPO, restoration order and acceptance criteria | Authorize service withdrawal/restoration under policy; accept operational residual risk within delegated authority |
| CISO / security duty manager | Resolve cross-team priorities, approve security decisions outside IR delegation, brief executives | Escalate material business risk and resources; do not substitute for the designated legal reporting authority |
| Legal counsel / privacy officer / compliance lead | Determine applicable reporting duties, contracts, legal holds, evidence release, privacy impact and disclosure approvals | Own the notification decision, applicable clock, recipients and retained proof of delivery |
| Executive / business continuity / communications lead | Approve major business decisions, customer messaging and continuity plans; manage external statements | Publish only approved facts; use one authorized spokesperson |
| ISSO / ISSM / authorizing official, if applicable | Route government security reporting, mission risk and formal risk acceptance | Follow the actual agency/contract chain; do not publish CUI, classified information or operational details here |
| External DFIR, vendor PSIRT, provider, insurer, law enforcement | Supply specialist assistance, product fixes, provider-side evidence or investigation support | Engage through the designated organizational liaison; preserve scope, confidentiality and evidence-transfer records |

The incident commander is accountable for coordination. The system owner is accountable for service acceptance; legal/privacy owns applicable notification decisions; each technical lead is responsible for the actions assigned to that workstream. The [private contact roster example](../reference/incident-response-contact-roster.md.example) records primary and backup contacts without exposing them in GitHub.

## Severity and when to escalate

**Proposed internal targets pending adoption:** clocks start when a credible signal is received; retain that timestamp when severity changes. These are planning targets, not regulatory deadlines, NIST requirements, or claims of existing staffing. Escalate immediately when evidence meets a higher tier; do not wait for a weekly report or conclusive actor attribution.

| Severity | Trigger and examples | Who to contact and when | Proposed updates |
| --- | --- | --- | --- |
| P1 Critical | Active exfiltration, destructive activity, major outage, safety risk, compromise of privileged identity/IdM/Splunk/backup trust, uncontrolled spread, or credible suspected zero-day exploitation on a critical or exposed service | Page SOC lead and incident commander immediately. Target acknowledgment within 5 minutes; engage CISO, service owner, forensic lead, relevant administrators and legal/privacy within 15 minutes. Engage executives/continuity and external specialists as impact requires | Every 30 minutes and after material changes, or the IC's shorter cadence |
| P2 High | Corroborated compromise on a bounded endpoint; high-impact persistence without observed spread; critical unpatched exposure without evidence of exploitation | Page SOC lead/IR lead; target acknowledgment within 15 minutes and coordinated assessment within 1 hour. Notify service owner and the technical/forensic leads; involve legal/privacy if sensitive data may be involved | Every 2 hours until risk and scope stabilize |
| P3 Moderate | Suspicious behavior with limited apparent impact, uncertain cause, or a material visibility gap | Assign Tier 2 and an owner; target acknowledgment within 4 hours and a documented next action within one business day | At agreed checkpoints and when new evidence changes severity |
| P4 Low / informational | Verified benign exercise, minor anomaly or routine improvement | Record evidence and route to the responsible backlog owner; proposed review within two business days | At disposition or the next routine review |

**Acknowledgment fallback:** for a P1, page primary and backup SOC/IR contacts at discovery. If no acknowledgment by 5 minutes, call the security duty manager using the independent roster. If none by 10 minutes, call the CISO/delegate and the service owner's duty manager. By 15 minutes invoke the executive/continuity duty path if coordination is still absent. Continue preauthorized emergency actions and safety notifications in parallel. A sent page or reassigned ticket is not an accepted handoff. For other tiers, use the roster's tier-specific fallback and escalate earlier if harm increases.

Promote severity when a new privileged identity, network segment, tenant, sensitive data class, or essential service is affected; when containment fails; when evidence is being destroyed; or when telemetry loss prevents ruling out ongoing harm. The incident commander documents any downgrade, supporting evidence, residual uncertainty and accepting owner.

## Who to contact for a suspected zero-day or highly critical incident

An unusual alert, missing signature or unknown file is not proof of a zero-day. Record the issue as **suspected novel exploitation** until product/security specialists assess it. A previously disclosed CVE can be actively exploited and critical without being a current zero-day.

1. **Immediately:** contact the duty SOC lead/incident commander. Provide case ID, discovery time, affected product/build and exposure, observed behavior, business impact, exploitation evidence, and containment state. Treat credible ongoing exploitation of a critical service as provisional P1.
2. **In parallel:** contact the forensic lead, product owner, vulnerability/PSIRT liaison and relevant network/identity administrators. The CISO and legal/privacy join the P1 path. Preserve representative artifacts privately before cleanup when feasible.
3. **Promptly through the liaison:** open an urgent product support case for response help and a private PSIRT report for the suspected vulnerability. Supply reproducible observations only within authorized testing scope; use the vendor's secure upload/encryption procedure. Do not publish exploit details in GitHub issues or this guide.
4. **If broader coordination is needed:** legal/IR leadership engages CISA, the appropriate national CSIRT, CERT/CC or law enforcement according to impact and jurisdiction. For urgent criminal activity in Hawaii, the verified FBI Honolulu route below supplies a public contact. Legal/contractual clocks can require earlier notification than an internal target.
5. **If the vendor does not acknowledge:** the liaison records attempts and invokes the vendor's published escalation process; the IC chooses exposure reduction or service suspension based on impact. Use CERT/CC for coordination needs, including difficult multi-vendor cases. Do not wait for a CVE assignment to contain credible exploitation.

| Recipient | Use and verified/public route | Organization's owner |
| --- | --- | --- |
| Red Hat Product Security | Suspected vulnerability in a Red Hat product: **secalert@redhat.com**, with the current secure communication instructions on [Security contacts and procedures](https://access.redhat.com/security/team/contact). Use entitled Red Hat Support for operational help and known-vulnerability applicability | Vulnerability liaison + RHEL lead |
| Microsoft Security Response Center | Suspected Microsoft product/service vulnerability: [MSRC reporting](https://www.microsoft.com/en-us/msrc). Open the appropriate customer support/incident case separately for operational response | Vulnerability liaison + Windows/cloud lead |
| Splunk Product Security / Support | Use the customer Support case or disclosure route on [Splunk vulnerability reporting](https://advisory.splunk.com/report); the page lists **splunk_prodsec@cisco.com** as an alternative to its reporting platform | Splunk lead + vulnerability liaison |
| Other affected vendor or service provider | Use the affected product's official PSIRT and urgent support channel, independently verified from its official site. For the featured remote-support exposure, start with [BeyondTrust BT26-05](https://www.beyondtrust.com/trust-center/security-advisories/bt26-05) | Product owner + vendor liaison |
| CISA 24/7 Operations Center | Public reporting route: [CISA report page](https://www.cisa.gov/report). **1-844-SAY-CISA (1-844-729-2472)** is published in [CISA advisory AA25-266A](https://www.cisa.gov/sites/default/files/2025-09/AA25_266A_advisory_cisa_shares_lessons_learned_from_ir_engagement.pdf) | IC/CISO-designated government liaison |
| FBI Honolulu | Suspected intrusion/criminal activity: **(808) 566-4300**, listed as a 24/7 reporting line on the [official Honolulu page](https://www.fbi.gov/contact-us/field-offices/honolulu?mobile-app=true&theme=false) | Legal + designated law-enforcement liaison |
| CERT Coordination Center | Coordinated vulnerability disclosure: [CERT/CC guidance](https://www.kb.cert.org/vuls/guidance/) and its reporting route. Attempt direct vendor contact and retain that history | Vulnerability liaison + legal |
| Regulator, customers, insurer, ISAC, agency chain | Use the organization's private register of applicable obligations, policies, contracts and contacts; preserve acknowledgment and reporting receipts | Legal/privacy, compliance and authorized leadership |

Public routes were researched on November 11, 2026 HST. CISA's live reporting pages returned HTTP 403 during preparation; its number above is supported by the cited published advisory rather than a completed live-page check. Reconfirm public routes from official sources during preparation and before disclosure. Keep personal contacts, internal numbers, bridge links, case data and receipts private. No messages are sent by publishing this documentation.

## Prerequisites and preparation

1. Assign the roster, emergency authority, independent bridge, evidence custodian, severity targets and external liaison. Exercise a primary-contact failure before relying on the escalation ladder.
2. Inventory critical assets, dependencies, owners, internet exposure, privileged identities, service accounts, backups, and recovery objectives. Include previously connected/dormant third-party applications.
3. Confirm authorized access to endpoint, Splunk, identity, firewall, application and backup consoles from a trusted response workstation. Keep recovery credentials in an approved independent vault.
4. Verify clock synchronization, actual log retention, ingestion delay, field parsing and tested alerts. Prepare approved evidence tools, immutable private storage, hashing and custody forms.
5. Test clean backups and rebuild procedures in an isolated environment. Establish an emergency patch/rollback path and a way to withdraw an exposed service safely.
6. Document visibility limits. The core lab has RHEL-SPLUNK01, WINHUNT01 and RHEL-IDM01 and indexes `win_security`, `win_system`, `powershell`, `sysmon`, `linux`, `lab`. The shipped Linux input monitors a lab log file; it does not establish full auditd/process coverage. Optional EDR, network sensors, appliance and cloud telemetry require separate validation.

## 1 Detection

**Owner:** duty SOC analyst, supported by the hunter and detection engineer. **Start:** an alert, user report, hunt candidate, vendor notification or unexplained service change.

1. Register a private case using the [incident record](templates/incident-record.md). Capture discovery and event times separately, timezone, reporter, source, affected service and initial confidence.
2. Preserve the original report/alert reference, search text/version, time bounds, job ID, source event IDs and any tool warnings. Preserve evidence in approved private storage; a copied chart is not a substitute for underlying events.
3. Confirm the intended system and source. Check hostname aliases, clock offset, event/ingestion timestamps, permissions, retention and extraction. Consult [hunt queries and visibility checks](weekly-threat-hunting/HUNT_QUERIES.md).
4. Compare the behavior to the weekly hypothesis and the asset's role. A tool name, command string, indicator or ATT&CK tag is a lead requiring context.
5. Check approved changes, maintenance, software deployment and authorized exercises with their owner. Preserve the result of that verification; do not suppress the signal based on an unsupported assumption.
6. Correlate one additional independent source where available: process creation with task registration; application access with host activity; identity authentication with a privilege change; or process execution with outbound traffic.
7. Assign provisional severity using observed business impact, privilege, spread, data exposure and uncertainty. Page immediately if P1 criteria are credible; collection and escalation proceed together.
8. If the signal is explained, record the supporting evidence and benign disposition. If coverage is missing, create a visibility task and an owner rather than claiming the host is clean.

**Exit:** a reproducible signal and owner, or an evidence-supported benign disposition. Every unresolved candidate has a severity, next action and review time.

## 2 Detection and Analysis Identification

**Owner:** incident commander with hunter/Tier 2 and forensic lead. **Purpose:** determine whether an incident exists, scope its effect and select an effective response.

1. Form at least two explanations: malicious activity and a plausible benign/administrative cause. List observations that would support or weaken each. Keep actor attribution separate from incident confirmation.
2. Build an initial UTC timeline linking source/evidence IDs. Record the original timestamps, clock offsets and uncertainty. Distinguish request, authentication, execution, persistence, access and exfiltration; one does not prove the next.
3. Inventory affected and potentially affected assets, users, service accounts, tokens, applications, tenants, network paths and data stores. Trace the permissions and secrets accessible to the compromised principal.
4. Extend the initial seven-day hunt to the plausible earliest compromise time within available retention. A campaign older than seven days needs an older scope. Record missing intervals; recent quiet activity does not exclude an older foothold.
5. Acquire evidence under the forensic plan: volatile process/network/session information when safe, followed by persistent disk/files/logs/configuration. Use trusted tools and working copies. Decide whether a live acquisition, image, provider export or specialist response is appropriate.
6. Analyze entry point, persistence, privilege changes, lateral movement, collection and possible exfiltration. Pivot on host plus process GUID, unique event/correlation IDs and identity object IDs; IPs or reused PIDs alone can mislead.
7. Check the exact product/build and exposure against the vendor advisory. RHEL backports and patched appliances require vendor evidence of effective fixes, not version-string guesses. Link a separate vulnerability record.
8. Establish the evidence basis for data impact: resource accessed, identity, operation/result and transfer context. Missing audit logs leave uncertainty. Bring legal/privacy in early when sensitive data could be affected.
9. The IC declares or updates the incident, severity, confidence, scope, objectives and next update. Record unknowns and request specialist help for suspected novel exploitation, privileged compromise or missing trust boundaries.
10. Produce a containment proposal with exact targets, dependencies, decision authority, preservation priorities, execution owner, rollback and independent validation. Escalate any action outside delegated authority.

**Exit:** incident decision documented; known/possible scope and gaps recorded; response owners assigned; containment plan accepted or emergency action recorded. Analysis continues during later phases as new evidence arrives.

## Evidence integrity and custody

| Field | Required private record |
| --- | --- |
| Identity | Case ID, unique evidence ID, source system/provider, artifact description and data classification |
| Acquisition | Collector, authorizing authority, UTC start/end, tool/version, method and exact scope |
| Integrity | SHA-256 of the acquired file/export, size, original location, acquisition errors and clock uncertainty |
| Preservation | Access-controlled original, working-copy reference, retention/legal hold, encryption and access log |
| Transfer | Sender/recipient, UTC time, purpose, approved channel and receipt; recheck hash after transfer |
| Interpretation | Facts supported, competing explanation, limitations, analyst and reviewer |

A hash shows whether the acquired artifact changed; it does not prove the source was trustworthy or the collection complete. Memory collection and ordinary live commands change system state; record those effects. Do not upload evidence to public services or an AI tool without approved handling and explicit authorization for that data.

## 3 Containment

**Owner:** IC directs; endpoint, network, identity and service owners execute approved actions. **Priority:** reduce harm while preserving the ability to manage, investigate and recover.

1. Identify the precise host, identity, application, service or route to restrict. Confirm it against current inventory; distinguish a shared gateway, NAT address or cloud application from a single affected endpoint.
2. Choose short-term containment: endpoint isolation, quarantine segment, egress restriction, removal of public reachability, temporary service suspension or account/application restriction. Prefer the smallest scope that effectively interrupts the observed behavior.
3. Record authority, business/safety effect, expected action result, management access, evidence needs, executor, time and rollback. Invoke existing emergency authority if waiting would prolong critical harm.
4. Execute and independently verify. A console action queued, API accepted or ticket completed does not prove the endpoint is isolated. Confirm disallowed paths fail and required response access still works.
5. For identity compromise, coordinate restriction, session/token revocation, credential rotation and application trust changes. Check provider-specific token behavior; already issued tokens may survive a password or secret change until expiry or supported invalidation.
6. For a suspected zero-day without a patch, withdraw or restrict the vulnerable service/feature, narrow management and inbound access, constrain egress and apply vendor-supported workarounds. Validate with safe checks; do not run a public exploit on production.
7. Protect adjacent trust: privileged identities, IdM, Splunk, backup/virtualization administration, secrets and third-party connections. If the control plane is affected, use independent trusted accounts and response infrastructure.
8. Search for related access on other assets and verify the containment holds across restart/failover, alternate network paths, service identities and cloud permissions. Reassess severity if spread or exfiltration continues.
9. Establish longer-term containment: clean administrative path, temporary replacement service, segmented recovery environment and expiring compensating rules. Assign each exception an owner and reassessment time.

**Exit:** observed harmful paths are interrupted and verified; affected assets/identities have containment owners; residual routes and business exceptions are documented. If the test fails, remain in containment, escalate and revise the plan.

## 4 Eradication

**Owner:** technical leads under IC direction; forensic lead preserves the evidence needed before removal.

1. Confirm the scoped entry path and persistence mechanisms as far as evidence allows. Include tasks/services/cron, startup files, web components, authorized keys, IdM privileges, OAuth credentials/grants and third-party access as applicable.
2. Preserve the selected artifacts and configuration before removal. Record what will be lost if an emergency rebuild is necessary.
3. Decide whether trust can be restored through targeted remediation. Prefer rebuilding from verified clean media when root/admin, security tooling, identity infrastructure or the base image may be compromised. Document why the selected path is sufficient.
4. Remove or disable confirmed unauthorized persistence and access through approved tools. Review across all affected identities and systems; deleting one file or stopping one process does not remove redundant footholds.
5. Apply the vendor-supported fix or maintain the tested compensating control. Validate product/build applicability, signatures/source, dependencies, reboot requirements and service compatibility in a representative isolated environment.
6. Rotate exposed credentials and reachable downstream secrets from a trusted system, in dependency order. Remove attacker-added methods, keys, grants, owners and trust relationships. Do not reset sensitive credentials from a compromised endpoint.
7. Address the enabling weakness: excessive privileges, exposed management, insecure update/configuration path, unreviewed application consent, weak egress or missing audit controls. Track unresolved root cause explicitly.
8. Re-run the hunt and targeted forensic checks against every affected asset. Verify fixed configuration, persistence removal and unauthorized access failure; inspect the actual enforcement logs and failures.
9. The forensic/technical leads present evidence to the IC and service owner. Keep containment if trust, entry-path remediation or scope remains materially uncertain. Record exceptions with an authorized risk owner, expiry and recovery restriction.

**Exit:** the chosen trust restoration is evidenced, known footholds and exposed access are addressed, the entry weakness is fixed or controlled, and independent review permits recovery.

## 5 Recovery

**Owner:** recovery lead and system owner; IC coordinates security acceptance.

1. Identify a clean recovery source predating the earliest plausible compromise. Verify backup integrity, provenance and required data point. A recent successful backup may contain persistence.
2. Restore/rebuild in a segmented environment, separate from suspected systems and compromised management infrastructure. Use clean administrative credentials and approved images/packages.
3. Reapply validated security configuration, patches, service identities and least-privilege access. Keep SELinux enforcing and TLS verification enabled; investigate compatibility failures through change control.
4. Verify detection readiness before reconnection: forwarder/agent health, timestamps, expected source events, parsing, retention, approved search execution and alert delivery. Treat each as a separate check.
5. Conduct service and data acceptance tests with the owner: authentication, application functions, integrations, file/database integrity, backup/restore and recovery objectives. Record actual results and errors.
6. Re-test the prior attack path safely. Confirm unauthorized persistence and access remain absent within the observed scope, restricted identities cannot reuse access, and approved business paths work.
7. The service owner and IC approve staged reconnection: one asset/service or limited population, then broader restoration after the defined observation gate. For vendor integrations, follow the current formal restoration guidance as well.
8. Monitor at an owner-approved heightened cadence. A proposed starting plan is continuous alerting plus daily review for seven days, extended for plausible dwell time, criticality and visibility gaps. A fixed quiet period is not proof of eradication.
9. Define rollback/re-isolation triggers in advance: recurring persistence, unexpected privilege changes, suspicious outbound access, integrity failures, missing critical telemetry or failed business tests. Re-enter containment immediately when a trigger is met.
10. Obtain documented service acceptance, residual-risk owner, follow-up actions and monitoring handoff. Preserve the evidence and timeline through closure.

**Exit:** service and security acceptance are evidenced, the accountable owner approves operation, monitoring is owned, and unresolved risk has explicit disposition.

## 6 Post Incident Activity Lessons Learned

**Owner:** IC with all workstream leads; system owner accepts closure and improvement ownership.

1. Hold a proposed initial review within five business days of stabilization, adjusted to organizational policy and investigation needs. Invite the SOC, forensics, administrators, service owner, legal/privacy, communications and affected business representatives.
2. Reconstruct the timeline from discovery through effective containment and restoration. Separate detection time, page time, acknowledgment, action request, actual action effect and acceptance.
3. Compare initial assumptions with the evidence. Explain what allowed entry, delayed recognition, preserved attacker access or made scope uncertain. Record contributing process/tool conditions without blaming reporters.
4. Evaluate mitigations and prevention with evidence: which controls blocked activity, which were missing, what telemetry failed, and whether the primary/backup escalation path worked.
5. Complete the incident report: executive impact, technical findings, confidence, unknowns, affected scope, data-impact assessment, evidence references, decisions, costs/effort and recovery acceptance.
6. Reconcile required notifications, vendor cases, disclosure decisions and receipts with legal/privacy. Record which rule/contract applied and who approved the action; do not assume one regulator's deadline applies to every incident.
7. Create corrective tasks with owner, priority, due date, test/acceptance criteria and rollback where relevant. Include detection tuning, prevention, patching, architecture, backup tests and staff exercises.
8. Measure defined outcomes: time to acknowledgment, validated triage, effective containment and service acceptance; recurrence; missed telemetry; false positives; and overdue tasks. Record small-sample limits.
9. Test the improvements using benign matching and nonmatching controls in an authorized isolated lab. Require actual evidence before changing a detection from a candidate to validated coverage.
10. Close only after the owner accepts the disposition, open tasks have accepted owners, notifications are recorded and retention/legal-hold instructions are set. Schedule a proposed 30-day action review and reopen if material new evidence appears.

**Exit:** approved closeout, retained evidence, accepted corrective actions and a verification date. Public lessons learned require a separate release review and synthetic/sanitized examples.

## Mitigations and prevention

The controls below are implementation proposals for owner review. Use current vendor guidance for the exact platform/build. Each change needs an impact check, authority, validation and rollback; this document does not apply it to the lab.

| Area and owner | Immediate mitigation during an incident | Prevention after stabilization | Testable evidence and rollback consideration |
| --- | --- | --- | --- |
| Exposed services — application/vulnerability lead | Withdraw or restrict a vulnerable interface; apply a supported workaround or fixed build | Maintain exposure inventory, vendor advisory subscriptions, supported versions and risk-based patch SLAs | Approved access test shows unwanted reachability blocked; fixed state verified; rollback must not restore vulnerable public exposure |
| Privileged identity — identity/IdM lead | Restrict affected identities and app trust; revoke supported sessions/tokens; rotate reachable secrets | Phishing-resistant MFA for people, separate admin identities, short-lived workload authentication, least privilege and reviewed recovery access | Old access fails in an approved test, required services use clean credentials, unauthorized grants are absent; keep an independent recovery path |
| RHEL host — Linux lead | Isolate, review process/persistence changes and rebuild if trust is lost | SELinux enforcing, minimum services/packages, protected management, audit coverage, reviewed file integrity and compatible execution restrictions | Owner-approved baseline comparison, effective audit events and required services work; any exception is scoped and expires |
| Windows host — endpoint lead | Isolate and investigate scheduled tasks, services, suspicious installers and script execution | Application control, attack surface reduction where supported, signed/approved software, least privilege and reviewed script logging | Benign allowed software works and an inert unapproved sample is blocked; pilot changes and preserve management access |
| Network/DNS — network lead | Contain affected segments; restrict unnecessary relay/egress paths; preserve DNS/proxy evidence | Allow only required outbound destinations, trusted DNS, segmented admin/data/backup paths and restricted remote access | Authorized traffic works, unapproved test path fails, enforcement logs arrive; revert only through an approved temporary exception |
| Software supply chain — development/IT lead | Suspend a suspect update or third-party integration; preserve artifacts and inventory installed versions | Approved signed packages, provenance checks, dependency review, secure update channels and protected build/release identities | Known-good artifact and publisher verified, monitored pilot install passes; recovery image must not contain the suspect component |
| GitHub and application secrets — repository/cloud owner | Revoke/rotate exposed authentication material and investigate its use; removal of the text alone is insufficient | Secret scanning/push protection where available, independent pre-publication review and managed/federated identities where supported | Revoked credential fails and audit scope is reviewed; restore service with new scoped authentication rather than reusing the exposed value |
| Telemetry/Splunk — detection lead | Preserve logs, identify ingestion gaps and monitor affected assets at increased frequency | Validate source generation, transport, timestamps, parsing, retention, role access, search behavior and alert routing separately | Matching and nonmatching controls are collected and produce the expected outcomes; keep the prior known-good parser/search for rollback |
| Backup/recovery — backup owner | Protect backup administration and clean copies from affected identities and segments | Offline/immutable protected copies where supported, separate admin trust and routine isolated restore exercises | Actual restore and integrity/functional tests meet owner-defined RTO/RPO; do not overwrite the last clean copy |
| People and coordination — SOC/HR/communications | Warn the affected audience through approved channels and preserve original reports | Exercise suspicious attachment, recruiter/helpdesk impersonation, primary-contact failure and zero-day escalation scenarios | Participants reach the correct responder and record acknowledgment; update training based on observed delays |

For unpatched zero-days, compensation is temporary risk reduction. Record the protected attack path, enforcement proof, bypass concerns, owner, expiry and vendor-update check. Replace it with a validated durable fix when available and still investigate any pre-fix compromise.

## Communications, handoff, and action records

Use a private update containing: case/severity; UTC time; facts and confidence; affected service/data scope; current business impact; containment status with evidence; completed/pending actions with owners; decisions required; reporting due times; and the next update. Verify recipients and use the approved independent channel if identity may be affected.

For every consequential action, retain exact target, authority, approver/delegation, executor, UTC times, intended effect, command/console/change reference, actual result, validation evidence and rollback. At shift change, the receiving lead acknowledges ownership, open hypotheses, containment state, evidence references, outstanding decisions and notifications due.

Reuse the existing [incident record](templates/incident-record.md), [hunt plan](templates/threat-hunt-plan.md), [hunt report](templates/threat-hunt-report.md), [briefing](templates/hunt-briefing.md), and [vulnerability workflow](VULNERABILITY_MANAGEMENT.md) in approved private case storage. Use [the weekly hunt pack](weekly-threat-hunting/HUNT_QUERIES.md) for bounded searches and harmless controls.
