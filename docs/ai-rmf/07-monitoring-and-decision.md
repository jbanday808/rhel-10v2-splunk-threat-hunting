# 07 — Risk Decisions, Monitoring, and Withdrawal

## Decision record template

| Field | Entry |
| --- | --- |
| AI capability / version | TBD — not deployed |
| Scope and owners | TBD |
| Data classification review | Pending |
| Privacy and provider review | Pending |
| Test / assessment result | Not performed |
| Open high risks | See example risk register; no real acceptance |
| Decision | **NO operational use authorized** |
| Decision maker / date | Not assigned |
| Next review date | TBD |

A lab owner's permission to experiment is not a federal Authorization to Operate. Only the appropriate designated authorizing official can make an actual RMF `AUTHORIZE` decision where that process applies.

## Proposed monitoring routine

- **Per test session:** record model/prompt version, sanitized sample ID, generated evidence references, analyst decision, unusual errors and prohibited action attempts.
- **Weekly while testing:** review error samples, open risks, secret-handling checks, access logs, provider change notices and synthetic canary outcomes.
- **On any material change:** update boundary and re-evaluate data, model/provider, retention, permissions, prompts, source SPL searches, and dependency versions.
- **Monthly (suggested lab cadence):** owner reviews open POA&M items and whether AI still adds value versus ordinary SPL/human review.
- **Before any real data:** obtain explicit data-owner/privacy/security approvals and document handling restrictions.

These are **proposed** cadences for this lab, not NIST-mandated frequencies.

## Rollback / kill switch

1. Disable the optional AI connector or remove its network access.
2. Revoke the connector's dedicated credentials (if issued).
3. Stop any queued processing and remove unapproved copies of data under the approved retention policy.
4. Preserve sanitized investigation evidence and audit identifiers.
5. Fall back to original SPL searches and human analysis.
6. Record incident/failure, decision, remediation, and retest before any redeployment.

**No rollback command is supplied** because this repo does not currently deploy an AI component.
