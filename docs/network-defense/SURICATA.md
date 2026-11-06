# Suricata IDS — RHEL 10.2, Offline PCAP, EVE and Alert Tuning

**Mode:** Offline and future passive IDS only; **no inline IPS or blocking**.

## Package installation (requires security/repository approval)

The [official OISF RPM guide](https://docs.suricata.io/en/suricata-8.0.6/install/rpm.html) documents the RHEL 10 COPR channel:

~~~bash
sudo dnf install -y epel-release dnf-plugins-core
sudo dnf copr enable @oisf/suricata-8.0
sudo dnf install -y suricata
suricata --build-info
~~~

**Command overview:** Adds approved EPEL/OISF package sources and Suricata; prints the build details. If those repos are not approved or available, stop and select a vetted alternative. Never silently install untrusted RPMs.

## Configuration and existing rule sources

~~~bash
sudo suricata -T -c /etc/suricata/suricata.yaml
sudo suricata-update
sudo suricata -T -c /etc/suricata/suricata.yaml
~~~

**Command overview:** Tests YAML/rules, retrieves configured signature updates and re-tests. Record exact rule update source and count. Don't add \`drop\` rules, NFQUEUE, netfilter hooks, or AF_PACKET copy-mode. Test with a private synthetic PCAP.

## Local lab detection (optional)

The repo includes a **harmless-only** DNS detection at [configs/network-defense/suricata/local.rules](../../configs/network-defense/suricata/local.rules). It matches `lab-marker.example.test` and SID `1000001`. To test it without modifying system defaults:

1. Copy the approved file to a *private* local test directory.
2. Run `suricata -T -c /etc/suricata/suricata.yaml -S /private/path/local.rules` to validate this additional rule.
3. Run `suricata -r /private/path/lab-dns.pcap -c /etc/suricata/suricata.yaml -S /private/path/local.rules -l /private/output`; review whether the SID appears in `eve.json`.
4. If no match, inspect DNS decoding, rule syntax, Suricata version, timestamps and \`fast.log\` without inventing a hit. If the rule keyword form changes, use current OISF rule syntax documentation.

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
