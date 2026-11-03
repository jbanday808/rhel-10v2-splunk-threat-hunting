**Step 49 — Perform the final checks**

On **RHEL**:

```
sudo systemctl is-active Splunkd

findmnt --mountpoint /splunkdata

df -h / /splunkdata

chronyc tracking

sudo -u splunk /opt/splunk/bin/splunk btool check

sudo journalctl -u Splunkd -n 50 --no-pager

sudo tail -n 50 /opt/splunk/var/log/splunk/splunkd.log

sudo openssl x509 \
  -in /opt/splunk/etc/auth/lab/splunk01.pem \
  -noout \
  -enddate
```

**Command overview:**

- `is-active` checks service state.
- `df -h` checks storage.
- `journalctl` shows service messages.
- `tail` shows recent Splunk messages.
- `openssl ... -enddate` checks certificate expiry.

| Problem                   | Check first                                                          |
| ------------------------- | -------------------------------------------------------------------- |
| Cannot connect            | VMware network, guest IP, gateway, and firewall zone.                |
| Updates fail              | DNS, NAT, and Red Hat repositories.                                  |
| Splunk will not start     | Data mount, storage, ownership, certificates, and logs.              |
| Windows data missing      | Event Viewer, forwarder service, permissions, TLS, and target index. |
| Fields are blank          | Add-ons and actual event sourcetype.                                 |
| Custom fields are missing | `siem:lab`, the `REPORT` reference, and expected format.             |
| Directory sign-in fails | IdM DNS, TCP 636, CA trust, final user password, and role mapping. |
| Data disappears early     | Index limits and Windows event-log rollover.                         |

For SELinux denials:

```
sudo ausearch -m AVC -ts recent
```

**Command overview:** `ausearch` finds specific denied operations for investigation.

### Reset the fishbucket for one source file

Use this optional troubleshooting procedure when you intend to read an already monitored file again. The fishbucket stores file-reading checkpoints.

**Single-source reset command — Option C in the reference question:**

```bash
splunk cmd btprobe \
  -d "$SPLUNK_HOME/var/lib/splunk/fishbucket/splunk_private_db" \
  --file "<source-file>" \
  --reset
```

Replace `<source-file>` with the actual file path. The example assumes the default fishbucket location; use the actual location if it was changed. Run the command on the Splunk instance that monitors the file.

For this lab, run the following on **RHEL-SPLUNK01** to reset the monitored file `/var/log/siem-lab/events.log`:

```bash
sudo systemctl stop Splunkd

sudo -u splunk /opt/splunk/bin/splunk cmd btprobe \
  -d /opt/splunk/var/lib/splunk/fishbucket/splunk_private_db \
  --file /var/log/siem-lab/events.log \
  --reset

sudo systemctl start Splunkd

sudo systemctl is-active Splunkd
```

Confirm the intended path if prompted. Stop Splunk before running `btprobe`; the change takes effect after startup.

**Command overview:**

| Command or option | Explanation |
| --- | --- |
| `sudo -u splunk` | Runs the utility as the Splunk service account. |
| `splunk cmd btprobe` | Opens Splunk's file-checkpoint utility. |
| `-d` | Specifies the fishbucket database folder. |
| `--file` | Selects one source file. |
| `--reset` | Resets that file's checkpoint. |
| `systemctl stop/start` | Stops and starts the Splunk service. |

**Summary:** This resets one file's reading checkpoint so an active file monitor can read it again. Existing indexed events remain; rereading can create duplicate events and increase ingestion-license use.

**Reference:** [Splunk Command Line Tools Guide](https://help.splunk.com/en/splunk-enterprise/administer/troubleshoot/10.6/contact-splunk-support/command-line-tools-for-use-with-support): This guide explains `btprobe` options and resetting a specific file's fishbucket checkpoint.

---
