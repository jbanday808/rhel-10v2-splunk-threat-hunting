# Passive Network Defense Workstream (WIP)

**[START HERE](../../START_HERE_NETWORK_DEFENSE.md)** · **[COMPLETE 30-STEP GUIDE](IMPLEMENTATION_GUIDE.md)**

Build a practical **passive** cybersecurity lab with Zeek, Wireshark/TShark, tcpdump, Suricata, YARA, Sigma, Splunk, and CMMC Level 2 risk/evidence planning. This is an **optional extension**; the original 52 Splunk steps, IdM, Windows forwarder and RHEL STIG/Zero Trust plans remain intact.

## Documents

| Resource | Focus |
| --- | --- |
| [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) | 30-step planning, installation, configuration, PCAP lab, Splunk integration, baseline, triage and operations |
| [OFFLINE_HTTP_WALKTHROUGH.md](OFFLINE_HTTP_WALKTHROUGH.md) | Positive and negative fixture replay, alert tuning, file analysis, and correlation in the existing `lab` index |
| [ARCHITECTURE.md](ARCHITECTURE.md) | VM roles, offline vs live sensing, trust and privacy boundaries |
| [CONOPS.md](CONOPS.md) | Mission, authorization, operation, analyst workflow, metrics, retention and escalation |
| [ZEEK_AND_WIRESHARK.md](ZEEK_AND_WIRESHARK.md) | Verified Zeek offline approach, TShark and PCAP analysis |
| [SURICATA.md](SURICATA.md) | RHEL 10 package checks, offline IDS, rules and EVE logging |
| [YARA_AND_SIGMA.md](YARA_AND_SIGMA.md) | Local file-matching and Sigma conversion to reviewed SPL |
| [SPLUNK_INTEGRATION.md](SPLUNK_INTEGRATION.md) | Proposed indexes, verified TLS forwarding, timestamp and parser tests |
| [CMMC_LEVEL2.md](CMMC_LEVEL2.md) | Illustrative 800-171 Rev 2 requirement/evidence links and scoping cautions |
| [DETECTIONS_AND_TESTING.md](DETECTIONS_AND_TESTING.md) | Baseline, passive vulnerability identification and alert triage |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | No packets, missing logs, false positives, rollback |
| [REFERENCES.md](REFERENCES.md) | Official 2026 vendor, NIST and DoD references |

**Source content:** `scripts/network-defense/`, `configs/network-defense/`, `rules/yara/`, `rules/sigma/`, `hunts/network-defense/`, `examples/network-defense/`, and `tests/test_network_defense.py`.

## Distinctions

- **Zeek:** Protocol metadata and network behaviors; not a traditional signature-based IPS.
- **Wireshark / TShark / tcpdump:** Analyze captured packets; may expose payloads, credentials and private data.
- **Suricata:** Passive network IDS/alerting from PCAPs or an authorized monitored interface; not run inline or in blocking mode here.
- **YARA:** Match patterns in **authorized local files** (or separately integrated extracted objects); a YARA rule is not a network capture sensor.
- **Sigma:** Detection rule representation that must be converted with the appropriate backend/pipeline and verified against actual Splunk fields.
- **CMMC:** A regulatory assessment program applicable by contract/scope. The lab contains **no CUI** and is **not CMMC certified**.

**Installation caveat:** Zeek does **not** currently guarantee official native binary packages for RHEL 10. Use a verified official container image or an independently tested source build; see [Zeek platform support](https://github.com/zeek/zeek/wiki/Zeek-Operating-System-Support-Matrix). Suricata's own instructions describe RHEL 10 packages through OISF COPR, subject to owner approval. No repository script installs third-party sources unattended.

See the [validation worksheet](../../evidence/sanitized/network-defense-validation.md) for observed offline checks and pending VM checks.
