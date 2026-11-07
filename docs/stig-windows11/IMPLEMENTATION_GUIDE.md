# Windows 11 STIG V2R11 — complete implementation guide

This guide helps you prepare, assess, harden, retest, and document the **WINHUNT01 Windows 11 virtual machine** described by the RHEL 10.2 Splunk home lab. It uses the supplied unclassified **Microsoft Windows 11 STIG Version 2 Release 11**, benchmark date **September 30, 2026**.

The manual source contains 257 rules. The [rule reference index](RULE_INDEX.md) links to the complete source check and fix text for every rule. Read those instructions and their applicability conditions before making a finding or a change. The workflow below does not modify the VM, prove compliance, or replace an authorized assessment.

## Before you start

- Work inside **WINHUNT01**, the guest VM, not the Windows computer running VMware. Confirm the displayed computer name before proceeding. The planned lab address is `172.25.250.20`; confirm actual addressing privately.
- Preserve the existing lab design: RHEL-SPLUNK01 `172.25.250.10`, WINHUNT01 `172.25.250.20`, and RHEL-IDM01 `172.25.250.30`. Windows is intended to forward events to Splunk over TCP `9997`; do not assume the connection or TLS is already working.
- Have a local VM console, authorized administrator, recovery method, compatible backup, and change window. Managed or production systems require the system owner's approval and policy owner; use a pilot first.
- Use the benchmark required by your assessment authority. DISA can publish newer releases; this guide describes the supplied V2R11 manual source. The manual file is **not** an automated SCAP scan package.
- Perform commands from an elevated Windows PowerShell window in the guest where noted. Read the expected result before proceeding. Do not publish actual machine details, event data, checklists, recovery secrets, or policy exports.

## Phase 1 — Identify the system and protect recovery

### Step 01 — Define the assessment

Record the system owner, administrator, assessor, VM purpose, benchmark version, scope, maintenance window, and approved evidence location in a private record. Decide who approves changes and findings. Treat the Windows 11 OS and [Windows Defender Firewall](../stig-windows-firewall/IMPLEMENTATION_GUIDE.md) as separate assessments where applicable.

### Step 02 — Confirm the target and edition

Inside WINHUNT01, open Windows PowerShell as administrator and run:

```powershell
$env:COMPUTERNAME
Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, BuildNumber, OSArchitecture
Get-CimInstance Win32_ComputerSystem | Select-Object PartOfDomain, Domain
```

**Command overview:** The first command displays the computer name. `Get-CimInstance` displays the Windows edition, build, architecture, and domain-join status; `Select-Object` limits the displayed fields. Domain and host details belong in the private record.

**Expected result:** Confirm the target is WINHUNT01 and record its actual edition and join state. Stop if the name or target is unexpected. The supplied overview says domain-joined systems are subject to the Enterprise edition rule; review each source rule for standalone or edition-specific applicability. Do not claim Enterprise features are present on an unverified edition.

### Step 03 — Identify who manages policy

Open **Settings → Accounts → Access work or school** and review domain, workplace, or device-management enrollment. Determine whether local policy, domain Group Policy, or Intune/another management system controls the VM. Record the responsible policy owner. A local change may be overwritten by a managed policy.

### Step 04 — Review the VM hardware

In VMware Workstation, review firmware type, Secure Boot support, virtual TPM, and virtual CPU settings. In Windows, check the TPM and Secure Boot without changing them:

```powershell
Get-Tpm | Select-Object TpmPresent, TpmReady
try { Confirm-SecureBootUEFI } catch { Write-Host 'Secure Boot status unavailable; review firmware and permissions.' }
```

**Command overview:** `Get-Tpm` reports whether the TPM is present and ready. `Confirm-SecureBootUEFI` checks Secure Boot; the `try/catch` reports when the check cannot run. **Expected result:** Record actual values. A missing vTPM, unsupported firmware, or unavailable status needs investigation; it is not an automatic pass.

### Step 05 — Protect BitLocker recovery

If encryption is present, locate and verify the correct recovery key using the organization's approved process **before** changing firmware, vTPM, boot configuration, or virtual machine encryption. Do not display or copy the recovery key into GitHub. Inspect status only:

