# Sudo activity after a Linux sign-in

**Status:** proposed, read-only hunt for the owned RHEL 10.2/Splunk lab. No command execution, privilege misuse, or live detection is established by this guide.

## Ask a narrow question

After a permitted SSH sign-in to the RHEL Splunk VM, did that same account run an administrator command that the owner did not expect? `sudo` is a normal administration tool. Its presence is a reason to review the account, command, timing, and approved change record, not an incident verdict.

The configured [local syslog pipeline](../SYSLOG_HUNTING_GUIDE.md) sends authentication-facility messages from the Splunk VM to `index=linux` with `sourcetype=syslog`. Confirm the effective input and a recent harmless marker first. The repository does not show that IdM server command logs or every shell command are forwarded.

## Build a short timeline

Run this candidate search in Splunk, then replace the time window and host with the approved scope:

```spl
index=linux sourcetype=syslog source="/var/log/siem-lab/linux.log" host=splunk01 earliest=-24h latest=now ("sshd" OR "sudo:")
| table _time host source _raw
| sort 0 _time
```

**Search overview:** the source and host restrict this to the documented local file; `sshd` and `sudo:` find candidate sign-in and privilege records; the original message remains visible for human interpretation. If the installed logger uses different program names or a message was not routed to this file, revise the search only after inspecting the real format and documenting the difference.

Compare the following before connecting two records:

1. Does the SSH message show an accepted sign-in for the **same account**? A failed sign-in did not establish access.
2. Does the sudo message identify the invoking user, target user, terminal, and `COMMAND=`? Preserve the full command only in approved private evidence.
3. Are the events close in time on the same host? A nearby timestamp does not prove the sudo process belongs to that SSH session. Shared accounts, local console sessions, automation, and clock differences may break the assumed link.
4. Is there an approved maintenance or troubleshooting task that explains the command? Ask the host owner or change owner.
5. Are there missing events or a gap in the local syslog pipeline? A missing sudo message cannot establish that no command ran.

**Synthetic example:** a sample account signs in and a later sudo record shows a service-status check. That is a candidate to compare with the change record. A benign control is a documented maintenance session with the same account and command. A nonmatching control is a sudo message for a different user, or a local console session during the same period.

## Record the decision

If the owner cannot explain the activity, retain private references to the sign-in, sudo record, authorized change history, and any collection gap, then seek approval for further review. Syslog can show an attempt or logged command; it does not by itself show the full process tree, command result, or intent. Do not claim a specific user ran the command merely because a shared account appears.

Record the question, time window, raw-message references, alternative explanations, and next owner in the [hunt report](../templates/threat-hunt-report.md). For a nontechnical audience: “We found administrator activity near a sign-in. We are checking whether the account owner expected that action.”

**Summary:** use the messages to form a timeline, verify account and session context, and explain uncertainty before recommending action.
