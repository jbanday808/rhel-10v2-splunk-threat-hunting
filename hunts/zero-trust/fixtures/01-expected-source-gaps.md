# Synthetic check: an expected source can be absent

Use this with [the coverage search](../01-siem-data-coverage.spl). The six expected index/host pairs in that search come from this lab's Windows and RHEL input configurations. Adjust the list to the approved scope before using it elsewhere. A missing row in ordinary event counts is easy to overlook; the revised search keeps each expected pair visible even when it has no events in the selected 24 hours.

## In-memory control

Run this in an authorized Splunk Search session. It creates no indexed events. The first two rows are expectations. The third row represents two recent Windows Security records. The other two observed rows are distractors: a different Windows host and an unlisted source.

```spl
| makeresults count=5
| streamstats count as seq
| eval index=case(seq=1,"win_security",seq=2,"powershell",seq=3,"win_security",seq=4,"win_security",true(),"lab"), host=case(seq=4,"other-win",seq=5,"splunk01",true(),"WINHUNT01")
| eval expected=if(seq<=2,1,null()), observed_events=case(seq=3,2,seq=4,9,seq=5,1), last_event_epoch=if(seq=3,now()-300,null()), last_ingest_epoch=if(seq=3,now()-180,null())
| stats max(expected) as expected max(observed_events) as observed_events max(last_event_epoch) as last_event_epoch max(last_ingest_epoch) as last_ingest_epoch by index host
| where expected=1
| eval observed_events=coalesce(observed_events,0), coverage=if(observed_events=0,"no events in window","events observed")
| eval last_event_age_min=if(observed_events>0,round((now()-last_event_epoch)/60,1),null()), last_ingest_age_min=if(observed_events>0,round((now()-last_ingest_epoch)/60,1),null())
| table index host coverage observed_events last_event_age_min last_ingest_age_min
| sort index host
```

**Expected:** `win_security / WINHUNT01` shows two events, an event age near five minutes, and an ingest age near three minutes. `powershell / WINHUNT01` shows zero and “no events in window.” Neither distractor appears. The zero is a **visibility question**, not proof that PowerShell was not used. Check the local channel, forwarder, audit settings, ingestion, time range, and permissions. An event with a timestamp older than the 24-hour event-time window can be absent even if it was ingested recently.

The fixture checks the expected-versus-observed logic only. It cannot prove that any real source is delivered, that its events have accurate clocks, or that monitoring meets a Zero Trust requirement. Keep actual host inventory and event samples in private evidence. See [Splunk's time-modifier reference](https://help.splunk.com/en/splunk-enterprise/search/spl-search-reference/9.0/time-format-variables-and-modifiers/time-modifiers) for the event-time window.
