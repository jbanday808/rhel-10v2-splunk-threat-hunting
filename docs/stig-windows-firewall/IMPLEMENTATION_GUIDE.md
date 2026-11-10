# Windows Defender Firewall STIG V2R2 — complete implementation guide

Use this guide to assess, configure, and recheck Windows Defender Firewall with Advanced Security on an authorized system such as the **WINHUNT01 Windows 11 guest VM**. The user-supplied manual source is **Version 2 Release 2, dated November 9, 2023**, and contains **21 rules**. The [complete rule reference](rules/all.md) provides every source check and fix, with its IDs and severity.

The supplied overview describes this STIG for systems not capable of using an approved ESS host intrusion prevention firewall, in conjunction with the appropriate operating-system STIG. Have the owner or assessor decide applicability for the actual system and confirm the required current release. Do not infer applicability simply because Windows Firewall is installed.

This guide and its commands do not prove a system has been assessed, hardened, or authorized. Treat all examples as planned work. Do not make changes on a managed or production system without an approved change, recovery plan, and policy owner.

## Phase 1 — Prepare and protect the lab

### Step 01 — Define the target

Record the owner, administrator, assessor, purpose, maintenance window, benchmark release, reporting location, and approved private evidence location. For this lab, the target is the **WINHUNT01 guest**, not the Windows host that runs VMware. Assess its [Windows 11 operating system](../stig-windows11/IMPLEMENTATION_GUIDE.md) separately.

### Step 02 — Confirm the benchmark and firewall product

Determine whether an approved ESS host intrusion prevention firewall is available and whether this Windows Firewall STIG is applicable. Record the assessor's decision. Identify any third-party firewall, endpoint protection, VPN, or management product that changes Windows Filtering Platform policy. If the relationship is unclear, stop and ask the responsible owner before changing controls.

### Step 03 — Confirm the guest and domain status

In an elevated Windows PowerShell window inside the guest:

```powershell
$env:COMPUTERNAME
Get-CimInstance Win32_ComputerSystem | Select-Object PartOfDomain, Domain
```

**Command overview:** The first line displays the computer name. `Get-CimInstance` reports domain membership; `Select-Object` limits the fields. **Expected result:** Confirm WINHUNT01 and privately record the actual join state. Stop if the target is unexpected.

### Step 04 — Identify the policy owner

Determine whether firewall policy is controlled by local settings, domain Group Policy, Intune/another management service, or a combination. On a managed system, coordinate with the owner of the winning policy. A local change may not become effective or may be overwritten.

### Step 05 — Preserve a recovery path

Use the VMware console or another independently verified access path, an authorized administrator, and a known recovery procedure. Back up the VM according to the approved plan and test recovery. Confirm any BitLocker recovery key is safely escrowed before VM firmware, TPM, or encryption changes. Do not depend only on the network connection whose firewall is being changed.

### Step 06 — Record required connections

Before making changes, privately list required DNS, management, update, and monitoring flows with direction, endpoints, protocol, port, application, and owner. The intended lab path is **outbound** from WINHUNT01 to Splunk at `splunk01.lab.test` TCP `9997`. No new inbound Windows rule is needed just for that outbound forwarder flow. Confirm the actual network and current TLS configuration instead of assuming deployment.

### Step 07 — Review the active network profile

```powershell
Get-NetConnectionProfile | Select-Object Name, InterfaceAlias, NetworkCategory, IPv4Connectivity
```

**Command overview:** `Get-NetConnectionProfile` displays the network category assigned to each interface. **Expected result:** Record whether the connected interface is DomainAuthenticated, Private, or Public. A VM may have more than one interface. This view identifies the current profile; the checklist also addresses applicable profiles that are not currently active.

### Step 08 — Review effective firewall settings

```powershell
Get-NetFirewallProfile -PolicyStore ActiveStore |
    Select-Object Name, Enabled, DefaultInboundAction, DefaultOutboundAction, LogFileName, LogMaxSizeKilobytes, LogAllowed, LogBlocked
```

