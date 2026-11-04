# 11 — AI RMF Evidence and Screenshot Plan

Use **one numbered figure per verified milestone**. Keep actual source artifacts in the appropriate secure workspace; publish **sanitized** copies only. No screenshots are claimed to exist for an AI model yet.

| Proposed figure | Suggested filename | What to capture | Initial status |
| --- | --- | --- | --- |
| Figure AI-01 | `AI_RMF_01_System_Boundary.png` | Current 3-VM diagram + clearly labeled optional AI boundary | Planned |
| Figure AI-02 | `AI_RMF_02_Use_Case_Inventory.png` | Proposed use case, owner, prohibited actions and deployment status | Planned |
| Figure AI-03 | `AI_RMF_03_Data_Flow_Review.png` | Sanitized allowed data flow and trust boundaries | Planned |
| Figure AI-04 | `AI_RMF_04_Control_Crosswalk.png` | Candidate NIST control mapping; show Proposed labels | Planned |
| Figure AI-05 | `AI_RMF_05_Risk_Register.png` | Risk IDs, mitigations and current proposed statuses | Planned |
| Figure AI-06 | `AI_RMF_06_TEVV_Synthetic_Tests.png` | Future test outcomes from harmless synthetic events | Pending |
| Figure AI-07 | `AI_RMF_07_Human_Approval.png` | Future analyst accept/reject workflow and review ID | Pending |
| Figure AI-08 | `AI_RMF_08_Continuous_Monitoring.png` | Future monitored metrics and remediation progress | Pending |

## Suggested one-sentence captions

- **Figure AI-01:** Proposed NIST AI RMF extension to the existing RHEL 10.2 Splunk lab, showing trust boundaries and human review.
- **Figure AI-04:** Illustrative NIST SP 800-53 control mapping for planned AI-assisted security triage, pending formal selection and assessment.
- **Figure AI-06:** Synthetic evaluation evidence demonstrating the observed results of AI output and instruction-injection tests—only after actual test execution.

## Evidence quality requirements

- Capture the actual source/date/tool and version when taking a screenshot.
- Use `Pending` when no run occurred; never replace with green check marks based on the existence of source files.
- Redact names, sensitive event text, passwords, private IPs where restricted, account identifiers and access tokens.
- No unredacted personal or protected data in GitHub, public Issues, Actions logs, or Copilot prompts.
- Add reviewer initials and a non-sensitive evidence ID when real testing occurs.
- Include false positives, failed tests and unresolved risks, not only favorable results.

Record milestone statuses in [AI RMF Validation Evidence](../../evidence/sanitized/ai-rmf-validation.md).
