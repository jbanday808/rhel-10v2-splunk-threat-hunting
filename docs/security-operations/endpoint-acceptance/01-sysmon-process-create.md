# Accept Sysmon process-creation evidence

**Status:** proposed check for WINHUNT01. Source files and a local command do not establish that events reached Splunk. Run this only in the owned lab after the Windows owner approves the test window.

## Question and prerequisites

Can an analyst find a new Sysmon process event with the fields needed to explain **what started, who ran it, and which process started it**? The [forwarder input](../../../apps/LAB_UF_WINDOWS/local/inputs.conf) assigns the Sysmon Operational channel to `index=sysmon`, and the [Sysmon rules](../../../sysmon/sysmon.xml) include process creation. First resolve the [Step 27 collection check](../../steps/27-verify-event-collection.md) and the open TLS/forwarding issue recorded in [Step 45](../../steps/45-create-and-test-an-alert.md). Do not mark this case passed while the indexed source is still missing.

Use the harmless encoded `Write-Output` command already documented in Step 28.9 of the [lab activity guide](../../steps/28-generate-harmless-hunting-activity.md). Record its UTC start time privately. It prints a marker locally; the command line contains an encoded value, so the plaintext marker need not appear in Sysmon Event ID 1.

## Check the endpoint and indexed copy

On WINHUNT01, review the local Sysmon Operational log for a new **Event ID 1** at the recorded time. Then search Splunk with a tight approved window:

```spl
index=sysmon host=WINHUNT01 earliest=-30m latest=now
| eval event_id=tonumber(coalesce(EventCode,EventID))
| where event_id=1
| table _time _indextime host source sourcetype Image ParentImage CommandLine User ProcessGuid ProcessId _raw
| sort 0 -_time
```

**Search overview:** this checks the configured index and host, accepts either common extracted event-ID field, and displays both event and index time plus the original record. Replace the relative window with the approved UTC bounds if indexing is delayed. Keep `_raw` in a private review; do not paste it into GitHub. If the event ID is only visible in XML, record an extraction gap rather than assuming no process event exists.

| Acceptance item | Expected observation to verify |
| --- | --- |
| Matching source | A local Event ID 1 and an indexed copy from the Sysmon Operational channel, not merely a count in `sysmon`. |
| Process identity | `Image` identifies the new PowerShell executable and `ProcessGuid` is populated; do not join later events by PID alone. |
| Parent and account | `ParentImage` and `User` can be interpreted from the original record. Blank fields require schema review. |
| Command and timing | `CommandLine` shows `-EncodedCommand` and `_time` is plausible against the privately recorded run time; inspect `_indextime` for delay. |

For a **nonmatching control**, inspect a separately observed, approved ordinary process event, such as the `cmd.exe` launched in Step 28.7 of the [lab activity guide](../../steps/28-generate-harmless-hunting-activity.md). Its presence confirms process coverage but should not satisfy the encoded-PowerShell search in [Step 45](../../steps/45-create-and-test-an-alert.md). Verify the control was actually collected before calling the filter selective. A process event alone does not prove that the command succeeded or that an alert ran.

## Record the outcome

In approved private evidence, retain the UTC test window, local event reference, indexed event reference, exact search, field gaps, ingestion delay, and any forwarding error. Mark **pass** only when the matching event and needed fields are observed; mark **inconclusive** when collection or extraction is missing. A plain-language result is: “We can see that the test process started and who launched it, but we still need separate evidence for what it did and whether the scheduled alert fired.”

Use the [hunt report template](../templates/threat-hunt-report.md) for the decision and next owner. [Microsoft's Sysmon event guide](https://learn.microsoft.com/en-us/windows/security/operating-system-security/sysmon/sysmon-events) describes Event ID 1 and Process GUID context.
