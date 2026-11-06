# CMMC Level 2 — Evidence Planning for a Passive Monitoring Lab

**Scope notice:** This is a **synthetic education lab with no controlled unclassified information (CUI)**. It is not a CMMC Organization Seeking Assessment (OSA), is not certified, and has no official assessment result. These examples do not implement or evaluate all **110** requirements.

**Program status checked November 5, 2026.** The department announced on July 13, 2026 that it was suspending Phase II, which was scheduled to begin November 10, 2026. Phase I self-assessment requirements remain in place. Check the current policy, applicable contract clauses and contracting officer for the assessment and affirmation requirements that apply. [CMMC Policy](https://dodcio.defense.gov/CMMC/Policy/) · [32 CFR Part 170](https://www.ecfr.gov/current/title-32/subtitle-A/chapter-I/subchapter-G/part-170) · [DFARS 252.204-7021](https://www.acquisition.gov/dfars/252.204-7021-contractor-compliance-cybersecurity-maturity-model-certification-level-requirements.)

The CMMC Level 2 assessment guide uses the 110 requirements in **NIST SP 800-171 Revision 2**. NIST superseded its general publication with Revision 3. For this crosswalk, use the revision and objectives specified by the CMMC program and confirm contract-specific applicability separately. [Level 2 Assessment Guide](https://dodcio.defense.gov/Portals/0/Documents/CMMC/AssessmentGuideL2v2.pdf) · [NIST SP 800-171 Rev. 2 publication record](https://csrc.nist.gov/pubs/sp/800/171/r2/upd1/final)

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
| `RA.L2-3.11.2` | Scan systems and applications on a defined schedule and when new relevant vulnerabilities are identified | Passive observations can prioritize validation | The fixture provides no evidence of scan coverage, frequency, or new-vulnerability scans |
| `3.12.1` | Periodically assess implemented security controls | Validation matrix, policy-change test plan | Not an actual assessment of CUI controls |
| `3.13.1` | Monitor, control and protect communications at boundaries | Sensor architecture and approved flow matrix | TAP/SPAN visibility and enforcement not installed |
| `3.13.8` | Use cryptographic mechanisms to prevent unauthorized disclosure in transit | Splunk TLS/LDAPS and test plans | Live end-to-end control evidence Pending |
| `SI.L2-3.14.6` | Monitor systems and inbound and outbound communications for attacks or indicators of attacks | The [worked case](OFFLINE_HTTP_WALKTHROUGH.md) shows a known alert, evidence pivot and analyst triage | In-scope system and boundary coverage, ongoing operation and response still require evidence |
| `SI.L2-3.14.7` | Identify unauthorized use | Baseline exception reviewed against an approved service inventory | The actual authorized-use policy and alert dispositions are needed |

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

### Example evidence handoff

For `SI.L2-3.14.6`, **examine** the approved boundary diagram, monitoring policy, source inventory and a sanitized alert timeline. **Interview** the analyst and network owner about visibility, dropped traffic and escalation. **Test** an approved positive and negative case and verify collection, triage and disposition. Record the exact objective from the guide, evidence ID, UTC date, tool and rule versions, reviewer, and coverage gap. Add an owner, due date and retest to the internal corrective-action log. Apply formal POA&M and SPRS rules only within the applicable authorized assessment.

## CMMC vs RMF vs DISA STIG

- **CMMC:** Contract-driven cybersecurity assessment for eligible defense contractor environments; Level 2 focuses on NIST 800-171 R2 and CUI.
- **RMF:** Risk management and authorization process for organizational information systems; an ATO decision isn't a CMMC certification.
- **DISA STIG:** Technical platform configuration requirements and guidance; passing a STIG scan does not establish CMMC compliance.
- **NIST 800-53:** Different broader control catalog with potentially relevant controls, **not** a substitute for the CMMC Level 2 800-171 assessment objectives.

**Evidence status:** Planning material only. No CUI, certification, score, SPRS submission or official claim.
