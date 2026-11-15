# A process with a new destination: match the process, not its name

TraceVector has a PowerShell start and connection with the same synthetic ProcessGuid. It also has a PowerShell start and a **different** PowerShell connection that should not be paired. A curl start/connection pair provides another example. Image name alone would mix separate executions. [Open the exercise](https://tracevector.jamesbanday.chatgpt.site/#scenarios).

## Candidate lab records

Use the existing `sysmon` index and the [process/network hunt](../../../hunts/mitre-attack/01-process-network.spl). It pairs Event 1 (process start) with Event 3 (network connection) by **host and ProcessGuid**. Inspect `EventCode`/`EventID`, `Image`, `ParentImage`, `User`, `ProcessGuid`, `DestinationIp`, `DestinationPort`, host, and `_time` in raw records; the Site's lowercase names are fixture fields. Verify consistent host names and clocks before correlating.

The shipped Event 3 rule covers only `powershell.exe` and `curl.exe`. It does not give every process connection. A destination port of 443 does not prove HTTPS, and a destination address alone does not identify its owner or intent. The [coverage map](../../mitre-attack/coverage.md) calls T1071.001 **context only**.

## A lab-controlled check

1. Confirm Event 1 and Event 3 collection separately for the Windows lab host. A missing Event 3 means a join cannot establish the absence of a connection.
2. If approved, use `curl` to contact a service controlled inside the isolated lab. This documented request is the benign control: both event types should share a host and ProcessGuid, yet it is expected activity.
3. Review an unexplained candidate's parent process, user, command line, destination, and change plan. Keep an orphan process start or connection separate; do not join by executable name or nearby timestamp.
4. Request authorized Zeek, Arkime, proxy, or packet evidence only if protocol details are needed and those sources exist for the period.

Updates, downloads, and administration can produce the same pattern. Event loss, filtering, and short retention can also remove one side of a pair. There is no live command-and-control validation in this guide.

**Plain-language next step:** “This particular program contacted a destination. Check who launched it, what the destination is, and whether the connection matched planned work.”
