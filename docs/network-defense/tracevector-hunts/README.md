# TraceVector hunts: from practice to lab evidence

The [TraceVector Site](https://tracevector.jamesbanday.chatgpt.site/#scenarios) teaches ten investigations with **synthetic** records and the placeholder `index=tracevector_lab`. These guides show what to verify before adapting each exercise to the documented RHEL 10.2 and Splunk Enterprise lab. They are plans for human review, not reports of live tests or detection coverage.

The lab's existing indexes are `win_security`, `win_system`, `powershell`, `sysmon`, `linux`, and `lab`. A guide names only candidate indexes; first check whether its log source, event type, and fields are actually present. The [interactive lab overview](../INTERACTIVE_LAB.md) explains the Site, and the [ATT&CK coverage map](../../mitre-attack/coverage.md) describes which repository hunts are candidates, context, or gaps.

| Practice hunt | What to check in the real lab | Guide |
| --- | --- | --- |
| A noisy SSH neighbor | Local RHEL SSH failures and accepted logins | [01 · SSH](01-a-noisy-ssh-neighbor.md) |
| Privilege in the wrong hands | Local RHEL sudo actor, target, and command | [02 · sudo](02-privilege-in-the-wrong-hands.md) |
| The job that came back | Cron and file-change visibility gap | [03 · cron](03-the-job-that-came-back.md) |
| A script behind the switch | Sysmon process start and optional script-block context | [04 · PowerShell](04-a-script-behind-the-switch.md) |

## Use one guide at a time

1. Finish the Site exercise and read its example search as a question, not a ready-to-run detection.
2. Confirm the named source reaches the existing index. Inspect original events to learn the real field names.
3. Limit a review to an authorized host and time window. Compare a harmless or approved control before judging a candidate.
4. Record what was observed, what was missing, and what the owner should check next. Keep real logs and identifiers out of this public repository; use the [report template](../../security-operations/templates/threat-hunt-report.md) and [publication checklist](../../reference/security-and-sanitization.md).

An empty search can mean that a source is absent, a field name differs, or the time window is wrong. It is not proof that the behavior did not occur.
