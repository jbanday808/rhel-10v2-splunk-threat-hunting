# 11 — Migration From Perimeter Trust to Resource Trust, Operations and Leadership

## Design objective

Replace “any user/VM on the subnet can access the service” with explicit policy decisions tied to resource, user, device and context. This lab starts with static identity and source restrictions; **dynamic adaptive access remains future work**.

## Six-stage migration plan

| Stage | Activity | Gate to move forward | Recovery |
| --- | --- | --- | --- |
| **1. Discover** | Inventory systems, owners, flows, dependencies, legacy implicit trust | Approved flow and identity tables | No changes |
| **2. Baseline** | Take snapshots, private backups, record existing firewall rules and Splunk role mappings | Console/recovery tested | Restore known-good configs |
| **3. Pilot** | Source-limit Splunk Web 8000 and Windows ingest 9997 with runtime rich rules | Positive/negative tests | Remove runtime rule, console recovery |
| **4. Harden** | Minimize roles, verify CA/TLS, endpoint posture, retention | End-to-end telemetry still works | Roll back individual change |
| **5. Integrate** | Evaluate compatible IdP MFA, verified device posture and ZTNA/PEP, under separate design approval | Independent product/compatibility tests | Disable new broker/integration |
| **6. Operate** | Continuous monitoring, change control, incident testing, re-evaluation and patching | Actual repeatable evidence | Incident runbook and retained local admin |

## Engineering change checklist

- State business purpose and protected resource.
- Obtain system-owner / security reviewer signoff.
- Record exact currently supported products, versions and interfaces.
- Identify affected users, ports, certificates, DNS, time, data stores and service dependencies.
- Plan a maintenance window and communicate impact.
- Capture both source and target state (private, authenticated evidence).
- Apply one reversible policy at a time.
- Execute explicit allowed/denied tests, service health checks and ingestion checks.
- Restore or back out on unexpected results.
- Update diagrams, inventory, risk register, POA&M and operation manuals.

## Multi-vendor and cloud integration planning (NOT installed)

| Component class | Example solution families | Required interface questions |
| --- | --- | --- |
| Network | Palo Alto, Cisco, Juniper, VMware virtual networking | What is the protected resource, enforcement point, logging and policy API? |
| Identity | Red Hat IdM, Entra ID, approved ICAM/PAM/IdP | Can it enforce MFA, device risk, session duration and least privilege? |
| Endpoint | Native Windows Defender/Sysmon, Linux auditd/SELinux, managed EDR/UEM | Are posture signals trusted, current, and usable by policy engine? |
| Cloud | Azure, AWS, approved government/DoD cloud offerings | Which identity, logging, authorization and residency boundaries apply? |
| Automation | GitHub Actions, policy-as-code validation, approved SOAR | Are changes reviewed, signed, tested, reversible and auditable? |

These are **evaluation options**; do not claim a Palo Alto/Cisco/Juniper/Entra/ZTNA installation until actually configured and observed. GitHub-to-Azure OIDC workflow examples are **not** a device-aware user ZTNA service.

## Operating model

**Lab owner / architect:** Owns architecture, inventory, risk register, service dependencies and major tradeoffs.

**Identity reviewer:** Validates account life cycle, least privilege, SSO integration and directory group membership.

**Network engineer:** Maintains resource-level allowlists, tests denied routes and documents rollback.

**SOC analyst:** Validates telemetry, triages Splunk detections, avoids automated response without approval.

**Risk assessor:** Reviews STIG/RMF evidence, remediations and exceptions; not a substitute for a government Authorizing Official.

## Incident and fail-safe behavior

1. Detect a policy failure, credential compromise, or missing telemetry using actual records.
2. Disable or isolate the **specific optional integration** according to the approved plan; do not disable all monitoring.
3. Preserve local emergency access and Splunk audit logs.
4. Record incident, affected systems and last-known-good rules.
5. Restore service and re-run both permission and denial tests.
6. Post-mortem: update risk register, automation and validation evidence.

### Success criteria for the job-role showcase

- Traceable architecture decisions.
- Demonstrable identity and network controls with negative tests.
- A credible phased migration and secure operations plan.
- Public DoD pillar mapping without target-level claims.
- RMF/ATO-aware documentation and accurate STIG version handling.
- Evidence of troubleshooting, change management and communication.
