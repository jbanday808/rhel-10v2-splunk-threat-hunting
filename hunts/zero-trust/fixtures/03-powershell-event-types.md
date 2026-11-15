# Synthetic check: PowerShell source versus event coverage

Use this with [the PowerShell activity search](../03-powershell-activity.spl). A nonzero `powershell` index count shows that some records reached Splunk; it does not show that module logging (4103) or script-block logging (4104) reached it. Those features depend on policy, the PowerShell version, the local channel, and forwarding. Script-block content may contain sensitive commands, so this summary deliberately displays counts rather than command text.

## In-memory control

Paste the following into an authorized Splunk Search session, then append every pipeline line starting with `| eval event_code` from the linked search. No script runs and no records are indexed.

```spl
| makeresults count=4
| streamstats count as seq
| eval _time=now()-240+seq, host="fixture-win", sourcetype="XmlWinEventLog:Microsoft-Windows-PowerShell/Operational", EventCode=case(seq=1,4103,seq=2,4104,seq=3,400), EventID=if(seq=4,4104,null())
```

**Expected:** one row with `all_events=4`, `module_4103=1`, `script_block_4104=2`, and `code_not_extracted=0`. The 400 row is an ordinary PowerShell operational event; it is not counted as module or script-block logging. The `EventID` row checks the alternative event-code extraction.

For a negative control, change the fixture's `seq=2,4104` to `seq=2,400` and its `seq=4,4104` to `seq=4,400`. Expect `all_events=4` but `script_block_4104=0`. That result is a request to check the approved logging configuration and local and indexed records, not proof that no scripts ran. A 4104 event can also be split into multiple records, so count is not the number of scripts or executions. The fixture checks summary logic only; real delivery remains pending until separately observed. See [Microsoft's Windows PowerShell logging guide](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging?view=powershell-5.1).
