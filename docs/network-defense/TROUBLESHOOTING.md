# Troubleshooting, Safety Gates and Rollback

| Symptom | First checks | Safe corrective direction |
| --- | --- | --- |
| Zeek image tag unavailable | Official image tags, digest, system architecture and registry policy | Choose a documented available official version; **do not** use random RPMs or unpinned latest |
| No Zeek JSON logs | PCAP SHA/path, image command, empty output directory, bind mounts/SELinux | Verify synthetic PCAP decoded in TShark; inspect container exit status |
| Cannot inspect unicast between other VMs | Sensor interface, vSwitch/Vmnet8 topology, known test traffic visibility | VMnet8 is not a mirror; use authorized TAP/SPAN or offline PCAP |
| Suricata config fails validation | `suricata -T` output, config version, local rule syntax and ruleset source | Correct only tested rule syntax; leave existing IDS rules unchanged |
| No Suricata alert | Was local rule enabled with `-S`? Did PCAP contain matching DNS? EVE enabled? | Confirm DNS event first; compare rule version and expected marker |
| High IDS false positives | Signature specificity, traffic ground truth and overlap | Tune/disable test rule under review, preserve evidence |
| TShark shows unexpected fields | TCP/IP/UDP version, VLAN/link layer, field name changes | Inspect `tshark -G fields` and actual decoded packet |
| YARA match missing | Rule syntax, target path, exact benign marker bytes | Run fixture file through vetted CLI; don't acquire live malware |
| Sigma conversion fails | CLI plugin version, backend, required pipeline, Sigma schema | Inspect `sigma plugin list` and `sigma list`; map actual Splunk fields |
| Splunk new index has no data | Index exists, UF TLS config, firewall source rule, monitored file path and line format | Confirm safe source exists; avoid broad inbound 9997 access |
| Splunk event time wrong | Old PCAP timestamp vs ingestion time, Zeek `ts`, EVE `timestamp` | Correct/test parsing-tier props with synthetic event before production |
| Missing HTTP/TLS in DNS-only fixture | Protocol not present | Do not invent protocol logs; add an **authorized** representative capture |
| System resource spike | CPU/disk/backpressure, rule count, capture rate | Stop optional sensor task; keep original Splunk/IdM resources untouched |

## Rollback order

1. Stop only the optional Zeek/Suricata offline process (or optional sensor forwarding after owner approval); do not touch existing Windows UF.
2. Preserve private forensic evidence and log hashes; do not delete active investigations.
3. Revert only newly deployed sensor input/outputs and narrow firewall change through documented VM console.
4. Verify Splunk Web, receiver, existing six indexes, IdM LDAP/DNS, Windows forwarding and storage are still healthy.
5. Restore last-known-good sensor snapshot if its configuration became inconsistent.
6. Re-run negative and positive connection tests and document the change/recovery.

## Data exposure warnings

Full PCAP, DNS, HTTP, SMB and RDP logs may expose credentials and personal/protected content. Never copy full output into public GitHub, Actions artifacts, public issues, logs attached to AI assistants, or personal cloud storage. Keep only synthetic samples in the public project.
