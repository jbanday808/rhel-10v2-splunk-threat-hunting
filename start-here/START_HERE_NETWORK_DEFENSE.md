# START HERE — Passive Network Defense: Zeek, Wireshark, Suricata, YARA, Sigma and CMMC

**Project:** RHEL 10.2 Splunk Threat Hunting Lab · **Status:** Work in Progress (documentation, sample detection content and offline tooling only; no sensor VM deployed or live captures validated).

**[OPEN FULL 30-STEP INSTALLATION, CONFIGURATION, DEPLOYMENT & VALIDATION GUIDE](../docs/network-defense/IMPLEMENTATION_GUIDE.md)**

**[Open the complete 28-step Zeek installation and deployment guide](../docs/network-defense/ZEEK_DEPLOYMENT.md)** for pinned containers, policy configuration, offline testing, optional live sensing, Splunk forwarding, and rollback.

**[Run the worked HTTP investigation](../docs/network-defense/OFFLINE_HTTP_WALKTHROUGH.md)** using synthetic captures on an analysis workstation. The Splunk portion uses the existing `lab` index. Use the 30-step guide when planning an optional dedicated sensor.

**[Explore the optional Arkime guide](START_HERE_ARKIME.md)** for a separate sensor, offline packet import, Viewer investigation and explicit live-capture readiness checks. Arkime does not automatically forward its sessions to Splunk.

## Purpose

Extend the existing three-VM VMware lab with an **optional, isolated passive network analysis sensor** and a documented end-to-end workflow. Cover protocol analysis, network baselining, low-impact vulnerability discovery, Suricata IDS alert triage, Zeek telemetry, Splunk investigations, YARA file classification, Sigma-to-SPL detection engineering, incident reporting and **CMMC Level 2 evidence mapping**. The documentation is project-focused and contains no company/job advertisement.

## Lab architecture

| Asset | Lab IP | Role |
| --- | --- | --- |
| Windows 11 + Ubuntu WSL | Management adapter 172.25.250.1 | VS Code, Git, approved analyst workstation |
| RHEL-SPLUNK01 | 172.25.250.10 | Existing Splunk Enterprise/search/indexer and TLS receiver |
| WINHUNT01 | 172.25.250.20 | Existing Windows 11 Sysmon + Universal Forwarder |
| RHEL-IDM01 | 172.25.250.30 | Existing Red Hat IdM, DNS, LDAPS |
| **RHEL-SENSOR01 (optional NEW VM)** | **172.25.250.40** | RHEL 10.2; optional Zeek/Suricata/TShark/tcpdump; forwarder after review |
| VMnet8 NAT | 172.25.250.0/24 | Existing VMware NAT network; **not** a TAP/SPAN or guaranteed full traffic mirror |

**Critical visibility rule:** A VMnet8 peer cannot assume visibility of unicast flows between other VMs. Promiscuous capture alone does not configure virtual-switch port mirroring. Start with a **synthetic offline PCAP**, then consider a dedicated TAP/SPAN or a pre-approved mirrored virtual switch/port group. Never place a passive sensor inline or enable IPS/drop mode.

## Suggested workflow

1. Run source-only checks, review the [CONOPS](../docs/network-defense/CONOPS.md) and create backups/VM snapshots.
2. Build optional sensor with a separate security boundary; verify exact installed package availability.
3. Generate a harmless **synthetic PCAP** on the sensor/WSL, run Wireshark/TShark and validate protocols.
4. Run Zeek offline to produce connection/DNS/HTTP/TLS metadata.
5. Run Suricata offline in IDS mode, inspect EVE JSON and safely tune a sample detection.
6. Run **YARA against local authorized files**, not arbitrary network traffic; test with benign synthetic bytes.
7. Convert Sigma YAML to Splunk SPL using the supported backend; review fields and query before using.
8. Create optional `net_zeek`, `net_suricata`, and `net_yara` indexes separately from the existing six.
9. Forward approved sanitized JSON logs to Splunk only after reviewing TLS, source access and timestamps.
10. Establish baseline, investigate outliers and document findings with [evidence](../evidence/sanitized/network-defense-validation.md).
11. Map practices to **CMMC Level 2 / NIST SP 800-171 Revision 2** as illustrative support—not a completed 110-requirement assessment.

## Repository navigation

- [Full implementation guide](../docs/network-defense/IMPLEMENTATION_GUIDE.md)
- [Architecture and visibility limits](../docs/network-defense/ARCHITECTURE.md)
- [CONOPS and measures of performance](../docs/network-defense/CONOPS.md)
- [Tool-by-tool instructions](../docs/network-defense/README.md)
- [CMMC Level 2 and 800-171 evidence mapping](../docs/network-defense/CMMC_LEVEL2.md)
- [Detection testing and review](../docs/network-defense/DETECTIONS_AND_TESTING.md)
- [Risk, troubleshooting and rollback](../docs/network-defense/TROUBLESHOOTING.md)
- [Official references](../docs/network-defense/REFERENCES.md)
- [Sanitized evidence log](../evidence/sanitized/network-defense-validation.md)
- [Synthetic PCAP generator](../scripts/network-defense/generate_synthetic_pcap.py)
- [Safe JSON telemetry summary](../scripts/network-defense/summarize_network_logs.py)
- [Suricata example rule](../configs/network-defense/suricata/local.rules)
- [YARA synthetic fixture rule](../rules/yara/lab_marker.yar)
- [Sigma synthetic fixture rule](../rules/sigma/lab_network_dns_marker.yml)
- [Four SPL hunt examples](../hunts/network-defense/README.md)

**Scope and privacy:** Packet captures can contain secrets, personal data or sensitive system details. Work only on systems and traffic you own or are authorized to analyze. Keep PCAPs, raw event logs, extracted binaries, keys, CUI and classified information outside public GitHub, GitHub Actions, connected AI tools and unapproved cloud services. No live test is claimed until you complete and record it.
