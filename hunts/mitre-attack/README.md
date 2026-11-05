# ATT&CK-aligned hunting searches

These are **read-only, unvalidated hunt candidates**, not deployed detections.
The [mapping](../../docs/mitre-attack/coverage.md) explains the technique
relationships and the [playbook](../../docs/mitre-attack/hunt-playbook.md)
provides the full investigation and testing workflow. Run only on an authorized
lab. Copy one search at a time into Splunk Search & Reporting or the Threat
Hunting Lab app.

Before interpreting results, run
[`00-data-health.spl`](../00-data-health.spl), verify the relevant event codes
and field names with your installed add-ons, and narrow the host and time range.
Results and raw events may contain real accounts, commands, addresses, script
blocks, or DNS names; keep them private.

| Search | Hypothesis / question | Important limitations |
| --- | --- | --- |
| [01-process-network.spl](01-process-network.spl) | A PowerShell or curl process may have both a start and a network event. | Joins on host and ProcessGuid; the Sysmon network rule covers only those two executable names. A connection is not proof of C2. |
| [02-failures-before-success.spl](02-failures-before-success.spl) | At least five failures precede a success for the same host, domain, account, and source in 15 minutes. | Requires extracted, nonlocal source addresses and both event types. Equal timestamps, event loss, missing domains, address formats, and `streamstats` limits can affect results. |
| [03-account-to-group.spl](03-account-to-group.spl) | A created account was added to a local security group on the same host within one hour. | Joins Event 4720 `TargetSid` to Event 4732 `MemberSid`, not the group's `TargetSid`; each returned group addition is filtered to the window. Equal timestamps, the search lookback, and `streamstats` limits can affect results. Check that the actual group is privileged before interpreting it as privilege escalation. |
| [04-scheduled-task-changes.spl](04-scheduled-task-changes.spl) | A task was created or modified. | Requires auditing and extracted task names; creation does not prove execution or malicious intent. |
| [05-lab-run-key.spl](05-lab-run-key.spl) | The specifically included SIEMLab Run key was modified. | The shipped Sysmon filter does **not** monitor all Run keys or Startup folders. |
| [06-event-log-clear-candidates.spl](06-event-log-clear-candidates.spl) | A Windows log-clear record may exist. | Security 1102 and System 104 are candidates; verify System 104's provider is `Microsoft-Windows-Eventlog`. A missing event does not rule out log clearing. |
| [07-multiple-account-failures.spl](07-multiple-account-failures.spl) | One source failed against at least five distinct domain/account pairs in a fixed 15-minute bucket. | A possible spray pattern is not proof that the same password was used. Bucket boundaries, missing source IPs, and small labs affect recall. |
| [08-powershell-dns-context.spl](08-powershell-dns-context.spl) | PowerShell made a DNS query. | The shipped Sysmon rule and this search select `powershell.exe`; a DNS query is not proof of C2. |
| [09-linux-ssh-context.spl](09-linux-ssh-context.spl) | SSH messages reached the local Linux authentication log. | Only the Splunk VM's configured auth log is included; an SSH login is not by itself lateral movement. |
| [10-rare-parent-child.spl](10-rare-parent-child.spl) | A parent/child image pair appeared three or fewer times in seven days. | This is an illustrative rarity threshold, not a statistically established baseline; missing processes and benign software changes are common. |
| [11-investigation-timeline.spl](11-investigation-timeline.spl) | Ordered events from available sources can support reconstruction. | A time-ordered list does not establish causality. Filter to the case scope and independently validate host, identity, ProcessGuid, and clock alignment. |

`sort 0` and `streamstats` are deliberately straightforward for a small lab.
They can be expensive or affected by Splunk result and memory limits at enterprise
scale; narrow the scope and redesign/test the approach before using it on large
datasets. `first_seen`, `last_seen`, `created_at`, and `added_at` are epoch values;
convert to UTC for the report. Source IP and user/domain normalization may need
adjustment for your actual events.

## Optional Microsoft Defender XDR example

[`optional-defender-powershell-network.kql`](optional-defender-powershell-network.kql)
is a separate, read-only example for a **separately licensed and deployed**
Microsoft Defender for Endpoint environment. The lab does not provision Defender,
connect those tables to Splunk, or claim results from this query. It correlates
on device ID, process ID, and process creation time to reduce PID-reuse errors.
Exact timestamp equality, the one-hour correlation window, and the 24-hour
lookback can miss events; verify schema and event availability in your tenant.
The `-enc` substring is deliberately broad and can match benign commands.

Sources: [DeviceProcessEvents](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-deviceprocessevents-table),
[DeviceNetworkEvents](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicenetworkevents-table),
and [Defender advanced hunting](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-query-language).
