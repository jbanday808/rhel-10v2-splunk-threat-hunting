# Trellix Product Overview — Customer Explanation and Consultant Checks

**Reviewed: November 8, 2026 (Hawaii).** This is a concise learning/reference guide based on public Trellix material. It does not claim deployment, certification, entitlement or hands-on mastery of these products in this lab. Confirm product edition, supported OS, agent/module version, management mode, license, lifecycle and approved connectivity for the actual customer. A marketing portfolio category is not an installed product.

## Core terms requested for the role

| Product / term | Short customer explanation | Example investigation use |
| --- | --- | --- |
| Endpoint Security (ENS) | Helps protect endpoints against malware and other threats through the configured protection modules. | Review the endpoint alert, prevention result and effective policy. |
| Application Control | Controls which applications are allowed to run. | Investigate a blocked or unexpectedly allowed program against the approved inventory. |
| Change Control | Protects designated files/configuration against unauthorized changes. | Review what changed, who initiated it and whether it matched an approved change. |
| Threat Intelligence Exchange (TIE) | Combines reputation information and makes it available to connected security products. | Compare reputation, first-seen context and the basis for a file verdict. |
| Data Exchange Layer (DXL) | Connects compatible tools so they can exchange security messages. | Check broker/client connectivity and whether an intended message reached its consumer. |
| Data Loss Prevention (DLP) | Helps detect and restrict unauthorized movement of sensitive information. | Review the policy match, data channel and approved exception context. |
| Endpoint Forensics (HX) | Collects endpoint evidence to support detailed investigations. | Examine an authorized acquisition, process history and related artifacts. |
| Intelligent Virtual Execution (IVX) | Analyzes suspicious content in a controlled analysis environment. | Review a submitted sample's job status, behavioral findings and analysis limitations. |

**Names that are easy to confuse:** ENS is the abbreviation for Trellix Endpoint Security, not a separate extra product. HX is associated with the Endpoint Forensics lineage; some technical documentation still calls its component Endpoint Security (HX). ENS, HX and EDR with Forensics are not interchangeable agent/version names. TIE supplies shared intelligence/reputation context; DXL supplies the communication framework. DLP protects data movement; encryption protects data confidentiality through cryptography. IVX results are analysis evidence, not a guarantee that a sample is safe or malicious in every environment.

