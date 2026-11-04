# START HERE — Zero Trust Architecture on RHEL 10.2 and Splunk

**Status: WORK IN PROGRESS — reference design and deployment instructions, not a production Zero Trust implementation or a DoD certification.**

This optional workstream extends the existing three-VM RHEL 10.2 Splunk lab. It is designed to demonstrate the **architecture, implementation, testing, and governance** skills described in the Booz Allen **ZT Engineer, Lead (R0242994, Honolulu)** job description, using publicly documented techniques. It is **not** a Booz Allen deliverable or a DoD operational system.

## Start with the complete implementation guide

➡️ **[Complete Step-by-Step Zero Trust Installation, Configuration, Deployment, Validation and Maintenance Guide](docs/zero-trust/IMPLEMENTATION_GUIDE.md)**

Also see [architecture and trust flows](docs/zero-trust/01-target-architecture.md), [seven DoD Zero Trust pillars](docs/zero-trust/02-dod-seven-pillars.md), [network policy](docs/zero-trust/06-network-microsegmentation.md), [RMF/STIG](docs/zero-trust/09-rmf-stig-ato.md), and [test/evidence plan](docs/zero-trust/10-verification-and-evidence.md).

| Lab system | Address | Role |
| --- | --- | --- |
| Windows 11 physical host + Ubuntu WSL | VMware host / management at 172.25.250.1 | VS Code, GitHub, controlled admin sessions |
| WINHUNT01 | 172.25.250.20 | Windows logs, Sysmon, Universal Forwarder |
| RHEL-SPLUNK01 | 172.25.250.10 | Splunk Enterprise, SIEM analytics, TLS receiver |
| RHEL-IDM01 | 172.25.250.30 | Red Hat IdM, DNS, LDAPS, group-based identity |
| VMnet8 | 172.25.250.0/24 | NAT lab segment; **not, by itself, Zero Trust segmentation** |

**Existing lab:** 52 numbered deployment procedures, 13 hunts, 7 appendices, Windows Forwarder, TLS, Splunk RBAC, and IdM. These are preserved.

**Proposed controls:** identity/group policy, tighter resource-specific allowlists, endpoint posture evidence, read-only policy checks, continuous monitoring, optional later SSO/MFA/device-aware access and ZTNA. No new product or service is implied to be installed.

**Scope warning:** Native Splunk LDAP authentication does **not** itself prove phishing-resistant MFA or continuous device posture. Host firewalls enforce static network rules, not a complete NIST policy engine / policy administrator / enforcement system. Target-level DoD maturity is **not** claimed.

**Do not commit:** passwords, LDAP bind secrets, TLS private keys, real threat intelligence tied to protected networks, raw event logs, or screenshots with identifiable/private information.

**Related:** [START_HERE_RHEL10v2.md](START_HERE_RHEL10v2.md) · [START_HERE_WSL.md](START_HERE_WSL.md) · [Original lab architecture](docs/architecture.md).

**Publishing:** Approved files are maintained on `main`; use reviewable feature branches for future additions.
