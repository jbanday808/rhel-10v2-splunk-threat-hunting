# RHEL 10.2 Splunk Threat Hunting Lab

This VMware lab combines Splunk Enterprise on RHEL 10.2, a Windows 11 endpoint, and Red Hat IdM for security monitoring and threat-hunting exercises. The repository contains procedures and configuration examples. Optional network sensors, STIG assessments, and other extensions remain work in progress; published files do not prove a live deployment or completed assessment.

## Start here

| Goal | Guide |
| --- | --- |
| Work in VS Code and WSL | [WSL quick start](start-here/START_HERE_WSL.md) · [Publishing guide](docs/reference/WSL_VSCODE_GITHUB_UPLOAD_GUIDE.md) |
| Build the core lab | [RHEL and Splunk](start-here/START_HERE_RHEL10v2.md) · [Windows alternative](start-here/START_HERE_WINDOWS.md) |
| Assess RHEL 10.2 | [RHEL STIG V1R1](start-here/START_HERE_RHEL10v2_STIG.md) |
| Assess Windows 11 | [Windows 11 STIG V2R11](start-here/START_HERE_WINDOWS11_STIG.md) |
| Assess Windows Firewall | [Defender Firewall STIG V2R2](start-here/START_HERE_WINDOWS_FIREWALL_STIG.md) |
| Assess an authorized ePO server | [ESS ePO 5.x STIG V3R8](start-here/START_HERE_EPO_STIG.md) |
| Plan Zero Trust controls | [Zero Trust guide](start-here/START_HERE_ZERO_TRUST.md) |
| Analyze network activity | [Kali workstation setup](docs/network-defense/KALI_DEPLOYMENT.md) · [Passive network defense](start-here/START_HERE_NETWORK_DEFENSE.md) · [Arkime sensor](start-here/START_HERE_ARKIME.md) |

[Browse all ten start guides](start-here/README.md).

## Project documentation

- [Complete 52-step deployment index](docs/steps/README.md) · [Full Markdown guide](docs/reference/RHEL_10_2_Splunk_Complete_Guide_with_LDAP.md) · [Word guide](docs/reference/RHEL_10_2_Splunk_Complete_Guide_with_LDAP.docx)
- [Optional appendices](docs/appendices/README.md) · [Reference files](docs/reference/README.md) · [Software downloads](docs/reference/downloads.md) · [Deployment order](docs/reference/deployment-order.md)
- [MITRE ATT&CK hunting](docs/mitre-attack/README.md) · [Cobalt Strike-associated hunt and safe Atomic validation](hunts/cobalt-strike/COBALT_STRIKE_ATOMIC_VALIDATION.md)
- [Kali Wireshark, Zeek, Suricata, Arkime, YARA and Sigma setup](docs/network-defense/KALI_DEPLOYMENT.md) · [Network defense](docs/network-defense/README.md) · [Complete RHEL Zeek deployment](docs/network-defense/ZEEK_DEPLOYMENT.md) · [RHEL Arkime installation and investigation](docs/arkime/IMPLEMENTATION_GUIDE.md)
- [Incident management, hunt reports, and AI-assisted forensic review](docs/security-operations/README.md) · [Trellix product overview](docs/security-operations/TRELLIX_PRODUCT_OVERVIEW.md)
- [IAVM guidance](docs/iavm/README.md) · [IdM setup troubleshooting](docs/troubleshooting/idm-installation-and-dns.md) · [Windows forwarding troubleshooting](docs/troubleshooting/splunk-forwarder-tls-and-kv-service.md) · [Windows test-account troubleshooting](docs/troubleshooting/windows-powershell-cmd-credentials.md)

## NIST AI RMF and security governance (proposed extension)

The [NIST AI RMF implementation guide](docs/ai-rmf/IMPLEMENTATION_GUIDE.md) and [AI risk governance documentation](docs/ai-rmf/README.md) describe an **optional future, read-only, human-reviewed AI-assisted Splunk alert summarizer**. This is a **Work in Progress**: no model is deployed, no AI test outcomes are asserted, and no security categorization or Authorization to Operate is granted. The documentation connects AI RMF `GOVERN/MAP/MEASURE/MANAGE` with SP 800-37 `PREPARE/CATEGORIZE/SELECT/IMPLEMENT/ASSESS/AUTHORIZE/MONITOR` and illustrative SP 800-53 controls.

## Lab systems

| System | Role |
| --- | --- |
| RHEL-SPLUNK01 | Splunk Enterprise, security searches, and TLS receiver |
| WINHUNT01 | Windows event collection, Sysmon, and Universal Forwarder |
| RHEL-IDM01 | IdM directory, DNS, and LDAPS |
| RHEL-SENSOR01 (optional; not installed) | Proposed passive network sensor and Arkime exercises |

The core Splunk indexes are `win_security`, `win_system`, `powershell`, `sysmon`, `linux`, and `lab`. The optional sensor does not automatically send Arkime sessions to Splunk.

## Repository layout

| Folder | Contents |
| --- | --- |
| [start-here](start-here/README.md) | Ten quick-start and workstream guides |
| [docs](docs/steps/README.md) | Detailed steps, appendices, STIGs, network and security-operations guides |
| [docs/reference](docs/reference/README.md) | Complete guide, architecture, templates, configuration examples, and publication notes |
| [apps](apps/) and [configs](configs/) | Splunk apps and reviewed configuration examples |
| [hunts](hunts/), [rules](rules/), and [scripts](scripts/) | Searches, detection examples, and lab helpers |
| [evidence/sanitized](evidence/sanitized/) and [screenshots](screenshots/) | Pending result templates and author-supplied images that require review |

## Validate and publish

From the repository root on RHEL or WSL, run:

```bash
python3 scripts/validate_project.py
python3 -B -m unittest discover -s tests -v
python3 tools/publication_preflight.py
```

These are source checks. Record live results in [sanitized validation templates](evidence/sanitized/validation.md) only after observing them. The historical `FILE_MANIFEST.json` describes the original ZIP, so its `--verify-manifest` mode applies to that unchanged package, not the reorganized checkout. Review [public repository safety](docs/reference/security-and-sanitization.md) and [SECURITY.md](SECURITY.md) before publishing screenshots or evidence. Never publish secrets.
