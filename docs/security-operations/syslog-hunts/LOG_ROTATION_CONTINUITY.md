# Check syslog continuity across normal log rotation

**Status:** proposed acceptance exercise for the owned RHEL 10.2/Splunk VM. Do not force a rotation or change the installed rule solely for this exercise. No live result is asserted here.

## Ask a narrow question

When the local syslog file rotates on its normal schedule, can an analyst still find a tagged message from **before** and one from **after** the rotation in the existing `linux` index? A gap could hide investigation clues, but an absent marker can also result from an unscheduled rotation, delayed indexing, search-window limits, or a failed test command.

The repository's [logrotate rule](../../../configs/logrotate/siem-lab) covers `/var/log/siem-lab/*.log`: daily review, seven rotations, compression with one-cycle delay, new file mode `0640 root:splunk`, and an rsyslog HUP after rotation. The [Splunk input](../../../apps/LAB_SIEM/local/inputs.conf) monitors the active `linux.log` file. These are source files; first confirm the effective rules and actual file ownership on the lab VM.

## Review the rule without rotating

On the RHEL Splunk VM, after the owner approves a test window:

```bash
sudo logrotate --debug /etc/logrotate.d/siem-lab
sudo -u splunk test -r /var/log/siem-lab/linux.log && echo readable
sudo ls -li /var/log/siem-lab/linux.log*
```

**Command overview:** `--debug` previews logrotate's decision without changing the files; `test -r` checks that Splunk can read the active file; `ls -li` shows file names, inode numbers, and permissions. Keep the output private because file names, host context, or timestamps may be sensitive. A debug preview alone does not establish that a scheduled rotation actually ran.

Before the expected normal rotation, send a harmless tagged marker:

```bash
logger -p local0.notice -t siem-lab "SIEM-LAB-ROTATE-BEFORE-$(date -u +%Y%m%dT%H%M%SZ)"
```

After the scheduled rotation **actually occurs**, confirm the new active and previous file in private host evidence, then send:

```bash
logger -p local0.notice -t siem-lab "SIEM-LAB-ROTATE-AFTER-$(date -u +%Y%m%dT%H%M%SZ)"
```

**Command overview:** `logger` adds only synthetic marker messages, and `date -u` makes each marker distinct. These do not create a threat or verify that real SSH events were logged. Do not run the after-marker early; if rotation did not occur, record the exercise as pending.

## Check both sides in Splunk

Choose an `earliest` value that includes both marker times and is within the index's actual retention:

```spl
index=linux sourcetype=syslog host=splunk01 earliest=-7d latest=now "SIEM-LAB-ROTATE-"
| table _time _indextime host source _raw
| sort 0 _time
```

**Search overview:** the search looks for both synthetic marker types in the existing index. Review the full markers, event and index times, source path, and order. Do not assume `-7d` matches the actual retention; shorten or widen it based on the approved test window. Check the raw event count so duplicate or missing markers are visible.

Accept continuity only when you have private evidence of an **actual** rotation, a readable new active file, and both unique markers indexed in plausible order without an unexplained collection gap. The old marker can remain searchable after its original file rotates because it was already indexed; its presence alone does not prove that Splunk read the rotated file. If the after-marker appears in the file but not Splunk, inspect the effective input and permissions using the [syslog practice guide](../SYSLOG_HUNTING_GUIDE.md#try-two-harmless-messages). If either marker is absent from the local file, inspect rsyslog and the installed rule before blaming Splunk.

Record the planned and actual rotation times, rule review, marker references, input status, search window, and any gap in the [hunt report](../templates/threat-hunt-report.md). Keep host output and real logs private. A plain-language update is: “We checked whether the lab kept receiving messages after its normal log file changed. We will treat any unexplained gap as missing visibility, not as evidence that nothing happened.”

**Summary:** distinguish rule preview from actual rotation, require a marker on each side, and describe the remaining visibility limits.
