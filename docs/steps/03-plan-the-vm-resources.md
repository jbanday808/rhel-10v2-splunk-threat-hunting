**Step 3 — Plan the VM resources**

| Setting | RHEL Splunk server | Windows hunting VM | RHEL directory server |
| --- | --- | --- | --- |
| Name | `RHEL-SPLUNK01` | `WINHUNT01` | `RHEL-IDM01` |
| Operating system | RHEL 10.2 x64 | Windows 11 x64 | RHEL 10.2 x64 |
| Virtual CPUs | 8 total | 4 total | 4 total |
| Memory | 16 GB | 8 GB | 8 GB |
| OS disk | 100 GB | 100 GB | 60 GB |
| Additional data disk | 250 GB | Not required | Not required |
| Firmware | UEFI | UEFI | UEFI |
| Secure Boot | Enabled | Enabled | Enabled |
| Virtual TPM | Not required | TPM 2.0 | Not required |
| Network | Custom: VMnet8 | Custom: VMnet8 | Custom: VMnet8 |

These are small learning-lab sizes. The three VMs allocate 32 GB RAM in total, so leave additional memory for the physical Windows host. A **64 GB host** is a practical target for running all three together. Create the separate directory VM in Step 32.

### Optional Kali Linux analysis workstation

| Setting | Suggested value |
| --- | --- |
| Role | Separate Kali VM for offline Wireshark, Zeek, Suricata, Arkime, YARA, and Sigma work |
| Virtual CPUs | 4 |
| Memory | 8 GB for the synthetic exercise; 12–16 GB is more comfortable with Arkime/OpenSearch |
| Disk | At least 80 GB free for the all-in-one synthetic exercise; plan separate private packet/database storage for larger work |
| Network | Management adapter on VMnet8; use a unique DHCP lease and confirm the route |
| Capture adapter | Only if a separate authorized mirror/TAP is available and tested |

With Kali running, the four VMs allocate at least **40 GB RAM** in total; leave sufficient memory for the physical Windows host. Snapshot Kali before installing analysis tools. The [Kali deployment guide](../network-defense/KALI_DEPLOYMENT.md) starts with saved synthetic packets and gives the detailed setup and checks. VMware VMnet8 alone does not show Kali other VMs' unicast traffic.

---
