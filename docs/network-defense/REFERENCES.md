# Official References — Verified Public Sources (November 2026)

| Source | What it supports |
| --- | --- |
| [Zeek releases](https://zeek.org/get-zeek/) | Current signed/source and official container release information |
| [Zeek installation](https://docs.zeek.org/en/current/install.html) | Supported vendor installation and container methods |
| [Zeek operating-system support](https://github.com/zeek/zeek/wiki/Zeek-Operating-System-Support-Matrix) | RHEL native binary availability limitations |
| [Zeek quick start](https://docs.zeek.org/en/current/quickstart.html) | `zeek -r file.pcap LogAscii::use_json=T` |
| [Zeek official image source, 9.0.1](https://github.com/zeek/zeek/tree/v9.0.1/docker) | Official registry, runtime command, and `/usr/local/zeek` installation path |
| [Podman Quadlet reference](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html) | Declarative container services, capture capability controls, and `[Install]` startup semantics |
| [TShark manual](https://www.wireshark.org/docs/man-pages/tshark.html) | Safe offline protocol decoding `-r -Y -T fields` |
| [RHEL 10 package manifest](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/package_manifest/) | `wireshark-cli` package naming and availability |
| [OISF Suricata RPM installation](https://docs.suricata.io/en/suricata-8.0.6/install/rpm.html) | Approved Suricata 8 COPR route for RHEL 10 |
| [Suricata documentation](https://docs.suricata.io/) | EVE JSON, rules, config and PCAP processing |
| [YARA command-line](https://yara.readthedocs.io/en/latest/commandline.html) | `yara RULE_FILE FILE` and controlled local file matching |
| [Sigma CLI](https://github.com/SigmaHQ/sigma-cli) | Installation, plugins and Splunk translation |
| [Sigma official documentation](https://sigmahq.io/docs/guide/getting-started.html) | Rule format, processing pipelines and backends |
| [Splunk Enterprise documentation](https://help.splunk.com/en/splunk-enterprise) | UF TLS forwarding, parsing, roles, indexing and search |
| [DoD CMMC](https://dodcio.defense.gov/CMMC/About/) | CMMC program level, assessment types and POA&M constraints |
| [CMMC Level 2 Assessment Guide](https://dodcio.defense.gov/Portals/0/Documents/CMMC/AssessmentGuideL2v2.pdf) | 110 NIST SP 800-171 R2 requirements and assessment objectives |
| [NIST SP 800-171 Rev. 2](https://csrc.nist.gov/pubs/sp/800/171/r2/upd1/final) | CUI safeguarding requirements used in current CMMC L2 model |
| [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final) | Zero Trust architectural concepts; separate from CMMC |

## Verification boundaries

Package names, plugin versions, repository availability, and exact supported Zeek image tags may change. Re-check official download pages when actually installing. No live installation, CMMC assessment, response authority or operational detection is asserted by these documents. The scenario is a public **synthetic lab**, not an approved DoD or Intelligence Community network.
