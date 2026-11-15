# A name worth a second look: DNS is context

The synthetic exercise shows three PowerShell lookups of one example name, one lookup of another name, and a browser lookup of the first name. Its search keeps the PowerShell events and groups by host and queried name. These reserved example names are not real threat indicators. [Open the exercise](https://tracevector.jamesbanday.chatgpt.site/#scenarios).

## Check the selected DNS source

The existing `sysmon` index is the candidate source. The [PowerShell DNS context search](../../../hunts/mitre-attack/08-powershell-dns-context.spl) uses Sysmon Event 22. Inspect `EventCode`/`EventID`, `Image`, `QueryName`, `QueryResults`, `ProcessGuid`, host, and `_time`. The Site's `query_name`, `query_result`, and short `image` are training fields; actual image values may be full paths.

The shipped Sysmon DNS rule selects `powershell.exe`. It is not full DNS visibility for the lab, and this search does not inspect DNS payloads. If the source is missing or the process filter differs, document that before discussing query frequency.

## Scope a harmless comparison

1. Confirm a known Event 22 record is indexed, then narrow the search to the Windows lab host and an approved short window.
2. Have the owner run a documented, harmless PowerShell name lookup for an owned lab name, if permitted. Record the expected process and time privately; look for the query and its ProcessGuid.
3. A browser lookup of the same approved name is the benign control for the process filter: it should not enter the PowerShell-only result. If browser events are not collected by this rule, use the source configuration to verify the boundary rather than assuming the event exists.
4. For an unexplained repeat, compare the process start, parent, account, schedule, and any authorized network evidence before escalation.

Health checks and scripts can repeat queries. Event 22 says a process asked a DNS question; it does not show a command channel, tunneling, or even a later successful connection. The [coverage map](../../mitre-attack/coverage.md) labels T1071.004 **context only**.

**Plain-language next step:** “This program looked up the same name several times. First confirm the program's approved job and whether it made any related connection.”
