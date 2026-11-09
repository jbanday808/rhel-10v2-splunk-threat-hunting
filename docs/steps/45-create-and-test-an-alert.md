**Step 45 — Create and test an alert**

This lab alert looks for a Sysmon process-creation event when `powershell.exe` starts with `-EncodedCommand`. A match is activity to investigate, not proof of malicious activity. Complete the test on **WINHUNT01** only. The alert depends on searchable Sysmon Event ID `1` data and an active Splunk license that permits scheduled alerts.

Ordinary Windows activity can already produce Sysmon Event ID `1`. The encoded-PowerShell test in Section 4 is a separate step; first make sure Splunk can search the existing process events.

### 1. Confirm the Windows process data is arriving

In Splunk Web, sign in as the local Splunk administrator and open **Search** in the **Threat Hunting Lab** app. If your release opens **Search & Reporting** as a separate app, note that app context and review the alert's sharing after saving. Set the time picker to **Last 24 hours** and run:

```spl
index=sysmon
| stats count AS sysmon_events
```

If `sysmon_events` is zero, skip the next search and follow **If either count is zero** below. Check the time range and role permissions; a zero count alone does not identify the cause. If events exist, check process creation:

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
& "$UfHome\bin\splunk.exe" btool inputs list --debug |
    Select-String 'WinEventLog://Microsoft-Windows-Sysmon/Operational' -Context 0,9
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

**Command overview:** `stats count` checks searchable Sysmon events; `coalesce` compares extracted event ID fields; `Get-Service` checks Windows services; `Get-WinEvent` checks Event ID `1` locally. `btool` shows effective input and output settings; `Test-NetConnection` checks TCP reachability; `Get-Content` shows recent forwarder messages. `$Payload` defines a harmless marker, `ToBase64String` encodes it, and `-EncodedCommand` runs it. The cron expression schedules the search every five minutes.

**Summary:** A successful test has a new Sysmon process event, a matching search result, and a triggered alert record for that event. Keep the observed result and UTC test time in sanitized lab evidence.

References:

- [Splunk Create Scheduled Alerts](https://help.splunk.com/en/splunk-enterprise/alert-and-respond/alerting-manual/10.6/create-alerts/create-scheduled-alerts): This guide explains the schedule, search window, trigger, and alert action settings.
- [Splunk Throttle Alerts](https://help.splunk.com/en/splunk-enterprise/alert-and-respond/alerting-manual/10.6/manage-alert-trigger-conditions-and-throttling/throttle-alerts): This guide explains field-based suppression for per-result alerts.
- [Splunk Monitor Triggered Alerts](https://help.splunk.com/en/splunk-enterprise/alert-and-respond/alerting-manual/10.6/configure-alert-actions/monitor-triggered-alerts): This guide explains how to review triggered alert records.
- [Microsoft Sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon): This guide identifies Event ID `1` as process creation and shows the Sysmon Operational event log.

---
