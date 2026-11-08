# RHEL 10.2 Splunk threat hunting lab with LDAP NGINX redaction HEC and Azure OIDC

Build a VMware learning lab with RHEL Splunk Enterprise, a Windows 11 hunting endpoint, and a RHEL IdM directory. The source package includes the complete procedures and assembled custom files.

**Start with VS Code + WSL on Windows 11:** [START_HERE_WSL.md](START_HERE_WSL.md) and the [complete WSL publishing guide](docs/WSL_VSCODE_GITHUB_UPLOAD_GUIDE.md).

For RHEL 10.2 lab installation, configuration, and validation, see **[START_HERE_RHEL10v2.md](START_HERE_RHEL10v2.md)**.

For a Windows-only alternative, see [START_HERE_WINDOWS.md](START_HERE_WINDOWS.md).

**Troubleshooting Windows forwarding:** [TLS handshake and KV service step-by-step guide](docs/troubleshooting/splunk-forwarder-tls-and-kv-service.md) covers the reported TCP 9997 error, effective UF settings, certificate checks, event delivery, and separate KV startup warnings. The cause and live resolution remain unverified.

**New RHEL 10.2 STIG hardening and SCAP assessment (V1R1):** [START_HERE_RHEL10v2_STIG.md](START_HERE_RHEL10v2_STIG.md) · [Full 26-Step STIG Implementation Guide](docs/stig-rhel10/IMPLEMENTATION_GUIDE.md) · [Uploaded Benchmark Metadata](docs/stig-rhel10/BENCHMARK_METADATA.md). Includes 396-rule inventory tooling, controlled non-remediating OpenSCAP scans, risk-aware remediation, POA&M and sanitized evidence. **No live systems are scanned or modified by GitHub files.**

**Optional Windows 11 STIG V2R11 workstream (WIP):** [Start here](START_HERE_WINDOWS11_STIG.md) · [34-step guide](docs/stig-windows11/IMPLEMENTATION_GUIDE.md) · [257-rule reference](docs/stig-windows11/RULE_INDEX.md). Covers WINHUNT01 assessment, careful remediation, recovery, and monitoring validation.

**Optional Windows Defender Firewall STIG V2R2 workstream (WIP):** [Start here](START_HERE_WINDOWS_FIREWALL_STIG.md) · [32-step guide](docs/stig-windows-firewall/IMPLEMENTATION_GUIDE.md) · [21-rule reference](docs/stig-windows-firewall/rules/all.md). Confirm applicability, preserve required connections, and keep assessment results private.

**Optional ESS ePO 5.x STIG V3R8 workstream:** [Start here](START_HERE_EPO_STIG.md) · [Complete assessment and hardening guide](docs/stig-epo/IMPLEMENTATION_GUIDE.md). Includes a private rule-by-rule workbook generator and CUI handling guidance. The supplied overview identifies server scope through ePO 5.9x; confirm applicability for other versions.

**New optional workstream — DoD-aligned Zero Trust Architecture (WIP):** [START_HERE_ZERO_TRUST.md](START_HERE_ZERO_TRUST.md) · [Complete installation/configuration/deployment guide](docs/zero-trust/IMPLEMENTATION_GUIDE.md) · [Seven DoD Zero Trust pillars and role mapping](docs/zero-trust/02-dod-seven-pillars.md). These files document proposed controls and testing; they do **not** deploy a central ZTNA/PDP or certify DoD Target Level.

**New passive network defense workstream (WIP):** [START_HERE_NETWORK_DEFENSE.md](START_HERE_NETWORK_DEFENSE.md) · [Complete 30-Step Deployment Guide](docs/network-defense/IMPLEMENTATION_GUIDE.md) · [CONOPS](docs/network-defense/CONOPS.md) · [Zeek/Wireshark/TShark](docs/network-defense/ZEEK_AND_WIRESHARK.md) · [Suricata](docs/network-defense/SURICATA.md) · [YARA/Sigma](docs/network-defense/YARA_AND_SIGMA.md) · [CMMC Level 2 evidence planning](docs/network-defense/CMMC_LEVEL2.md). **Offline synthetic PCAPs first; no live sensor or CMMC certification claimed.**

**MITRE ATT&CK threat hunting:** [Start here](docs/mitre-attack/README.md) · [Technique and telemetry mapping](docs/mitre-attack/coverage.md) · [Navigator layer](docs/mitre-attack/navigator-layer.json) · [Hunt playbook](docs/mitre-attack/hunt-playbook.md). Candidate searches, context-only signals, and telemetry gaps are distinguished; no detection is claimed as validated until tested.

**Information Assurance Vulnerability Management (IAVM):** [IAVM home](docs/iavm/README.md) · [Splunk Enterprise notice 2026-A-1195](docs/iavm/notices/2026-A-1195.md). The user-provided notice and vendor advisory differences are documented; lab applicability and remediation are unverified.


**Existing GitHub repository:** [jbanday808/rhel-10v2-splunk-threat-hunting](https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting). Do **not** create a duplicate repository. The provided ZIP omits `LICENSE` so the MIT license in GitHub is preserved.

## Guides

