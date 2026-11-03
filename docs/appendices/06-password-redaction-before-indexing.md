## Appendix Password redaction before indexing

**Question 151 answer: B.** Put `SEDCMD-redact_pw` in `props.conf` under the source type that receives the events. The following lab procedure uses `[identity]`. It changes the incoming raw event during parsing before storage. `REGEX-redact_pw` is not a valid substitute for this setting, and `SEDCMD` does not belong in `transforms.conf`.

Run this exercise after `LAB_SIEM` and the `lab` index work. Configure RHEL-SPLUNK01, which parses this local text file. In a distributed deployment, configure and test the first full parsing tier before sending sensitive events. This exercise does not use structured indexed extractions.

This example masks lowercase, unquoted `password=value` tokens whose values end at whitespace, a comma, or the end of the event. It supports slashes within the value. Quoted values containing spaces, JSON properties, and other field spellings need separate rules and tests. Use only the fake `LAB-DUMMY` values below until the live result is verified.

### Redaction step 1 Open the project on the RHEL server

Copy the extracted source project to RHEL-SPLUNK01 using the guide's existing transfer process, then open a terminal there. Use your actual project location if it differs:

```bash
cd ~/rhel-splunk-threat-hunting
test -d apps/LAB_SIEM/local
sudo systemctl is-active Splunkd
sudo -u splunk /opt/splunk/bin/splunk btool indexes list lab --debug
```

**Command overview:** `cd` opens the source project; `test` checks its app folder; `systemctl` checks the service; `btool` shows the effective lab index and the files supplying its settings. Confirm the index and service before continuing.

Keep the existing `siem:lab` source type and other inputs. The ZIP already includes the additions in `apps/LAB_SIEM/local`; the next snippets also support updating an older installed app.

### Redaction step 2 Define the dedicated file input

The ZIP includes this snippet. To recreate it from the project root:

```bash
mkdir -p configs/redaction
cat > configs/redaction/inputs.conf.example <<'EOF'
[monitor:///var/log/siem-lab/identity.log]
disabled = 0
index = lab
sourcetype = identity
host = splunk01
EOF
```

**Command overview:** `mkdir -p` creates the snippet folder; the quoted heredoc writes the stanza literally. The monitor reads one dedicated file, assigns source type `identity`, and stores events in `lab`. The input is enabled with `disabled = 0`.

### Redaction step 3 Define the parsing rule in props conf

Create or review the matching snippet:

```bash
cat > configs/redaction/props.conf.example <<'EOF'
[identity]
SHOULD_LINEMERGE = false
LINE_BREAKER = ([\r\n]+)
TIME_PREFIX = ^
TIME_FORMAT = %Y-%m-%dT%H:%M:%SZ
MAX_TIMESTAMP_LOOKAHEAD = 20
TZ = UTC
KV_MODE = none
REPORT-lab-fields = lab_fields
SEDCMD-redact_pw = s/\b(password=)[^,\s]+/\1REDACTED/g
EOF
```

**Command overview:** `[identity]` matches the input source type. The timestamp settings match the generator's UTC timestamp, and line breaking keeps each log line separate. `REPORT-lab-fields` reuses the existing search time extraction for action, result, and account. The `SEDCMD` setting performs the masking before indexing.

Read the substitution as follows:

| Part | Purpose |
| --- | --- |
| `s/…/…/g` | Replace every matching occurrence in the event. |
| `\b(password=)` | Match the lowercase key at a word boundary and capture it. |
| `[^,\s]+` | Match one or more value characters through the next comma or whitespace. |
| `\1REDACTED` | Keep the captured key and replace the value with `REDACTED`. |

For example, `password=LAB-DUMMY-ONE` becomes `password=REDACTED`. The replacement preserves the key and uses the correctly spelled marker. Preserve the backslashes and straight quotes when copying commands.

### Redaction step 4 Merge the additions and restart Splunk

Review the supplied helper files before running them. Preview the changes first:

```bash
sudo python3 scripts/merge_redaction_config.py \
  --target-dir /opt/splunk/etc/apps/LAB_SIEM/local
```

**Command overview:** The merger checks both installed configuration files before proposing changes. Preview mode writes nothing. It appends an absent stanza, accepts a matching stanza, and stops if the named stanza exists with incomplete or conflicting settings.

Then use the RHEL installer:

```bash
sudo bash scripts/rhel/install-redaction-lab.sh
```

**Command overview:** The installer applies the preflighted merge, backs up changed files under `/var/backups/siem-lab/redaction-*`, prepares the dedicated log with `root:splunk` ownership and mode `0640`, restores SELinux labels, checks the configuration, and restarts `Splunkd`. It does not truncate an existing log.

For a manual update, back up the installed app outside the repository. Merge the snippets into its `local/inputs.conf` and `local/props.conf`, adding each stanza once. Retain existing stanzas and `transforms.conf`; never overwrite a complete configuration with a snippet.

Resolve conflicting stanzas manually, then rerun preview. If installation stops after a change, inspect its backup and configuration errors before retrying. Use dummy credentials throughout.

### Redaction step 5 Verify the effective configuration

Run these commands even when the installer has printed them:

```bash
sudo -u splunk /opt/splunk/bin/splunk btool check
sudo -u splunk /opt/splunk/bin/splunk btool props list identity --debug
sudo -u splunk /opt/splunk/bin/splunk btool inputs list \
  'monitor:///var/log/siem-lab/identity.log' --debug
sudo -u splunk test -r /var/log/siem-lab/identity.log
sudo systemctl is-active Splunkd
```

