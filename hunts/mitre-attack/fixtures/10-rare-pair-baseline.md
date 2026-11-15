# Synthetic check: rare process pair by host

Use this in-memory exercise with [the rare parent-child search](../10-rare-parent-child.spl). It starts no process and indexes no event. The search is exploratory and its three-execution threshold is illustrative.

## Question and controls

If the same parent-child image pair appears once on one host and four times on another, can the analyst see the rare host separately? Grouping across hosts can hide a local difference. A rare pair can also be a normal updater, new software, or a short observation window.

| Synthetic host | Pair count | Expected search result |
| --- | --- | --- |
| fixture-a | 1 | Included as a candidate for review. |
| fixture-b | 4 | Excluded by the illustrative `executions<=3` threshold. |

Paste this fixture, then append every pipeline line beginning with **the first** `| eval` from the [production search](../10-rare-parent-child.spl):

```spl
| makeresults count=5
| streamstats count as seq
| eval _time=now()-300+seq, host=if(seq=1,"fixture-a","fixture-b"), EventCode=1, ParentImage="C:\\Example\\updater.exe", Image="C:\\Example\\helper.exe"
```

**Expected:** exactly one row for `fixture-a` with `executions=1`. `fixture-b` is the nonmatching threshold control. Before interpreting a real result, compare the same host's approved software changes, role, collection health, and a representative healthy period. A single-host practice lab cannot establish an enterprise baseline.

This fixture tests grouping and the threshold only. It does not verify Sysmon event delivery, parentage in a real process tree, execution intent, or detection quality. Keep real command lines and host names in approved private evidence.
