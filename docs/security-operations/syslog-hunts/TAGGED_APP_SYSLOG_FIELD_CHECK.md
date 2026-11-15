# Tagged application syslog: check the clues before hunting

**Status:** proposed visibility exercise on the owned RHEL 10.2/Splunk VM. The two harmless messages below test collection and fields; they do not simulate an attacker or prove a live application integration.

## Ask a narrow question

Can a message tagged like an application event reach the existing `linux` index with enough host, source, and time context to support an investigation? Compare it with an authentication-facility message sent through the same [rsyslog rule](../../../configs/rsyslog/30-siem-lab.conf). This matters before a customer asks a hunter to interpret application events: a missing or misleading field can change the story.

The rule selects `auth`, `authpriv`, or program name `siem-lab`, and writes `/var/log/siem-lab/linux.log`. The [Splunk input](../../../apps/LAB_SIEM/local/inputs.conf) labels that file `sourcetype=syslog`, `host=splunk01`, `index=linux`. This is a **local file** example, not a remote collector or an additional cloud feed.

## Send and find two safe markers

After confirming you are on the owned RHEL Splunk VM and the [logging setup](../../steps/16-configure-linux-logging.md) was reviewed, run:

```bash
sudo rsyslogd -N1
logger -p authpriv.notice -t syslog-lab 'SIEM-LAB-SYSLOG-AUTH-CHECK'
logger -p local0.notice -t siem-lab 'SIEM-LAB-SYSLOG-APP-CHECK'
sudo grep -F 'SIEM-LAB-SYSLOG-' /var/log/siem-lab/linux.log
```

**Command overview:** `rsyslogd -N1` checks the rule syntax; `logger` creates one auth-facility marker and one tagged application marker; `grep` checks whether the local file contains them. Stop and review the service, rule, path, and permissions privately if either marker is absent. Do not replace on-host settings just to force a passing example.

Search the expected file in Splunk:

```spl
index=linux sourcetype=syslog source="/var/log/siem-lab/linux.log" earliest=-15m ("SIEM-LAB-SYSLOG-AUTH-CHECK" OR "SIEM-LAB-SYSLOG-APP-CHECK")
| rex field=_raw "(?<check>SIEM-LAB-SYSLOG-(?:AUTH|APP)-CHECK)"
| eval ingest_delay_seconds=_indextime-_time
| table _time _indextime ingest_delay_seconds host source sourcetype check _raw
| sort 0 _time
```

**Search overview:** the first line limits results to the configured source and two markers; `rex` labels which marker was found; the delay calculation compares the event and index times. Inspect the raw message, not just the extracted label. Earlier runs may create duplicate markers, so narrow the window before counting. Time parsing can differ by format, time zone, and year; review an implausible or negative delay before using it.

Check both markers and these fields:

| Field or clue | What a useful result shows | Limit |
| --- | --- | --- |
| `_time` and `_indextime` | Plausible event time and collection delay | A recent index time cannot repair a wrong event timestamp. |
| `host` | Expected `splunk01` label | The input sets this value; it is not independent proof of the sender. |
| `source` and `sourcetype` | The monitored local path and `syslog` label | These identify the input, not the application identity. |
| Raw tag and marker | `siem-lab` for the app marker, `syslog-lab` for the auth marker | A tag can be chosen by the sender and needs separate trust review. |

**Synthetic controls:** the auth marker is a comparison for the facility route, and the app marker checks the program-name route. If the first appears but the second does not, investigate the tag/rule path. If both reach the file but neither reaches Splunk, inspect the effective file input and read permission as shown in the [syslog practice guide](../SYSLOG_HUNTING_GUIDE.md#try-two-harmless-messages). A missing result indicates a visibility gap, not a quiet environment.

## Explain the result

Record the test time, configuration version, two marker references, fields, and any gaps in the [hunt report](../templates/threat-hunt-report.md). Keep real application messages private. For a nontechnical audience: “We checked whether the lab can carry an application message into the search tool. The test tells us about log delivery; it does not tell us whether customer activity is safe.”

**Summary:** compare both routing paths, verify the original message and time context, and resolve collection gaps before making a security claim.