**Command overview:** `btool` checks configuration and shows effective settings and their files; `test -r` checks source access; `systemctl` checks service status.

Confirm that effective `[identity]` includes the intended `SEDCMD-redact_pw`, that the monitor uses `sourcetype = identity`, `index = lab`, and `disabled = 0`, and that the values come from the intended local configuration. Resolve conflicting overrides before continuing. A successful configuration listing does not prove that an event has been masked.

### Redaction step 6 Generate a fresh dummy event

After the restart and checks succeed, run the supplied generator:

```bash
sudo bash scripts/rhel/generate-redaction-marker.sh
```

**Command overview:** The generator appends one UTC record containing two fake password tokens and prints a unique `SIEM-LAB-REDACTION-…` test ID. Copy that exact ID. The second token tests the global replacement flag.

The source record has this layout, with generated timestamp and ID values:

```text
2026-11-01T12:00:00Z action=redaction_check result=success account=labadmin password=LAB-DUMMY-ONE password=LAB-DUMMY-TWO test_id=SIEM-LAB-REDACTION-EXAMPLE
```

This is an example, not an observed event. The actual source file still contains its fake plaintext values. `SEDCMD` changes the ingested event, not the original file. Protect source logs and configure the producing application to avoid logging real passwords.

### Redaction step 7 Inspect the stored raw event

In Splunk Search, use an account allowed to search `lab`. Replace the example marker with the exact newly printed ID:

```spl
index=lab sourcetype=identity source="/var/log/siem-lab/identity.log"
"SIEM-LAB-REDACTION-REPLACE-WITH-EXACT-ID" earliest=-15m latest=now
| table _time host source sourcetype _raw
```

**Command overview:** The base search selects the dedicated source and test ID; `table` displays the stored `_raw` value. Allow ingestion time, then rerun the same search. Both `password=` occurrences should read `password=REDACTED`. This search applies no display masking.

Use the same exact ID in the count check:

```spl
index=lab sourcetype=identity source="/var/log/siem-lab/identity.log"
"SIEM-LAB-REDACTION-REPLACE-WITH-EXACT-ID" earliest=-15m latest=now
| eval unmasked=if(match(_raw,"password=LAB-DUMMY-"),1,0)
| eval masked=if(match(_raw,"password=REDACTED"),1,0)
| stats count AS events sum(masked) AS masked_events sum(unmasked) AS unmasked_events
```

**Command overview:** `match` checks the stored event text; `eval` labels each event; `stats` counts the retrieved, masked, and unmasked events. A pass requires `events > 0`, `masked_events = events`, `unmasked_events = 0`, and visual confirmation that both values are replaced. Zero matching events is an incomplete test.

The ZIP includes a reusable recent-event overview search:

```bash
cat > hunts/11-password-redaction-check.spl <<'EOF'
index=lab sourcetype=identity source="/var/log/siem-lab/identity.log"
"SIEM-LAB-REDACTION-" earliest=-15m latest=now
| eval unmasked=if(match(_raw,"password=LAB-DUMMY-"),1,0)
| eval masked=if(match(_raw,"password=REDACTED"),1,0)
| stats count AS events sum(masked) AS masked_events sum(unmasked) AS unmasked_events
EOF
```

**Command overview:** The heredoc saves the search for later use. Its broad marker covers recent redaction exercises; use an exact ID when validating a specific change. Record the live observations in `evidence/sanitized/redaction-validation.md`.

### Redaction step 8 Test changes and troubleshoot

From the extracted project root on RHEL or WSL, run the source checks and offline tests:

```bash
python3 scripts/validate_project.py
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
```

**Command overview:** The validator checks source files and lab settings. Tests cover dummy values, delimiters, repeated keys, and safe merging; `-B` prevents bytecode files. Python checks shared regex features, so live Splunk verification remains required. GitHub's Linux workflow runs these tests.

If events are missing, check the exact ID, time range, index permission, monitor path, source readability, service status, and Splunk internal logs. If plaintext dummy values remain, confirm the event source type and effective parsing rule, check for overrides, restart the parsing instance, and generate a fresh marker. Search time `replace` or `rex mode=sed` can change displayed output, so do not use them to prove stored-data redaction.

The rule applies only to events ingested after activation. It does not rewrite existing indexed events. The fishbucket reset in the earlier guide can cause replay; it is not a repair for previously stored secrets. Use a new dummy event for each test. For real historical exposure, follow your organization's incident and data-remediation process, including credential rotation where applicable.

Retest the original `siem:lab` marker. Record the new test ID, count, configuration path, commit, and time. Review the diff before publishing; keep backups and raw evidence outside GitHub.

**Summary:** Match the input's source type to `[identity]`, place `SEDCMD-redact_pw` in the parsing tier's `props.conf`, restart, generate a fresh dummy record, and verify its stored `_raw` before relying on the rule.

References:

- [Splunk Props Configuration Reference](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.6/configuration-file-reference/10.6.0-configuration-file-reference/props.conf): Defines `SEDCMD`, substitution syntax, captured replacements, and index time use.
- [Splunk Data Anonymization Guide](https://help.splunk.com/en/splunk-enterprise/get-started/get-data-in/10.6/configure-event-processing/anonymize-data): Explains source type matching and deployment on the parsing Splunk Enterprise instance.

---
