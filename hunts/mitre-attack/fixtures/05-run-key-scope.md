# Synthetic check: the monitored Run value

Use this in-memory exercise with [the lab Run-key hunt](../05-lab-run-key.spl). It creates no registry value and indexes no event. The shipped [Sysmon rule](../../../sysmon/sysmon.xml) includes a narrow `CurrentVersion\Run\SIEMLab` pattern; it is not general Run-key or Startup-folder coverage.

## Question and controls

Does the search keep the exact `SIEMLab` value under `CurrentVersion\Run` while rejecting similarly named paths? A substring search can mistakenly include `SIEMLabExtra` or `RunOnce`.

| Synthetic row | Registry path ending | Expected |
| --- | --- | --- |
| 1 | `CurrentVersion\Run\SIEMLab` | Candidate; review actor, image, details, and authorization. |
| 2 | `CurrentVersion\Run\SIEMLabExtra` | Excluded: a different value name. |
| 3 | `CurrentVersion\RunOnce\SIEMLab` | Excluded: a different key. |

Paste this fixture, then append every pipeline line beginning with **the first** `| eval` from the [production search](../05-lab-run-key.spl):

```spl
| makeresults count=3
| streamstats count as seq
| eval _time=now()-300+seq, host="fixture-win", EventCode=13, TargetObject=case(seq=1,"HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run\\SIEMLab",seq=2,"HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run\\SIEMLabExtra",true(),"HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnce\\SIEMLab"), User="training-admin", Image="example-installer.exe", Details="synthetic"
```

**Expected:** exactly one row, ending in `CurrentVersion\Run\SIEMLab`. The two lookalike paths are nonmatching controls. The result is still a candidate: the actual value data, owner, signer, and approved change must be checked. If a field is not extracted in the real lab, inspect a private raw event before changing the search.

This exercise tests the search suffix filter only. The actual Sysmon rule is also narrow, and no result here proves that other Run values would have been collected. Do not publish a real registry value or command line.
