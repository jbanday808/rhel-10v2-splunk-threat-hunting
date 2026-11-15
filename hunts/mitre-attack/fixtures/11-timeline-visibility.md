# Synthetic check: timeline context and ingest delay

Use this in-memory case with the [investigation timeline search](../11-investigation-timeline.spl). It creates no host activity and indexes no event. A timeline shows possible context; nearby events do not prove cause.

| Made-up event | Expected timeline behavior |
| --- | --- |
| Sysmon process start on fixture-win | Included with ten-second ingest delay. |
| SSH message on fixture-rhel | Included with original Linux message and 180-second delay. |
| Security 4624 on fixture-win | Included with ten-second delay. |
| Security 999 on fixture-win | Excluded by selected event codes. |

Paste the fixture, then append every pipeline line beginning with the first `| eval` from the [production search](../11-investigation-timeline.spl):

```spl
| makeresults count=4
| streamstats count as seq
| eval _time=now()-400+seq*60, host=if(seq=2,"fixture-rhel","fixture-win"), index=case(seq=1,"sysmon",seq=2,"linux",true(),"win_security"), EventCode=case(seq=1,1,seq=3,4624,seq=4,999,true(),null()), _raw=if(seq=2,"sshd: Accepted publickey for training-user from 192.0.2.10","synthetic event")
| eval _indextime=_time+if(seq=2,180,10)
```

**Expected:** three rows ordered by event time. The Linux row retains `linux_message` and shows `ingest_delay_seconds=180`; the other two show ten seconds. Event 999 is excluded. Delayed indexing changes when an analyst sees a record, not necessarily when the source says it happened. Check source clocks, host identity, ProcessGuid, and original private events before constructing a causal story.

This tests display and selected event codes, not cross-host collection, clock accuracy, completeness, or incident sequence. Keep real timeline details private.
