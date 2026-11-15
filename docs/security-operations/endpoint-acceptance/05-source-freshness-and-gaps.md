# Check source freshness before a Windows hunt

**Status:** proposed source-health review. A recent count in one index does not establish that every expected Windows channel or field is current. No live source-health result is asserted here.

## Question and expected sources

Before interpreting an empty hunt, ask: **“Were the records needed for this question actually arriving and searchable during the chosen window?”** The [Windows forwarder input](../../../apps/LAB_UF_WINDOWS/local/inputs.conf) maps Security to `win_security`, System and Application to `win_system`, Windows PowerShell Operational to `powershell`, and Sysmon Operational to `sysmon`. The RHEL local syslog path uses `linux`; custom lab events use `lab`. These are the repository's six existing indexes, not six independently verified live feeds.

Use the [Step 27 checks](../../steps/27-verify-event-collection.md) and the [data-health search](../../../hunts/00-data-health.spl) as starting points. Agree with the owner which channels should have activity, a UTC review period, and any harmless marker that was actually generated. An inactive channel may legitimately be quiet; a missing row is a coverage question.

## Compare event time with index time

Run this read-only summary with an approved range, then inspect the individual source needed for the hunt:

```spl
(index=win_security OR index=win_system OR index=powershell OR index=sysmon OR index=linux OR index=lab) earliest=-7d latest=now
| eval ingest_lag_minutes=(_indextime-_time)/60
| stats count max(_time) as last_event max(_indextime) as last_index perc95(ingest_lag_minutes) as p95_ingest_lag_minutes by index host sourcetype
| eval event_age_minutes=round((now()-last_event)/60,1), index_age_minutes=round((now()-last_index)/60,1), p95_ingest_lag_minutes=round(p95_ingest_lag_minutes,1)
| table index host sourcetype count event_age_minutes index_age_minutes p95_ingest_lag_minutes
| sort index host sourcetype
```

**Search overview:** `count` is searchable events in the selected event-time window. `event_age_minutes` describes the newest event timestamp; `index_age_minutes` describes when the newest matching event was indexed. The 95th-percentile lag compares `_indextime` and `_time` **within each event**; a large or negative lag needs raw timestamp, time-zone, and clock review. The query produces **no row** for an index/host/source type without matching events; it cannot prove the source is healthy or even distinguish no input from no activity.

| Synthetic pattern | What to investigate |
| --- | --- |
| Event and index times are both recent for the expected source | Promising freshness; still verify the needed event ID and fields. |
| Index time is recent but event time is old | Backfill, delayed forwarding, or a timestamp/clock problem; not proof of current activity. |
| A previously expected source row is absent | Search range, access, source configuration, local generation, forwarding/TLS, and index mapping. |
| A marker is local but absent from Splunk | A collection or searchability gap until the owner resolves the exact cause. |

For a **positive control**, use a harmless event already described in the lab: Step 28.13's Application marker for `win_system`, Step 28.9's encoded PowerShell test for `powershell`/`sysmon`, or the [RHEL syslog markers](../SYSLOG_HUNTING_GUIDE.md) for `linux`. Verify its local source event and indexed copy; a marker in one index does not validate another. For a **nonmatching control**, inspect another collected channel or host and confirm it does not satisfy the candidate's source filter. Record when no control was available.

## Decide what the search supports

When a source is missing, review its local event log, the effective forwarder input/output, permissions, TLS receiver, and search role before changing a hunt. The [Step 45 troubleshooting record](../../steps/45-create-and-test-an-alert.md) documents an unresolved Windows forwarding case; do not mark it fixed based on this guide. The query's `earliest`/`latest` filters use **event time**. A badly parsed future timestamp or an older backfill may fall outside the window despite recent indexing; widen a diagnostic search only within the approved scope. Splunk's `_index_earliest` modifier can check index time, but its documentation says an event-time window still applies, so design that diagnostic carefully.

Keep the exact query, UTC window, expected source list, local marker references, indexed references, `_time`/`_indextime` differences, gaps, and owner action in approved private evidence. Say **inconclusive** when the needed source or field is missing. A plain-language update is: “The search was empty, but the records it needs were not confirmed in the lab, so we cannot say the activity did not happen.”

Use the [hunt report template](../templates/threat-hunt-report.md) for the outcome. Splunk documents [event indexing delay](https://help.splunk.com/en/splunk-enterprise/administer/troubleshoot/10.2/data-acquisition-problems/event-indexing-delay) and [index-time search limits](https://help.splunk.com/en/splunk-enterprise/search/spl-search-reference/10.6/time-format-variables-and-modifiers/time-modifiers).
