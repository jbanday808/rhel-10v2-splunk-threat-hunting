# Suricata IDS — RHEL 10.2, Offline PCAP, EVE and Alert Tuning

**Mode:** Offline and future passive IDS only; **no inline IPS or blocking**.

## Package installation

On a registered, optional RHEL 10.2 sensor, verify approval for EPEL 10, CodeReady Builder and the OISF COPR. Follow the Fedora EPEL signing-key instructions and review the proposed package transaction. [Fedora EPEL 10](https://communityblog.fedoraproject.org/epel-10-is-now-available/) · [OISF RPM guide](https://docs.suricata.io/en/latest/install/rpm.html)

~~~bash
sudo subscription-manager repos --enable "codeready-builder-for-rhel-10-$(arch)-rpms"
sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-10.noarch.rpm
sudo dnf install dnf-plugins-core
sudo dnf copr enable @oisf/suricata-8.0
sudo systemctl mask suricata.service
sudo dnf install suricata
systemctl is-active suricata.service
suricata --build-info
~~~

**Command overview:** The first four commands enable and install the approved sources. `mask` prevents a service start while you install the offline analyzer. Expect `inactive` from `is-active` and record the `--build-info` output. If a repository or package is unavailable, use the approved workstation setup in the [worked case](OFFLINE_HTTP_WALKTHROUGH.md#1-set-up-an-analysis-workspace).

## Configuration and existing rule sources

The offline exercise loads one project-owned rule with `-S`. For an approved operational ruleset on the dedicated sensor, verify `suricata-update` is installed from the approved source, review the enabled feeds, then run `sudo suricata-update` followed by `sudo suricata -T -c /etc/suricata/suricata.yaml`. Record the rule source, version and count. Keep the sensor in alert-only IDS mode. [OISF rule management](https://docs.suricata.io/en/latest/rule-management/suricata-update.html)

## Local lab detection (optional)

The repo includes a **harmless-only** DNS detection at [configs/network-defense/suricata/local.rules](../../configs/network-defense/suricata/local.rules). It matches `lab-marker.example.test` and SID `1000001`. To test it without modifying system defaults:

1. Copy the approved file to a *private* local test directory.
2. Run `suricata -T -c /etc/suricata/suricata.yaml -S /private/path/local.rules` to validate this additional rule.
3. Run `suricata -r /private/path/lab-dns.pcap -c /etc/suricata/suricata.yaml -S /private/path/local.rules -l /private/output`; review whether the SID appears in `eve.json`.
4. If no match, inspect DNS decoding, rule syntax, Suricata version, timestamps and \`fast.log\` without inventing a hit. If the rule keyword form changes, use current OISF rule syntax documentation.

## Additional custom passive rules

The optional [custom-rule guide](SURICATA_CUSTOM_RULES.md) covers 12 additional rules for DNS policy/bursts, cleartext HTTP authentication, obsolete TLS negotiation, SMB, and RDP. It includes a separate offline configuration, synthetic positive/negative controls, exact alert-count replay, tuning limits, and owner-validation steps. The existing marker and HTTP rules remain unchanged; no live sensor configuration is installed.

For a separate senior-analyst exercise, the [passive review rules and validation plan](../../configs/network-defense/suricata/README.md) add eight **optional** DNS, HTTP, TLS, SMB and RDP observations. Their headers contain documentation-only addresses; they are not live lab detections. Load the example file explicitly with `-S` in an isolated offline check, compare positive and negative synthetic captures, and confirm the result with a service owner before treating any alert as a vulnerability.

## EVE JSON

Under approved package settings, \`/var/log/suricata/eve.json\` is a newline JSON stream with multiple \`event_type\` values such as \`alert\`, \`dns\`, \`http\`, \`tls\`, \`flow\`. A missing `alert` is not equivalent to no threat: the rule must be enabled, the packet captured, and the protocol decoded.

Use the offline parser:

~~~bash
python3 scripts/network-defense/summarize_network_logs.py \
  "$HOME/network-lab/suricata-out/eve.json" --type suricata
~~~

Review alert `signature_id`, `category`, `severity`, `src_ip`, `dest_ip`, `proto` and `timestamp`, plus benign explanations and duplicates.

## Detection tuning lifecycle

1. Define hypothesis and actual evidence of a problem.
2. Record SID, source ruleset/version, threshold, payload condition and intended protocol.
3. Apply a test rule to *synthetic* PCAP traffic; compare ground truth.
4. Quantify both true/false positives, duplicates and missing packets.
5. Use tightly scoped suppression/thresholding only after documented approval.
6. Rescan the same fixture after rule updates; keep source version and test outcome.
7. Only after operational acceptance, deploy selected rules as a passive IDS change.

**Rollback:** Remove only the new local test rule and stop the optional sensor instance; don't overwrite production rules or change Splunk's existing indexes.
