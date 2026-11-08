---
applyTo: "docs/zero-trust/**,configs/zero-trust/**,scripts/zero-trust/**,hunts/zero-trust/**,examples/zero-trust/**,tests/test_zero_trust_*.py,evidence/sanitized/zero-trust-validation.md,start-here/START_HERE_ZERO_TRUST.md"
---

# Copilot — DoD-aligned Zero Trust Lab Workstream

- This public RHEL 10.2 Splunk lab has three VMs: Splunk .10, WINHUNT01 .20, IdM .30, on VMware VMnet8 172.25.250.0/24; management adapter .1.
- Preserve the existing Splunk/Windows/IdM source files, 52 numbered steps and six index names.
- Never state that documentation constitutes a deployed Zero Trust architecture, DoD Target Level, formal STIG compliance or a federal ATO.
- Distinguish **static** host firewall and Splunk RBAC from a **dynamic** PDP/PEP, MFA, device posture and continuous authorization (these are not installed).
- Use only public DoD, NIST, DISA and vendor references; never ask for or publish classified or contractor-proprietary configuration.
- Apply network rules only on authorized VM consoles; first inspect existing rich rules, management paths and dependencies, and preserve rollback.
- Do not publish secrets, raw event logs, bind passwords, private keys, identity attributes or screenshots with personal data.
- Explain each command's location, purpose, expected result, and rollback; maintain positive AND negative validation.
- Review commands/versions for the installed product; avoid blanket STIG auto-remediation or disabled SELinux/TLS checks.
- Keep policy-as-code validation offline/read-only; require explicit human review for any live change.
- Keep evidence statuses Pending until real tests occur. Never fabricate passing logs or compliance results.
