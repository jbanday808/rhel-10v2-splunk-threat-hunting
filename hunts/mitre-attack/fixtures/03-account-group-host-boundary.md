# Synthetic check: account and group host boundary

The [hunt playbook](../../../docs/mitre-attack/hunt-playbook.md#in-memory-identity-join-fixture) already checks SID and one-hour boundaries. This case checks the **host boundary** in [the account-to-group hunt](../03-account-to-group.spl). It creates no account or group and indexes no event.

| Row | Event and host | Expected |
| --- | --- | --- |
| 1 | Account created with SID `1001` on fixture-a | Establishes candidate. |
| 2 | SID `1001` added to a group on fixture-b | No cross-host match. |
| 3 | SID `1001` added to ordinary Users group on fixture-a | One candidate; benign group comparison. |
| 4 | Different member SID added to Administrators on fixture-a | No match to created account. |

Paste the fixture, then append every pipeline line beginning with the first `| eval` from the [production search](../03-account-to-group.spl):

```spl
| makeresults count=4
| streamstats count as seq
| eval _time=now()-300+seq*30, host=if(seq=2,"fixture-b","fixture-a"), EventCode=if(seq=1,4720,4732), TargetSid=case(seq=1,"S-1-5-21-1-2-3-1001",seq=3,"S-1-5-32-545",true(),"S-1-5-32-544"), MemberSid=case(seq=1,null(),seq=4,"S-1-5-21-1-2-3-9999",true(),"S-1-5-21-1-2-3-1001"), TargetUserName=case(seq=1,"training-user",seq=3,"Users",true(),"Administrators"), SubjectUserName="training-admin"
```

**Expected:** exactly one row: `fixture-a`, account SID ending `1001`, `target_group=Users`. Cross-host and different-member rows are nonmatching controls. Ordinary Users membership is not privilege escalation. Check real SID extraction, group privileges, and approval before interpreting an event.

This tests host and SID grouping, not collection, local-account scope, or intent. Keep real SIDs and account names private.
