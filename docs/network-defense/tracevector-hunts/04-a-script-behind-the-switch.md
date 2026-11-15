# A script behind the switch: review encoded PowerShell

TraceVector's fixed example contains one PowerShell process start with `-EncodedCommand`, a related synthetic network record, and an ordinary `Get-Date` command. The encoded text is a training marker and the Site never executes it. The search selects the **process-start** event; a network event for the same process is a separate clue. [Open the exercise](https://tracevector.jamesbanday.chatgpt.site/#scenarios).

## Translate the fields

Start in the existing `sysmon` index with Event 1 and the [encoded PowerShell example](../../../hunts/01-encoded-powershell.spl). Check whether your installed fields are `EventCode` or `EventID`, `Image`, `CommandLine`, `ParentImage`, `User`, and `ProcessGuid`. The Site's lowercase `image`, `command_line`, and `process_guid` are normalized training names. If available, use the existing `powershell` index for Event 4104 script-block context and `sysmon` Event 3 for a process-specific network pivot. Confirm these sources were actually delivered before interpreting their absence.

## Check a bounded lab window

1. Verify a known Sysmon process-start event appears for the Windows 11 lab host, then narrow to PowerShell and the approved time window.
2. Use an authorized `Get-Date` run as the benign control. It should establish that PowerShell process starts are visible while staying outside the encoded-argument filter.
3. If a preapproved encoded-command exercise exists, compare the raw command line, parent, user, and ProcessGuid with the planned activity. Do not decode or run an unknown argument just to test the search. Pivot to Event 3 or 4104 only when those records are present and access is authorized.

Encoding can be used in legitimate scripts. The argument alone does not show what ran, whether it succeeded, or whether a network connection was malicious. Sysmon Event 3 in this repository is restricted to selected executables; missing 4104 can reflect collection or logging settings. The [coverage map](../../mitre-attack/coverage.md) labels PowerShell a candidate, not a validated detection.

**Plain-language next step:** “This command hides its text in an encoded argument. We need its owner, parent program, approved purpose, and any recorded script content before deciding what it means.”