```powershell
Get-BitLockerVolume | Select-Object MountPoint, VolumeStatus, ProtectionStatus
```

**Command overview:** `Get-BitLockerVolume` lists drive encryption state; `Select-Object` omits recovery keys. **Expected result:** Record the actual protection state privately. Check the source rules for encryption, preboot PIN, and exceptions; do not enable, suspend, decrypt, or rotate keys without an approved recovery plan.

### Step 06 — Back up and rehearse rollback

Confirm an authorized VM backup or snapshot and any application-consistent backups, verify available storage, and test recovery according to your VM and encryption design. Record where the backup is kept, who can restore it, and how to regain console access. A snapshot alone is not proof of a working backup or recovery-key escrow.

### Step 07 — Preserve essential services

Review existing Windows Security, System, PowerShell Operational, and Sysmon logging; also identify the Universal Forwarder if installed:

```powershell
Get-Service -Name SplunkForwarder, Sysmon, Sysmon64 -ErrorAction SilentlyContinue |
    Select-Object Name, Status, StartType
Get-WinEvent -ListLog Security, System, 'Microsoft-Windows-PowerShell/Operational', 'Microsoft-Windows-Sysmon/Operational' -ErrorAction SilentlyContinue |
    Select-Object LogName, IsEnabled, RecordCount
```

**Command overview:** `Get-Service` lists the named services when present. `Get-WinEvent -ListLog` checks the named log channels without exporting events. `Select-Object` limits the output. **Expected result:** Record existing services and channels; missing names may mean a component is not installed or a channel is unavailable. Investigate rather than treating missing output as success.

### Step 08 — Identify required network paths

Document the guest's access to DNS, update services, authentication, management, and the lab's intended Splunk receiver. Determine the actual forwarder destination and TLS settings from the approved configuration. The lab intends an outbound connection from WINHUNT01 to `splunk01.lab.test:9997`; it does not require a new inbound port on WINHUNT01 for that flow.

### Step 09 — Record the starting policy

Privately review effective policy and audit settings:

```powershell
gpresult /scope computer /r
auditpol /get /category:*
```

**Command overview:** `gpresult` displays applied computer policy; `auditpol` displays current audit categories. **Expected result:** Record the managing policy source and initial audit state. A standalone system may have limited domain policy information. These commands do not change policy.

## Phase 2 — Obtain and load the correct benchmark

### Step 10 — Verify the supplied package

Obtain the approved benchmark from DISA or your organization's trusted distribution channel. Confirm the title, **Version 2 Release 11**, and the benchmark date. Compare the source file's hash with a trusted copy when one is available. A file hash alone does not authenticate the publisher.

```powershell
$WinStig = 'C:\REPLACE_WITH_APPROVED_FOLDER\U_MS_Windows_11_STIG_V2R11_Manual-xccdf.xml'
Test-Path -LiteralPath $WinStig -PathType Leaf
Get-FileHash -LiteralPath $WinStig -Algorithm SHA256 | Select-Object Algorithm, Hash
```

**Command overview:** `$WinStig` is the full path to the XML; replace the placeholder. `Test-Path` checks that the file exists. `Get-FileHash` calculates a SHA-256 fingerprint. **Expected result:** `True` and a hash matching your trusted copy. The supplied copy's fingerprint is recorded in [references](REFERENCES.md); a match identifies those bytes only.

### Step 11 — Install or open STIG Viewer

Use an organization-approved STIG Viewer from DISA and follow local software installation policy. The supplied XSL file is for presentation and is not a scan engine. Choose a protected location for the viewer library, saved checklists, screenshots, and exports.

### Step 12 — Import the manual XCCDF

In STIG Viewer 3.x, open **STIG Explorer**, select **Add STIG to Library**, browse to the XML, and select **Load**. Confirm the title, version, release, date, and rule list. Menus can differ between viewer versions. Importing the XML does not scan the VM.

### Step 13 — Create a checklist

Open **Checklists → Create Checklist**. Enter an approved name; add the Windows 11 STIG, select the option to fill the checklist, and enter the authorized asset information. Save it in the approved private location. Confirm that the full source rule set appears; a profile or filter must not silently exclude rules you are required to assess.

