# Synthetic check: when Splunk warnings appeared

Use this with [the Splunk health search](../04-splunk-internal-errors.spl). This search reads Splunk's built-in, protected `_internal` index, **not** a seventh lab index. An authorized administrator should run it. It groups warnings and errors from `splunkd.log` into one-hour windows so an investigator can compare their timing with an expected-source gap from [the coverage search](../01-siem-data-coverage.spl). A matching hour is a lead, not a proven cause.

## In-memory control

In an authorized Splunk Search session, paste this fixture and then append every pipeline line starting with `| eval component` from the linked search. It generates no log messages on the server and indexes no data.

```spl
| makeresults count=5
| streamstats count as seq
| eval _time=relative_time(now(),"@h")-7200+case(seq=1,60,seq=2,120,seq=3,180,seq=4,3660,true(),3720), host="fixture-splunk", component=if(seq=4,"TcpInputProc","TailReader"), log_level=case(seq=1,"WARN",seq=2,"ERROR",seq=3,"INFO",seq=4,"FATAL",true(),"WARN")
| where in(log_level,"WARN","ERROR","FATAL")
```

**Expected:** three rows: the first hour has `TailReader` with one warning and one error; the second hour has `TcpInputProc` with one fatal; and the second hour has `TailReader` with one warning. The INFO control is excluded before the production pipeline. If the INFO row appears in the output, the severity filter was omitted from the test.

For actual operations, check the exact private message, component, host, source, config, and known maintenance before assigning a cause. No rows can mean no matching message, a wrong time range, a different log source or field name, or insufficient access. Some forwarding problems may leave no matching `splunkd.log` warning. The fixture verifies aggregation only; it does not demonstrate that Splunk or the lab inputs are healthy. Displayed hours use the analyst's Splunk time zone. [Splunk's troubleshooting guide](https://help.splunk.com/en/splunk-enterprise/administer/troubleshoot/9.0/splunk-web-and-search-problems/i-cant-find-my-data) describes checking missing data and index delay.