**Command overview:** `Get-NetFirewallProfile` reads the firewall profiles; `-PolicyStore ActiveStore` shows the active combined policy. `Select-Object` selects the most relevant fields. **Expected result:** Record all three profiles and investigate unexpected or unset values. This view supports the review but does not replace the registry checks and conditions in each source rule.

### Step 09 — Export local firewall policy privately

With an approved, existing private folder and a unique filename, run in an elevated window:

```powershell
$FirewallBackup = 'C:\REPLACE_WITH_APPROVED_PRIVATE_FOLDER\firewall-before.wfw'
if (Test-Path -LiteralPath $FirewallBackup) { throw 'Choose a new backup filename.' }
netsh advfirewall export "$FirewallBackup"
if ($LASTEXITCODE -ne 0) { throw 'Firewall export failed.' }
```

**Command overview:** The variable specifies the private backup file. `Test-Path` prevents replacing an existing file. `netsh advfirewall export` exports firewall policy; the final line stops on an error. **Expected result:** A new protected `.wfw` file and a successful export message. Do not publish it. This export does not back up domain GPOs or Intune configuration; obtain those backups from their owners and verify restoration procedures separately.

### Step 10 — Capture an initial connection baseline

Confirm the forwarder and relevant event channels if they are installed, and record actual status. Perform only approved tests. For the intended lab Splunk listener:

```powershell
Test-NetConnection -ComputerName splunk01.lab.test -Port 9997
```

**Command overview:** `Test-NetConnection` attempts a TCP connection to the lab receiver. **Expected result:** `TcpTestSucceeded : True` when the name, route, receiver, and relevant firewall rules permit it. This active connection test does not verify TLS or data ingestion. If forwarding is not deployed yet, record it as pending rather than inventing a pass.

## Phase 2 — Build the checklist

### Step 11 — Verify the manual source

Obtain the authorized source from DISA or an organization-approved distribution channel. Verify the title, **V2R2**, and **November 9, 2023** benchmark date. Compare its hash to a trusted copy where available; a hash alone does not prove publisher identity. The supplied file's fingerprint is recorded in [references](REFERENCES.md).

### Step 12 — Import the source in STIG Viewer

In an approved STIG Viewer 3.x installation, open **STIG Explorer → Add STIG to Library**, choose the manual XML, and select **Load**. Confirm the title, release, and source rule list. The XML and optional XSL are not an automated scan. Store the viewer library and assessment files in approved private locations.

### Step 13 — Create a firewall checklist

Open **Checklists → Create Checklist**, add this Firewall STIG, and enter approved target information. Save the checklist privately. Verify the full set of **21 rules** is visible and that a filter has not hidden required entries. Menus may vary with the installed Viewer version.

### Step 14 — Record accurate statuses

Use **Not Reviewed** for incomplete checks, **Open** for unmet applicable requirements, **Not a Finding** when evidence supports the requirement, and **Not Applicable** only with a source-supported reason and the required assessor approval. Record evidence, date, and reviewer privately. No automatic pass follows from the firewall merely being enabled.

### Step 15 — Map every source rule

The table is a navigation aid; use the [full check and fix](rules/all.md) for exact criteria, exceptions, and policy paths.

| Area | V2R2 rule IDs |
| --- | --- |
| Domain profile: state, inbound, outbound, size, dropped and successful logging | WNFWA-000001, 000004, 000005, 000009, 000010, 000011 |
| Private profile: state, inbound, outbound, size, dropped and successful logging | WNFWA-000002, 000012, 000013, 000017, 000018, 000019 |
| Public profile: state, inbound, outbound, local-rule merging, connection-security merging, size, dropped and successful logging | WNFWA-000003, 000020, 000021, 000024, 000025, 000027, 000028, 000029 |
| Domain workstation: authorized inbound management scope | WNFWA-000100 |

The supplied source contains three high, nine medium, and nine low severity rules. These are benchmark counts, not assessment results.

## Phase 3 — Review profile settings

### Step 16 — Open the firewall console

