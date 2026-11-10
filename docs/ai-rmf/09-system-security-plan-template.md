# 09 — System Security and Privacy Plan (SSP) Template

> **Template / Draft — not an approved SSP.** Complete under the applicable organization's processes if a real system assessment is required. Current AI extension is not deployed.

## 1. General information

| Field | Value |
| --- | --- |
| Project / system name | RHEL 10.2 Splunk Threat Hunting Lab — proposed AI-assisted triage |
| System owner / organization | TBD |
| Mission and intended users | Optional drafting assistance for human Splunk analysts |
| Version / review date | Draft 0.1 / TBD |
| Decision authority / authorizing official | TBD / not assigned |
| System boundary | See [02-system-boundary-and-flow.md](02-system-boundary-and-flow.md) |
| Deployment status | No AI model, integration, or service deployed |
| Security categorization (FIPS 199) | **Not determined / Pending formal review** |
| Applicable privacy assessment | TBD; evaluate before using real-person data |
| Interconnections | No AI interconnection approved |

## 2. Existing environment

RHEL-SPLUNK01, WINHUNT01 and RHEL-IDM01 form the source lab, on VMnet8 NAT. Existing source configurations and expected log pathways appear in the main [architecture documentation](../architecture.md). Do not assume every planned part is operational.

## 3. Proposed AI extension

- **Purpose:** draft a human-reviewed summary from explicitly approved redacted Splunk events.
- **Model/provider/version:** not selected.
- **Input sensitivity:** synthetic test data only until formal review.
- **Output:** draft narrative, event citations, uncertainties and suggested investigative questions.
- **Trust boundary:** no direct AI connection to privileged Splunk endpoints, identity control, endpoint administration or containment tools.
- **Human oversight:** analyst must manually verify the source events and accept/reject output.

## 4. Control implementation worksheet

| Control | Owner | Intended implementation | Actual configuration/evidence | Assessment result |
| --- | --- | --- | --- | --- |
| AC-3 / AC-6 | TBD | Read-only access and least privilege | None — proposed | Pending |
| AU-2 / AU-12 | TBD | Sanitized logging and reviewer traceability | None — proposed | Pending |
| CM-2 | TBD | Versioned model/prompt configurations | None — proposed | Pending |
| SC-8 / SC-28 | TBD | Approved encrypted transit and storage | None — proposed | Pending |
| RA-3 / CA-7 | TBD | Risk register, periodic review | Draft templates only | Pending |
| IR-4 | TBD | Stop integration and investigate failure | Planned | Pending |

Crosswalk: [05-control-crosswalk.md](05-control-crosswalk.md). The official selection and tailoring process may require other controls.

## 5. Required supporting documents

- Configuration baseline and version inventory.
- Dataflow diagram and information-type inventory.
- Data-owner/security/privacy/provider approvals.
- Risk and impact assessment.
- Assessment plan, actual test record, findings and POA&M.
- Incident response and data retention / disposal procedures.
- Formal decision record by appropriate authority.

**Status:** This is a student/portfolio planning artifact. It does not represent a government authorization package or an ATO.
