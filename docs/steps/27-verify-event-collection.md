**Step 27 — Verify event collection**

In Splunk **Search & Reporting**:

```
(index=win_security OR index=win_system OR index=powershell OR index=sysmon OR index=linux OR index=lab) earliest=-24h
| stats count by index host sourcetype
```

Check custom fields:

```
index=lab sourcetype=siem:lab earliest=-30m
| table _time host action result account _raw
```

Expected values:

| Field     | Value            |
| --------- | ---------------- |
| `action`  | `pipeline_check` |
| `result`  | `success`        |
| `account` | `labadmin`       |

Check Sysmon fields:

```
index=sysmon EventCode=1 earliest=-30m
| table _time host User Image ParentImage CommandLine ProcessGuid
| head 20
```

**Search overview:**

- `index` selects stored records.
- `earliest` sets the time range.
- `stats count` counts records.
- `table` selects columns.
- `head` limits displayed rows.

If records arrive but useful fields are blank, verify the add-ons and actual sourcetype.

---