### Step 14 — Use status correctly

| Status | Meaning |
| --- | --- |
| Not Reviewed | The check is incomplete or evidence is insufficient. |
| Open | An applicable check shows the required condition is not met. |
| Not a Finding | Evidence supports the applicable requirement. |
| Not Applicable | The rule does not apply and the justification is accepted by the assessment authority. |

Do not mark an unknown result as a pass. Record the date, observed evidence, assessor, and reason for each decision in the private checklist.

### Step 15 — Plan the full 257-rule review

Use the [rule index](RULE_INDEX.md). For every rule, compare its full check text and exceptions with the actual system; record the group ID, rule revision, severity, result, and evidence. Source severity high, medium, and low correspond to CAT I, CAT II, and CAT III respectively. Prioritize with the owner based on severity and actual operational risk.

## Phase 3 — Assess the rule families

### Step 16 — Check system and platform requirements

Work through [WN11-00](rules/00.md), including edition, TPM, Secure Boot, encryption, supported features, and installed components. Read each rule's exceptions and evidence instructions. For example, BitLocker and preboot authentication changes can affect boot and recovery; review the source, VMware capabilities, and key access before any change.

### Step 17 — Check account policies

Review [WN11-AC](rules/ac.md) for lockout and password policy. Determine whether the relevant policy applies to local or domain accounts, and use the effective policy source. The supplied V2R11 includes a maximum-password-age rule; read its check, exceptions, and organizational requirements rather than applying an isolated number to every identity provider.

### Step 18 — Check auditing and event logs

Review [WN11-AU](rules/au.md) using each rule's audit category, success/failure selection, log size, and access instructions. Compare `auditpol` output with the exact rule, and inspect **Event Viewer → Windows Logs** properties where requested. Size the Security log to the source requirement and actual retention needs. Do not reduce event collection or remove the forwarder's approved access while changing permissions.

### Step 19 — Check computer configuration

Review [WN11-CC](rules/cc.md) against effective policy, registry values, virtualization prerequisites, and feature availability. Examples include Credential Guard, remote access, and PowerShell logging. Some settings require a restart, domain policy, supported edition, or VM hardware changes; plan and verify those dependencies first.

### Step 20 — Check endpoint, certificate, and registry rules

Review the separate [WN11-EP](rules/ep.md), [WN11-PK](rules/pk.md), and [WN11-RG](rules/rg.md) rules. Use approved trust anchors and the applicable environment's certificate process. Do not import DoD certificates or change certificate stores blindly in a standalone home lab; document applicable requirements and authorized exceptions.

### Step 21 — Check security options and user settings

Review [WN11-SO](rules/so.md) and [WN11-UC](rules/uc.md). Check account, sign-in, protocol, and user-policy settings against the actual rule scope. When testing access restrictions, retain approved administrator recovery access and a console session.

### Step 22 — Check user rights

Review [WN11-UR](rules/ur.md) and each rule's permitted principals. Identify how the Splunk Universal Forwarder obtains event-log access before changing local groups, user rights, or audit-log permissions. Validate the specific right and group assignment in the approved effective policy. Do not remove an unfamiliar service account or group until its owner confirms its purpose.

### Step 23 — Decide applicability individually

For standalone systems, domain-specific rules can have source-defined exceptions. Other rules may still apply. Record the rule-specific condition, evidence, and reviewer approval; do not mark an entire family Not Applicable merely because this is a home lab, VM, or non-domain system.

## Phase 4 — Change one approved item at a time

### Step 24 — Review and prioritize findings

For each open item, document the source rule revision, actual condition, affected service, risk, owner, fix, maintenance window, dependencies, and rollback. Discuss conflicting operational needs with the owner. Track accepted exceptions and unresolved work in the approved risk process.

### Step 25 — Select the authoritative policy path

For a standalone lab, use the local setting specified in the rule when available. For a domain or managed system, have the policy owner modify the approved GPO or management policy. Record the original setting and avoid competing local changes. Not every STIG rule maps to one Group Policy setting.

