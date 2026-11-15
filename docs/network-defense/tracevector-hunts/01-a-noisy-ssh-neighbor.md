# A noisy SSH neighbor: from practice to the lab

**Question:** Did repeated SSH sign-in failures on the RHEL Splunk VM come from an expected source? TraceVector's six records are made up. Five failures from one example address meet its training threshold, while a successful login comes from a different address. The latter is **not** evidence that the first source gained access. [Open the exercise](https://tracevector.jamesbanday.chatgpt.site/#scenarios).

## Find the real records

The candidate destination is the existing `linux` index. The configured local path is `/var/log/siem-lab/linux.log` with `sourcetype=syslog`; it receives selected authentication messages from the **RHEL Splunk VM only**. Start with the [SSH context search](../../../hunts/mitre-attack/09-linux-ssh-context.spl) and the [syslog setup and health guide](../../security-operations/SYSLOG_HUNTING_GUIDE.md). Do not copy the Site's `index=tracevector_lab` into a real search: it is a training placeholder.

Before counting attempts, inspect a few original `sshd` messages. Confirm `_time`, `host`, `source`, the attempted account, remote address, result (failed or accepted), and any session identifier. The Site's `src_ip`, `user`, and `action` fields are simplified; real syslog may require extraction from `_raw`. Also confirm clocks and whether accepted and failed records reach the same file.

## Validate in a small, authorized window

1. Verify the pipeline with the harmless `logger` markers in the syslog guide. They prove delivery, **not** SSH detection.
2. With the host owner, select a short window containing an approved SSH test or maintenance session. Compare original failed and accepted messages before grouping by remote address and host. If permitted, arrange a small number of failed attempts to a disposable lab account; record the source, time, and expected count privately.
3. Use an approved successful login from a **different** source as a benign control. It should remain distinct from the failure cluster. Check the underlying events if a grouped result appears to mix them.
4. Record the actual event count, missing fields, time window, and source health. If no SSH messages arrive, report a visibility gap rather than a clean hunt.

Five failures is a practice threshold, not a universal attack threshold. A typo, a stale service credential, or approved testing can create a burst; missing remote addresses or logs can hide one. The IdM VM's authentication logs are not automatically ingested here.

**Plain-language next step:** “We found repeated sign-in attempts on this host. We need the system owner to confirm the source and any later access before calling it an attack.” Use the [hunt report template](../../security-operations/templates/threat-hunt-report.md) and keep raw records private.
