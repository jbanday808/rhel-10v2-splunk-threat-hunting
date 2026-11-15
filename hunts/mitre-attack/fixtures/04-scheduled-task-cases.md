# Synthetic check: task creation and update

Use this in-memory exercise to review [the scheduled-task hunt](../04-scheduled-task-changes.spl). It creates no Windows task and indexes no event. Run it only in an authorized Splunk Search session. The production search still requires Security auditing and confirmed field extraction.

## Question and controls

Can the hunt show a task's creation separately from its later update? Event 4698 is a task creation candidate and 4702 is an update candidate. Neither event proves that a task ran or that its action was harmful.

| Synthetic row | Task | Event | Expected review |
| --- | --- | --- | --- |
| 1 | Lab-Check | 4698 | Created; ask who approved it. |
| 2 | Lab-Check | 4702 | Updated; review what changed. |
| 3 | Lab-Other | 4698 | Separate, potentially expected task. |
| 4 | Lab-Check | 4700 | Nonmatching control; exclude it. |

Paste this fixture, then append every pipeline line beginning with **the first** `| eval` from the [production search](../04-scheduled-task-changes.spl):

```spl
| makeresults count=4
| streamstats count as seq
| eval _time=now()-300+seq, host="fixture-win", EventCode=case(seq=1,4698,seq=2,4702,seq=3,4698,true(),4700), TaskName=if(seq=3,"Lab-Other","Lab-Check"), SubjectUserName=if(seq=3,"approved-updater","training-admin")
```

**Expected:** three result rows: `Lab-Check / created`, `Lab-Check / updated`, and `Lab-Other / created`, each with `changes=1`. The 4700 row must not appear. Check that the two `Lab-Check` rows have different `event_codes` rather than treating their combined count as task execution. A known approved task is a benign control for interpretation, not a reason to remove its event.

The fixture tests the search pipeline against made-up fields. It cannot verify Windows event delivery, task XML, auditing, an actor's authority, or live alert behavior. Keep actual task names, XML, and account details in approved private evidence. [Splunk's `makeresults` reference](https://help.splunk.com/en/splunk-enterprise/search/spl-search-reference/10.0/search-commands/makeresults) describes in-memory result generation.
