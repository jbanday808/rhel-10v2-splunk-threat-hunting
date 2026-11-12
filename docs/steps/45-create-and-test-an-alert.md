**Step 45 — Create and test an alert**

This lab alert looks for a Sysmon process-creation event when `powershell.exe` starts with `-EncodedCommand`. A match is activity to investigate, not proof of malicious activity. Complete the test on **WINHUNT01** only. The alert depends on searchable Sysmon Event ID `1` data and an active Splunk license that permits scheduled alerts.

Ordinary Windows activity can already produce Sysmon Event ID `1`. The encoded-PowerShell test in Section 4 is a separate step; first make sure Splunk can search the existing process events.

### 1. Confirm the Windows process data is arriving

In Splunk Web, sign in as the local Splunk administrator and open **Search** in the **Threat Hunting Lab** app. If your release opens **Search & Reporting** as a separate app, note that app context and review the alert's sharing after saving. Set the time picker to **Last 24 hours** and run:

```spl
index=sysmon
| stats count AS sysmon_events
```

If `sysmon_events` is zero, skip the next search and follow **If either count is zero** below. Check the time range and role permissions; a zero count alone does not identify the cause. The [troubleshooting record in Section 7](#7-troubleshooting-record--zero-sysmon-events-and-forwarding-tls-failures) documents the supplied zero-event case, attempted corrections, and its unresolved status. If events exist, check process creation:

```spl
index=sysmon EventCode=1
| stats count AS process_events
```

If `process_events` is zero, do not save the alert yet. Use the checks below to investigate missing events or event-ID fields.

#### If either count is zero

First select **Last 7 days** and repeat the `sysmon_events` count above. This wider range may reveal older events, but does not rule out events outside that range or other causes.

- If `sysmon_events` is **greater than zero**, find the event ID field and values actually present:

  ```spl
  index=sysmon
  | eval event_id=coalesce(EventCode,EventID,"not extracted")
  | stats count by event_id
  | sort - count
  ```

  If ID `1` appears, rerun the `EventCode=1` check with **Last 7 days**. If it still returns zero, the ID may be extracted under `EventID` instead; inspect the raw event and field extraction with [Step 27](../steps/27-verify-event-collection.md). The value `not extracted` means neither field was available; inspect the raw event before drawing conclusions. If ID `1` is absent, check whether WINHUNT01 generated it locally.

- If `sysmon_events` is **zero**, check whether Sysmon events reached a different index:

  ```spl
  index=* (source=*Sysmon* OR sourcetype=*Sysmon*)
  | stats count by index source sourcetype
  ```

  Keep **Last 7 days** selected and run this as the Splunk administrator. If events appear in another index, review the Windows forwarder's effective input mapping. If none appear, inspect the Windows event log and forwarding path.

On **WINHUNT01**, open **Administrator PowerShell** and check the service and local process events:

```powershell
Get-Service -Name Sysmon,Sysmon64 -ErrorAction SilentlyContinue |
    Select-Object Name,Status

Get-WinEvent -FilterHashtable @{
    LogName = 'Microsoft-Windows-Sysmon/Operational'
    Id = 1
    StartTime = (Get-Date).AddDays(-7)
} -MaxEvents 5 | Select-Object TimeCreated,Id
```

If Windows has no recent Event ID `1`, run the harmless marker in Section 4 and repeat this check. If Windows has Event ID `1` but Splunk has no Sysmon events, check the forwarding path before testing the alert. In **Administrator PowerShell** on WINHUNT01:

```powershell
$UfHome = 'C:\Program Files\SplunkUniversalForwarder'
Get-Service SplunkForwarder | Select-Object Name,Status
& "$UfHome\bin\splunk.exe" btool inputs list 'WinEventLog://Microsoft-Windows-Sysmon/Operational' --debug
& "$UfHome\bin\splunk.exe" btool outputs list --debug |
    Select-String 'defaultGroup|lab_tls|server\s*=|useSSL\s*='
Test-NetConnection splunk01.lab.test -Port 9997
Get-Content "$UfHome\var\log\splunk\splunkd.log" -Tail 200 |
    Select-String 'TcpOutputProc|WinEventLog|SSL|TLS|certificate|ERROR|WARN' |
    Select-Object -Last 20
```

The Sysmon input should be enabled (`disabled = 0`) and assigned to `index = sysmon`; the output should target `splunk01.lab.test:9997` with TLS enabled. `btool --debug` shows which configuration file supplies each setting, but a recently edited setting may not be loaded by the running service. A successful TCP port test does not prove that the TLS connection or event delivery succeeded. If these values differ or the recent forwarder log shows errors, use the [Windows forwarding and TLS troubleshooting guide](../troubleshooting/splunk-forwarder-tls-and-kv-service.md) to check the current receiver and correct the identified cause. Keep raw logs and any sensitive configuration output private. Do not change the hunt SPL to hide a collection failure.

### 2. Run the hunt as a normal search

Use the search from [`hunts/01-encoded-powershell.spl`](../../hunts/01-encoded-powershell.spl), but remove its inline `earliest=-30m` when pasting into Splunk Web:

```spl
index=sysmon EventCode=1
| eval command=coalesce(CommandLine,process_command_line), image=coalesce(Image,process_path), account=coalesce(User,user)
| where match(image,"(?i)powershell[.]exe$") AND match(command,"(?i)-encodedcommand\s+")
| table _time host account image ParentImage command ProcessGuid
```

Keep **Last 24 hours** selected while checking older data. No matches can be normal if no matching process ran during that period. The saved alert will use its own time settings. Before enabling per-result suppression, verify that a matching result has both `host` and `ProcessGuid` populated.

### 3. Save the scheduled alert

Before saving, change the time picker to **Last 10 minutes**, or use a custom relative range from 10 minutes ago through now, and rerun the search. From the results page, select **Save As → Alert**. Use these settings; menu labels may vary slightly by Splunk release:

| Setting | Value |
| --- | --- |
| Title | `LAB - Encoded PowerShell` |
| Owner | Local Splunk administrator for the initial lab test |
| Alert type | Scheduled; **Run on Cron Schedule** if offered |
| Cron schedule | `*/5 * * * *` (every five minutes) |
| Search time range | Earliest `-10m`; Latest `now` |
| Trigger condition | Number of results **greater than 0** |
| Trigger action | **Add to Triggered Alerts** |
| Trigger mode | **For each result** if using the suppression fields below |
| Suppression | 15 minutes, fields `host,ProcessGuid`, only after verifying both fields are present |

The 10-minute search window overlaps runs that start five minutes apart. The 15-minute per-result suppression prevents repeat alert actions for the same `host` and `ProcessGuid` during the overlap; a new process with a different `ProcessGuid` can trigger separately. If either field is blank, correct the field extraction before relying on that suppression; missing fields can make it group unrelated results. Save the alert, then confirm it is **enabled** and its saved time range is `-10m` through `now` under **Settings → Searches, Reports, and Alerts** (or your release's **Alerts** page).

### 4. Generate one harmless test on WINHUNT01

In **Administrator PowerShell** on **WINHUNT01**, run these commands one at a time:

```powershell
$Payload = "Write-Output 'SIEM-LAB-ENCODED-TEST'"
$Encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($Payload))
powershell.exe -NoProfile -EncodedCommand $Encoded
```

**Expected PowerShell output:** `SIEM-LAB-ENCODED-TEST`. This confirms the test command ran on Windows; it does not by itself confirm that Splunk received the event.

### 5. Check the search and the alert

In Splunk Web, set the time picker to **Last 10 minutes** or the same custom relative range and rerun the Step 2 search. Confirm it shows the new `powershell.exe` process with `-EncodedCommand`, the correct `host`, and a nonempty `ProcessGuid`. The command line contains the encoded value, so the plaintext marker need not appear there. Then allow the next five-minute scheduled run and open **Activity → Triggered Alerts** (or the equivalent page in your release). Look for `LAB - Encoded PowerShell` and inspect the matching result. The alert record can expire; check it soon after the test.

If the search returns a matching row but the alert does not appear, check that the alert is enabled, its owner can search `sysmon`, the cron schedule and `-10m` to `now` range were saved, **Add to Triggered Alerts** is selected, and the result was not suppressed. Review the alert's last run or job messages.

If the Windows marker prints but the hunt returns no row, select **Last 24 hours** and inspect recent process events:

```spl
index=sysmon EventCode=1
| table _time host Image CommandLine ProcessGuid
| head 20
```

If the new process is missing, check the forwarder, Sysmon Event ID `1` collection, and clock alignment with Step 27. If it appears, compare the actual `Image` and `CommandLine` fields with the hunt filter. Do not mark the alert validated until the scheduled run produces a triggered record.

### 6. Preserve reviewed settings

Review the alert in **Settings → Searches, Reports, and Alerts**. A Splunk Web alert can be stored under the owner's user directory or an app directory, depending on its sharing and ownership; do not assume it was written to `/opt/splunk/etc/apps/LAB_SIEM/local/savedsearches.conf`. Do not copy an entire live `savedsearches.conf` or `metadata/local.meta` into this public repository. If you need a reproducible example, record only the reviewed alert stanza and its required permissions in a sanitized example after removing tokens, addresses, and other private values.

### 7. Troubleshooting record — zero Sysmon events and forwarding TLS failures

**Case status: investigation remains open.** On **11 November 2026**, the last supplied search still showed `sysmon_events = 0`. The CA-path edit below was shown in the Windows configuration, but no subsequent configuration-check result, confirmed service reload, or fresh startup result was supplied. Neither event delivery nor the scheduled alert has been validated.

These observations summarize the supplied lab output. Raw logs, process identifiers, certificate fingerprints, credentials, and the unrelated management destination are omitted. The commands below are for the named, isolated lab VMs; updating this document does not run them or change the live systems.

#### 7.1 — Errors, checks, and results so far

| Observation or message | Check or correction | Result and remaining work |
| --- | --- | --- |
| `sysmon_events = 0` over 24 hours, then seven days | Expanded the range and searched other searchable indexes for Sysmon sources/sourcetypes. | Both searches remained empty for the account used. Time and role permissions still matter; the display name alone does not establish local administrator access. |
| Recent local Sysmon Event ID `1` records | `Get-WinEvent` returned recent process-creation events on WINHUNT01. | Local generation works. This does not prove forwarding or indexing. |
| Effective input: `disabled = 0`, `index = sysmon`, `renderXml = true` | Inspected the complete input stanza with `btool --debug`. Some settings came from `TA-Sysmon/local/inputs.conf`; enabled state, index, and XML overrides came from `etc/system/local/inputs.conf`. `current_only = 0` and `start_from = oldest` were present. | The inspected files enable collection. Disk settings are distinct from the running service's loaded state. No explicit sourcetype appeared in the excerpt, but that cannot explain zero results for a search filtering only on `index=sysmon`. |
| Forwarder running as `NT SERVICE\SplunkForwarder` | Compared the service and running `splunkd.exe` executable paths. | Both used the expected Universal Forwarder installation; a different installation was not shown. |
| Effective `lab_tls` output group | Target was `splunk01.lab.test:9997`, with `useSSL = true`, certificate/name verification, the expected alternate name, and TLS 1.2/1.3. No server-specific output override appeared in the supplied excerpt. | The inspected on-disk configuration matches the intended TLS design. The group's `useACK = true` does not by itself identify the failure. |
| `TcpTestSucceeded : True` | Tested TCP 9997 from WINHUNT01. | TCP reachability works; this does not prove TLS or delivery. |
| `TcpOutputFd`: connection forcibly closed by remote host | Compared recurring sender errors with receiver messages. | Forwarding connections fail. This message alone does not identify the exact cause. |
| Applying/removing target quarantine | Observed `AutoLoadBalancedConnectionStrategy` retries and backoff. | This is the forwarder's connection backoff, not endpoint-security quarantine. |
| `TcpOutputProc`: output paused/blocked for increasing seconds | Observed the blocked group and destination in fresh messages. | Event forwarding is stalled. The suggestion to review receiver health is a lead, not a confirmed diagnosis. |
| Receiver `TcpInputProc`: `SSL routines::wrong version number` | Confirmed recurring TLS-handling failures from the Windows lab address. Effective `[splunktcp-ssl:9997]` was enabled, used the intended certificate, allowed TLS 1.2/1.3, and had `requireClientCert = false`. | Those connections failed TLS handling. Plaintext sent to a TLS listener is one hypothesis; no packet capture has established it in this case. |
| Receiver storage check | Both checked filesystems had substantial available space. | The supplied result does not support disk exhaustion as the explanation. |
| Windows forwarder restarted | Reloaded reviewed output settings. New remote-close, quarantine, and blocked-output messages followed; the count remained zero. | This restart did not resolve forwarding. |
| Direct OpenSSL test: TLS 1.3, `Verification: OK`, expected verified peer name | Used Splunk's bundled OpenSSL on WINHUNT01 with the public CA path shown in `server.conf`. | The diagnostic connection validates the live receiver. It does not prove the service's own TLS context or event delivery. |
| CA folder/file ACLs | Displayed permissions grant the service read access, with full control for Administrators and SYSTEM. | No missing read grant was shown. An ACL listing is not an impersonated service-account access test. |
| Startup `SSLCommon`: `Can't read ca certificate file` with no path displayed | Found the message by searching the complete current log. It appeared in `TcpOutEloop` during startup, including after the earlier restart, with error `2147483648` and `system library::No error`. | A concrete CA-loading error needs surrounding output-context evidence. The blank path does not prove that spaces/backslashes caused it, or by itself establish the active group's final failure mechanism. |
| CA path changed to literal `$SPLUNK_HOME/etc/auth/lab/ca.pem` | Backed up the existing file, changed its existing `[sslConfig]` CA line, and retained `caTrustStore = splunk`. | The latest screenshot still showed zero events. Application of this edit and its effect remain unconfirmed; complete 7.5 before calling it a fix. |

Splunk Web displayed **10.6.1.1** in the supplied screenshots. Forwarder management messages reported **10.4.0**; confirm the installed binary with `splunk.exe version` before using version-specific guidance. Do not infer a known defect from a different release.

#### 7.2 — Inspect the Windows sender

Run these searches as the **local Splunk administrator**. Inline time bounds take precedence over the time picker; check the job's displayed bounds.

```spl
index=sysmon earliest=-7d latest=now
| stats count AS sysmon_events
```

```spl
index=* earliest=-7d latest=now (source=*Sysmon* OR sourcetype=*Sysmon*)
| stats count by index source sourcetype
```

**Expected:** A positive count establishes searchable data for that account/range. Another index points to input mapping that needs review. Neither result proves that a newly generated event arrived.

In **Administrator PowerShell on WINHUNT01**, define paths and inspect the local event log, service, executable, and exact input stanza:

```powershell
$UfHome = 'C:\Program Files\SplunkUniversalForwarder'
$SplunkExe = Join-Path $UfHome 'bin\splunk.exe'
$CaPath = Join-Path $UfHome 'etc\auth\lab\ca.pem'
$LogPath = Join-Path $UfHome 'var\log\splunk\splunkd.log'

Get-WinEvent -FilterHashtable @{
    LogName = 'Microsoft-Windows-Sysmon/Operational'
    Id = 1
    StartTime = (Get-Date).AddDays(-7)
} -MaxEvents 5 | Select-Object TimeCreated,Id

Get-CimInstance Win32_Service -Filter "Name='SplunkForwarder'" |
    Format-List Name,State,StartName,ProcessId,PathName

Get-CimInstance Win32_Process -Filter "Name='splunkd.exe'" |
    Format-List ProcessId,ParentProcessId,ExecutablePath

& $SplunkExe btool inputs list 'WinEventLog://Microsoft-Windows-Sysmon/Operational' --debug
```

**Expected:** Recent local ID `1`, a running service at the intended installation, and an enabled input assigned to `sysmon`. Review each setting's source path; local overrides can change an app's intended configuration. Multiple processes alone do not establish a fault.

Inspect connection settings without dumping password/token values:

```powershell
& $SplunkExe btool outputs list --debug |
    Select-String '\[tcpout|\s(defaultGroup|server|disabled|useSSL|clientCert|sslRootCAPath|sslVerifyServerCert|sslVerifyServerName|sslAltNameToCheck|sslCommonNameToCheck|sslVersions|socksServer|socksResolveDNS|sendCookedData|useClientSSLCompression|useACK)\s*=' |
    ForEach-Object { $_.Line }

& $SplunkExe btool server list sslConfig --debug |
    Select-String 'sslRootCAPath|caTrustStore' |
    ForEach-Object { $_.Line }

Test-NetConnection splunk01.lab.test -Port 9997
```

**Expected:** The selected output group targets the intended receiver with TLS and verification enabled. Review any `[tcpout-server://...]` overrides. If the configured CA path differs from the lab example, inspect and use the actual path for `$CaPath`.

Read recent messages, then search the complete current log for startup failures that a tail-only check can miss:

```powershell
Get-Content -LiteralPath $LogPath -Tail 500 |
    Select-String 'TcpOutput|AutoLoadBalanced|WinEventLog|winevtlog|SSL|TLS|certificate|ERROR|WARN' |
    Select-Object -Last 25 |
    ForEach-Object { $_.Line }

Select-String -LiteralPath $LogPath `
    -Pattern 'SSLCommon|SSLConfig|SSLContext|SSLOptions|Failed to create SSL context|ca\.pem|certificate|access.*denied' |
    Select-Object -Last 30 |
    ForEach-Object { $_.Line }

icacls.exe "$UfHome\etc\auth\lab"
icacls.exe $CaPath
```

**Expected:** Compare errors with the most recent service start. Historical messages remain after a correction. If startup messages rotated out of the current log, review the corresponding rotated log privately. The ACL commands display permissions; they do not grant access.

#### 7.3 — Check the receiver and test TLS separately

On **RHEL-SPLUNK01**, inspect the receiving input, shared TLS settings, current errors, and storage:

```bash
sudo -u splunk /opt/splunk/bin/splunk btool inputs list 'splunktcp-ssl:9997' --debug |
  grep -E '\[|[[:space:]](disabled|serverCert|requireClientCert|sslVersions|acceptFrom)[[:space:]]*='

sudo -u splunk /opt/splunk/bin/splunk btool inputs list SSL --debug |
  grep -E '\[SSL\]|[[:space:]](serverCert|requireClientCert|sslVersions|cipherSuite)[[:space:]]*='

sudo tail -n 1000 /opt/splunk/var/log/splunk/splunkd.log |
  grep -Ei 'TcpInput|SSL|TLS|certificate|IndexProcessor|DiskMon|blocked|ERROR|WARN' |
  tail -n 40

df -h /opt/splunk /splunkdata
```

**Expected:** This lab's server-authenticated TLS design uses enabled `[splunktcp-ssl:9997]`, `serverCert = /opt/splunk/etc/auth/lab/splunk01.pem`, `requireClientCert = false`, and TLS 1.2/1.3. These are comparison values, not instructions to overwrite live configuration. Match receiver messages to current sender attempts. Available disk space alone does not prove receiver health.

On **WINHUNT01**, use the actual CA file from 7.2. Run the TLS test only if `Test-Path` returns `True`:

```powershell
Test-Path -LiteralPath $CaPath -PathType Leaf
& $SplunkExe cmd openssl version
```

```powershell
'' | & $SplunkExe cmd openssl s_client -connect 'splunk01.lab.test:9997' -servername 'splunk01.lab.test' -CAfile $CaPath -verify_hostname 'splunk01.lab.test' -verify_return_error -brief
```

**Observed:** TLS 1.3 negotiated, verification returned `OK`, and the verified peer name matched the lab receiver. This validates a diagnostic connection from the interactive account. It does not prove the service loaded the same settings, initialized its TLS context, or delivered an event. The diagnostic's closure can create its own receiver message; distinguish that from the forwarder's attempts.

#### 7.4 — Other messages encountered

| Message family | Interpretation and disposition |
| --- | --- |
| `HttpPubSubConnection` / `HttpClientRequest`: Winsock `10061`, HTTP `502`, broker-response parsing failure on `8089` | These requests targeted a different management/deployment destination from static forwarding to `9997`. No removal or repair of that configuration was performed here. Investigate it separately; it does not by itself explain the forwarding resets. |
| Telemetry HTTP `502` and DNS failures | External telemetry requests failed. These messages do not establish why the lab receiver rejected a connection. |
| `PYTHONHTTPSVERIFY = 0` warning | Embedded Python HTTPS verification needs a separate configuration review. This does not establish that `lab_tls` verification is disabled. No Python setting was changed. |
| `SSLOptions` warns that `server.conf/[sslConfig]/sslVerifyServerCert` or global `outputs.conf/[tcpout]/sslVerifyServerCert` is false | Distinguish those contexts from the group's explicit `sslVerifyServerCert = true`. The global warning alone does not prove the group inherited `false`. No verification setting was disabled as a repair. |
| `X509Verify` warning about the default Splunk CA; HTTP-server certificate metadata | These concern the displayed default local certificate context. Do not confuse it with the separately verified receiver certificate or publish its fingerprint/serial output. No certificate regeneration was performed. |
| Deprecated TLS 1.0/1.1 unavailable; certificate-status validation defaults to none | Informational startup/configuration messages, distinct from the CA-loading error. Forwarding settings already allowed TLS 1.2/1.3. No protocol-version change was made. |
| Malformed JWT header, missing optional AI-assistant object, loopback client sent no data, HEC cache disabled with HTTP `500`, a `cooked` handler capability-check warning, and distributed-index introspection not enabled | These appeared during UI/background requests. The supplied output does not connect them to the Sysmon forwarding failure. No token deletion, HEC change, capability grant, optional app installation, or introspection change was performed. |

The default TLS-compression value and `useACK = true` do not establish a cause. Do not change compression, acknowledgments, protocol negotiation, verification, or the receiver based only on a generic reset/wrong-version message. The [forwarding/TLS and KV-service guide](../troubleshooting/splunk-forwarder-tls-and-kv-service.md) covers earlier receiver and KV context; those earlier observations are not a current KV diagnosis for this case.

#### 7.5 — Attempted CA-path correction and next verification

The latest supplied Windows configuration shows this sanitized excerpt:

```ini
[sslConfig]
sslRootCAPath = $SPLUNK_HOME/etc/auth/lab/ca.pem
caTrustStore = splunk
```

Preserve the rest of the existing file. `$SPLUNK_HOME` is literal configuration text; do not expand it in PowerShell while preparing an edit. This change tests CA-path loading; the evidence does not establish path separators or spaces as the proven cause.

Before editing live configuration, retain a private backup outside Git, Splunk's directories, and all monitored paths, then merge only the reviewed change. Reuse the paths defined in 7.2. Select an existing access-controlled backup directory using the [private-backup procedure](../troubleshooting/splunk-forwarder-tls-and-kv-service.md#step-13--back-up-the-file-that-owns-the-setting); replace the placeholder below before running it.

```powershell
$ConfigPath = Join-Path $UfHome 'etc\system\local\server.conf'
$PrivateBackupDir = 'C:\REPLACE_WITH_APPROVED_PRIVATE_FOLDER'
if (!(Test-Path -LiteralPath $PrivateBackupDir -PathType Container)) {
    throw 'Choose an existing protected backup folder outside Git, Splunk and monitored paths.'
}
$BackupPath = Join-Path $PrivateBackupDir ('server-ca-before-' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '.bak')
Copy-Item -LiteralPath $ConfigPath -Destination $BackupPath -ErrorAction Stop
notepad.exe $ConfigPath
```

**Expected:** A timestamped private backup exists before editing; its permissions and exclusion from collection/publication have been reviewed. The earlier session placed a backup in Splunk's log directory. That location is not recommended: log-directory inputs might collect the file. Review that earlier copy privately and relocate it to approved unmonitored storage after checking the applicable inputs; no relocation or indexing outcome has been confirmed here. The backup operation does not prove the edited configuration was loaded.

For the already reviewed change, first run in **Administrator PowerShell on WINHUNT01**:

```powershell
& $SplunkExe version
& $SplunkExe btool check
```

Resolve relevant configuration errors before restarting. If the check is acceptable and the reviewed change needs a reload:

```powershell
Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz'
Restart-Service -Name SplunkForwarder -ErrorAction Stop
Get-Service -Name SplunkForwarder | Select-Object Name,Status
Get-Process -Name splunkd | Select-Object Id,StartTime,Path

& $SplunkExe btool server list sslConfig --debug |
    Select-String 'sslRootCAPath|caTrustStore' |
    ForEach-Object { $_.Line }
```

**Expected:** The service is `Running` with a new process start time after the recorded restart. A brief forwarding interruption occurs. A Windows-only change requires only the Windows forwarder reload. If the service fails, inspect the fresh error and restore the exact reviewed backup to its original path before rechecking.

After about 30 seconds, inspect fresh startup/connection messages using 7.2. Compare timestamps with the restart; older CA-loading errors do not establish failure after this edit. Then run as the local Splunk administrator:

```spl
index=sysmon earliest=-30m latest=now
| stats count AS sysmon_events
```

A positive count is the first collection check, not completion of Step 45. Generate the Section 4 marker, match its new local ID `1` to a searchable event, confirm the Section 2 hunt result, and verify the scheduled triggered-alert record. If the path change makes no difference, record that result, restore the prior reviewed setting as appropriate, and continue a focused TLS-context investigation rather than stacking unverified changes.

**Windows-specific setting:** The 10.4 `server.conf` reference documents `sslRootCAPathHonoredOnWindows` with default `true`. Its absence from an excerpt does not establish `false`; explicitly changing it was not part of the observed correction. The deprecated output-level `sslRootCAPath` is documented as a fallback when the server setting is unset, so a duplicate output CA setting is not a proven override. Packet capture or debug logging may be a later discriminator if fresh evidence still cannot explain the failing connection; neither was completed in this record.

#### 7.6 — Separate optional-tool errors: module discovery and execution policy

The later PowerShell check returned no loaded `Invoke-AtomicRedTeam` / `powershell-yaml` modules, and `Get-Command Invoke-AtomicTest -Syntax` raised `CommandNotFoundException`. That established that the command was unavailable in that session, not that the packages were absent from disk.

The subsequent `Find-Module` result selected **Invoke-AtomicRedTeam 2.3.0** and **powershell-yaml 0.4.12**. The version-pinned `Install-Module` loop returned without a reported error. Both imports then failed because Windows PowerShell blocked the `powershell-yaml.psm1` script with **running scripts is disabled**, `PSSecurityException`, and `UnauthorizedAccess`. The framework depends on that module, so `Invoke-AtomicTest` remained unavailable. No successful import or Atomic test execution was supplied.

**Step 45's encoded-PowerShell marker does not require Atomic Red Team.** For the separate optional pipe-validation exercise, inspect discoverable modules and the actual policy scopes in the same PowerShell session:

```powershell
Get-Module -ListAvailable -Name Invoke-AtomicRedTeam,powershell-yaml |
    Select-Object Name,Version,Path

Get-ExecutionPolicy -List
Get-ExecutionPolicy
```

**Expected:** Discovery shows the installed versions/paths; the policy list identifies which scope controls script loading. An empty discovery result can also reflect a different user's installation or module search path. Resolve discovery/import errors with [the optional Atomic validation guide, Step 3](../../hunts/cobalt-strike/COBALT_STRIKE_ATOMIC_VALIDATION.md#step-3--install-the-execution-framework-from-an-approved-source).

If `MachinePolicy` or `UserPolicy` is defined, follow the controlling policy and its approved module-signing/distribution process. A process-scoped setting cannot override Group Policy; do not try to bypass it.

For the owned, unmanaged lab, if the packages and their source have been reviewed and a temporary policy change is permitted, the following limits `RemoteSigned` to the **current PowerShell window**:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
Get-ExecutionPolicy
```

**Expected:** The effective policy is `RemoteSigned` if no higher-priority policy overrides it. This allows eligible scripts but still requires trusted signatures on internet-marked scripts. The setting ends when this PowerShell session closes; it does not change the machine/user policy persistently. Review any prompt. If signing or policy still blocks a module, inspect that exact error and use the approved signed package rather than blanket unblocking or switching to `Bypass`/`Unrestricted`.

After policy and discovery checks are satisfied, import the reviewed modules:

```powershell
Import-Module powershell-yaml -ErrorAction Stop
Import-Module Invoke-AtomicRedTeam -ErrorAction Stop
Get-Module Invoke-AtomicRedTeam,powershell-yaml | Select-Object Name,Version,Path
Get-Command Invoke-AtomicTest -Syntax -ErrorAction Stop
```

**Expected:** Both imports succeed and command syntax appears. Stop on the first failed import; repeating dependent commands will not repair it. Importing the framework and displaying syntax do not execute an Atomic test. The session-policy correction remains **proposed and unverified** in this record, and it does not resolve the separate forwarding failure. Complete collection verification before attempting the optional exercise.

#### 7.7 — Preserve safe evidence

Record actual binary versions, test time in UTC, search account/role verification, relevant configuration origins, restart/start time, sanitized fresh errors or connection results, and the matching indexed event. Mark this case resolved only after observing delivery and the scheduled alert.

The supplied configuration screenshot contains encrypted `sslPassword` and `pass4SymmKey` values. Redact those values, other credentials, certificate identifiers, and unrelated endpoint details before publishing screenshots. Encrypted credential values are not suitable public evidence. Keep the original screenshot, raw configuration/logs/events, private keys, and backups outside this public repository.

**Command overview:** `stats count` checks searchable Sysmon events; `coalesce` compares extracted event ID fields; `Get-Service` checks Windows services; `Get-WinEvent` checks Event ID `1` locally. `btool` shows effective input and output settings; `Test-NetConnection` checks TCP reachability; `Get-Content` and `Select-String` inspect recent or startup messages; `Get-CimInstance` checks service identity and executable paths; `icacls` displays CA permissions. OpenSSL tests a diagnostic TLS connection, while `df` checks receiver storage. A private backup, `btool check`, and a recorded restart support a reviewed CA-path change. `$Payload` defines a harmless marker, `ToBase64String` encodes it, and `-EncodedCommand` runs it. The cron expression schedules the search every five minutes.

**Summary:** A successful test has a new Sysmon process event, a matching search result, and a triggered alert record for that event. Keep the observed result and UTC test time in sanitized lab evidence.

References:

- [Splunk Create Scheduled Alerts](https://help.splunk.com/en/splunk-enterprise/alert-and-respond/alerting-manual/10.6/create-alerts/create-scheduled-alerts): This guide explains the schedule, search window, trigger, and alert action settings.
- [Splunk Throttle Alerts](https://help.splunk.com/en/splunk-enterprise/alert-and-respond/alerting-manual/10.6/manage-alert-trigger-conditions-and-throttling/throttle-alerts): This guide explains field-based suppression for per-result alerts.
- [Splunk Monitor Triggered Alerts](https://help.splunk.com/en/splunk-enterprise/alert-and-respond/alerting-manual/10.6/configure-alert-actions/monitor-triggered-alerts): This guide explains how to review triggered alert records.
- [Microsoft Sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon): This guide identifies Event ID `1` as process creation and shows the Sysmon Operational event log.
- [Splunk TLS testing and troubleshooting](https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.2/secure-splunk-platform-communications-with-transport-layer-security-certificates/test-and-troubleshoot-tls-connections): Explains diagnostic TLS connections and sender/receiver log checks.
- [Splunk 10.4 outputs.conf reference](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.4/configuration-file-reference/10.4.0-configuration-file-reference/outputs.conf): Documents output precedence, TLS settings, restart requirements, and the deprecated CA fallback.
- [Splunk 10.4 server.conf reference](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.4/configuration-file-reference/10.4.0-configuration-file-reference/server.conf): Documents the CA store, Windows CA-path setting, and installation-path notation.
- [OpenSSL s_client reference](https://docs.openssl.org/3.0/man1/openssl-s_client/): Explains the TLS diagnostic, CA/hostname verification, and brief output.

- [Microsoft Get-Module](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/get-module?view=powershell-5.1): Distinguishes loaded modules from discoverable modules.
- [Atomic Red Team installation](https://www.atomicredteam.io/docs/invoke-atomicredteam/getting-started): Documents the optional framework and YAML module packages.

- [Microsoft execution policies](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-5.1): Explains scope precedence, RemoteSigned, script-module restrictions, and process-only policy lifetime.

---
