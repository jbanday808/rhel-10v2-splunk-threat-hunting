# Windows Defender Firewall STIG references

- **Supplied DISA manual XCCDF:** Microsoft Windows Defender Firewall with Advanced Security STIG V2R2, dated November 9, 2023; 21 rules. SHA-256 of the supplied XML: `1ab51658e50cbcd6a7bf139dee884afca60de1049a8ed19391160fbd36e769bd`. The hash identifies the supplied copy but does not establish publisher authenticity.
- **Supplied V2R2 overview and revision history:** Explain the ESS host intrusion prevention scope, the relationship to the OS STIG, and version changes.
- [DISA STIG downloads](https://www.cyber.mil/stigs/downloads/): Provides official STIG packages. Verify the required release before an assessment.
- [DISA SCAP resources](https://www.cyber.mil/stigs/SCAP): Lists separately distributed benchmarks. The firewall SCAP benchmark listed there is V2R3; it is not the same file or release as this manual V2R2 STIG. Confirm applicability, coverage, and your organization's approved version before using it.
- [STIG Viewer 3.x User Guide](https://dl.dod.cyber.mil/wp-content/uploads/stigs/pdf/U_STIG_Viewer_3-x_User_Guide_V1R7.pdf): Explains benchmark import and checklists.
- [Microsoft firewall logging](https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/configure-logging): Explains profile logging, paths, capacity, and permissions.
- [Microsoft active firewall profile settings](https://learn.microsoft.com/en-us/powershell/module/netsecurity/get-netfirewallprofile): Explains the ActiveStore view of effective profile settings.
- [Microsoft netsh advfirewall](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/netsh-advfirewall): Documents export and import of local firewall policy.

An official benchmark and the authorized assessor remain authoritative for individual findings and exceptions. Keep actual firewall exports, logs, and completed checklists private.
