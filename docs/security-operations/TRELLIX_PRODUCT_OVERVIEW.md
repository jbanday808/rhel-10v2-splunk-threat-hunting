# Trellix Product Overview

Trellix offers cybersecurity products that help organizations protect computers, sensitive information, networks, and email. These products also help security teams investigate suspicious activity and respond when a threat is found.

This guide explains each product in terms you can use when speaking with a customer.

**Project status:** This is a learning and customer-explanation reference. The lab does not include a validated Trellix deployment or customer engagement. Available features depend on the customer's product, version, license, and configuration.

## 1. Protecting computers and mobile devices

These products help protect and manage the devices employees use for work.

- **Trellix Endpoint Security (ENS):** Helps protect computers and servers from malicious software and other threats. For example, it can detect and quarantine a suspicious file.
- **Trellix EDR with Forensics:** Helps security teams identify suspicious activity on a device, investigate what happened, and take supported response actions.
- **Trellix Endpoint Forensics (HX):** Helps investigators collect and examine information from devices to understand what happened and whether other systems were affected.
- **Trellix Application Control:** Helps ensure that only approved applications are allowed to run on protected devices.
- **Trellix Change Control:** Helps prevent unauthorized changes to important files and system settings.
- **Trellix Mobile Threat Defense:** Helps identify threats affecting mobile devices, their applications, and the networks they use.
- **Trellix ePolicy Orchestrator (ePO):** Gives administrators a central place to manage supported Trellix products, security settings, and alerts.

**A helpful distinction:** ENS is short for Trellix Endpoint Security. Endpoint Forensics (HX) and EDR with Forensics are distinct offerings; some Trellix documentation also uses the name *Endpoint Security (HX)* for an HX component.

## 2. Protecting sensitive information

These products help organizations control and protect important information.

- **Trellix Data Loss Prevention (DLP):** Helps prevent sensitive information from being shared or removed without authorization. For example, it can help prevent a confidential document from being copied to an unapproved USB drive.
- **Trellix Data Encryption:** Protects information by making it unreadable to people who do not have the proper access. This can help protect information if a laptop or storage device is lost.
- **Trellix Database Security:** Helps monitor and protect sensitive information stored in databases, such as customer or employee records.

## 3. Protecting the network

These products help security teams identify and investigate suspicious activity across an organization's network.

- **Trellix Network Detection and Response (NDR):** Helps identify unusual network activity and gives security teams information to investigate it.
- **Trellix Intrusion Prevention System (IPS):** Examines network traffic and can block certain threats before they reach their destination.
- **Trellix Network Security:** Provides network protection capabilities that help detect and prevent suspicious or malicious traffic.
- **Trellix Network Forensics:** Helps investigators review recorded network activity to understand how a threat communicated or moved through the network.

**A helpful distinction:** NDR helps the security team find and investigate suspicious activity. IPS is designed to detect and block certain threats. Their capabilities can overlap depending on the products in use.

## 4. Understanding threats

Threat intelligence is information about known or emerging threats. These products and services help organizations use that information to make security decisions.

- **Trellix Threat Intelligence Exchange (TIE):** Brings together information about whether files may be trustworthy or harmful and makes that information available to compatible security tools.
- **Trellix Data Exchange Layer (DXL):** Helps compatible security tools communicate and share information. For example, it can help a product request information from TIE about a suspicious file.
- **Trellix Insights:** Helps organizations understand which threats may be relevant to them and decide where to focus their security efforts.
- **Trellix SecondSight:** A threat-hunting service where Trellix specialists help look for suspicious activity that may require further investigation.
- **Trellix Intelligence as a Service:** Gives customers access to threat-intelligence expertise and information tailored to their needs.
- **Trellix Private Global Threat Intelligence:** Provides threat information to supported Trellix products through a private deployment option.
- **Trellix Advanced Threat Landscape Analysis System (ATLAS):** Helps customers explore information about malicious files, websites, and internet addresses identified around the world.

**A helpful distinction:** TIE provides information about a potential threat, while DXL helps compatible tools share that information.

## 5. Protecting email and shared content

These products help organizations identify threats that arrive through email or are shared through business applications.

- **Trellix Email Security:** Helps protect email against phishing, malicious attachments, and other suspicious messages.
- **Trellix Phishing Simulator:** Helps organizations train employees by sending approved practice messages that imitate phishing attempts.
- **Trellix Intelligent Virtual Execution (IVX):** Examines suspicious content in a controlled environment to help determine whether it behaves like a threat.
- **Trellix IVX for Collaboration Platforms:** Helps identify malicious files and links shared through supported collaboration tools.
- **Trellix IVX for Enterprise Applications:** Helps identify malicious files shared through supported business applications.

For example, if an unfamiliar attachment requires further investigation and submission is permitted, IVX can help the security team observe its behavior in a controlled environment. The team then reviews the results alongside other evidence.

## 6. Supporting security operations

These products help security teams bring information together and coordinate their work.

- **Trellix Helix:** Brings security information from different sources together to help analysts investigate and respond to threats.
- **Trellix Hyperautomation:** Helps automate approved security tasks and coordinate actions across compatible tools.
- **Trellix Enterprise Security Manager (ESM):** Collects and analyzes security information from multiple systems so analysts can identify and investigate suspicious activity.

## Example: How the products can work together

Imagine an employee receives a suspicious email attachment:

1. **Email Security** may identify or block the suspicious message before the employee opens it.
2. If the attachment reaches the employee's computer, **Endpoint Security** may detect and quarantine the file.
3. If further investigation is needed, the security team can use **EDR with Forensics** or **Endpoint Forensics** to review activity on the computer.
4. **TIE** can provide information about the file, while **IVX** may examine its behavior in a controlled environment if the customer permits the submission.
5. Based on the evidence and the organization's approval process, the security team can remove the threat or temporarily isolate the computer from the network.

Quarantining a file restricts that file. Isolating a computer restricts the computer's network access. The products and response options available depend on what the customer has purchased and configured.

## Questions to ask a customer

Before recommending a product or change, ask:

- What devices and information are most important to your organization?
- Which security products do you already use, and are they working as expected?
- What should happen when a threat is detected, and who approves the response?
- Where can security information be stored, and who is allowed to access it?

## Short customer explanation

> “Trellix provides tools that help protect your devices, sensitive information, network, and email. If suspicious activity occurs, these tools can give your security team the information it needs to investigate and respond. We'll work with you to understand your environment and identify the protections that best support your organization.”

## References

- [Trellix Products](https://www.trellix.com/products/): Provides an overview of Trellix products and services by security category.
- [How EDR with Forensics Works](https://docs.trellix.com/docs/how-edrf-works): Explains how supported Trellix products can work together to investigate and respond to threats.
- [Trellix Product Documentation](https://docs.trellix.com/): Provides product-specific guides and technical information.
- [Endpoint Forensics Bridge Product Guide](https://docs.trellix.com/docs/endpoint-forensics-bridge-product-guide): Explains the HX naming and its relationship to EDR and ePO.
- [Submitting File Samples to IVX](https://docs.trellix.com/docs/submitting-file-samples-to-intelligent-virtual-execution-ivx): Explains the controlled analysis of suspicious files and related submission conditions.
