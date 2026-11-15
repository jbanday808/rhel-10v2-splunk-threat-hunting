# The startup entry that changed: respect the sensor's scope

TraceVector shows two synthetic changes to `HKCU\Software\Microsoft\Windows\CurrentVersion\Run\SIEMLab`, plus unrelated registry changes. A Run value may start a program at sign-in, but a value change alone does not prove the program ran. [Open the exercise](https://tracevector.jamesbanday.chatgpt.site/#scenarios).

## Find what is actually watched

The existing `sysmon` index is the candidate source. The [lab Run-key search](../../../hunts/mitre-attack/05-lab-run-key.spl) looks for Sysmon Events 12, 13, and 14 with the specifically monitored `SIEMLab` path. Check `EventCode`/`EventID`, `TargetObject`, `Details`, `Image`, `User`, `ProcessGuid`, host, and `_time` against the original Sysmon events. The Site's lowercase fields are normalized fixture names.

The shipped Sysmon rule is intentionally narrow: it does **not** monitor every Run value or Startup folder. A blank result cannot establish that startup persistence is absent. Check [the coverage map](../../mitre-attack/coverage.md) before describing the monitored path to someone else.

## Review an approved change

1. Verify that recent Sysmon registry events from the Windows lab host reach Splunk and that the configured rule actually includes the `SIEMLab` path.
2. If the owner approves a harmless change to that monitored lab value, record the expected writer, time, and `Details`; compare Events 12/13/14 and preserve the raw record privately. Revert under the same change plan.
3. Use a documented, unrelated application preference change as the benign control. Its absence from this focused search is expected and shows the **filter's boundary**, not a general registry outage. If source health is uncertain, inspect Sysmon collection independently.
4. To assess execution, separately inspect approved sign-in and process-start records for the same host and time. Match identity and process context; do not infer execution from the registry value.

Software installers and update agents often change startup settings legitimately. The destination path could be absent or a harmless file. The exercise supports a T1547.001 question only within this monitored path, and no live test is claimed.

**Plain-language next step:** “A watched startup setting changed. Confirm who changed it, why, and whether the named program actually started.”
