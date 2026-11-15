# SSH failures followed by a successful sign-in

**Status:** proposed, read-only hunt for the owned RHEL 10.2/Splunk lab. The sequence below is an investigation question, not an observed incident or a validated alert.

## Ask a narrow question

Did several failed SSH sign-ins precede a successful sign-in to the **same account on the same RHEL host** from a source the owner cannot explain? A forgotten password, approved test, or automated client can produce a similar pattern. Agree on the host, account, time window, permitted records, and person who can verify the access before searching.

The [syslog setup guide](../SYSLOG_HUNTING_GUIDE.md) describes the existing RHEL Splunk VM pipeline: rsyslog writes selected authentication messages to `/var/log/siem-lab/linux.log`; Splunk monitors that file as `index=linux sourcetype=syslog`. It does not establish that IdM server logs or another Linux host are collected. First confirm a recent [pipeline marker](../SYSLOG_HUNTING_GUIDE.md#try-two-harmless-messages) reached Splunk. A marker proves file delivery only, not SSH-event coverage.

## Review the permitted messages

Run this candidate search in Splunk Search & Reporting, then narrow the time window and host to the approved case:

```spl
index=linux sourcetype=syslog source="/var/log/siem-lab/linux.log" host=splunk01 earliest=-24h latest=now sshd ("Failed password" OR "Accepted password" OR "Accepted publickey")
| table _time host source _raw
| sort 0 _time
```

**Search overview:** the first line limits records to the configured local syslog file and common OpenSSH outcome wording; `table` shows the original messages; `sort` places them in time order. Confirm that the actual `sshd` messages use this wording before relying on the filter. If they do not, search the same source for `sshd` alone and inspect the format. Do not treat an empty result as a clean bill of health.

For each candidate, record privately:

| Check | What to compare |
| --- | --- |
| Identity | Same account in the failed and successful messages; avoid combining different usernames. |
| Origin | Source address when present; check NAT, jump hosts, and shared clients with the owner. |
| Time | Event order and gap in UTC; check clock and indexing delay if the sequence looks wrong. |
| Coverage | A recent pipeline marker, the relevant file input, and any missing portion of the requested window. |
| Approval | Maintenance, password reset, access test, or expected automation. |

**Synthetic example:** three failures for a sample account are followed two minutes later by an accepted login from the same test source. The initial result is **needs owner review**. A benign control is a documented password-reset test with the same pattern. A nonmatching control is a success for a different account or a different source; do not present those events as one session.

## Decide and explain

If the owner cannot account for the successful access, preserve private event references and request the approved wider review. A message showing `Accepted` is evidence of an SSH authentication outcome on this host, not proof of who used the account, what happened afterward, or lateral movement. The local file does not supply IdM-wide or network-wide visibility. If timestamps, usernames, or source context are missing, state that limitation.

Use the [hunt report](../templates/threat-hunt-report.md) to record the hypothesis, exact search, window, competing explanations, evidence references, and next owner action. A plain-language update is: “We found sign-in failures followed by access to the same lab account. We need the account owner's confirmation before deciding whether it was expected.”

**Summary:** verify collection, compare the same account and source, check normal explanations, and report the supported finding only.