On the authorized guest, open **Windows Defender Firewall with Advanced Security** by searching for it or running `wf.msc`. In the console, select **Windows Defender Firewall Properties**. Review the **Domain Profile**, **Private Profile**, and **Public Profile** tabs, plus **Inbound Rules** and **Connection Security Rules**. The exact display name can vary by Windows version.

### Step 17 — Review the Domain profile

If the system is not domain-joined, the source allows the domain-profile rules to be marked Not Applicable; document the actual condition and reviewer decision. For a domain-joined system, use the source checks to review firewall state, default inbound and outbound actions, and the three logging settings. Review both policy-based registry values and the fallback registry path when the source directs you to do so.

### Step 18 — Review the Private and Public profiles

For each profile, compare the source rules with firewall state, default inbound action, default outbound action, and logging settings. For these V2R2 checks the requested baseline is firewall on, unsolicited inbound connections blocked, outbound connections allowed unless a rule blocks them, log size at least **16,384 KB**, and dropped and successful connection logging enabled. Read each source check and local requirements before assigning a result or changing a value.

Inbound **Block (default)** means unsolicited inbound traffic without a matching allowed rule is blocked. It is different from blocking all inbound connections, which can also override allowed rules. Do not select a stricter mode without evaluating the impact.

### Step 19 — Review public-profile rule merging

For **domain-joined** systems, WNFWA-000024 and WNFWA-000025 check whether local firewall rules and local connection-security rules merge with Group Policy on the Public profile. The source says both are Not Applicable on non-domain systems. For applicable domain systems, inspect the exact policy-based registry checks and the Public Profile → **Settings → Customize → Rule merging** settings.

Disabling local-rule merging can change remote access. Verify equivalent approved managed rules, console access, and policy ownership before changing it. Do not mark either rule Not Applicable solely because the Public profile is not currently active.

### Step 20 — Review authorized inbound exceptions

WNFWA-000100 applies to **domain workstations**, not servers or non-domain workstations, according to its source. With the firewall owner, review enabled inbound allow rules, their applications/services, profiles, and remote address scopes. Verify that allowed exceptions are limited to authorized management systems and hosts as required by the source. Rules can be complex; evaluate each one and test it. No universal management IP address should be copied into the lab.

### Step 21 — Verify logging paths and capacity

In each applicable profile tab, select **Logging → Customize** and inspect log location, maximum size, dropped packets, and successful connections. Confirm the folder exists, the Windows Firewall service can write to it, and the retention plan accounts for rollover. The source minimum is 16,384 KB for each applicable profile; larger sizes must still fit operating limits and local retention needs. Logging paths and entries can reveal sensitive network data.

Microsoft documents `%windir%\System32\LogFiles\Firewall\pfirewall.log` as a default path, but the configured path may differ. Do not assume the file exists until logging is enabled and traffic produces entries.

### Step 22 — Review the effective policy source

For any mismatch between the GUI, effective profile and the source registry check, inspect the precise source check and the managing GPO or device policy with its owner. The V2R2 source often checks a policy registry value first and a local firewall-policy registry value if the policy value is absent. Note that the Private profile fallback in the source uses the `StandardProfile` registry branch. Do not edit registry values directly as a shortcut around policy ownership.

## Phase 4 — Make approved changes and verify

### Step 23 — Plan each finding

For every applicable Open rule, record the current setting, source requirement, proposed change, affected profile, owner, risk, required connections, test plan, and rollback. Give the three high-severity inbound default rules appropriate priority while protecting recovery access.

### Step 24 — Change the authoritative policy

For an authorized standalone lab, open the corresponding **profile tab** in firewall properties. For a domain-managed system, the policy owner edits the approved GPO at **Computer Configuration → Policies → Windows Settings → Security Settings → Windows Defender Firewall with Advanced Security**. For an MDM-managed system, use the approved management policy. Select the exact rule's required field and value, then save the change. Apply one reviewed change or small change set at a time; do not reset the firewall or import an unreviewed policy.

### Step 25 — Example: configure logging after approval

For an applicable profile with an approved change:

