# Architecture — Separate Passive Sensor and Splunk Monitoring

## Existing three-VM lab + optional analysis VMs

The [Kali workstation guide](KALI_DEPLOYMENT.md) is an **alternative offline analysis path** for Wireshark, Zeek, Suricata, Arkime, YARA and Sigma. It does not make Kali a mirrored sensor, replace the proposed RHEL-SENSOR01, or change the three existing VMs.

~~~mermaid
flowchart TD
    H["Windows 11 host / VS Code + WSL\n172.25.250.1"]
    W["WINHUNT01\n172.25.250.20\nWindows logs and Sysmon"]
    S["RHEL-SPLUNK01\n172.25.250.10\nSplunk Enterprise"]
    I["RHEL-IDM01\n172.25.250.30\nDNS / LDAPS"]
    N["RHEL-SENSOR01 (PROPOSED)\n172.25.250.40\nZeek / Suricata / TShark"]
    K["Kali Linux VM (OPTIONAL)\nVMnet8 DHCP lease\nOffline analysis"]
    P["Authorized synthetic/offline PCAP\nPRIVATE location"]
    W -->|"Existing TLS forwarding TCP 9997"| S
    S -->|"Existing TLS LDAPS TCP 636"| I
    H -->|"Managed HTTPS TCP 8000"| S
    P -->|"Offline packet analysis"| N
    P -->|"Offline packet and rule analysis"| K
    N -.->|"Optional reviewed UF TLS 9997"| S
    M["Dedicated TAP/SPAN/mirror (NOT PROVIDED BY VMnet8)\nFUTURE / requires verification"] -.->|"Future passive packet feed"| N
    N -->|"local private JSON files"| L["Zeek logs / Suricata EVE"]
~~~

**Figure 1:** The optional RHEL sensor or Kali workstation can analyze private synthetic PCAPs; live mirroring and Splunk forwarding require separate validation.

## Why not assume the network sensor sees all traffic?

VMware Workstation's VMnet8 provides NAT and ordinary switching. A promiscuous interface can still miss unicast between other vNICs. Validated network visibility needs an approved capture point (TAP, SPAN/mirror, or carefully designed lab bridge/port group). Avoid altering the current VMnet8 topology just to make a diagram true.

## Deployment levels

| Level | What exists | Packet access | Risk |
| --- | --- | --- | --- |
| **Level 0** | Current Splunk / Windows / IdM systems | Existing endpoint/syslog only | Preserve as is |
| **Level 1** | New optional RHEL-SENSOR01 with synthetic local PCAP | Offline approved file only | Safe and reproducible |
| **Level 2** | Sensor sends selected metadata to Splunk | Only approved Zeek/Suricata JSON via UF/TLS | Parser/index/retention review needed |
| **Level 3** | Approved mirrored feed to sensor | Real authorized packets | CAPTURE APPROVAL; privacy, performance, loss and storage concerns |
| **Level 4** | Operational baseline, alerts and case workflows | Reviewed observations and authorized evidence | Requires ongoing analyst and owner governance |

## Network and identity boundaries

- Sensor management IP (if installed): `172.25.250.40` on VMnet8, chosen only after collision/availability check.
- Sensor to Splunk `172.25.250.10:9997/tcp` for optional UF forwarding; server CA/hostname verification and explicit firewall source allowlist required.
- No direct access from sensor to IdM administration, Splunk management API 8089, or protected workloads except approved analysis paths.
- Zeek and Suricata sensors remain passive: no AF_PACKET IPS copy-mode, NFQUEUE drop or blocking firewall policy.
- RHEL-SPLUNK01 remains search/index/receiver; do not install heavy packet-processing services on it.
- Split metadata indices `net_zeek`, `net_suricata` and `net_yara` are **proposed** additions; do not modify existing index retention until review.
- Packet captures and file extracts remain in **private encrypted storage** with access, retention and secure disposal plans.

## Protocol limitations

DNS, cleartext HTTP, SMB and TCP metadata may allow passive inference. Encrypted HTTPS/TLS limits application-content visibility; certificate metadata does **not** reveal protected content. You cannot confirm a patch-level CVE or all hosts affected solely from a port or banner. Validate findings with authorized system owners and configuration evidence; avoid active scanning on protected networks.
