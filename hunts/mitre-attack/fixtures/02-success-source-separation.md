# Synthetic check: success from another source

The [hunt playbook](../../../docs/mitre-attack/hunt-playbook.md#in-memory-threshold-fixture-failures-before-success) already tests the five-failure threshold. This case checks a different risk in the [production hunt](../02-failures-before-success.spl): a success from another source must not inherit the first source's failures. It creates no sign-ins or indexed events.

| Sequence | Expected |
| --- | --- |
| Five failures for `training-user` from `192.0.2.10` | No result yet. |
| Success for that account from `192.0.2.20` | No match to the first source. |
| Success for that account from `192.0.2.10` | One candidate with five preceding failures. |

Paste the fixture, then append every pipeline line beginning with the first `| eval` from the [production search](../02-failures-before-success.spl):

```spl
| makeresults count=7
| streamstats count as seq
| eval _time=now()-900+seq*60, host="fixture-win", EventCode=if(seq<=5,4625,4624), TargetUserName="training-user", TargetDomainName="example", IpAddress=if(seq=6,"192.0.2.20","192.0.2.10"), LogonType=3
```

**Expected:** one row for `192.0.2.10`, with `preceding_failures=5`. The success from `192.0.2.20` is a nonmatching control. Forgotten-password recovery is a benign explanation for the matching pattern. Verify actual host, source normalization, time, logon type, and account owner.

This tests source grouping, not Windows delivery, password use, or compromise. Shared NAT and missing source fields can make real results ambiguous; keep real identifiers private.
