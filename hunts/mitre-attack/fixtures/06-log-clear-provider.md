# Synthetic check: Windows log-clear provider

Use this in-memory exercise with [the log-clear candidate search](../06-event-log-clear-candidates.spl). It creates no Windows event, clears no log, and indexes no record.

## Question and controls

Can an analyst distinguish a Security 1102 candidate from a System 104 record with the expected `Microsoft-Windows-Eventlog` provider, and from another provider that reused Event ID 104? Event ID alone is insufficient.

| Synthetic row | Index and event | Provider | Expected label |
| --- | --- | --- | --- |
| 1 | `win_security`, 1102 | Security | Security audit candidate. |
| 2 | `win_system`, 104 | Microsoft-Windows-Eventlog | Eventlog provider candidate. |
| 3 | `win_system`, 104 | Example-Other | Verify provider before treating as a clear. |
| 4 | `win_system`, 1102 | Example-Other | Excluded by index and event pairing. |

Paste this fixture, then append every pipeline line beginning with **the first** `| eval` from the [production search](../06-event-log-clear-candidates.spl):

```spl
| makeresults count=4
| streamstats count as seq
| eval _time=now()-300+seq, host="fixture-win", index=if(seq=1,"win_security","win_system"), EventCode=case(seq=1,1102,seq=4,1102,true(),104), ProviderName=case(seq=1,"Microsoft-Windows-Security-Auditing",seq=2,"Microsoft-Windows-Eventlog",true(),"Example-Other"), SubjectUserName="training-admin", source="synthetic"
```

**Expected:** three rows. Row 3 remains visible for review but its `provider_review` warns against treating it as a log clear. Row 4 must be absent. Confirm the actual provider and surrounding activity in private source events before describing any clear as intentional or malicious. Do not clear a live log merely to generate a test case.

The fixture tests the candidate labeling and index/event pairing, not Windows ingestion or independent record retention. A missing event cannot establish that no log was cleared.
