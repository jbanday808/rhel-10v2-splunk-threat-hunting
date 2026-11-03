## Appendix Splunk local data integrity checks

Use `check-integrity` to compare stored local event data with the hashes recorded by Splunk. Run this procedure on **RHEL-SPLUNK01** after the Splunk app and local `lab` index are working. The procedure includes a short maintenance stop of this standalone lab server.

### Choose the correct command scope

The two supported forms select different amounts of data:

```bash
./splunk check-integrity -index lab -verbose
```

```bash
./splunk check-integrity -bucketPath "/full/path/to/one/bucket" -verbose
```

| Option | Meaning |
| --- | --- |
| `./splunk` | Runs the program from the current directory, normally `/opt/splunk/bin`. The lab commands below use its full path. |
| `check-integrity` | Checks recorded data hashes against the selected local data. |
| `-index lab` | Selects the local index named `lab`, covering its buckets. |
| `-bucketPath` | Selects one actual bucket directory, rather than the index's parent directory. |
| `-verbose` | Displays additional details. |

The supplied question displays `-index` but its explanation switches to `-bucketPath`. Use the first form for an index and the second for one bucket. Do not type the square brackets used to illustrate optional arguments in documentation.

This feature supports local Splunk Enterprise indexes, including this lab's `/splunkdata` storage. It does not support SmartStore indexes or Splunk Cloud Platform. Integrity hashes must have been generated when the data was indexed; enabling the feature now does not create a historical baseline for previously unhashed data.

### Integrity check 1 Review the existing index

On RHEL:

```bash
sudo -u splunk /opt/splunk/bin/splunk btool indexes list lab --debug

findmnt --mountpoint /splunkdata
```

**Command overview:** `sudo -u splunk` runs as the Splunk service account; `btool indexes list lab` shows the merged settings for the lab index; `--debug` identifies their configuration files; `findmnt --mountpoint` checks the exact data mount.

Confirm `homePath = /splunkdata/lab/db` and `coldPath = /splunkdata/lab/colddb`. Check `enableDataIntegrityControl`; its default is `false`.

### Integrity check 2 Enable hashing and preserve the project copy

Back up the current index settings before editing them:

```bash
install -d -m 700 "$HOME/siem-private"

sudo cp -a /opt/splunk/etc/apps/LAB_SIEM/local/indexes.conf \
  "$HOME/siem-private/indexes.conf.before-integrity"

sudoedit /opt/splunk/etc/apps/LAB_SIEM/local/indexes.conf
```

**Command overview:** `install -d -m 700` creates a private backup folder; `cp -a` preserves a copy and its attributes; `sudoedit` opens the configuration with administrator permission.

Add the following setting inside the **existing** `[lab]` section. Keep its storage paths, limits, and all other index sections:

```ini
[lab]
enableDataIntegrityControl = true
```

This snippet shows only the setting to add. It is not a replacement for the complete file from Step 10.

Check the file and apply the change:

```bash
sudo chown splunk:splunk /opt/splunk/etc/apps/LAB_SIEM/local/indexes.conf
sudo chmod 640 /opt/splunk/etc/apps/LAB_SIEM/local/indexes.conf

sudo -u splunk /opt/splunk/bin/splunk btool check
sudo -u splunk /opt/splunk/bin/splunk btool indexes list lab --debug
```

**Command overview:** `chown` assigns ownership; `chmod 640` sets file access; `btool check` validates configuration; the final command confirms which file supplies `enableDataIntegrityControl = true`.

Resolve configuration errors before restarting. Then:

```bash
sudo systemctl restart Splunkd
sudo systemctl is-active Splunkd

cd "$HOME/rhel-splunk-threat-hunting"
sudo cat /opt/splunk/etc/apps/LAB_SIEM/local/indexes.conf \
  > apps/LAB_SIEM/local/indexes.conf
```

**Command overview:** `systemctl restart` reloads Splunk with the new settings; `is-active` checks its state; `cd` selects the project; `sudo cat ... > ...` copies the installed index settings back into the user's project file.

### Integrity check 3 Create and confirm new covered data

Hashing uses SHA-256. Splunk records hashes of new data slices in `rawdata/l1Hashes`; when a bucket becomes warm, it creates `rawdata/l2Hash` from those recorded hashes.

Append one new test record after hashing has been enabled:

```bash
printf '%s action=integrity_check result=success account=labadmin\n' \
  "$(date -u +%FT%TZ)" \
  | sudo tee -a /var/log/siem-lab/events.log
```

