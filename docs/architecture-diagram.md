# VMware Splunk Threat Hunting Lab architecture

The diagram shows the **planned** connections; verify actual flows in your VMs.

```mermaid
flowchart LR
    A[Windows 11 Host with VMware and VS Code WSL]
    W[WINHUNT01 Windows 11 172.25.250.20]
    S[RHEL-SPLUNK01 RHEL 10.2 172.25.250.10]
    I[RHEL-IDM01 RHEL 10.2 172.25.250.30]
    G[VMnet8 NAT 172.25.250.2]
    W -->|TLS Forwarding TCP 9997| S
    S -->|LDAPS TCP 636| I
    S -->|DNS| I
    A -->|Lab access VMnet8| S
    A -->|Lab access VMnet8| W
    S --> G
    I --> G
    W --> G
```

Splunk Web uses HTTPS TCP 8000. Windows sends logs using the Universal Forwarder; Sysmon produces endpoint telemetry. RHEL IdM provides identity and verified LDAPS access. A GitHub-hosted Actions runner does not directly reach this private VMware subnet.
