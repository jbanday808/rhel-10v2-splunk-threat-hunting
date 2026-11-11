# 12 — Official Public References and Version Guidance

The following resources support **public lab alignment**. Always verify the current revisions, especially before using a control identifier, STIG package or vendor command.

| Reference | Purpose |
| --- | --- |
| [DoD Zero Trust Strategy (October 2022)](https://dodcio.defense.gov/Portals/0/Documents/Library/DoD-ZTStrategy.pdf) | Seven pillars, Target and Advanced goals, execution enablers |
| [DoD public strategy release](https://www.defense.gov/News/Releases/Release/Article/3225919/department-of-defense-releases-zero-trust-strategy-and-roadmap/) | Department's 2027 Target planning context |
| [DoD Zero Trust Strategy Buyers Guide (May 2025)](https://buy.gsa.gov/api/system/files/documents/dod-zero-trust-strategy-buyer-s-guide-version-1.4-may-2025-508-reviewed_0.pdf) | Public buyer and implementation planning |
| [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final) | No implicit trust, PDP/PEP, explicit subject/resource policies |
| [NIST SP 800-207A: Cloud-Native Access](https://csrc.nist.gov/pubs/sp/800/207/a/final) | Workload/service identity and cloud-native enforcement |
| [NIST SP 800-37 Rev. 2](https://csrc.nist.gov/pubs/sp/800/37/r2/final) | PREPARE, CATEGORIZE, SELECT, IMPLEMENT, ASSESS, AUTHORIZE, MONITOR |
| [NIST SP 800-53 Rev. 5](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) | Control catalog (actual applicability and enhancements must be reviewed) |
| [NIST SP 800-53B](https://csrc.nist.gov/pubs/sp/800/53/b/upd1/final) | Baseline selection and tailoring |
| [FIPS 199](https://csrc.nist.gov/pubs/fips/199/final) | System and information categorization under applicable authority |
| [CISA Zero Trust Maturity Model v2](https://www.cisa.gov/zero-trust-maturity-model) | Civilian federal maturity perspective (not the DoD seven pillars) |
| [Red Hat Enterprise Linux 10 firewalld guidance](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/configuring_firewalls_and_packet_filters/using-and-configuring-firewalld) | Runtime vs permanent rules, rich rules, zones |
| [DISA STIG library](https://public.cyber.mil/stigs/downloads/) | Official STIG/SRG content; verify applicable OS/version |
| [Splunk Enterprise Documentation](https://help.splunk.com/en/splunk-enterprise) | Native LDAP, authorization, TLS and service settings by installed version |
| [Microsoft Sysmon documentation](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon) | Endpoint telemetry behavior and configuration |

## Version and claim boundaries

- 2022 DoD Strategy is a public framework reference, **not a certificate** that a three-VM test lab meets 2027 Target capabilities.
- Host-based rules + directory groups + telemetry support Zero Trust design but are **not a complete policy engine / dynamic enforcement system**.
- OpenSCAP supports scanning when suitable benchmark content exists; do not assert RHEL 10 DISA STIG applicability until an exact matching benchmark is verified.
- Never claim an ATO, FedRAMP accreditation, or DoD certification in README or LinkedIn materials without actual authorized findings.
- Booz Allen R0242994 requirements informed the example portfolio scope; this is not a proprietary Booz Allen document.
