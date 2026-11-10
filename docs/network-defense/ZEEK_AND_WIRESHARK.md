# Zeek, Wireshark, TShark and tcpdump — Passive Packet Analysis

**Current state:** Instructions only. No packet capture or tool installation verified.

For the complete RHEL 10.2 installation, configuration, optional live service, Splunk integration, and rollback procedure, follow the [28-step Zeek deployment guide](ZEEK_DEPLOYMENT.md). This page remains the short packet-analysis companion.

## Installation and version inventory

On **RHEL-SENSOR01** (optional, owner-approved RHEL 10.2 system):

~~~bash
sudo dnf install -y wireshark-cli tcpdump podman
tshark --version
tcpdump --version
podman --version
~~~

RHEL 10 supplies `wireshark-cli`. For the graphical Wireshark client, use an approved Windows desktop installation. **Zeek's official Linux support matrix warns it may not provide RPM binaries for RHEL-based distributions**: inspect the [official Zeek releases](https://zeek.org/get-zeek/) and [OS support](https://github.com/zeek/zeek/wiki/Zeek-Operating-System-Support-Matrix). An approved official container or reviewed source build is appropriate; record the exact image digest/package source.

## Offline PCAP first

~~~bash
python3 scripts/network-defense/generate_synthetic_pcap.py \
  --output "$HOME/network-lab/private-pcaps/lab-dns.pcap"

tshark -r "$HOME/network-lab/private-pcaps/lab-dns.pcap" \
  -Y "dns" -T fields \
  -e ip.src -e ip.dst -e dns.qry.name

tcpdump -nn -r "$HOME/network-lab/private-pcaps/lab-dns.pcap"
~~~

**Command overview:** Generates a harmless DNS packet (documentation addresses), lists decoded DNS metadata, and displays an independent packet summary. There is **no live sniffing**.

Zeek official examples use:

~~~bash
zeek -r /path/to/approved.pcap LogAscii::use_json=T
~~~

This writes `conn.log`, `dns.log` and any supported additional protocol logs in the current directory. Run inside a dedicated empty output folder. For the optional official container, see [Steps 12–14](IMPLEMENTATION_GUIDE.md). Zeek doesn't produce logs for protocols absent from the PCAP. Do not expect TLS metadata from a DNS-only fixture.

## Baseline protocol investigation

| Protocol | Data and questions | Limitations |
| --- | --- | --- |
| TCP/IP | Conversations, source/destination, handshake, retransmissions, reset flags | Packet loss or capture at only one direction may distort |
| DNS | Queries, responses, SERVFAIL/NXDOMAIN, new domain volume | Encrypted DNS may obscure queries |
| HTTP | Methods, hosts, user agents, cleartext requests | Captures can contain credentials; do not upload |
| TLS | Version, certificate details, SNI when present, negotiated suites | TLS 1.3 and encrypted payload reduce visibility |
| SMB | Dialect negotiation, server responses and connection patterns | SMB encryption can hide payloads. Signing authenticates messages and can coexist with visible payloads. |
| RDP | Transport and connection attempts | Encryption limits user/session detail |

**TShark examples (run only on an authorized file):**

~~~bash
tshark -n -r /path/to/approved.pcap -q -z io,phs
tshark -n -r /path/to/approved.pcap -Y 'tcp.flags.syn==1 && tcp.flags.ack==0'
tshark -n -r /path/to/approved.pcap -Y 'tls.handshake.type==2'
tshark -n -r /path/to/approved.pcap -Y 'dns.flags.response==1 && dns.flags.rcode != 0'
tshark -n -r /path/to/approved.pcap -Y 'smb2.cmd == 0'
tshark -n -r /path/to/approved.pcap -Y 'tcp.port == 3389'
~~~

**Command overview:** These searches show the protocol mix, TCP connection attempts, TLS ServerHello messages, DNS error replies, SMB negotiation and common RDP-port traffic. For TLS 1.3, inspect the negotiated version in the Supported Versions extension. For SMB, check the server's selected dialect and signing flags in negotiation. A connection to TCP 3389 establishes an observed port, so use endpoint events and policy to verify RDP and authentication. Record empty or incomplete views as visibility limits.

## Live visibility prerequisites

- Approved source and privacy impact, supported TAP/SPAN or mirrored virtual switch, sensor placement and expected flows.
- Network engineer verifies actual packets from at least two test endpoints reach the sensor, with both directions and measured capture drops.
- Prefer bounded capture with limited snap length and duration; store only in private encrypted locations.
- RHEL-SENSOR01 is **not an IPS**. Never enable packet injection, routing/bridging or capture of an unauthorized network.
- VMnet8 NAT/persistent promiscuous mode alone **does not guarantee access** to all other VMs' unicast streams.

**Validation:** [evidence matrix](../../evidence/sanitized/network-defense-validation.md). Use observed results, not screenshots of example code.
