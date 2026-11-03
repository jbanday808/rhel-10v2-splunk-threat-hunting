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

---
