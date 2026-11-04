---
applyTo: "docs/ai-rmf/**,examples/ai-rmf/**,tests/test_ai_rmf_docs.py,evidence/sanitized/ai-rmf-validation.md"
---

# GitHub Copilot instructions — NIST AI RMF lab extension

- This repository is a security-monitoring lab, **not currently an AI deployment**. Never describe the model, agent, or AI evaluation as operational.
- Keep NIST AI RMF (GOVERN/MAP/MEASURE/MANAGE) distinct from SP 800-37 (PREPARE/CATEGORIZE/SELECT/IMPLEMENT/ASSESS/AUTHORIZE/MONITOR).
- Do not claim an ATO, FIPS impact level, NIST certification, FedRAMP authorization, 800-53 control compliance or successful tests without independent recorded evidence.
- Only generate synthetic safe examples. Never add secrets, raw logs, personal data, identifiable real users, or production credentials.
- Keep AI use read-only and human-reviewed; no autonomous Splunk/endpoint/identity configuration or security actions.
- Keep all unknown approvals and implementation states labeled Pending, TBD, Not deployed, or Not granted.
- Cite official NIST source links and state framework versions.
- Before suggesting changes, check the existing 52 deployment steps, the current architecture, and whether a change is an optional future AI extension.
