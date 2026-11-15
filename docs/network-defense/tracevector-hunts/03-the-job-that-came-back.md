# The job that came back: separate schedule from evidence

In TraceVector's synthetic story, a file is created under `/etc/cron.d/` and a job then runs three times, five minutes apart. The exercise supplies a shared `resource` field to connect the records. An ordinary cron message may not name the originating file, so that relationship must be established separately in a real hunt. [Open the exercise](https://tracevector.jamesbanday.chatgpt.site/#scenarios).

## First check the visibility gap

The candidate index is the existing `linux` index, **only if** cron and file-change records are actually collected there. The current [local syslog configuration](../../../configs/rsyslog/30-siem-lab.conf) selects authentication messages and the `siem-lab` tag; it does not establish monitoring of `/etc/cron.d/` changes or cron executions. Do not interpret an empty `linux` search as evidence that no job exists. The Windows [scheduled-task search](../../../hunts/mitre-attack/04-scheduled-task-changes.spl) uses `win_security` and different events; it is not a substitute for Linux cron evidence.

If authorized collection is later available, inspect host, `_time`, original source, task path, file owner and permissions, task content, creator identity, schedule, and the execution account. Correlate a file-change event with a cron execution using the host, task details, and time; do not rely on a shared filename alone. Keep task content and real host details private.

## Plan a benign check

1. Have the owner verify a documented, approved cron job and its expected schedule. This is the benign control: repeating on schedule should not be treated as persistence by itself.
2. Confirm which source can record both a task change and a run. If only a local `logger` marker reaches Splunk, record that as pipeline health, not cron coverage.
3. If the owner approves a harmless, temporary lab job, record its expected file change and runs, then review the raw records and remove it under the same change plan. If the sources are absent, stop at a visibility-gap finding.

A recurring backup or update job can resemble the exercise. Conversely, a job can be created without a visible run or can run from a different scheduler. The candidate T1053.003 mapping needs task provenance and execution context before a persistence conclusion.

**Plain-language next step:** “We can see how the practice story connects a new task to repeated runs. We first need evidence that this lab records both events.”
