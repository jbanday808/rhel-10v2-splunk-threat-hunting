# Syslog for a simple threat hunt

**Status:** practice guide for the existing RHEL and Splunk lab. The commands below are examples to run only in your authorized lab; no live system was changed by adding this guide.

## Why a threat hunter uses it

Syslog is a way for a computer or application to record what happened. A record may show that someone tried to sign in or that a service reported a problem. A threat hunter compares those records with other clues and asks whether the activity was expected. One unusual message is not proof of an attack.

The supplied Trellix Cyber Threat Hunter role (JR0038010) calls for configuring application and operating-system logging using syslog or flat files, analyzing events in a SIEM, and explaining findings to customers. This exercise practices those skills with RHEL 10.2 and Splunk Enterprise. It does not claim a Trellix product integration or a real customer finding.

## Follow the record

```text
RHEL system or app message
  → rsyslog selects the message
  → /var/log/siem-lab/linux.log
  → Splunk reads the file
  → linux index
  → analyst reviews the event
```

The lab already has the [rsyslog rule](../../configs/rsyslog/30-siem-lab.conf) and [Splunk file input](../../apps/LAB_SIEM/local/inputs.conf). The rule selects `auth`, `authpriv`, and messages tagged `siem-lab`; Splunk monitors the resulting file as `sourcetype=syslog` in the existing `linux` index. [Step 16](../steps/16-configure-linux-logging.md) describes the RHEL setup and [Step 17](../steps/17-deploy-the-splunk-app-and-automatic-startup.md) describes the Splunk app. Complete and review those steps on the lab VM before this exercise. No extra listening port or new index is needed for this local example.

## Try two harmless messages

On the RHEL Splunk lab VM, check the logging service and send two test records:

```bash
sudo rsyslogd -N1
sudo systemctl is-active rsyslog
logger -p authpriv.notice -t syslog-lab 'SIEM-LAB-SYSLOG-AUTH-CHECK'
logger -p local0.notice -t siem-lab 'SIEM-LAB-SYSLOG-APP-CHECK'
sudo grep -F 'SIEM-LAB-SYSLOG-' /var/log/siem-lab/linux.log
```

**Command overview:** `rsyslogd -N1` checks the logging configuration; `systemctl is-active` reports whether rsyslog is running. `logger` creates synthetic messages. The first tests the authentication-facility rule; the second tests the application-tag rule. `grep` looks for only the test markers in the local file.

**Expected result:** rsyslog reports a valid configuration, its service is active, and the file contains both markers. These commands do **not** perform a real sign-in or prove that an application is integrated. If a check fails, stop and review the installed configuration, service status, file path and permissions privately; do not overwrite live settings just to match the example.

In Splunk Search & Reporting, run:

```spl
index=linux sourcetype=syslog source="/var/log/siem-lab/linux.log" earliest=-15m ("SIEM-LAB-SYSLOG-AUTH-CHECK" OR "SIEM-LAB-SYSLOG-APP-CHECK")
| table _time host source _raw
| sort 0 -_time
```

**Expected result:** two recent test events appear after indexing. If the file contains the markers but Splunk does not, check the effective file input and Splunk's permission to read the file:

```bash
sudo -u splunk /opt/splunk/bin/splunk btool inputs list 'monitor:///var/log/siem-lab/linux.log' --debug
sudo -u splunk test -r /var/log/siem-lab/linux.log && echo readable
```

**Command overview:** `btool` displays the active file-input settings and where they came from. `test -r` checks read access as the lab's Splunk account. Confirm `disabled = 0`, `index = linux`, `sourcetype = syslog`, and a `readable` result; also check ingestion delay and the search time window. A missing result is a collection question, not evidence that the hunt found no threat. Keep any real log output out of this public repository.

## Turn the logs into a hunt

Ask: **“Were unsuccessful SSH sign-ins followed by access that the owner cannot explain?”**

1. Agree on the RHEL host, time period, records you may inspect, and who can confirm expected activity.
2. Run the [syslog review search](../../hunts/linux/01-syslog-review.spl) in Splunk. It shows SSH, `sudo`, and test-marker messages from this lab file in time order. The existing [SSH context search](../../hunts/mitre-attack/09-linux-ssh-context.spl) offers a narrower view.
3. Read the underlying messages. Compare failed and accepted sign-ins, accounts, source addresses if present, and timestamps. Check with the system owner about approved tests, maintenance and normal access. Do not assume messages with similar times belong to the same person or session.
4. If permitted network evidence exists, compare the same host and time window in [Zeek, Wireshark or Arkime](../network-defense/ZEEK_AND_WIRESHARK.md). A network connection can add context, but it does not by itself prove a successful sign-in. Record missing logs, clock differences and capture limits.
5. Use the [hunt report template](templates/threat-hunt-report.md) to state the question, observed records, alternate explanations, gaps and recommended owner action. Brief the customer in everyday language: “We saw these sign-in attempts. We have not yet confirmed whether the later access was authorized.”

**Summary:** verify that messages are collected, ask a scoped question, compare independent clues, and report only what the evidence supports. The two `logger` records check the pipeline; they are not a threat simulation or a detection test.

## If the source is a different device

Remote syslog collection is an **optional future design**, not part of the configured lab. For another RHEL host, network device, or application, agree on which logs are permitted, choose a collector, protect logs in transit, separate sources and hosts, set file permissions and rotation, and then monitor the collector's files in Splunk. Review parsing, time zones, retention and ownership before using those records in a hunt. Avoid sending sensitive records over unencrypted TCP or UDP, and do not assume that a remote sender's claimed host name is trustworthy without checking the source.

Red Hat's [RHEL 10 logging guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/risk_reduction_and_recovery_operations/index) includes rsyslog validation and protected remote transport in chapter 5. Splunk's [syslog collection guidance](https://help.splunk.com/en/data-management/splunk-validated-architectures/getting-data-in-forwarding-and-preprocessing/syslog-data-collection) describes collector-based collection; its [file input reference](https://help.splunk.com/en/data-management/splunk-enterprise-admin-manual/10.2/configuration-file-reference/10.2.0-configuration-file-reference/inputs.conf) documents monitored files. Adapt any remote design to the customer's actual Splunk version, security rules and approved architecture.
