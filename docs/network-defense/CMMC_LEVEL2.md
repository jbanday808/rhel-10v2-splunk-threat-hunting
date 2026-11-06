# CMMC Level 2 — Evidence Planning for a Passive Monitoring Lab

**Scope notice:** This is a **synthetic education lab with no controlled unclassified information (CUI)**. It is not a CMMC Organization Seeking Assessment (OSA), is not certified, and has no official assessment result. These examples do not implement or evaluate all **110** requirements.

**As of the documented 2026 CMMC model**, Level 2 uses **NIST SP 800-171 Revision 2** requirements. Do not substitute SP 800-171 Revision 3 without official program rule changes. The DoD describes Level 2 **self assessments and third-party C3PAO assessments** depending on contract requirements; required assessment type and schedule derive from the applicable contract/DFARS/CMMC program, not from a homelab. See [DoD CMMC Program About](https://dodcio.defense.gov/CMMC/About/) and [Level 2 Assessment Guide](https://dodcio.defense.gov/Portals/0/Documents/CMMC/AssessmentGuideL2v2.pdf).

## Applicability and scope first

1. Confirm a real contract requires CMMC and its specific level/assessment type.
2. Identify the actual CUI, its authorized systems and exchanges; categorize in-scope assets per current assessment guidance.
3. Determine where Zeek/Suricata packet data and Splunk logs may contain CUI or other sensitive information.
4. Document the protected boundary, external service providers, controls, inheritance, SSP, POA&M and evidence ownership.
5. Never use public GitHub, a personal home lab, external AI or an unapproved service as a repository for actual CUI.
6. Have authorized assessors interpret requirements and objectives, not just a scanner score or a SIEM dashboard.

## Selective Level 2 NIST SP 800-171 Revision 2 mapping (examples only)

| Requirement | What it requires (plain language) | Possible lab evidence contribution | Gap and actual status |
| --- | --- | --- | --- |
| `3.3.1` | Create and retain system audit logs for analysis | Approved Zeek/Suricata/Splunk event inventory and retention plan | Real in-scope auditing, retention and coverage not assessed |
| `3.3.2` | Trace users' actions when needed | Splunk user/IdM audit mapping | Real identity traceability unverified |
| `3.3.3` | Review and update logged events | Detection rule review, change tickets, alert QA | No operational review results |
| `3.6.1` | Establish operational incident-handling capability | CONOPS triage and escalation flow | Organization IR plan and capability not evaluated |
| `3.6.2` | Track, document and report incidents | Sanitized case/evidence templates | Not an official incident-reporting process |
| `3.11.1` | Periodically assess risk to operations and information | Passive baseline risk register and findings | Not a formal risk assessment |
| `3.11.2` | Scan for vulnerabilities at defined intervals and with new findings | **Passive analysis can supplement** vulnerability analysis | Passive monitoring **alone does not satisfy** vulnerability-scanning requirement |
| `3.12.1` | Periodically assess implemented security controls | Validation matrix, policy-change test plan | Not an actual assessment of CUI controls |
| `3.13.1` | Monitor, control and protect communications at boundaries | Sensor architecture and approved flow matrix | TAP/SPAN visibility and enforcement not installed |
| `3.13.8` | Use cryptographic mechanisms to prevent unauthorized disclosure in transit | Splunk TLS/LDAPS and test plans | Live end-to-end control evidence Pending |

**Caution:** Mapping a tool to a requirement is not the same as satisfying **all assessment objectives**. Determine coverage from the **current CMMC Assessment Guide**, not a portfolio summary.

## Assessment workbook fields

| Field | Record |
| --- | --- |
| Requirement and assessment objective | NIST 800-171 R2 identifier + exact objective |
| In-scope asset / CUI type | Real authorized inventory; synthetic lab is out of scope |
| System owner and shared service | Responsible organization |
| Implementation description | Actual configuration and limitations |
| Examine / interview / test | Assessment methodology and observed evidence |
| Date and tool version | Explicit product/configuration source |
| Finding status | Met / Not Met / Not Applicable only when properly assessed |
| POA&M and corrective action | Approved owner, due date, re-test |
| Assessor/decision authority | Actual qualified authority, not GitHub workflow |

## CMMC vs RMF vs DISA STIG

- **CMMC:** Contract-driven cybersecurity assessment for eligible defense contractor environments; Level 2 focuses on NIST 800-171 R2 and CUI.
- **RMF:** Risk management and authorization process for organizational information systems; an ATO decision isn't a CMMC certification.
- **DISA STIG:** Technical platform configuration requirements and guidance; passing a STIG scan does not establish CMMC compliance.
- **NIST 800-53:** Different broader control catalog with potentially relevant controls, **not** a substitute for the CMMC Level 2 800-171 assessment objectives.

**Evidence status:** Planning material only. No CUI, certification, score, SPRS submission or official claim.
