# Check event time and arrival time before a hunt

**Status:** read-only procedure for the documented Splunk lab. The example table below is synthetic. No live source, alert, or timing result has been validated by this page.

## Why this matters

A record has at least two useful times. `_time` is when Splunk believes the activity happened. `_indextime` is when Splunk stored the record. A search such as `earliest=-24h` normally selects records by event time. A record that arrives today with an older event time can be missing from that search even though collection is now working.

The [data-health search](../../hunts/00-data-health.spl) groups records by index, host, and sourcetype. Run it before interpreting an empty hunt. It reports the latest event, latest arrival, an estimated 95th-percentile arrival delay, and how long the group has been idle. The six expected indexes are `win_security`, `win_system`, `powershell`, `sysmon`, `linux`, and `lab`.

## Check one source

1. Confirm the permitted host, source, and time window with the lab owner. Search a wider event-time window when investigating delayed data.
2. In Splunk Search & Reporting, run this read-only search. Replace `<approved-host>` with the host you are authorized to examine; keep the quotes. Use the actual index and sourcetype observed in that environment.

```spl
index=linux host="<approved-host>" earliest=-7d
| eval arrival_delay_s=_indextime-_time
| stats count min(_time) as first_event max(_time) as last_event max(_indextime) as last_arrival perc95(arrival_delay_s) as p95_arrival_delay_s count(eval(arrival_delay_s<0)) as future_dated_events by host source sourcetype
| eval last_event_local=strftime(last_event,"%Y-%m-%d %H:%M:%S"), last_arrival_local=strftime(last_arrival,"%Y-%m-%d %H:%M:%S")
| table host source sourcetype count last_event_local last_arrival_local p95_arrival_delay_s future_dated_events
```

**Search overview:** `arrival_delay_s` compares arrival with event time. The percentile summarizes the group; `future_dated_events` counts records whose event time appears later than their arrival time. Splunk displays these date strings in the searching user's time zone. Record that time zone with the result, or display the raw epoch values when comparing systems. Do not interpret a negative delay as a fast pipeline; check clocks and timestamp parsing.

3. Open a few underlying records around the suspected gap. Confirm `_time`, `_indextime`, `host`, `source`, `sourcetype`, and the actual message. The latest event and latest arrival in the grouped search can come from **different records**.
4. Compare the result with the approved source schedule. A missing row means that the selected time range returned no matching events; it does not prove the source was silent or that no activity occurred. Check the file input, source permissions, collection path, and a wider authorized window before drawing a conclusion.
5. Record the search window, Splunk user time zone, source, observed delay, and any gap in the private hunt record. Keep raw logs and host identifiers out of this public repository.

## Interpret the result

| Synthetic observation | What it may mean | Next check |
| --- | --- | --- |
| Latest event and arrival are both recent | The source is producing and arriving in this window | Review representative events and expected fields |
| Arrival is recent but event time is old | Backfill, a delayed forwarder, or incorrect timestamp extraction | Review raw timestamp, source clock, forwarding path, and parsing |
| Event time is later than arrival | Source clock or timestamp interpretation may be wrong | Compare approved clock and time-zone settings |
| No row for an expected source | No matching indexed events in this search window | Confirm inventory, index, host, source, permissions, and a wider window |
| Arrival stopped after a known rotation | Collection may have lost the active file | Use the [log rotation continuity check](../security-operations/syslog-hunts/LOG_ROTATION_CONTINUITY.md) |

An index can contain events while one host or sourcetype is missing. Confirm each required source separately. This check establishes whether the evidence is usable for a hunt; it does not establish that a threat was present or absent.

## Record a decision

In the private hunt record, write: “Source ___, event-time window ___, latest arrival ___, arrival delay ___, missing periods ___, owner check ___.” Mark the hunt **inconclusive** when the necessary records or timestamp confidence are missing. Re-run the substantive detection search only after the evidence window is understood.
