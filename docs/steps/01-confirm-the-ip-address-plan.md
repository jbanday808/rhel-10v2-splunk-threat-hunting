**Step 1 — Confirm the IP address plan**

Your screenshot confirms VMnet8 uses subnet `172.25.250.0` with mask `255.255.255.0`. Configure or confirm the remaining values:

| Component                      | Address or setting |
| ------------------------------ | ------------------ |
| VMware network                 | `VMnet8 — NAT`     |
| Network                        | `172.25.250.0/24`  |
| Subnet mask                    | `255.255.255.0`    |
| Physical host’s VMnet8 adapter | `172.25.250.1`     |
| NAT gateway                    | `172.25.250.2`     |
| RHEL Splunk server             | `172.25.250.10`    |
| Windows hunting VM             | `172.25.250.20`    |
| Gateway for all three VMs | `172.25.250.2` |
| Initial DNS for the original VMs | `172.25.250.2` |
| RHEL IdM directory server | `172.25.250.30` |
| Final DNS for Splunk after Step 35 | `172.25.250.30` |
| Final DNS for IdM after Step 33 | `172.25.250.30` |
| Windows hunting VM DNS | `172.25.250.2` |
| DHCP starting address          | `172.25.250.100`   |
| DHCP ending address            | `172.25.250.200`   |

The gateway and DHCP values are settings to configure or confirm because those details were not displayed in your screenshot.

In VMware Workstation Pro:

1. Open **Edit → Virtual Network Editor**.
2. Click **Change Settings**.
3. Select **VMnet8**.
4. Keep **NAT** selected.
5. Keep subnet `172.25.250.0` and mask `255.255.255.0`.
6. Open **NAT Settings** and confirm gateway `172.25.250.2`.
7. Open **DHCP Settings** and configure `.100–.200`.
8. Keep the host virtual adapter connected.
9. Click **Apply → OK**.

For the physical host’s **VMnet8 adapter**, use `.1` and the subnet mask. Leave its gateway and DNS fields blank.

Confirm `.10`, `.20`, and `.30` are available before assigning them. The IdM VM initially uses `.2` for DNS while packages are installed; it hosts DNS at `.30` after Step 33. Splunk switches to that DNS server in Step 35. All three VMs keep the NAT gateway at `.2`.

VMware NAT supplies a private network shared by the host and VMs, with outbound access through the host. This lab does not require inbound NAT port forwarding. [knowledge.broadcom.com](https://knowledge.broadcom.com/external/article/339371/using-the-virtual-network-editor-in-vmwa.html?utm_source=chatgpt.com)

---
