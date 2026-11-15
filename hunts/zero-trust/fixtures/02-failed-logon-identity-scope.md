# Synthetic check: keep failed sign-in identities separate

Use this with [the failed-logon search](../02-windows-failed-logons.spl). A Windows Security 4625 records a failed sign-in attempt, not an attacker or a successful session. The same account name in different domains can refer to different identities. A missing or placeholder source address cannot identify one originating device.

## In-memory control

In an authorized Splunk Search session, paste the fixture below, then append every pipeline line starting with `| eval event_code` from the linked search. `makeresults` creates no sign-ins or indexed events.

```spl
| makeresults count=5
| streamstats count as seq
| eval _time=now()-300+seq, host="fixture-win", EventCode=if(seq=5,4624,4625), TargetUserName="training-user", TargetDomainName=if(seq=3,"DEV","LAB"), IpAddress=if(seq=4,"-","192.0.2.10"), LogonType=3, Status="0xC000006D", SubStatus="0xC000006A"
```

**Expected:** three rows: `LAB / training-user / 192.0.2.10` has two failures; `DEV / training-user / 192.0.2.10` has one; and `LAB / training-user / -` has one. The 4624 control must be excluded. Do not add the three rows into a single “source” or “account” finding. An approved test, a mistyped password, a service, or a scanner can explain a failure.

For real records, privately verify `TargetUserName`, `TargetDomainName`, `IpAddress`, `LogonType`, `Status`, and `SubStatus` against the original Windows event and the installed field extraction. The displayed time follows the analyst's Splunk time zone. Check the source and destination context, authorized changes, and sign-in outcomes before escalating. The fixture proves only this grouping logic; it does not validate log delivery or a detection. Keep real account names, IPs, and raw events in approved private evidence. [Microsoft's 4625 reference](https://learn.microsoft.com/windows/security/threat-protection/auditing/event-4625) describes these event fields.