**Command overview:** `date -u` supplies the UTC time; `printf` formats one record; `|` passes it onward; `sudo tee -a` appends it to the monitored file.

In the Threat Hunting Lab app, confirm collection:

```spl
index=lab sourcetype=siem:lab "action=integrity_check"
earliest=-15m latest=now
| table _time host action result account _raw
```

**Command overview:** `index` and `sourcetype` choose the lab data; the quoted text finds the test record; `earliest` and `latest` set the time range; `table` displays the selected fields.

### Integrity check 4 Locate a completed bucket

For this small lab, use a planned clean restart after the test record is searchable, then inspect the resulting warm buckets. A normal hot-to-warm roll also creates the bucket-level hash. Do not repeatedly force small bucket rolls as a routine check.

```bash
sudo systemctl restart Splunkd
sudo systemctl is-active Splunkd

sudo -u splunk find /splunkdata/lab/db /splunkdata/lab/colddb \
  -type f -name l2Hash -print
```

**Command overview:** `systemctl` restarts and checks the service; `find` searches local lab storage; `-type f` selects files; `-name l2Hash` finds completed bucket hashes; `-print` displays their paths.

If no matching file exists, do not record a successful integrity check. Confirm hashing is active, new data arrived, and a covered bucket has completed its roll. Repeat the inspection after a normal roll if needed.

Select an actual bucket from the displayed paths. For a path ending in `/rawdata/l2Hash`, the bucket path is the part before `/rawdata/l2Hash`:

```bash
read -r -p 'Full path to the selected warm or cold lab bucket: ' INTEGRITY_BUCKET

sudo -u splunk ls -l -- \
  "$INTEGRITY_BUCKET/rawdata/l1Hashes" \
  "$INTEGRITY_BUCKET/rawdata/l2Hash"
```

**Command overview:** `read -r` stores the selected directory; `ls -l` displays both hash files; `--` ends the command's options. Use the bucket directory itself, not `/splunkdata/lab/db` or the `rawdata` directory.

### Integrity check 5 Run the index and bucket checks

The following lab procedure pauses ingestion and searches while the standalone service is stopped. It gives you a stable inspection window:

```bash
sudo systemctl stop Splunkd

sudo -u splunk /opt/splunk/bin/splunk check-integrity \
  -index lab -verbose

sudo -u splunk /opt/splunk/bin/splunk check-integrity \
  -bucketPath "$INTEGRITY_BUCKET" -verbose

sudo systemctl start Splunkd
sudo systemctl is-active Splunkd
```

**Command overview:** `stop` pauses Splunk; `-index lab` checks the named local index; `-bucketPath` narrows the check to the selected bucket; `-verbose` provides details; `start` resumes the service; `is-active` confirms it returned.

Record both outputs and any warnings before classifying the result. A bucket selected for checking must have an applicable hash baseline. Older buckets in the index may lack one even when the newly covered bucket verifies successfully.

### Integrity check 6 Interpret and record the result

| Result observed | Meaning and next action |
| --- | --- |
| The selected covered data passes its reported checks. | Record the index or bucket scope, command, time, Splunk version, and actual output. |
| Hash files or a historical baseline are missing. | Record that data as not verified. Confirm when hashing was enabled and whether the bucket rolled. |
| A hash mismatch is reported. | Preserve the output and affected data. Investigate with a known backup or Splunk Support before changing files. |
| The path or permissions are wrong. | Confirm the real bucket path and that the `splunk` account can read it. |
| The index uses SmartStore. | This local data integrity feature does not apply. |

Do not delete, edit, or regenerate hash files to make a mismatch disappear. The check validates data against its recorded hashes; it does not repair corruption. Confirm the service is active when you finish, and retain the project configuration update for future deployments.

**Summary:** Enable hashes before collecting the data, select a local index or an individual covered bucket, run the appropriate `check-integrity` command, and record the observed result.

References:

- [Splunk Data Integrity Guide](https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.6/audit-activity-in-splunk-enterprise/manage-data-integrity): This guide explains local data integrity, hash files, and the index and bucket command forms.
- [Splunk Index Configuration Reference](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.6/configuration-file-reference/10.6.0-configuration-file-reference/indexes.conf): This reference explains `enableDataIntegrityControl` and index settings.
- [Splunk Indexed Data Backup Guide](https://help.splunk.com/en/splunk-enterprise/administer/manage-indexers-and-indexer-clusters/10.6/back-up-and-archive-your-indexes/back-up-indexed-data): This guide explains bucket states, clean restarts, and considerations for manual bucket rolls.

---
