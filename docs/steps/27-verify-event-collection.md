**Step 27 — Verify event collection**

Open **Splunk Web → Search & Reporting** and run each search separately. These searches only return events that have been collected, indexed, and made available to your Splunk role. Keep raw event details in an approved private location.

## Step 27.1 — Review the lab indexes

```spl
(index=win_security OR index=win_system OR index=powershell OR index=sysmon OR index=linux OR index=lab) earliest=-24h
| stats count by index host sourcetype
```

**Query overview:** `index` selects the six existing lab indexes. `earliest=-24h` searches the previous 24 hours, and `stats count` groups the matching events by index, host, and sourcetype.

**Expected result:** A count appears for each combination with searchable events in the time range. An index with no matching events does not appear; its absence does not prove it is missing or that collection is configured correctly.

## Step 27.2 — Check the custom lab event

Paste this search into Splunk Web and click the green **Search** button:

```spl
index=lab sourcetype="siem:lab" earliest=-24h latest=now
| table _time host action result account _raw
```

**Query overview:**

- `index=lab`: Searches the lab index.
- `sourcetype="siem:lab"`: Selects custom lab messages.
- `earliest=-24h latest=now`: Searches the previous 24 hours through the current time.
- `table`: Displays the requested fields and the original message.

**Expected result:** The previously observed lab event appears if it is still within the last 24 hours, is searchable by your role, and has the specified index and sourcetype. The sample `pipeline_check` event may show `action=pipeline_check`, `result=success`, and `account=labadmin`; actual events can contain different values.

The time range in this search is written directly in SPL and overrides the corresponding range selected in Splunk Web. If the event is older than 24 hours, use the alternative below.

### Alternative: search using the time-range picker

Select **Last 7 days** in Splunk Web, paste this search, and click **Search**:

```spl
index=lab sourcetype="siem:lab"
| table _time host action result account _raw
```

**Expected result:** The search uses the selected seven-day range because it has no inline time modifiers. Check that the event timestamp falls within that range.

### If lab fields are blank

If `_raw` contains the expected values but `action`, `result`, or `account` is blank, review the event's actual sourcetype, the `LAB_SIEM` app context and permissions, and its search-time field extraction. The packaged `lab_fields` transform expects `action`, `result`, and `account` in that order with whitespace between them. Compare the actual message format with the transform before changing configuration. Do not publish raw event data.

If no event appears, review the time range, index and sourcetype, role permissions, and whether the event was indexed. Absence from this search alone does not identify the cause.

## Step 27.3 — Check Sysmon process-creation events

Select **Last 7 days** in Splunk Web, paste this search, and click **Search**:

```spl
index=sysmon EventCode=1
| table _time host User Image ParentImage CommandLine ProcessGuid
| head 20
```

**Query overview:**

- `index=sysmon`: Searches the Sysmon index.
- `EventCode=1`: Selects events where the extracted event code is 1, typically Sysmon process creation.
- `table`: Displays the requested process details.
- `head 20`: Shows up to 20 matching results.

**Expected result:** Up to 20 matching events appear if Event ID 1 is present and `EventCode` is extracted as expected. This search has no inline time modifiers, so it uses the **Last 7 days** selection. Field names and values depend on the event format, add-ons, and search-time extraction.

## Step 27.4 — If the Sysmon search returns no results

Keep **Last 7 days** selected and first check for any searchable Sysmon events:

```spl
index=sysmon
| stats count AS sysmon_events
```

**Query overview:** `index=sysmon` selects the Sysmon index. `stats count AS sysmon_events` reports the number of matching events as `sysmon_events`.

- **Count is zero:** No events were searchable in `sysmon` within the selected range for your current role. Check the time range and permissions, the Sysmon Operational channel, the forwarder's input and destination, and the receiving/indexing path. This result alone does not establish where the problem occurred.
- **Count is greater than zero:** Events are present. Check whether process-creation events exist and whether their event ID is extracted as `EventCode`.

To inspect a few events and their available fields, run:

```spl
index=sysmon
| table _time host source sourcetype EventCode EventID _raw
| head 20
```

**Query overview:** `table` displays the event metadata, possible event-ID fields, and original message; `head 20` limits the output. **Expected result:** Inspect `_raw` for an event ID of 1 and compare it with the extracted fields. A blank `EventCode` may require an appropriate add-on or field extraction; a nonzero count alone does not prove Event ID 1 exists. The first 20 results may not include every event type. Keep raw events private.

For missing Windows events or TLS handshake errors, follow the [forwarder TLS and KV service troubleshooting guide](../troubleshooting/splunk-forwarder-tls-and-kv-service.md) and compare a recent local event with its indexed copy.

## Reference

- [Splunk time modifiers](https://help.splunk.com/en/splunk-enterprise/search/spl-search-reference/10.6/time-format-variables-and-modifiers/time-modifiers): Explains how inline `earliest` and `latest` settings interact with the time-range picker.

---