Sources: [ENS overview](https://docs.trellix.com/docs/overview-of-trellix-endpoint-security-ens), [Application and Change Control](https://www.trellix.com/products/trellix-application-control/), [TIE](https://www.trellix.com/products/threat-intelligence-exchange/), [DXL guide](https://docs.trellix.com/data-and-email/docs/data-exchange-layer-6-0-x-product-guide), [DLP](https://www.trellix.com/products/dlp/), [HX](https://www.trellix.com/products/endpoint-forensics/), and [IVX analysis](https://docs.trellix.com/network-and-platform/docs/submitting-malware-to-the-virtual-machine-for-analysis).

## What to verify when consulting

These are analyst discovery and validation questions, not console commands or an assertion that every edition exposes the same fields.

| Area | Practical questions before recommending a change |
| --- | --- |
| ENS | Is the agent healthy? Which modules and policies are effective? Was an alert detected, prevented, quarantined or merely reported? Are exclusions approved? |
| Application Control | Is the expected inventory/policy applied? What operational mode is in use? Are trusted installers, update paths and exception owners documented? |
| Change Control | Which objects are protected? Was the modifying process authorized? Is there a change window and tested rollback for required maintenance? |
| TIE | Which source supplied the verdict? Is the reputation current? Who can override it, and what evidence/approval supports the override? |
| DXL | Are clients/brokers trusted and healthy? Are certificates, routing, service zones, permissions and message-delivery observations correct? |
| DLP | What classifier and policy fired? Was content actually blocked, permitted or monitored? Can the incident be reviewed without unnecessarily exposing the sensitive content? |
| HX | Is acquisition authorized and complete? Which OS/agent supports the collection? Are timestamps, tool versions, acquisition hashes, custody and access recorded? |
| IVX | Is sample submission permitted for this data/classification? Which analysis environment and job completed? Could timeouts, missing dependencies or evasive behavior limit the result? |

Across products, check logging/export fields, time synchronization, tenant/environment boundaries, roles, audit trails, retention and change/rollback. Review the customer's supported integration path before assuming that events appear in Splunk or that a response action is available.

## Related products in the supplied portfolio

| Product | Brief explanation |
| --- | --- |
| EDR with Forensics | Adds endpoint detection, investigation and supported response capabilities. |
| ePolicy Orchestrator (ePO) | Centralizes supported endpoint product and policy management. |
| Mobile Threat Defense | Helps assess threats affecting mobile devices, apps and connections. |
| Data Encryption | Protects information on enterprise devices and removable media. |
| Database Security | Helps monitor and protect sensitive database information. |
| Network Detection and Response (NDR) | Helps investigate suspicious activity across network traffic. |
| Intrusion Prevention System (IPS) | Detects and can block traffic matching configured prevention controls. |
| Network Security | Provides network threat inspection and prevention capabilities. |
| Network Forensics | Supports packet capture and later traffic investigation. |
| Insights | Helps prioritize relevant threats and campaigns. |
| SecondSight | A managed threat-hunting service. |
| Intelligence as a Service | Provides threat-intelligence expertise as a service. |
| Private Global Threat Intelligence | Supplies reputation intelligence through a private deployment option. |
| Advanced Threat Landscape Analysis System (ATLAS) | Explores global file, domain and IP threat detections. |
| Email Security | Helps protect email against phishing and malicious content. |
| Phishing Simulator | Supports authorized phishing-awareness simulations. |
| IVX for Collaboration Platforms | Examines content shared through supported collaboration tools. |
| IVX for Enterprise Applications | Examines content shared through supported business applications. |
| Helix | Brings security context together for investigation and response. |
| Hyperautomation | Connects and automates approved security workflows. |
| Enterprise Security Manager (ESM) | A SIEM for collecting and analyzing security events. |

Sources: [Trellix portfolio](https://www.trellix.com/products/), [EDR with Forensics](https://www.trellix.com/products/edrf/), [ePO](https://www.trellix.com/products/epo/), [NDR](https://www.trellix.com/products/network-detection-and-response/), [ATLAS](https://www.trellix.com/products/advanced-threat-landscape-analysis-system/), [IVX Collaboration](https://www.trellix.com/products/collaboration/), [IVX Enterprise Applications](https://www.trellix.com/products/enterprise-application-security/), [Helix](https://www.trellix.com/products/helix/), and [ESM](https://www.trellix.com/products/enterprise-security-manager/).

Endpoint, data, network, threat-intelligence, email and security-operations **Solutions** labels group related offerings. Do not assume overlapping products are identical or that deploying one enables another. Check [current lifecycle information](https://www.trellix.com/support/end-of-life-products/) and product-specific compatibility before designing an implementation.

## A short customer explanation

“ENS helps protect the device, Application and Change Control govern trusted software and protected changes, and DLP helps protect sensitive information. TIE shares reputation context through compatible integrations such as DXL. HX supports deeper endpoint investigation, while IVX analyzes suspicious content in a controlled environment. We verify the evidence and your operational needs before recommending a response.”

## Example incident workflow

An endpoint alert becomes a case. The analyst checks the actual prevention outcome, available endpoint evidence, relevant reputation and network context. The incident owner decides whether an authorized collection, isolation or other response is needed. The administrator executes the approved action and verifies its effect; the forensic analyst records evidence and the owner verifies recovery.

Keep **file quarantine** separate from **host network isolation**. The available action, authority, management connectivity and restoration path depend on the licensed product/version and policy. Trellix's [EDRF containment documentation](https://docs.trellix.com/docs/unified-quarantine-and-containment-in-edrf) describes version-specific behavior; do not infer it for every installation. Neither a reputation verdict nor an AI recommendation authorizes the action.
