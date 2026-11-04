# 05 — Illustrative SP 800-53 Controls Crosswalk

**Not an approved baseline or an official NIST AI RMF-to-800-53 mapping.** These are plausible control candidates from SP 800-53 Rev. 5, Release 5.2.0. Final applicability, tailoring, and assessment require system categorization, requirements, and an authorized review.

| Control | Purpose in proposed AI extension | AI RMF function | Evidence to collect | Status |
| --- | --- | --- | --- | --- |
| **PL-2** — System Security and Privacy Plans | Document lab and AI extension boundaries, implementation and ownership. | GOVERN / MAP | SSP, reviewed scope, version. | Proposed |
| **RA-3** — Risk Assessment | Analyze misleading summaries, unauthorized disclosure, and adversarial event content. | MAP / MANAGE | Risk register, approval history. | Proposed |
| **AC-3** — Access Enforcement | Limit AI data access to approved Splunk searches/roles. | GOVERN / MANAGE | RBAC test, permissions, denied-access results. | Proposed |
| **AC-6** — Least Privilege | Ensure proposed assistant cannot administer Splunk, IdM, Windows or containment. | GOVERN / MANAGE | Service-account permissions, read-only tests. | Proposed |
| **AU-2** — Event Logging | Define logs for input provenance, model version, review and decisions. | MEASURE / MANAGE | Logging requirements and sanitized evidence. | Proposed |
| **AU-12** — Audit Record Generation | Verify review trail is produced without storing raw secrets. | MEASURE | Sanitized audit samples. | Proposed |
| **SC-8** — Transmission Confidentiality and Integrity | Protect approved event extracts in transit if an integration is later deployed. | GOVERN / MANAGE | TLS configuration and test. | Proposed |
| **SC-28** — Protection of Information at Rest | Encrypt retained samples and set retention/deletion rules. | GOVERN / MANAGE | Storage policy, encryption evidence. | Proposed |
| **CM-2** — Baseline Configuration | Track exact model, prompt/template, dependency and system versions. | GOVERN / MANAGE | Version inventory, approved change. | Proposed |
| **SI-4** — System Monitoring | Watch for access misuse, data leakage, integration errors, and unusual behavior. | MEASURE / MANAGE | Review reports and alerts. | Proposed |
| **CA-7** — Continuous Monitoring | Define reassessment cadence and triggers. | MEASURE / MANAGE | Schedule and completed review records. | Proposed |
| **IR-4** — Incident Handling | Define how to disable AI processing, preserve evidence, and escalate incidents. | MANAGE | Response runbook and exercise result. | Proposed |
| **SR-3** — Supply Chain Controls and Processes | Evaluate model/provider/dependency provenance and change notices. | GOVERN / MAP | Provider review, component inventory. | Proposed |

These control IDs are starting points, not a claim that any control has been implemented or assessed. SP 800-53B baseline selection occurs only after scope and categorization are established.

## Example assessment approach

For each candidate control: document owner, applicable component, expected mechanism, actual implementation (or Not Implemented), test method (examine/interview/test), actual evidence identifier, finding, remediation, and reviewer/date. Keep `Pending` until a test has happened.
