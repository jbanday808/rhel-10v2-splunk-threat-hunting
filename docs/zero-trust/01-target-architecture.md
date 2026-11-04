# 01 — Architecture, Resource Flows and Zero Trust Decisions

## Current documented three-VM architecture

```mermaid
flowchart LR
  H["Windows 11 host / VS Code + Ubuntu WSL<br/>Management host adapter .1"]
  W["WINHUNT01 .20<br/>Sysmon + Universal Forwarder"]
  S["RHEL-SPLUNK01 .10<br/>Splunk Web + Indexer + Search"]
  I["RHEL-IDM01 .30<br/>Red Hat IdM DNS / LDAPS"]
  G["GitHub repository<br/>source & documentation"]
  W -->|"TLS TCP 9997: event forwarding"| S
  H -->|"HTTPS TCP 8000: approved browser"| S
  S -->|"LDAPS TCP 636: lookup"| I
  S -->|"DNS TCP/UDP 53"| I
  H -->|"Git & reviewed docs"| G
```

All VM addresses are on VMware VMnet8 `172.25.250.0/24`; gateway `172.25.250.2`. The network provides NAT isolation from other networks **but does not automatically prevent lateral movement among VMnet8 peers**.

**Existing implementation statements require live verification.** The diagram illustrates the lab's documented intended data flows, not verified network captures or DoD compliance.

## Proposed phased Zero Trust architecture

```mermaid
flowchart TD
  U["Human / service identity"] --> PE["Policy evaluation<br/>Future ZTNA/IdP: NOT DEPLOYED"]
  P["Device posture and risk<br/>Sysmon/Defender/RHEL checks"] -. "proposed signal" .-> PE
  D["IdM groups + managed identities"] -. "identity signal" .-> PE
  PE -->|"future allow/deny decision"| EP["Policy enforcement<br/>ZTNA gateway: NOT DEPLOYED"]
  EP -->|"resource access only"| S["Splunk Web / API resource"]
  FW["Current local enforcement:<br/>firewalld + Splunk roles"] --> S
  W["WINHUNT01: logs via verified TLS"] --> S
  S --> SIEM["Splunk analytics + audit evidence"]
  I["IdM LDAPS service"] --> S
  PE -. "not connected today" .-> SIEM
```

This separates **design target** (dynamic policy decision point and enforcement point, MFA and device posture) from **current measures** (firewall rules, native LDAP role mapping, verified TLS and SIEM). Under NIST SP 800-207, a true policy engine and policy administrator decide and orchestrate requests across resources; simply labeling Splunk a PDP would be inaccurate.

## Trust boundaries and enforcement locations

| Boundary | Decision signal | Actual or proposed enforcement | Status |
| --- | --- | --- | --- |
| Human → Splunk Web | Group membership, authenticated session | Splunk RBAC; source-limited firewalld | Existing configuration, requires tests |
| Windows VM → indexer | Forwarder TLS certificate, network source | Splunk TLS receiver + host firewall | Configured source, requires tests |
| Splunk → directory | Trusted IdM CA, LDAP bind access | LDAPS server + Splunk LDAP role map | Documented source, requires tests |
| Data → index | Index + role permissions | Splunk role, index grants, retention | Documented source, requires tests |
| Device trust → app | Posture, MFA, identity risk | Approved IdP/ZTNA policy | **Not deployed** |
| Automation → endpoint | Explicit approvals and risk | Future policy administrator / SOAR | **Not deployed** |

## Migration priorities

Begin by shrinking allowed flows and identities around **one resource**: Splunk Web, not by declaring the whole VMnet8 subnet trusted. Preserve administrator console break-glass access. Record which services depend on DNS, IdM and updates before applying restrictive egress controls.

## Architecture acceptance criteria

- Resource-by-resource connectivity matrix, user role matrix and data sensitivity approved.
- Both allowed and denied accesses actually tested and logged.
- Recovery after policy change demonstrated.
- Optional MFA/device posture/ZTNA is marked absent until independently implemented and assessed.
