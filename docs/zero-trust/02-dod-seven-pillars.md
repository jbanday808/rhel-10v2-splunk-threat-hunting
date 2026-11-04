# 02 — DoD Zero Trust Seven-Pillar Mapping

Source: [DoD Zero Trust Strategy](https://dodcio.defense.gov/Portals/0/Documents/Library/DoD-ZTStrategy.pdf), October 2022. It describes **seven pillars**, **45 capabilities**, and Target vs Advanced activity levels. The lab implements only selected **building blocks**, not all DoD Target activities.

| Pillar | Existing lab/source components | This workstream | Remaining gap |
| --- | --- | --- | --- |
| **1. User** | IdM account/group design, verified LDAPS, Splunk \`lab_hunter\` and \`admin\` roles | Group audit, least privilege, denied-auth tests, emergency access | Dynamic identity risk, integrated MFA, continuous reauthentication |
| **2. Device** | Windows Sysmon, Defender, Windows firewall, RHEL SELinux/auditd | Device inventory and posture checks, event telemetry | Continuous attestation, UEM/MDM, managed compliance policy |
| **3. Application & Workload** | Splunk app, TLS listeners, service accounts, Linux service controls | Resource-specific app privileges, version inventory, change control | Policy-aware service identity and fine-grained workload authorization |
| **4. Data** | Six Splunk indexes, TLS certificates and redaction examples | Limit index read permission, establish retention/secret controls | Formal data classification, labeling and policy enforcement |
| **5. Network & Environment** | VMware VMnet8 NAT and source-based \`firewalld\` rules | Verify and narrow explicit flows, test denied connections | Dynamic microsegmentation, SDN-backed enforcement, verified east–west zoning |
| **6. Automation & Orchestration** | GitHub Actions source checks, existing Azure OIDC sample workflows | Policy-as-code **static validation**, review gates and human approval | Central dynamic PDP/PA, controlled SOAR orchestration |
| **7. Visibility & Analytics** | Splunk Enterprise, 13 SPL hunts, Linux+Windows logs | Additional ZT-focused detections, gaps/latency/evidence reporting | Correlation with IdP/ZTNA device signals and operational response workflows |

**Execution enablers:** governance, policy, training, personnel and change management. Treat these as required organizational capabilities, not software deployments.

## Demonstrating the job-role capabilities

| Booz Allen R0242994 qualification area | GitHub evidence |
| --- | --- |
| Enterprise network and ZT architecture | [01 architecture](01-target-architecture.md), flow matrix, source diagrams |
| IAM and protected resources | [04 identity](04-identity-and-access.md), verified LDAP and Splunk RBAC evidence |
| Network/security engineering, microsegmentation | [06 network](06-network-microsegmentation.md), safe firewall migration and deny tests |
| Endpoint security | [05 endpoints](05-endpoint-security.md), RHEL/Windows posture and logging |
| Multi-vendor integration | [11 operations](11-migration-and-operations.md), interfaces/gap table; no vendor products falsely claimed installed |
| RMF/STIG, audit/ATO support | [09 RMF](09-rmf-stig-ato.md), SSP/POA&M/evidence plan; ATO not claimed |
| Automation/policy as code | \`configs/zero-trust/allowed-flows.example.json\`, validator and tests |
| Detection and continuous monitoring | Splunk searches and monitoring evidence |
| Mission and operations leadership | Migration stages, explicit approval/rollback, customer requirement mapping |

### Note on maturity

The DoD strategy's Target-Level goal is for Department-wide programs, not a badge earned by a small lab. Do not describe this project as “DoD Target Compliant” or as a certified Zero Trust deployment.
