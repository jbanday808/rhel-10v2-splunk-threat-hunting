# Architecture

| System | Address | Purpose |
| --- | --- | --- |
| VMware host adapter | 172.25.250.1 | Host access |
| RHEL-SPLUNK01 | 172.25.250.10 | Splunk Enterprise |
| WINHUNT01 | 172.25.250.20 | Windows monitoring and tests |
| RHEL-IDM01 | 172.25.250.30 | IdM directory and lab DNS |
| NAT gateway | 172.25.250.2 | Outbound access |

RHEL combines indexing and the search interface.
Windows sends records over verified TLS on TCP 9997.
Splunk Web uses HTTPS on TCP 8000.
Splunk queries IdM over verified LDAPS on TCP 636.
Splunk uses IdM DNS at 172.25.250.30; IdM forwards external queries to .2.
The splunk-hunters group maps only to lab_hunter.
The splunk-admins group maps to admin.
The native Splunk admin remains available for recovery.
WSL and VS Code are used only for the final GitHub upload.

## Optional Kali Linux Analysis Workstation

Kali Linux is an additional **optional** VM on VMnet8 with a unique verified DHCP lease; no fixed address or completed deployment is assumed. It analyzes privately stored synthetic PCAPs with Wireshark/TShark, Zeek, Suricata, and Arkime, and tests approved files/rules with YARA and Sigma. It does not replace RHEL-SENSOR01 or automatically forward logs to Splunk. VMnet8 does not mirror other VMs' unicast traffic. Follow [Step 28.16](../steps/28-generate-harmless-hunting-activity.md#step-2816--optional-kali-linux-analysis-workstation) and the [Kali deployment guide](../network-defense/KALI_DEPLOYMENT.md); live capture requires a separate verified, authorized mirror/TAP.

## Optional Passive Network Sensor (NOT DEPLOYED)

A **proposed** separate VM, RHEL-SENSOR01 at 172.25.250.40, may analyze synthetic offline PCAPs with Zeek, Suricata and TShark, then send approved sanitized JSON via verified TLS to the existing Splunk server. **VMnet8 NAT does not automatically mirror other VM traffic.** Live sensing requires approved TAP/SPAN or verified virtual port mirroring. See [Passive Network Defense Architecture](../network-defense/ARCHITECTURE.md) and [30-Step Guide](../network-defense/IMPLEMENTATION_GUIDE.md). This preserves the original three-VM topology and sources.
