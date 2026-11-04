# 01 — AI Use Case, Scope, and Roles

## Intended mission

Propose a **read-only AI-assisted triage drafting capability** that helps a human analyst summarize selected Splunk security events and identify next investigative questions. This is an extension to the existing SIEM lab, **not a capability already deployed**.

## Existing telemetry sources

- Windows Security/System, PowerShell Operational, Sysmon event streams sent by WINHUNT01 through Splunk Universal Forwarder.
- RHEL Linux security/logging events on RHEL-SPLUNK01.
- Existing indexes `win_security`, `win_system`, `powershell`, `sysmon`, `linux`, and `lab`.
- Existing SPL saved searches and detections; AI is neither a replacement for SPL nor an automatic source of verified detections.

## Proposed AI functionality

- Input: manually selected **synthetic first**, then formally approved **sanitized** search excerpts.
- Model/provider: **TBD; not selected or connected**.
- Output: draft event summary, evidence references, confidence/uncertainty statement, and suggested investigation questions.
- Human: reviews, corrects, and accepts or rejects any output.
- Prohibited: autonomous containment, firewall/identity changes, malware execution, privileged Splunk searches, sensitive data export, undocumented model training on events, or access to secrets.

## Roles (assign names only after actual approval)

| Role | Responsibility | Status |
| --- | --- | --- |
| Lab project owner | Controls scope and maintains records | TBD |
| AI use-case owner | Defines intended use and safe boundaries | TBD |
| Security reviewer | Evaluates vulnerabilities, controls, misuse cases | TBD |
| Privacy reviewer | Checks event-data classification and disclosure | TBD |
| Independent evaluator | Executes and records test results | TBD |
| Decision authority | Approves or denies experiment; formal AO only where applicable | TBD |
| Analyst | Reviews every output before action | TBD |

## Key decision before beginning

Could a deterministic SPL alert plus an analyst checklist meet the need without an AI model? If so, keep AI out of scope. Document reasons if the AI option provides measurable incremental benefit. Record resulting risks and stop conditions in the risk register.
