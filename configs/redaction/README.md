# Password redaction configuration

Read the password redaction appendix before deployment. The assembled `apps/LAB_SIEM/local` files already include these stanzas. The two `.example` files contain only the additions, for merging into an older installed lab app.

`scripts/merge_redaction_config.py` previews by default. It appends an absent stanza, accepts an existing matching stanza, and refuses a conflicting stanza before writing either file. The RHEL installer applies the merge with backups under `/var/backups/siem-lab`, prepares the dummy log, checks configuration, and restarts Splunk.

The rule covers lowercase unquoted `password=value` tokens terminated by whitespace, comma, or end of event. It preserves `password=` and replaces the whole token value with `REDACTED`. It is not a rule for JSON or quoted values containing spaces. Only use dummy records until the actual stored `_raw` has been verified in Splunk.

Apply the rule where these events are parsed. In this standalone lab that is RHEL-SPLUNK01, not the Windows Universal Forwarder. Existing indexed events and original source logs do not change.
