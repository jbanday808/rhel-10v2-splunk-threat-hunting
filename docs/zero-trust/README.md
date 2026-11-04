# DoD-aligned Zero Trust Architecture — RHEL 10.2 + Splunk (WIP)

This **hands-on Zero Trust architecture lab** follows publicly available security guidance, including the [DoD Zero Trust Strategy](https://dodcio.defense.gov/Portals/0/Documents/Library/DoD-ZTStrategy.pdf), [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final), [CISA Zero Trust Maturity Model v2](https://www.cisa.gov/zero-trust-maturity-model), and applicable NIST RMF/DISA STIG publications.

**Not a DoD accreditation, contractor deliverable, complete dynamic ZTNA/PDP, or assertion that systems were deployed/tested.** DoD Target maturity is not achieved merely by producing these files.

## Table of contents

| Order | Document | Result |
| --- | --- | --- |
| **Start** | [Complete Step-by-Step Guide](IMPLEMENTATION_GUIDE.md) | Installation/configuration/deployment workflow with commands |
| 01 | [Architecture and Trust Decisions](01-target-architecture.md) | Current vs target diagrams, policy engine / PEP boundaries |
| 02 | [Seven DoD ZT Pillars](02-dod-seven-pillars.md) | User, device, workload, data, network, automation, visibility |
| 03 | [Preflight, Inventory & Backout](03-preflight-and-inventory.md) | Recovery, versions, dependencies and baseline |
| 04 | [Identity and Access](04-identity-and-access.md) | Red Hat IdM, Splunk RBAC, privileged accounts, future MFA |
| 05 | [Endpoint Security](05-endpoint-security.md) | RHEL/Windows posture and logging |
| 06 | [Microsegmentation](06-network-microsegmentation.md) | Source-bound host firewall policy and denial tests |
| 07 | [Application and Data](07-app-data-security.md) | TLS, Splunk app, six indexes, least privilege, retention |
| 08 | [SIEM Analytics & Automation](08-siem-and-automation.md) | SPL hunting and change-controlled policy as code |
| 09 | [RMF, STIG, ATO](09-rmf-stig-ato.md) | Prepare→Monitor and evidence with no false compliance claims |
| 10 | [Validation and Screenshot Plan](10-verification-and-evidence.md) | Positive + negative checks and status |
| 11 | [Migration and Operations](11-migration-and-operations.md) | Legacy-to-ZT staged rollout, incidents and maintenance |
| 12 | [Official References](12-official-references.md) | Official sources, versions, vendor manuals |

**Reusable examples:** [Network policy matrix](../../configs/zero-trust/allowed-flows.example.json), [flow validator](../../scripts/zero-trust/validate_policy.py), [read-only lab assessment](../../scripts/zero-trust/verify-lab-readonly.sh), [example Splunk searches](../../hunts/zero-trust/README.md), [risk register](../../examples/zero-trust/risk-register.example.csv), [evidence log](../../evidence/sanitized/zero-trust-validation.md), [Copilot guidance](../../.github/instructions/zero-trust.instructions.md).

## Scope and terminology

**PDP (policy decision point)** decides whether a request is allowed; **PEP (policy enforcement point)** enforces the decision. For this lab, Splunk RBAC and firewalld represent **local or static enforcement mechanisms**, not a centralized adaptive PDP. IdM groups provide identity information, and Splunk provides visibility. A **future ZTNA broker + approved IdP/MFA + verified endpoint posture** would be needed for a fuller dynamic access design. These are explicitly NOT INSTALLED.

The DoD strategy's seven pillars organize this lab, but a three-VM learning environment does not satisfy all 45 DoD capabilities or prove Target Level compliance.

**State:** Documentation source prepared. Deployment, continuous access evaluation, product integration and independent control assessment remain **Pending**.
