# 04 — NIST AI RMF 1.0 Core Mapping

The NIST AI Risk Management Framework has four continuing functions: **GOVERN, MAP, MEASURE, MANAGE**. The NIST Playbook is voluntary guidance, not a required sequence or certification.

| Function | Lab application | Initial artifacts | Initial status |
| --- | --- | --- | --- |
| **GOVERN** | Assign accountable owners, AI use policy, reviewer competence, recordkeeping, monitoring triggers and stop rules. | Use-case card, roles table, decision log. | Draft / TBD |
| **MAP** | Identify use purpose, expected benefit, affected stakeholders, permitted data, provider dependency, context, failures and harmful misuse. | Data-flow diagram, dataset inventory, threat scenarios. | Draft / TBD |
| **MEASURE** | Compare outputs with a verified answer key; test evidence grounding, hallucination, prompt injection, data disclosure, human override and reliability. | Synthetic test plan and results; signed review. | Not tested |
| **MANAGE** | Prioritize risk, choose mitigations, document no-go gates, accept/reject with authority, monitor and withdraw when needed. | Risk register, POA&M, decision record, monitoring plan. | No operational approval |

## Generative-AI considerations (NIST AI 600-1, if later applicable)

1. **Confabulation / ungrounded output:** AI summary invents account activity, events, or indicators that are absent from logs.
2. **Information integrity:** Source events can be maliciously crafted; treat them as untrusted data, not instructions.
3. **Data privacy and confidentiality:** Logs can contain personal identifiers, secrets, hostnames, and command lines.
4. **Human-AI configuration:** Analyst must see supporting evidence and be able to reject the AI summary.
5. **Security and resilience:** Restrict access, rate-limit, monitor changes, and handle upstream provider outages.
6. **Supply chain:** Document provider, model version, dependencies, updates, data retention and contract terms.

## Suggested measures (local project examples, not NIST thresholds)

- **Evidence grounding:** each factual assertion in a draft links to at least one input event ID or is explicitly labeled uncertain.
- **Secret disclosure:** zero synthetic secret strings in output.
- **Autonomous action:** zero side-effect calls; human-only actions.
- **Prompt injection:** embedded log instructions are ignored as instructions and treated as data.
- **Reviewer control:** each accepted summary receives explicit reviewer confirmation.

Set quantitative pass criteria **before** running a test. Report actual numerator, denominator, failures, limitations and test version; never report a planned target as a measured result.
