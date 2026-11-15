# When the log goes quiet: check the event provider

TraceVector includes a Security 1102 record, a System 104 record from `Microsoft-Windows-Eventlog`, and a second System 104 from a different training provider. The event number alone does not identify a log-clear operation. [Open the exercise](https://tracevector.jamesbanday.chatgpt.site/#scenarios).

## Two existing indexes, one scoped question

Use `win_security` for Event 1102 and `win_system` for Event 104. The [log-clear candidate search](../../../hunts/mitre-attack/06-event-log-clear-candidates.spl) combines them. Check `EventCode`/`EventID`, channel/index, `Provider_Name` or equivalent, actor when supplied, host, `_time`, and the original event message. For System 104, verify that the provider is `Microsoft-Windows-Eventlog`; the Site's `training_source` field is only a fixture label.

The repository's [reviewed ATT&CK mapping](../../mitre-attack/coverage.md) uses T1685.005 for Clear Windows Event Logs. Even a correctly identified record leaves the reason for clearing open.

## Validate without clearing a real log

1. Confirm Security and System events are arriving from the Windows lab host within the selected period. Check each channel separately so a failure in one is visible.
2. Use the Site's synthetic records or an offline test fixture to confirm that the query retains 1102 and provider-verified 104 but excludes the other-provider 104. That other-provider event is the benign control for the provider filter.
3. If a real candidate already exists, ask the owner about maintenance, log rotation, and the account involved. Compare records forwarded **before** the time in question with independent collection or service records, where authorized. Preserve evidence privately.

Do not clear Security or System logs merely to test this hunt; doing so destroys investigative context. A missing event may reflect forwarding delay, a stopped sensor, retention, time selection, or no activity. A gap in events by itself does not prove deliberate clearing.

**Plain-language next step:** “The records suggest a log may have been cleared. Verify the source and maintenance reason, then check whether an independent copy is available.”
