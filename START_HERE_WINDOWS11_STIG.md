# Start here — Windows 11 STIG V2R11

This optional workstream guides an assessment and careful hardening of the **WINHUNT01 Windows 11 guest VM** in the RHEL 10.2 Splunk home lab. It uses the supplied **Microsoft Windows 11 STIG, Version 2 Release 11**, manual XCCDF dated September 30, 2026. It does not assess or change a VM by itself.

1. Read the [complete Windows 11 implementation guide](docs/stig-windows11/IMPLEMENTATION_GUIDE.md).
2. Use the [257-rule reference index](docs/stig-windows11/RULE_INDEX.md) and the supplied manual XCCDF in STIG Viewer to review every applicable rule.
3. Record actual results privately; use the [sanitized, pending evidence template](evidence/sanitized/windows11-stig-validation.md) only after reviewing it for public release.
4. Assess Windows Defender Firewall separately with the [Firewall V2R2 guide](START_HERE_WINDOWS_FIREWALL_STIG.md), if the benchmark applies.

**Work in progress:** The VM edition, features, policies, actual configuration, scans, hardening, and event forwarding are not verified by these files. This guide is not a finding of compliance or authorization to operate. Back up and arrange console access before any change.
