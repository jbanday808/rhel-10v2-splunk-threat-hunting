# NIST AI RMF + NIST SP 800-37 Integration (Work in Progress)

This section documents **proposed, not yet deployed** AI-assisted security analysis for the existing RHEL 10.2 Splunk Threat Hunting Lab.

**Start:** [Complete VS Code + WSL implementation guide](IMPLEMENTATION_GUIDE.md)

## Important distinction

- **NIST AI RMF 1.0 (NIST AI 100-1):** voluntary AI risk management using **GOVERN, MAP, MEASURE, MANAGE**.
- **NIST SP 800-37 Rev. 2:** seven-step security and privacy RMF for information systems: **PREPARE, CATEGORIZE, SELECT, IMPLEMENT, ASSESS, AUTHORIZE, MONITOR**.
- **NIST SP 800-53 Rev. 5, Release 5.2.0:** catalog of security and privacy controls used as examples here; actual baseline selection depends on a properly approved categorization and organizational requirements.
- **NIST AI 600-1:** additional considerations if a generative-AI summarizer is eventually used.

These are complementary frameworks, **not identical standards**. An AI RMF worksheet is **not an Authorization to Operate (ATO)** or evidence that NIST has certified this lab.

## Existing systems, unchanged

| System | IP | Function |
| --- | --- | --- |
| RHEL-SPLUNK01 | 172.25.250.10 | Splunk Enterprise indexing, search, Linux log collection |
| WINHUNT01 | 172.25.250.20 | Windows logs, Sysmon, Universal Forwarder |
| RHEL-IDM01 | 172.25.250.30 | IdM, DNS, proposed LDAP integration |
| Windows 11 + Ubuntu WSL | Local development | VS Code, version control, offline document checks |

The 52 deployment steps, 13 searches, and the existing architecture remain valid source documentation. **No AI model, agent, LLM endpoint, autonomous response, or ATO is claimed to be running.**

## Files in this section

| File | Purpose |
| --- | --- |
| [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) | Detailed staged VS Code + WSL implementation guide |
| [01-use-case-scope.md](01-use-case-scope.md) | Mission, permitted and prohibited AI uses, roles |
| [02-system-boundary-and-flow.md](02-system-boundary-and-flow.md) | Current and optional future data flows |
| [03-nist-rmf-7-steps.md](03-nist-rmf-7-steps.md) | Federal system RMF step-by-step evidence plan |
| [04-ai-rmf-core.md](04-ai-rmf-core.md) | GOVERN / MAP / MEASURE / MANAGE activities |
| [05-control-crosswalk.md](05-control-crosswalk.md) | Illustrative 800-53 controls mapped to risks |
| [06-testing-and-assessment.md](06-testing-and-assessment.md) | Synthetic tests and human-review gates |
| [07-monitoring-and-decision.md](07-monitoring-and-decision.md) | Risk acceptance, POA&M, monitoring, withdrawal |
| [08-official-references.md](08-official-references.md) | Official NIST publications and version notes |
| [09-system-security-plan-template.md](09-system-security-plan-template.md) | SSP outline—draft only |
| [10-poam-template.md](10-poam-template.md) | Open finding and remediation worksheet |
| [11-evidence-and-screenshots.md](11-evidence-and-screenshots.md) | Evidence names, screenshot plan, status gates |

Supporting: [use-case inventory](../../examples/ai-rmf/ai-use-case.example.json), [risk register](../../examples/ai-rmf/ai-risk-register.example.csv), [sanitized evidence](../../evidence/sanitized/ai-rmf-validation.md), and [offline unit test](../../tests/test_ai_rmf_docs.py).

## Current status

**Documentation scaffold: Work in Progress. AI system: Not selected / not deployed. RMF categorization: Not approved. Independent assessment: Not performed. Authorization: Not granted.**

Keep all example artifacts synthetic or sanitized. Never send real credentials, raw security events, personal data, or regulated information to an unapproved AI provider. Do not make containment decisions automatically.
