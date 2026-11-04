# 10 — Plan of Action and Milestones (POA&M) Template

**A draft finding is not a confirmed vulnerability.** Create a POA&M entry only after an assessment, review, or test identifies an actual gap.

| Field | Example placeholder |
| --- | --- |
| Finding ID | AI-FIND-YYYY-NNN (not assigned) |
| Linked risk ID | AI-RISK-XX |
| Affected asset | Proposed AI-assisted triage component |
| Description / observed evidence | Pending actual test |
| Applicable control | Relevant 800-53 ID after selection |
| Severity / justification | Pending assessment |
| Corrective action | Document an actionable fix |
| Owner | TBD |
| Target date | TBD after owner accepts |
| Interim protection | Keep AI unconnected and use manual Splunk triage |
| Validation method | Repeat relevant synthetic test and examine logs |
| Actual retest evidence | Not available |
| Status | Not opened until a real finding is observed |
| Risk acceptance / decision authority | None |

## Example tracking workflow

1. Record the **observed** deficiency and exact sanitized evidence identifier.
2. Connect it to a risk-register row and any selected security/privacy control.
3. Assign an owner, priority, proposed fix and realistic deadline.
4. Define an interim protection and a repeatable test.
5. Implement the fix in a reviewable branch.
6. Re-run the test and attach sanitized results.
7. Obtain appropriate reviewer confirmation before closing the finding.

Never put passwords, private keys, sensitive raw log messages, or personal information in a public POA&M.
