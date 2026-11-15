# Accept Sysmon network-connection evidence

**Status:** proposed check for WINHUNT01; no live connection or indexed Event ID 3 is claimed. Use only an approved destination and time window on the owned lab VM. Skip the connection test when outbound access is not approved.

## Question and prerequisites

Can an analyst connect a permitted network connection to the **process that opened it**, while keeping a connection separate from proof of web activity or malicious intent? The [Sysmon rule](../../../sysmon/sysmon.xml) includes NetworkConnect for images ending in `powershell.exe` or `curl.exe`. The [Windows forwarder input](../../../apps/LAB_UF_WINDOWS/local/inputs.conf) assigns the Sysmon Operational channel to `index=sysmon`. The rule does not promise visibility for every executable or a full packet record.

First complete the basic [Step 27 collection check](../../steps/27-verify-event-collection.md) and resolve the pending forwarding/TLS issue recorded in [Step 45](../../steps/45-create-and-test-an-alert.md). If collection is absent, this acceptance check stays pending.

## Use a known, harmless connection

If the owner approved outbound traffic, use the existing `curl.exe` request to `https://example.com/` in Step 28.10 of the [lab activity guide](../../steps/28-generate-harmless-hunting-activity.md). Record the UTC time and expected destination privately. A successful `curl.exe` response shows that the command reached a server; it does not show that Sysmon logged or Splunk indexed the connection. DNS, proxy, TLS and network rules can change which destination address appears in the event.

On WINHUNT01, inspect the Sysmon Operational log for a new **Event ID 3** near that time. Then run this candidate search in Splunk with the approved window:

```spl
index=sysmon host=WINHUNT01 earliest=-30m latest=now
| eval event_id=tonumber(coalesce(EventCode,EventID))
| where event_id=3
| eval process_guid=coalesce(ProcessGuid,ProcessGUID)
| table _time _indextime host Image User process_guid SourceIp SourcePort DestinationIp DestinationPort Protocol Initiated _raw
| sort 0 -_time
```

**Search overview:** the search keeps the configured Sysmon index and host, limits to network-connection records, and exposes the original event for private review. Replace the relative window with the recorded UTC bounds if needed. If `EventCode` and `EventID` are blank but XML shows Event ID 3, document an extraction gap. Do not publish raw addresses or event details.

| Acceptance item | What to verify |
| --- | --- |
| Local and indexed event | A local Event ID 3 and a corresponding indexed copy with plausible times. |
| Process link | `ProcessGuid` is populated and matches a separately observed Event ID 1 for the same host and process. Do not join only on a reused PID or a shared address. |
| Network context | Destination, port, protocol and `Initiated` are interpreted from the original record, with proxy or DNS uncertainty noted. |
| Benign explanation | The approved `example.com` request and any network change record explain this particular connection; the record is not a threat finding. |

For a **nonmatching control**, inspect an actually collected Event ID 1 for a different `ProcessGuid` or an Event ID 3 for a different host/process. It must stay outside the candidate's process link. If no suitable control was collected, leave that check pending. The [process/network hunt](../../../hunts/mitre-attack/01-process-network.spl) is a hypothesis-driven follow-up, not a substitute for the original records.

## Record the outcome

Keep the local event reference, indexed event reference, approved destination, UTC window, Process GUID match, field gaps and collection delay in private evidence. Mark **pass** only for the observed source and scope; mark **inconclusive** when the local event, forwarding, or process identity is missing. Explain it simply: “We can connect this test network request to its program. The log shows a connection, not what the person intended or what an encrypted session contained.”

Use the [hunt report template](../templates/threat-hunt-report.md) for the next owner decision. [Microsoft's Sysmon event guide](https://learn.microsoft.com/en-us/windows/security/operating-system-security/sysmon/sysmon-events) describes Event IDs 1 and 3 and their Process GUID relationship.
