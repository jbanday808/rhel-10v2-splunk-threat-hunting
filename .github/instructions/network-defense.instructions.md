---
applyTo: "start-here/START_HERE_NETWORK_DEFENSE.md,docs/network-defense/**,scripts/network-defense/**,configs/network-defense/**,apps/SENSOR_UF/**,rules/yara/**,rules/sigma/**,hunts/network-defense/**,evidence/sanitized/network-defense-validation.md,tests/test_network_defense.py"
---

# Copilot — Passive Network Defense Lab Extension

- RHEL-SPLUNK01 .10, WINHUNT01 .20, RHEL-IDM01 .30 are existing; RHEL-SENSOR01 .40 is **proposed**, not deployed.
- Preserve original 52 deployment steps, existing six Splunk indexes, TLS/LDAPS, Splunk storage and Windows forwarding.
- VMware VMnet8 NAT is **not** a TAP or SPAN; do not claim all east-west flows are captured. Begin with synthetic PCAPs outside Git.
- Zeek native RHEL binary support is not guaranteed; use verified official releases/packages/containers and pinned digests.
- Suricata example is a **passive IDS**; never activate IPS/drop/NFQUEUE, inline routing, or uncontrolled live monitoring.
- YARA rules apply to **approved local files**, not arbitrary live network packets; Sigma rules need actual Splunk backend/field checks.
- Never publish real PCAPs, raw Zeek/Suricata logs, extracted payloads, credentials, CUI/classified records or sensitive host data.
- CMMC Level 2 planning maps select SP 800-171 Rev 2 controls only; never claim certification, SPRS score, compliance or third-party assessment.
- Keep live test outcomes Pending until authorized observations, actual tool versions, true/false positives, reviewer and evidence ID are recorded.
- No automated GitHub Actions job may connect to private VMware or push changes to firewalls/IdM/production Splunk.
- Include the execution host, intended outcome, rollback and negative tests in each deployment instruction.
