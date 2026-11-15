# Synthetic check: multi-account failures by source

The [hunt playbook](../../../docs/mitre-attack/hunt-playbook.md#multi-account-threshold-fixture) checks the five-account threshold. This case checks that [the production hunt](../07-multiple-account-failures.spl) does not pool failures from different source addresses or count an event with no source. It performs no sign-in and indexes no event.

| Synthetic source | Accounts in one fixed bucket | Expected |
| --- | --- | --- |
| `192.0.2.10` | Five distinct accounts | One candidate. |
| `192.0.2.20` | Four distinct accounts | No result. |
| Missing address | One account | Excluded before aggregation. |

Paste the fixture, then append every pipeline line beginning with the first `| eval` from the [production search](../07-multiple-account-failures.spl):

```spl
| makeresults count=10
| streamstats count as seq
| eval _time=relative_time(now(),"@h")+60, host="fixture-win", EventCode=4625, TargetUserName="training-user".seq, TargetDomainName="example", IpAddress=case(seq<=5,"192.0.2.10",seq<=9,"192.0.2.20",true(),"")
```

**Expected:** one row for `192.0.2.10` with `distinct_accounts=5`. The four-account source and missing-source event are nonmatching controls. Even a matching row could be approved testing or a shared address; these events do not reveal whether the same password was used.

This tests grouping and source filtering, not real authentication coverage. Fixed buckets can split activity at a boundary. Compare source ownership and an ordinary baseline; keep real usernames and addresses private.