- [Complete Word guide](docs/RHEL_10_2_Splunk_Complete_Guide_with_LDAP.docx)
- [Complete text guide](docs/RHEL_10_2_Splunk_Complete_Guide_with_LDAP.md)
- [All 52 numbered steps](docs/steps/README.md)
- [Detailed appendices](docs/appendices/README.md)
- [Complete Zeek, Wireshark, Suricata, YARA, Sigma and CMMC Network Defense Guide](docs/network-defense/IMPLEMENTATION_GUIDE.md)
- [Worked passive HTTP investigation with Splunk](docs/network-defense/OFFLINE_HTTP_WALKTHROUGH.md)
- [Deployment order](docs/deployment-order.md)
- [Zero Trust architecture — installation, configuration, deployment, RMF/STIG and testing](docs/zero-trust/README.md)
- [RHEL 10.2 DISA STIG V1R1 — Complete Installation, Assessment and Safe Hardening Guide](docs/stig-rhel10/IMPLEMENTATION_GUIDE.md)
- [Windows 11 STIG V2R11 — Complete Assessment and Hardening Guide](docs/stig-windows11/IMPLEMENTATION_GUIDE.md)
- [Windows Defender Firewall STIG V2R2 — Complete Assessment and Hardening Guide](docs/stig-windows-firewall/IMPLEMENTATION_GUIDE.md)
- [ESS ePO 5.x STIG V3R8 — Complete Assessment and Hardening Guide](docs/stig-epo/IMPLEMENTATION_GUIDE.md)
- [Vendor software and generated files](docs/downloads.md)

## Lab systems

| System | Address | Purpose |
| --- | --- | --- |
| RHEL-SPLUNK01 | 172.25.250.10 | Indexing, searches, TLS receiver, local NGINX test |
| WINHUNT01 | 172.25.250.20 | Windows logs, Sysmon, Universal Forwarder |
| RHEL-IDM01 | 172.25.250.30 | IdM directory, DNS, LDAPS |
| RHEL-SENSOR01 (optional, not installed) | 172.25.250.40 | Proposed passive PCAP/Zeek/Suricata processing on a separate VM |
| VMnet8 gateway | 172.25.250.2 | NAT outbound access |

## Included source

| Folder | Contents |
| --- | --- |
| apps | Server and forwarder apps plus NGINX local input overlay |
| configs | Linux logging, NGINX, redaction, HEC, systemd, and PKI examples |
| scripts/rhel | Storage, logging, backup, verification, NGINX, redaction, and HEC helpers |
| scripts/windows | Endpoint setup and read-only source validation |
| scripts/azure | Cloud Shell OIDC identity setup |
| sysmon | Lab XML rules |
| hunts | Hunting, redaction, HEC, and data-health searches |
| hunts/mitre-attack | Hypothesis-driven SPL and an optional Defender XDR KQL example |
| docs/mitre-attack | ATT&CK mapping, Navigator layer, hunt methodology, and visibility gaps |
| docs/iavm | User-provided vulnerability notice, vendor references, and assessment guidance |
| tests | Offline dummy redaction, safe merge, and HEC sender checks |
| docs/zero-trust, configs/zero-trust and scripts/zero-trust | DoD-aligned Zero Trust design, source-limited policy examples, offline checks and evidence templates (optional WIP) |
| docs/stig-rhel10 and scripts/stig | User-provided V1R1 benchmark documentation, offline rule inventory, private read-only assessment and result summarizer (WIP) |
| docs/stig-windows11 | Windows 11 V2R11 manual assessment guide and complete 257-rule reference (WIP) |
| docs/stig-windows-firewall | Firewall V2R2 manual assessment guide and complete 21-rule reference (WIP) |
| docs/stig-epo and scripts/stig-epo | Optional ePO V3R8 assessment workflow and private rule workbook generator |
| docs/network-defense, scripts/network-defense | Passive network analysis CONOPS, 30-step guide, synthetic PCAP and aggregate JSON tools |
| rules/yara, rules/sigma, hunts/network-defense | Benign YARA/Sigma test rules and proposed network SPL hunts |
| configs/network-defense, apps/SENSOR_UF | Proposed Suricata IDS rule and Splunk indexes/UF overlays, not deployed |
| docs | Full guide, WSL publishing guide, steps, appendices, architecture, and sanitized LDAP examples |
| evidence/sanitized | Validation and investigation records |
| .github/workflows | Linux/Windows source checks and two manual Azure OIDC workflows |
| .github/instructions and .github/prompts | VS Code / GitHub Copilot project rules and prompt templates |
| tools | Publication preflight and repository support checks |
| screenshots | 22 user-supplied lab screenshots; review before public use |

## Source validation

On RHEL or WSL: `python3 scripts/validate_project.py`. Add `--verify-manifest` before editing the downloaded release to verify initial file hashes.

On Windows: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\windows\Test-Project.ps1`. Add `-VerifyManifest` for the initial release.

Run `python3 -B -m unittest discover -s tests -v` on RHEL or WSL for the offline behavior checks.

The source-check workflow runs on push and pull request. The OIDC workflows are manual and need the separate Azure trust setup. No workflow deploys directly into private VMnet8.

## Results

[Validation templates](evidence/sanitized/validation.md) start at Pending. Record actual observed results and sanitized screenshots after each live test. The sample NGINX record is example data.

## Local settings

The official NGINX add-on is installed separately. Apply `apps/Splunk_TA_nginx/local/inputs.conf` after installation. The packaged lab index enables data integrity for new data. The LAB_SIEM app includes the dedicated identity redaction source; follow that appendix to prepare its source file and verify stored events. The HEC settings are examples to merge separately, with tokens created only on your server. LDAP passwords, TLS keys, Azure session tokens, installers, backups, and raw evidence stay outside the repository.

## Repository publication

To publish using VS Code + WSL, open [START_HERE_WSL.md](START_HERE_WSL.md).
Actual VM results remain in the `Pending` status until observed and verified. The 22 screenshots were supplied by the project author; review them individually for private information before committing.
