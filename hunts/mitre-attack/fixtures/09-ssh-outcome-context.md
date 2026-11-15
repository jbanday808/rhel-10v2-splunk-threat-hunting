# Synthetic check: SSH message outcome

Use this in-memory case with the [local Linux SSH context search](../09-linux-ssh-context.spl). It sends no SSH traffic, changes no account, and indexes no event. The configured `linux` source is the RHEL Splunk VM's local syslog file, not the IdM server or every host.

| Made-up message | Expected label |
| --- | --- |
| `sshd: Failed password` | `failed` |
| `sshd: Accepted publickey` | `accepted` |
| `sshd: Connection closed` | `other sshd context` |
| `sudo: command allowed` | Excluded; no `sshd` text. |

Paste the fixture, then append every pipeline line beginning with the first `| where` from the [production search](../09-linux-ssh-context.spl):

```spl
| makeresults count=4
| streamstats count as seq
| eval _time=now()-300+seq*10, host="fixture-rhel", source="/var/log/siem-lab/linux.log", sourcetype="syslog", _raw=case(seq=1,"sshd: Failed password for training-user from 192.0.2.10",seq=2,"sshd: Accepted publickey for training-user from 192.0.2.20",seq=3,"sshd: Connection closed by 192.0.2.10",true(),"sudo: command allowed")
```

**Expected:** three rows with the labels above; the `sudo` row is absent. The accepted login is from a **different** example address, so it does not show that the failed source gained access. Inspect actual message wording and source health before using these labels; keep unfamiliar forms as other context until reviewed.

This tests text classification only, not syslog delivery or authentication truth. A successful SSH message does not establish who used an account or that lateral movement occurred. Keep real messages private.
