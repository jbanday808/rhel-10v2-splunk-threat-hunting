---
applyTo: "docs/stig-rhel10/**,scripts/stig/**,tests/test_stig_rhel10_tools.py,examples/stig-rhel10/**,evidence/sanitized/rhel10-stig-validation.md,START_HERE_RHEL10v2_STIG.md"
---

# GitHub Copilot guidance — RHEL 10 STIG SCAP V1R1

- This public homelab uses the user's DISA RHEL 10 STIG SCAP **V1R1** as uploaded, 396 rules. The separate Red Hat vendor profile aligns with **V1R2**; do not confuse or merge results.
- Keep source ZIP/XML, raw OpenSCAP XCCDF/ARF/HTML/reports, credentials and IdM/CA data **outside the public repository**.
- Preserve the original RHEL 10.2 Splunk and IdM VMs, 52 deployment steps, Splunk data volume and index names.
- The local scanner can only assess; NEVER run automatic remediation, privileged remote scripts, generic mass hardening, partition changes, or FIPS migration.
- Record an owner's approved profile choice. MAC-3_Public is an educational example, not a formal system categorization.
- Flag FIPS/SSH crypto, gssproxy/Kerberos, SSL/TLS, SELinux, firewalld, rsyslog/audit, system mounts and Splunk storage as potentially service-impacting.
- Explain each command's execution host, purpose, expected evidence and rollback.
- OpenSCAP exit 2 can mean a completed scan with failing controls. Never equate scan success with security compliance.
- No ATO, official STIG pass, or assessed control is claimed without observed independent evidence.
- Keep evidence Pending until actual scans, tests, reviews and sanitization have occurred.
