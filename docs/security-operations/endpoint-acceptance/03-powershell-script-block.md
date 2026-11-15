# Accept Windows PowerShell script-block evidence

**Status:** proposed check for WINHUNT01. No Event ID 4104 delivery or live detection is established by this document. Script-block records can contain sensitive commands, so review them only in approved private storage.

## Question and prerequisites

Can an analyst find a harmless Windows PowerShell script block in the **PowerShell Operational** channel and the existing `powershell` index? [Step 23](../../steps/23-enable-windows-auditing-and-powershell-logging.md) describes enabling script-block logging, and the [forwarder input](../../../apps/LAB_UF_WINDOWS/local/inputs.conf) maps `Microsoft-Windows-PowerShell/Operational` to `index=powershell`. This is the `powershell.exe` path in the lab; PowerShell 7 uses a different provider/channel unless separately configured.

Confirm [Step 27](../../steps/27-verify-event-collection.md) shows the channel is searchable and resolve the pending forwarding/TLS problem in [Step 45](../../steps/45-create-and-test-an-alert.md) first. A process event in `sysmon` is not evidence that the PowerShell Operational channel is collected.

## Match one safe marker end to end

With the WINHUNT01 owner's approval, run the harmless encoded `Write-Output 'SIEM-LAB-ENCODED-TEST'` example in Step 28.9 of the [lab activity guide](../../steps/28-generate-harmless-hunting-activity.md). Record the UTC run time privately. The local console output confirms only that this command ran; it does not establish a logged script block or an indexed copy.

On WINHUNT01, check the **Microsoft-Windows-PowerShell/Operational** log for a new Event ID 4104 and inspect its original text privately. In Splunk, search the approved window:

```spl
index=powershell host=WINHUNT01 earliest=-30m latest=now
| eval event_id=tonumber(coalesce(EventCode,EventID))
| where event_id=4104
| table _time _indextime host source sourcetype ScriptBlockId MessageNumber MessageTotal ScriptBlockText _raw
| sort 0 -_time
```

**Search overview:** the query uses the configured index and host, accepts either common extracted event-ID field, and keeps source/time context. Inspect the original record when `ScriptBlockText` or other fields are blank. Narrow the window to the approved UTC period and keep command content private. Script-block text can be split across messages; review parts together only when their actual identifiers and counts support that relationship.

| Acceptance item | What to verify |
| --- | --- |
| Local and indexed record | A local 4104 and corresponding indexed copy are present after the test. |
| Test text | The harmless marker appears in the original script-block content; an encoded process command line alone is insufficient. |
| Field and time context | Event ID, host, source, `_time`, and `_indextime` are plausible; document extraction or clock gaps. |
| Benign control | The marker is the approved test, not a finding of malicious PowerShell use. |

For a **nonmatching control**, inspect an actually collected 4104 from a different approved script and confirm it is not labeled as the marker test. If no separate 4104 exists, leave this control pending. A Sysmon Event ID 1 for the encoded PowerShell process is useful context but does not replace 4104 or prove the output succeeded.

## Record the outcome

Keep the local and indexed event references, UTC window, full private query, any multi-part message details, field gaps, and owner confirmation in private evidence. Mark **pass** only when both source and indexed marker are observed; mark **inconclusive** when the Operational channel or extraction is missing. In everyday terms: “The lab recorded the test script's contents, so an analyst can review what was submitted to PowerShell. This does not tell us that every PowerShell version or host is covered.”

Use the [hunt report template](../templates/threat-hunt-report.md) for the outcome. [Microsoft's Windows PowerShell logging guide](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging?view=powershell-5.1) describes the 4104 channel and warns that script-block text can be sensitive.
