# Splunk Integration — New Network Indexes Without Disrupting Existing Sources

## Required baseline

Existing Splunk: `RHEL-SPLUNK01`, HTTPS `8000`, TLS receiver `9997`. Original lab indexes (`win_security`, `win_system`, `powershell`, `sysmon`, `linux`, `lab`) and source apps are **not replaced**. New network indexes and sensor forwarding are **proposed**.

Start with the [one-time upload walkthrough](OFFLINE_HTTP_WALKTHROUGH.md#8-upload-a-small-fixture-to-the-existing-splunk-index) to practice source validation, event time and correlation in `lab`. Use the forwarding procedure below for an approved dedicated sensor deployment.

## Step A — Create or merge new indexes (RHEL-SPLUNK01)

Review [configs/network-defense/splunk/indexes.conf.example](../../configs/network-defense/splunk/indexes.conf.example). Create optional indexes `net_zeek`, `net_suricata`, `net_yara` in an approved Splunk \`local/indexes.conf\` location. Confirm volume location, ownership, retention, disk budget and RBAC. Do not copy `.example` files into active app directories without review or change approval.

Read current effective definitions:

~~~bash
sudo -u splunk /opt/splunk/bin/splunk btool indexes list --debug
sudo -u splunk /opt/splunk/bin/splunk btool authorize list role_lab_hunter --debug
~~~

**Command overview:** Displays merged index/role settings and file precedence. Index creation alone does not grant analyst role access, nor prove log ingestion.

## Step B — Verify TLS forwarder path (RHEL-SENSOR01 only after installed)

Sensor can run **Splunk Universal Forwarder** from a verified vendor package and send approved JSON metadata to `splunk01.lab.test:9997`, requiring server CA and hostname verification. The current Splunk firewalld source rules may only permit Windows `.20`: the new sensor `.40` must get a separately approved source-limited rule, not a broad all-host allow.

Review the disabled [sensor input template](../../apps/SENSOR_UF/local/inputs.conf). Stage only approved metadata in the example directories. Enable individual inputs on the sensor after confirming the dedicated service account can read the staged files and the verified TLS receiver, destination indexes and parsers are ready.

Read effective UF settings only after installation:

~~~bash
sudo /opt/splunkforwarder/bin/splunk btool outputs list --debug
sudo /opt/splunkforwarder/bin/splunk btool inputs list --debug
~~~

If installed elsewhere or service identity differs, use the actual path/identity. Verify endpoint and certificate trust from the sensor. Do not weaken \`sslVerifyServerCert\` or use untrusted certificates.

## Step C — JSON indexing and timestamp caveat

Zeek JSON has an epoch-seconds `ts`, while Suricata EVE has an ISO 8601 `timestamp`. Confirm each source's `_time` matches the event time on a sanitized test. Older events can age out immediately in short-retention indexes. For the DNS fixture, supply a recent `--timestamp` to the generator before regenerating the offline logs and keep the replay labeled as synthetic.

Proposed inputs use `sourcetype=zeek:json` and `sourcetype=suricata:eve`; matching parsing configuration must be reviewed for the actual ingestion mechanism and installed Splunk version. Parsing is not guaranteed by this source template. Set explicit line-breaking for newline JSON and proper timezone if necessary, and account for forwarding/rotation behavior. \`INDEXED_EXTRACTIONS=json\` is not prescribed blindly.

## Step D — Queries to prove data actually arrived

~~~spl
(index=net_zeek OR index=net_suricata OR index=net_yara) earliest=-24h
| stats count latest(_time) as last_event by index host sourcetype
| eval last_seen=strftime(last_event,"%Y-%m-%d %H:%M:%S")
~~~

~~~spl
index=net_suricata earliest=-24h event_type=alert
| stats count by alert.signature_id alert.signature src_ip dest_ip
| sort -count
~~~

**Command overview:** First search summarizes sources and last event, second groups actual Suricata alerts. No returned rows means there is no matching indexed evidence, not a passing test.

## Step E — RBAC, retention and protection

- Explicit analyst role/index allowlist, auditability and safe backups.
- PCAPs and raw malware samples **never** indexed in a public lab.
- Approved DNS queries/IPs/identities only; consider stripping or hashing sensitive fields before indexing.
- Record retention and source controls, including minimum necessary information.
- Keep Splunk management port `8089` private; use existing verified LDAPS identity plan.
- Verify Windows UF, IdM and original Splunk hunts still work after optional sensor changes.

**Acceptance:** Source logs inspected, index count greater than zero, expected `_time` and JSON fields, server cert validated, failed/denied unauthorized access tested and evidence sanitized.