### Step 26 — Apply a pilot change

For an approved rule: (1) open its check and fix text; (2) verify the current value and applicability; (3) record the old value; (4) change the specified setting using the approved management method; (5) record the action and time; and (6) repeat the source check. Do not run a whole benchmark's fixes, import an unreviewed GPO, or apply a bulk remediation script as a first step.

### Step 27 — Restart only when required

If the rule or approved change requires a restart, confirm the backup, console access, and BitLocker recovery method first. Restart during the agreed window. Sign in through the authorized method and confirm Windows and the VM start normally.

### Step 28 — Validate monitoring after changes

Repeat Step 07 and confirm the required services and event channels are present and running or enabled as appropriate. Generate only approved harmless test activity, then check the expected event locally. Follow existing [Windows event collection verification](../steps/27-verify-event-collection.md) to check Splunk. No data in Splunk may mean collection is still in progress, not that a STIG rule passed.

For an approved lab connectivity check:

```powershell
Test-NetConnection -ComputerName splunk01.lab.test -Port 9997
```

**Command overview:** `Test-NetConnection` attempts the stated TCP connection from WINHUNT01 to the intended receiver. **Expected result:** `TcpTestSucceeded : True` only when DNS, network, receiver, and firewall permit the connection. This is an active connectivity test; it does not validate TLS identity or event ingestion. Obtain approval before using it outside the lab.

### Step 29 — Review results in Splunk

If event forwarding has already been configured, run the existing collection search from Step 27 of the lab. Compare actual recent Windows Security, System, PowerShell, and Sysmon events with local activity and expected sourcetypes. Record missing data as an operational issue. The project uses existing indexes `win_security`, `win_system`, `powershell`, `sysmon`, `linux`, and `lab`; this guide creates no new indexes.

### Step 30 — Retest the source check

After each approved fix, run the exact source check again and update the private checklist with observed evidence. If the condition remains unmet, keep it Open. If a change broke a required service, follow the approved rollback plan and document the outcome.

## Phase 5 — Complete evidence and follow-up

### Step 31 — Understand optional automated scanning

The supplied file is a **manual XCCDF**. If an authorized scan is required, obtain a separate Windows 11 SCAP package and an approved, compatible Windows scanner. Confirm its benchmark version, supported platform, configuration, and rule coverage with the assessor before scanning. Automated passes do not resolve manual, Not Checked, error, or Not Applicable results. Do not claim V2R11 coverage from a different release.

### Step 32 — Reconcile all results

Review all 257 source rules, applicable automated results, remaining manual checks, justified Not Applicable entries, and open findings. Reconcile conflicts with the assessor. Record approved findings and action plans, including owner, due date, risk, and compensating measures where applicable.

### Step 33 — Sanitize any public evidence

Keep completed Viewer checklists, scan outputs, actual system names, addresses, account information, event contents, screenshots, keys, and policy exports in approved private storage. The repository's [pending evidence template](../../evidence/sanitized/windows11-stig-validation.md) is for approved sanitized summaries only.

### Step 34 — Schedule review and recovery testing

Agree on a reassessment date and triggers such as a Windows update, new STIG release, policy change, VM hardware change, or failed forwarding check. Test recovery according to the backup plan. A completed checklist, tested lab, or public guide is not by itself an authorization to operate.

## Troubleshooting

| Symptom | First checks |
| --- | --- |
| Local setting reverts | Identify winning GPO or device-management policy and contact its owner. |
| Secure Boot or TPM check is unavailable | Verify the guest edition, virtual firmware, vTPM support, and administrator permissions before changing hardware. |
| BitLocker asks for recovery | Use the approved escrowed recovery key and recovery procedure; do not post it publicly. |
| Forwarder stops sending | Check service, event-log access, DNS, destination, TCP 9997, TLS configuration, and receiver health separately. |
| Source rule cannot be tested | Leave Not Reviewed and record the blocker; request guidance from the assessor. |

See [references](REFERENCES.md), the [complete rule index](RULE_INDEX.md), and the separate [firewall guide](../stig-windows-firewall/IMPLEMENTATION_GUIDE.md).
