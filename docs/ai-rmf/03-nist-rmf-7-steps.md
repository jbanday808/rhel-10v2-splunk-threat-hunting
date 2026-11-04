# 03 — NIST SP 800-37 Rev. 2: Seven-Step Implementation Plan

This is the **information-system** security and privacy RMF, separate from NIST AI RMF 1.0.

| RMF step | Action for the proposed AI-assisted Splunk use case | Deliverable / acceptance |
| --- | --- | --- |
| **1. PREPARE** | Appoint owner, reviewer, risk decision maker; scope lab, stakeholders and dependencies. | Assigned roles, system boundary, mission rationale. |
| **2. CATEGORIZE** | Identify data types and confidentiality/integrity/availability impacts; use FIPS 199 and organizational guidance when applicable. | Reviewed impact rationale and appropriately approved categorization. **Pending** |
| **3. SELECT** | Determine applicable baseline using SP 800-53B, tailor controls to boundary, assign owners. | Control selection and security/privacy plan; example crosswalk is not approval. |
| **4. IMPLEMENT** | Restrict Splunk queries, sanitize test events, secure integration, log decisions, prohibit autonomous response. | Actual configuration snapshots and change records. **Not deployed** |
| **5. ASSESS** | Perform independent/security review, synthetic failure tests and evidentiary validation. | Test cases with observed results and findings. **Pending** |
| **6. AUTHORIZE** | Present risks to the proper risk decision maker or authorizing official where applicable. | Documented decision. **No ATO granted** |
| **7. MONITOR** | Track drift, false positives, access, changes, provider updates, new data types and open weaknesses. | Monitoring cadence, risk register updates and evidence reviews. **Planned** |

## Required safeguards

- No unsupported claims of system categorization, FedRAMP compliance, eMASS approval, or government ATO.
- Do not assign LOW/MODERATE/HIGH without evidence and the appropriate formal determination.
- SSP, POA&M, control assessment, authorization memo, and monitoring strategy are **templates** until filled with real observed results.
- Treat supply-chain and software provenance risks as part of the reviewed boundary.
- Document an AI-specific privacy review if events include information about real individuals.

## Suggested outputs

Use [SSP template](09-system-security-plan-template.md), [control crosswalk](05-control-crosswalk.md), [test plan](06-testing-and-assessment.md), [POA&M](10-poam-template.md), and [monitoring strategy](07-monitoring-and-decision.md).
