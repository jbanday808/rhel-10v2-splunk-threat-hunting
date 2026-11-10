# 03 — Preflight, Asset Inventory, Approval and Backout

## Before any changes

1. Confirm this is an **owned, isolated lab**; no production, classified or government system is being modified.
2. Complete the original [52-step baseline](../steps/README.md) to the extent required for this phase; inspect actual service status.
3. Confirm VMware Workstation Pro VM console access, a management browser from the Windows host, and SSH backup access.
4. Back up **privately** (not GitHub): Splunk configs and indexes as permitted, IdM directory state, VM snapshots and TLS keys. Test restore separately.
5. Identify dependencies of each exposed port; certificate expiry, DNS, NTP, IdM, package repositories and update traffic.
6. Appoint a change owner, independent reviewer, rollback owner, test window and incident contact (can all be lab roles, but document conflicts).
7. Record changes in a timestamped local journal, and publish **sanitized** evidence only.

## Asset inventory

| Asset | Identifier | Role | Owner | State |
| --- | --- | --- | --- | --- |
| VMware host | Windows 11 / VMnet8 .1 | Managed workstation / hypervisor | Lab owner | Verify |
| Splunk VM | RHEL-SPLUNK01 / .10 | Application/resource, SIEM | Lab owner | Verify |
| Windows VM | WINHUNT01 / .20 | Telemetry source | Lab owner | Verify |
| IdM VM | RHEL-IDM01 / .30 | Directory, DNS, PKI | Lab owner | Verify |
| Virtual network | VMnet8 172.25.250.0/24 | NAT transit | Lab owner | Verify |
| GitHub | `jbanday808/rhel-10v2-splunk-threat-hunting` | Public source documents | Lab owner | Verified repository; **not** evidence of live deployment |

Record installed versions using [docs/reference/versions.md](../reference/versions.md).

## Read-only diagnostic commands

**RHEL VM console:**

```bash
hostnamectl
ip -brief address
nmcli -f NAME,DEVICE,TYPE connection show --active
getenforce
sudo firewall-cmd --get-active-zones
sudo ss -lntp
sudo systemctl status Splunkd.service --no-pager -l
```

Run the Splunk service command on **RHEL-SPLUNK01 only**; it does not apply to the IdM VM.

**Windows 11 hunting endpoint PowerShell:**

```powershell
Get-NetIPConfiguration
Get-NetFirewallProfile
Get-MpComputerStatus | Select AntivirusEnabled,RealTimeProtectionEnabled
Get-Service SplunkForwarder -ErrorAction SilentlyContinue
```

All commands above are **read-only**. Record what actually runs successfully rather than converting exceptions into false passes.

## Change-control and recovery record

| Field | Example |
| --- | --- |
| Change ID | ZT-CHANGE-001 |
| Planned change | Narrow Splunk Web 8000 allowed sources |
| Target | RHEL-SPLUNK01 `siem-lab` |
| Current policy/snapshot | Save privately / Pending |
| Approved source | Management host `172.25.250.1/32` |
| Positive test | Management browser can reach HTTPS 8000 |
| Negative test | Other *authorized test VM* cannot reach HTTPS 8000 |
| Rollback | Remove runtime rule or restore saved zone from console |
| Approver | TBD |
| Result/evidence | Pending |

**Stop conditions:** loss of console control, failing DNS/IdM lookup, TLS trust failure, unexpected data-ingestion outage, new broad privileges, or authentication breakage. Resume from known-good configuration, not by disabling SELinux or certificate validation.
