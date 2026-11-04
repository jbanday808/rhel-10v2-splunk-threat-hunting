# 05 — Device Visibility, Endpoint Hardening and Posture

## Objective

Establish accurate asset inventory and security posture for Windows and RHEL systems. Local telemetry is **posture evidence**, not an authoritative device-compliance signal for a future IdP/PEP until integrated into its policy engine.

## Step A — RHEL checks (each RHEL VM console)

```bash
cat /etc/redhat-release
hostnamectl
getenforce
sudo systemctl is-active firewalld
sudo systemctl is-active auditd
sudo dnf check-update --security || true
rpm -q openscap-scanner scap-security-guide
```

**Command overview:** Shows OS version, hostname, SELinux status, firewall/audit services, candidate security updates, and whether OpenSCAP/scap-security-guide packages are installed. `dnf check-update` exit code can indicate updates, so `|| true` prevents the command list stopping—**review the actual output**, not just exit status.

**Target:** SELinux Enforcing, explicit services, a maintained update plan. Do not disable SELinux to resolve Splunk errors. For policy conflicts, investigate AVCs and apply minimal approved fixes.

## Step B — Windows hunting VM checks (PowerShell on WINHUNT01)

```powershell
Get-ComputerInfo | Select-Object WindowsProductName,WindowsVersion,OsBuildNumber
Get-MpComputerStatus | Select-Object AntivirusEnabled,RealTimeProtectionEnabled
Get-NetFirewallProfile | Select-Object Name,Enabled,DefaultInboundAction
Get-Service SplunkForwarder -ErrorAction SilentlyContinue
Get-WinEvent -ListLog 'Microsoft-Windows-Sysmon/Operational'
Get-WinEvent -LogName 'Microsoft-Windows-Sysmon/Operational' -MaxEvents 3 -ErrorAction SilentlyContinue
```

**Command overview:** Reads Windows build, Microsoft Defender, Windows Firewall, Universal Forwarder service and Sysmon event availability. Some checks may return no data if the software is missing; **do not mark Pass** merely because the command didn't crash.

## Step C — Verify reporting and protected transport

Follow existing [Windows forwarding Steps 21–27](../steps/README.md). Confirm Windows logs arrive in actual Splunk searches and the forwarder verifies the Splunk receiving certificate. A green Defender status on its own does not prove compliant access, continuous attestation or endpoint protection effectiveness.

## Step D — Apply approved hardening only

Use **current** applicable DISA STIG/SRG guidance and Red Hat hardening guidance. Verify benchmarks suit installed RHEL 10.2 packages, role and services. Where SCAP is available, *inspect* content/profiles before running an assessment. Do not deploy a generic `oscap --remediate` against the Splunk or IdM servers without reviewing effects and having a snapshot/rollback plan.

## Step E — Plan endpoint-to-identity integration

A real posture-aware access decision requires: (1) managed device inventory, (2) authenticated posture signals, (3) policy engine/IdP/PEP, (4) time-limited access and re-evaluation, (5) denial + audit tests. These are **future capabilities**, not current claims.

**Expected evidence:** platform/version screenshot, SELinux/firewall/audit status, endpoint-protection status, actual Sysmon and Windows event arrival, patch-management actions and approved exceptions. Redact personal identifiers and keys.
