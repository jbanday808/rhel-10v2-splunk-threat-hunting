# Synthetic check: PowerShell DNS context by process

Use this in-memory exercise with [the DNS context search](../08-powershell-dns-context.spl). It makes no DNS request and indexes no record. The shipped Sysmon rule includes DNS queries from `powershell.exe` only.

## Question and controls

If two different PowerShell processes ask for the same name, do their records stay separate? A query name by itself is not process identity, a network connection, or proof of command and control.

| Synthetic row | Image | Process GUID | Name | Expected |
| --- | --- | --- | --- | --- |
| 1 | powershell.exe | GUID-A | example.invalid | One PowerShell process row. |
| 2 | powershell.exe | GUID-B | example.invalid | Separate PowerShell process row. |
| 3 | curl.exe | GUID-C | example.invalid | Excluded by the query's image scope. |

Paste this fixture, then append every pipeline line beginning with **the first** `| eval` from the [production search](../08-powershell-dns-context.spl):

```spl
| makeresults count=3
| streamstats count as seq
| eval _time=now()-300+seq, host="fixture-win", EventCode=22, QueryName="example.invalid", Image=if(seq=3,"C:\\Windows\\System32\\curl.exe","C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"), ProcessGuid=case(seq=1,"GUID-A",seq=2,"GUID-B",true(),"GUID-C"), QueryResults="192.0.2.10"
```

**Expected:** two rows for `example.invalid`, one per PowerShell `process_identity`. The curl row is a nonmatching control. If the real event lacks a ProcessGuid, the search labels it `missing ProcessGuid`; do not join several such records to one process merely because the host and name match. Check process creation and other independent evidence before drawing a security conclusion.

This tests grouping against made-up fields, not actual Sysmon collection, DNS answer accuracy, or a live destination connection. Keep real queried names and IPs private.
