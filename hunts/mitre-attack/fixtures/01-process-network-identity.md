# Synthetic check: process and network identity

Use this in-memory case with the [process/network hunt](../01-process-network.spl). It starts no process, makes no connection, and indexes no data. The question is whether a process start and connection share **both host and ProcessGuid**.

| Synthetic events | Expected |
| --- | --- |
| Start and connection, `fixture-win / GUID-A` | One candidate. |
| Start only, `fixture-win / GUID-B` | No result. |
| Connection only, `fixture-win / GUID-C` | No result. |
| Connection, `fixture-other / GUID-A` | No cross-host match. |

Paste the fixture, then append every pipeline line beginning with the first `| eval` from the [production search](../01-process-network.spl):

```spl
| makeresults count=5
| streamstats count as seq
| eval _time=now()-300+seq*10, host=if(seq=5,"fixture-other","fixture-win"), EventCode=if(seq=1 OR seq=3,1,3), ProcessGuid=case(seq<=2,"GUID-A",seq=3,"GUID-B",seq=4,"GUID-C",true(),"GUID-A"), Image="powershell.exe", ParentImage=if(seq=1 OR seq=3,"explorer.exe",null()), DestinationIp=if(seq=1 OR seq=3,null(),"192.0.2.10"), DestinationPort=if(seq=1 OR seq=3,null(),443)
```

**Expected:** one row for `fixture-win / GUID-A`, with `process_events=1` and `network_events=1`. The other events are nonmatching controls. An approved administration script or update is a benign explanation to check. Review the private process, command, and destination records before describing intent.

The case tests grouping, not Sysmon coverage, TLS content, destination ownership, or command and control. Keep real command lines and addresses private.
