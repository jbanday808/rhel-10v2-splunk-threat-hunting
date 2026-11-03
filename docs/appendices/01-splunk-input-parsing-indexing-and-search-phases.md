## Appendix Splunk input parsing indexing and search phases

Splunk processes data in this order: **Input → Parsing → Indexing → Search**. The first three phases collect, prepare, and store records. The search phase lets you investigate the stored events and use them in dashboards and alerts.

Read this section alongside **Step 9**. The examples use the existing `siem:lab` configuration from Step 10. Run the RHEL checks after Steps 16–20 are complete; check Windows collection after Step 27 and directory-user access after Step 41.

### Where each phase runs in this lab

| Phase | Main purpose | Location in this lab |
| --- | --- | --- |
| Input | Collect records and identify their source. | Windows Universal Forwarder for Windows channels; RHEL Splunk for local files. |
| Parsing | Separate text into events and recognize event times. | RHEL Splunk processes the custom text input. Official add-ons support Windows event formats. |
| Indexing | Store events and the files used to find them. | RHEL Splunk indexer using `/splunkdata`. |
| Search | Retrieve events, extract fields, and display results. | RHEL Splunk provides both the search interface and local search execution. |

The Windows Universal Forwarder collects and sends records; it cannot index or search them. It has limited parsing capabilities for certain structured inputs. This guide places the full custom text parsing rules on RHEL. If you later add a heavy forwarder, review where parsing occurs before moving those rules.

### Input phase

The input phase reads data and assigns source information such as `host`, `source`, `sourcetype`, and the destination `index`.

For the custom RHEL input, `inputs.conf` monitors `/var/log/siem-lab/events.log`, assigns `host = splunk01` and `sourcetype = siem:lab`, and selects `index = lab`.

For Windows, `inputs.conf` on WINHUNT01 selects the event channels. Its `outputs.conf` sends the collected records to `splunk01.lab.test:9997` over TLS. The RHEL receiver accepts that connection. Steps 11 and 26 contain the forwarder settings and checks.

The fishbucket tracks reading progress for monitored files. The single-file reset in Step 49 is an optional replay procedure. Windows Event Log inputs use their own checkpoints, so that fishbucket command does not reset Windows event-channel collection.

**Summary:** Input chooses what Splunk collects and labels where it came from.

### Parsing phase

Parsing turns incoming text into individual events and determines each event's timestamp. It can also apply configured rules that change, filter, or route events before storage.

The existing `[siem:lab]` section in `props.conf` uses these settings:

- `LINE_BREAKER` separates records at line endings.
- `SHOULD_LINEMERGE = false` keeps the test records separate.
- `TIME_PREFIX = ^` starts timestamp detection at the beginning of the record.
- `TIME_FORMAT = %Y-%m-%dT%H:%M:%SZ` recognizes the lab's UTC date format.
- `MAX_TIMESTAMP_LOOKAHEAD = 20` limits the timestamp area to 20 characters.
- `TZ = UTC` sets the time zone for this source type.

Apply these rules to `siem:lab` on RHEL. Keep the Windows and Sysmon add-on rules for their own source types. Changing parsing settings affects newly processed records; it does not automatically correct events already stored.

**Summary:** Parsing defines each event and its time before Splunk stores it.

### Indexing phase

The indexer stores the parsed events as compressed event data with associated search index files. Splunk groups these files into storage units called buckets.

In this guide, the `[lab]` section of `indexes.conf` places active data under `/splunkdata/lab/db` and older searchable data under `/splunkdata/lab/colddb`. Its size and age limits determine when data is retired. Step 10 defines these settings, and Step 13 prepares the mounted data disk.

The `_time` field represents the event's time; `_indextime` records when Splunk indexed it. They can differ when older records arrive later.

**Summary:** Indexing saves the events and prepares them for efficient retrieval.

### Search phase

The search phase retrieves stored events and applies search commands, field extractions, and other search settings. Reports, dashboards, and alerts use searches.

In this lab, `REPORT-lab-fields = lab_fields` in `props.conf` references `[lab_fields]` in `transforms.conf`. This rule extracts `action`, `result`, and `account` when a search runs. `KV_MODE = none` disables automatic key-value extraction for `siem:lab`, so the named extraction is especially useful.

The same `props.conf` therefore contains settings used in different phases. `LINE_BREAKER` and `TIME_FORMAT` control parsing; `REPORT-lab-fields` and `KV_MODE` control search-time extraction. A `REPORT` reference applies at search time, while a `TRANSFORMS` reference can apply transformations during parsing.

LDAPS verifies a directory user's identity. The mapped Splunk role controls access to indexes and search features. After Step 41, `hunter01` should use the `lab_hunter` role to search the six permitted lab indexes, including `lab`.

**Summary:** Search turns stored events into useful results within the user's permissions.

### Verify the four phases step by step

Use the installed settings under `/opt/splunk`, rather than only reviewing the project copies. The following checks inspect configuration; the test in Check 5 deliberately adds one harmless record.

**Check 1 — Review the input**

On **RHEL-SPLUNK01**:

```bash
sudo -u splunk /opt/splunk/bin/splunk btool inputs list \
  'monitor:///var/log/siem-lab/events.log' --debug
```

**Command overview:** `sudo -u splunk` runs as the Splunk service account; `btool inputs list` displays the merged input settings; the quoted name selects this file monitor; `--debug` shows the source configuration files.

Confirm `disabled = 0`, `index = lab`, `sourcetype = siem:lab`, and `host = splunk01`.

**Check 2 — Review parsing**

```bash
sudo -u splunk /opt/splunk/bin/splunk btool props list siem:lab --debug
```

**Command overview:** `btool props list siem:lab` shows the effective settings for the custom source type; `--debug` identifies where each setting comes from.

Confirm the line-breaking and UTC timestamp settings listed above. This command shows configuration on disk; the new-event test below checks the running behavior.

**Check 3 — Review indexing and storage**

```bash
sudo -u splunk /opt/splunk/bin/splunk btool indexes list lab --debug

findmnt --mountpoint /splunkdata

df -h /splunkdata
```

**Command overview:** `btool indexes list lab` displays the lab index settings; `findmnt --mountpoint` confirms the data disk is mounted at the exact path; `df -h` displays storage use in readable units.

Confirm the configured paths point to `/splunkdata/lab`, the mount exists, and the disk has free space.

**Check 4 — Review search field extraction**

```bash
sudo -u splunk /opt/splunk/bin/splunk btool transforms list lab_fields --debug
```

**Command overview:** `btool transforms list lab_fields` displays the extraction rule referenced by `REPORT-lab-fields`; `--debug` shows its configuration file.

Confirm the rule extracts `action`, `result`, and `account`. Run the search in the Threat Hunting Lab app so the app's search settings are available.

**Check 5 — Add a new test record**

```bash
printf '%s action=phase_check result=success account=labadmin\n' \
  "$(date -u +%FT%TZ)" \
  | sudo tee -a /var/log/siem-lab/events.log
```

**Command overview:** `date -u +%FT%TZ` creates the expected UTC timestamp; `printf` formats one record; `|` passes it to the next command; `sudo tee -a` appends it to the monitored file with administrator permission.

**Summary:** This creates a new entry that can pass through input, parsing, and indexing without resetting an existing checkpoint.

**Check 6 — Search for the new event**

In Splunk Web, sign in as the local `admin` account, open the **Threat Hunting Lab** app, and run this search:

```spl
index=lab sourcetype=siem:lab source="/var/log/siem-lab/events.log"
"action=phase_check" earliest=-15m latest=now
| table _time host source sourcetype action result account _raw
```

**Command overview:** `index`, `sourcetype`, and `source` select this input's stored events; the quoted text finds the test record even if field extraction fails; `earliest=-15m latest=now` limits the time range; `| table` displays the named fields; `_raw` shows the original event text.

Allow a few seconds for collection. Confirm that the new event appears, `_time` represents the same moment as its UTC timestamp, allowing for your displayed time zone, `host` is `splunk01`, and the extracted fields show `action = phase_check`, `result = success`, and `account = labadmin`.

After Step 41, repeat the search as `hunter01`. Confirm the mapped `lab_hunter` role permits the `lab` index. The same record may appear several times if you deliberately repeat Check 5.

### Find the phase to investigate

| Observation | Phase or setting to check first |
| --- | --- |
| The test record is absent from the source file. | Event generation and the file path, before Splunk input. |
| The file contains the record, but Splunk never reads it. | Input enablement, file permissions, and the monitored path. |
| Records merge together or have the wrong time. | Parsing rules for `siem:lab`; use All time temporarily if the event time is wrong. |
| Splunk reports a missing index or cannot write data. | Index definition, the `/splunkdata` mount, free space, and ownership. |
| The raw event appears, but custom fields are empty. | Search-time `REPORT-lab-fields`, `[lab_fields]`, and app permissions. |
| Admin finds the event, but the directory hunter cannot. | LDAP group mapping, `lab_hunter` index permissions, and the search time range. |

Record the observed event, timestamp, extracted fields, and directory-user result in your lab evidence. Configuration output alone does not prove that all four phases succeeded.

References:

- [Splunk Data Pipeline Guide](https://help.splunk.com/en/splunk-enterprise/administer/distributed-deployment-manual/10.6/overview-of-splunk-enterprise-distributed-deployments/how-data-moves-through-splunk-deployments-the-data-pipeline): This guide explains the input, parsing, indexing, and search phases.
- [Splunk Configuration and Data Phases Guide](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.6/administer-splunk-enterprise-with-configuration-files/configuration-parameters-and-the-data-pipeline): This guide explains which settings apply during each phase and where to configure them.
- [Splunk Indexing Guide](https://help.splunk.com/en/splunk-enterprise/administer/manage-indexers-and-indexer-clusters/10.6/indexing-overview/how-indexing-works): This guide explains how Splunk processes events and stores searchable data.
- [Splunk Universal Forwarder Guide](https://help.splunk.com/en/splunk-cloud-platform/forward-and-process-data/ingest-actions/process-data-with-forwarders/the-universal-forwarder): This guide explains what the Universal Forwarder collects and forwards and its processing limits.

---
