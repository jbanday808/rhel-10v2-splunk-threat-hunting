# TraceVector · Threat Hunting Lab

[Open the current TraceVector Site](https://tracevector.jamesbanday.chatgpt.site/) · [Start a guided hunt](https://tracevector.jamesbanday.chatgpt.site/#scenarios) · [Browse the Site source](../../website/tracevector-lab/)

TraceVector is a practice space for asking a security question, reviewing clues, and explaining what the clues do and do not show. It offers **10 guided hunts** with made-up records. You can also organize evidence, draft Splunk searches, and write a short report. You do not need to run the lab to try the guided exercises.

## Start in five steps

1. Open the [Scenario lab](https://tracevector.jamesbanday.chatgpt.site/#scenarios) and choose a question that interests you.
2. Read the sample records. They are training examples, not activity from a real customer or the live lab.
3. Answer the three questions. The feedback explains why each answer matters.
4. Read the example Splunk search. Splunk Search Processing Language (SPL) is a way to ask questions of collected logs. The Site shows the search; it does not run it.
5. Note what you would check next. Use the [hunt report template](../security-operations/templates/threat-hunt-report.md) to explain the finding, uncertainty, and next action in plain language.

## What you can explore

| Section | Plain-language purpose |
| --- | --- |
| [Lab overview](https://tracevector.jamesbanday.chatgpt.site/#overview) | See the practice environment and your progress. |
| [Lab objectives](https://tracevector.jamesbanday.chatgpt.site/#objectives) | Track the skills you want to practice. |
| [Scenario lab](https://tracevector.jamesbanday.chatgpt.site/#scenarios) | Work through 10 guided investigations. |
| [Evidence & screenshots](https://tracevector.jamesbanday.chatgpt.site/#evidence) | Organize lab images and your own investigation notes. |
| [Hunt follow-up](https://tracevector.jamesbanday.chatgpt.site/#remediation) | Plan what to check or recommend after a hunt. |
| [Detection studio](https://tracevector.jamesbanday.chatgpt.site/#detections) | Draft and review Splunk searches. |
| [Project documentation](https://tracevector.jamesbanday.chatgpt.site/#docs) | Find the supporting hunting and lab guides. |
| [Progress tracking](https://tracevector.jamesbanday.chatgpt.site/#progress) | Keep a journal and export or import your workspace. |
| [Lab proposals](https://tracevector.jamesbanday.chatgpt.site/#review) | Prepare a proposed update for human review. |

## The 10 practice hunts

| Hunt | Question to investigate |
| --- | --- |
| A noisy SSH neighbor | Do repeated sign-in failures need a closer look? |
| Privilege in the wrong hands | Was an elevated command expected? |
| The job that came back | Is a recurring task approved? |
| A script behind the switch | What did a PowerShell script do? |
| An account fast-tracked to admin | Was a new account given elevated access? |
| The startup entry that changed | Why did a startup setting change? |
| When the log goes quiet | Was an event log cleared? |
| A name worth a second look | Are repeated DNS lookups worth investigating? |
| A process with a new destination | Did a program connect to an unexpected address? |
| One source, several accounts | Were several accounts targeted from one source? |

The searches use `index=tracevector_lab` and simplified training fields. That name is a **practice placeholder**, not an index configured in the lab. To adapt a search for the real Splunk lab, first check which logs are available and use one of its six documented indexes: `win_security`, `win_system`, `powershell`, `sysmon`, `linux`, or `lab`. A sample result or completed exercise does not prove that a detection works against live data.

For a step-by-step bridge from each practice story to the possible real lab records, use the [TraceVector hunt transition guides](tracevector-hunts/README.md). Each guide includes a harmless comparison and a source-visibility check.

## Save your work

Your progress, notes, drafts, and attachments are stored in the browser you use. Export a workspace backup from **Progress tracking** before clearing browser data or changing devices. Keep that backup private because it can contain your notes and evidence. Importing a backup replaces the current browser's TraceVector workspace after a confirmation step.

Use the [private hunt-report handoff](TRACEVECTOR_PRIVATE_HANDOFF.md) when a practice idea becomes a separately approved investigation. It explains how to carry over the question and draft while keeping backups and real evidence private.

The Site does not connect to Splunk, collect logs, test a host, or change GitHub. Proposed updates stay in your browser until someone reviews and applies them separately.

## Learn more

- [Threat-hunting method](../security-operations/THREAT_HUNTING_METHOD.md): plan a question, check the available evidence, and explain the result.
- [Syslog hunting guide](../security-operations/SYSLOG_HUNTING_GUIDE.md): use local RHEL logs to investigate SSH and sudo activity.
- [Splunk threat-hunting reference](../reference/SPLUNK_THREAT_HUNTING_REFERENCE_GUIDE.md): understand example searches and common troubleshooting steps.
- [Tools and cloud hunting](../reference/tools-and-cloud.md): see how Zeek, Wireshark, Splunk Enterprise, Arkime, RHEL 10.2, Kali, VMware Workstation Pro, AWS, Azure, and VS Code fit into a hunt.
- [Evidence publication checklist](../reference/security-and-sanitization.md): review records and images before putting them in a public repository.

The [Site source](../../website/tracevector-lab/) contains the public interface and training examples. Hosting controls access to the live Site; the repository source does not include your browser data.