1. In **Windows Defender Firewall Properties**, select the profile tab.
2. Under **Logging**, select **Customize**.
3. Set **Size limit (KB)** to at least `16384`, and set **Log dropped packets** and **Log successful connections** to **Yes**, when required by that profile's source rules and your approved policy.
4. Confirm the authorized file location, select **OK**, and allow the managing policy to apply.
5. Reopen the properties and repeat the exact source checks, including policy registry precedence.

Use the appropriate profile and management source; do not assume a setting changed on one profile covers the others.

### Step 26 — Recheck settings and safe connectivity

Repeat the applicable source checks, Steps 07–08, and approved connectivity tests. Verify the firewall service and effective profiles, management access, DNS, and required application connections. Where forwarding is deployed, repeat the TCP 9997 test from Step 10 and separately check TLS and recent events in Splunk. A TCP success alone is not a TLS or ingestion test.

### Step 27 — Verify log generation

After approved test traffic, inspect the active profile's configured log in its private location. Confirm new records are written and times are sensible. Review path permissions, space, and policy if the file is missing. Use a bounded read only after replacing the placeholder path:

```powershell
$FirewallLog = 'C:\REPLACE_WITH_APPROVED_LOG_PATH\pfirewall.log'
if (Test-Path -LiteralPath $FirewallLog -PathType Leaf) { Get-Content -LiteralPath $FirewallLog -Tail 10 }
```

**Command overview:** `Test-Path` checks the file, and `Get-Content -Tail 10` displays at most the last ten lines. **Expected result:** Recent firewall log entries if logging is active and qualifying traffic occurred. Output contains network data; keep it private. No output may mean a missing or empty file, wrong path, permissions, or no relevant traffic.

### Step 28 — Validate the Splunk data path

The existing Windows Universal Forwarder inputs cover Windows event channels. This guide does **not** automatically ingest the text firewall log. If firewall-log collection is approved later, design and review the specific input, service read permissions, sourcetype, parsing, retention, and one of the existing appropriate indexes with the lab owner. Test locally and verify recent real events before claiming ingestion; never expose private firewall data in this public repository.

### Step 29 — Roll back if needed

Stop the change if console access, management, DNS, forwarding, or another required function fails. Use the documented recovery path and coordinate with the responsible policy owner. A reviewed local `.wfw` export may support `netsh advfirewall import`, but importing replaces the current local firewall policy and does not restore centrally managed GPO or Intune policy. The appropriate owner must approve and perform restoration, then retest. Preserve the prior export and record the outcome privately.

### Step 30 — Reassess and report

Retest each changed rule using its **exact source check** and update the checklist with evidence. Keep unresolved findings Open. Record approved exceptions, owner, due date, and compensating measures in the authorized process. Do not publish actual rules, network scopes, host data, logs, checklists, or screenshots without review and sanitization.

### Step 31 — Understand automated scans

DISA lists a separately distributed **Firewall STIG SCAP Benchmark V2R3**. It is not the supplied manual V2R2 file. If automated scanning is required, the assessment authority must select an approved package and compatible scanner, evaluate the version difference, and reconcile automated and manual checks. Missing, Not Checked, or error results are not passes.

### Step 32 — Schedule follow-up

Reassess after firewall policy, network, management, Windows, or benchmark changes, and at the required review interval. The [pending evidence template](../../evidence/sanitized/windows-firewall-stig-validation.md) is for approved sanitized summaries; it does not contain a completed assessment.

## Troubleshooting

| Symptom | First checks |
| --- | --- |
| Setting reverts | Identify the effective GPO or MDM source; involve its owner. |
| Splunk connection fails | Review DNS, route, listener, effective outbound rules, receiving-side firewall, and TLS separately. Do not open arbitrary inbound ports. |
| Firewall log is absent | Check active profile, configured path, log settings, folder permissions, free space, and test traffic. |
| A rule appears in the GUI but not ActiveStore | Review profile, rule enablement, policy merging, and management source with the owner. |
| Remote management is lost | Use the prearranged VM console and recovery process; do not disable the firewall blindly. |

See the [full 21-rule reference](rules/all.md), [Windows 11 guide](../stig-windows11/IMPLEMENTATION_GUIDE.md), and [references](REFERENCES.md).
