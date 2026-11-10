# Worked case — Investigate an unexpected cleartext HTTP transfer

**Question.** Why did a client download a file over cleartext HTTP from a hostname outside the approved baseline, and what would you ask the service owner to verify?

This is an optional worked case for the [30-step implementation guide](IMPLEMENTATION_GUIDE.md). Two synthetic captures represent a routine window and a review window. The approved fixture hostname is `updates.example.test`. The review window adds `review.example.test` with the same destination IP and file path. The expected finding is a cleartext transfer to a hostname outside the fixture's approved list. The scenario gives you a reason to investigate the HTTP listener, DNS alias, virtual host, or redirect policy. You will need owner evidence to determine the cause and affected scope.

## 1. Set up an analysis workspace

Use the optional RHEL analysis VM from the [installation guide](IMPLEMENTATION_GUIDE.md) or an Ubuntu 24.04 WSL analysis environment. Run the commands in Bash from the repository root, as your regular analysis user except where `sudo` is shown. For the GUI, install [Wireshark for Windows](https://www.wireshark.org/download.html) from the publisher and verify its digital signature. The saved-file workflow needs no live capture permissions.

For a dedicated Ubuntu WSL environment with systemd running, use approved Ubuntu package sources. In a fresh analysis environment, mask the Suricata service before installing it and verify the service stays inactive. Choose **No** if the TShark installer asks to grant non-root users capture privileges. If you already have an analysis host with these tools, record its versions and skip its installation commands.

~~~bash
sudo apt update
sudo systemctl mask suricata.service
sudo apt install --no-install-recommends python3-venv curl gnupg tshark jq yara suricata
systemctl is-active suricata.service
~~~

**Command overview.** `apt` refreshes and installs packages, `mask` prevents a daemon start, and `is-active` reports its state. Expect `inactive`, which is a nonzero exit status for that check. If the service is running, stop and review the host setup before proceeding.

Create a new private run directory outside the repository. Keep the terminal open for the later steps. The virtual environment stays with this run and can be recreated from the recorded package versions.

~~~bash
umask 077
REPO="$PWD"
mkdir -p "$HOME/network-lab"
chmod 700 "$HOME/network-lab"
RUN=$(mktemp -d "$HOME/network-lab/http-XXXXXXXX")
RUN_ID=${RUN##*/}
python3 -m venv "$RUN/venv"
"$RUN/venv/bin/python" -m pip install dpkt==1.9.8 sigma-cli pysigma-backend-splunk
"$RUN/venv/bin/python" -m pip freeze > "$RUN/python-versions.txt"
~~~

**Command overview.** `umask` protects new files, `mktemp` creates a distinct run directory, and `venv` isolates Python dependencies. Use an approved package source for the three dependencies. The version inventory lets you reproduce the run.

On Ubuntu 24.04, use the official [Zeek binary package instructions](https://github.com/zeek/zeek/wiki/Binary-Packages). For an approved fresh setup, download the repository key and compare its fingerprint with the GPG fingerprint on the publisher's [Zeek repository signing key page](https://build.opensuse.org/projects/security%3Azeek/signing_keys). Use a key scoped to this package source. If the host already has the official source configured, use that source.

~~~bash
ZEEK_REPO='https://download.opensuse.org/repositories/security:/zeek/xUbuntu_24.04'
curl -fSL "$ZEEK_REPO/Release.key" -o "$RUN/zeek-release.key"
gpg --show-keys --with-fingerprint "$RUN/zeek-release.key"
~~~

After matching the key fingerprint and confirming the repository is approved, install the Zeek core package.

~~~bash
gpg --dearmor --output "$RUN/zeek-lab.gpg" "$RUN/zeek-release.key"
sudo install -d -m 0755 /etc/apt/keyrings
sudo install -m 0644 "$RUN/zeek-lab.gpg" /etc/apt/keyrings/zeek-lab.gpg
printf 'deb [signed-by=/etc/apt/keyrings/zeek-lab.gpg] %s /\n' "$ZEEK_REPO" |
  sudo tee /etc/apt/sources.list.d/zeek-lab.list > /dev/null
sudo apt update
sudo apt install zeek-9.0-core
ZEEK=/opt/zeek/bin/zeek
"$ZEEK" --version
tshark --version
suricata -V
yara --version
~~~

**Summary.** Record each actual version. On the optional RHEL sensor, install the approved tools from the implementation guide, then make sure `jq` and `python3-pip` are available from approved repositories for this worked case. Use the approved Zeek image reference from the implementation guide or set `ZEEK` to the absolute path of a verified native Zeek install.

## 2. Generate and verify the captures

~~~bash
"$RUN/venv/bin/python" "$REPO/scripts/network-defense/generate_http_fixtures.py" "$RUN/captures"
sha256sum "$RUN/captures/baseline.pcap" "$RUN/captures/investigation.pcap" > "$RUN/capture-sha256.txt"
capinfos -c -a -e "$RUN/captures/"*.pcap
~~~

**Command overview.** The generator writes two local files. `sha256sum` records their fingerprints, and `capinfos` reads packet totals and time bounds. The script only writes packets to disk and uses documentation IPs. It timestamps the captures a few minutes before the run for easy Splunk testing. Use `--start-epoch` with the same UTC epoch seconds to regenerate the same packet bytes for a regression test. For a Splunk run, keep timestamps within the index retention window.

| Capture | Packets | DNS exchanges | HTTP requests | Candidate HTTP request |
| --- | ---: | ---: | ---: | --- |
| `baseline.pcap` | 33 | 3 | 3 | None |
| `investigation.pcap` | 22 | 2 | 2 | Frame 17, TCP client port 51005 |

## 3. Verify DNS and HTTP in Wireshark or TShark

Open the investigation capture in Wireshark. In **View → Time Display Format**, choose a UTC display. Apply `dns.qry.name == "review.example.test"` to locate the query and response. Then apply `http.host == "review.example.test" && http.request.uri == "/downloads/review.txt"`. Inspect the source, destination, and request in frame 17. Right-click the request and choose **Follow → TCP Stream** to verify the HTTP 200 response and view the synthetic text. Record the DNS answer and the TCP tuple separately. A matching destination IP alone is insufficient to distinguish the two hostnames.

Use TShark to obtain the same evidence in the analysis terminal.

~~~bash
tshark -n -r "$RUN/captures/investigation.pcap" \
  -Y 'dns.qry.name == "review.example.test"' -T fields \
  -e frame.number -e frame.time_epoch -e ip.src -e ip.dst -e dns.qry.name -e dns.a

tshark -n -r "$RUN/captures/investigation.pcap" \
  -Y 'http.host == "review.example.test" && http.request.uri == "/downloads/review.txt"' \
  -T fields -e frame.number -e frame.time_epoch -e ip.src -e tcp.srcport \
  -e ip.dst -e tcp.dstport -e http.request.method -e http.request.uri
~~~

**Command overview.** `-n` disables address resolution, `-r` opens a saved capture, `-Y` applies a display filter, and `-T fields` with `-e` prints chosen values. Expect the DNS response to show `192.0.2.10` and the HTTP request to show `192.0.2.20:51005 → 192.0.2.10:80`.

For TLS, SMB and RDP analysis on separately approved packet files, use the [protocol review guide](ZEEK_AND_WIRESHARK.md). Record what was visible and whether encrypted payloads, packet loss, asymmetric capture, or NAT limit the conclusion.

## 4. Build the Zeek baseline

~~~bash
mkdir -p "$RUN/zeek/baseline" "$RUN/zeek/investigation"
~~~

For a native Zeek installation, run:

~~~bash
for sample in baseline investigation; do
  (cd "$RUN/zeek/$sample" &&
    "$ZEEK" -r "$RUN/captures/$sample.pcap" \
      LogAscii::use_json=T policy/protocols/conn/community-id-logging) || break
done
~~~

For rootless Podman on RHEL, use the approved `ZEEK_IMAGE` from the [implementation guide](IMPLEMENTATION_GUIDE.md#step-13--run-zeek-offline-against-the-synthetic-pcap).

~~~bash
for sample in baseline investigation; do
  podman run --rm --pull=never --network none --cap-drop=all \
    -v "$RUN/captures:/pcaps:ro,Z" -v "$RUN/zeek/$sample:/out:Z" \
    -w /out "$ZEEK_IMAGE" zeek -r "/pcaps/$sample.pcap" \
    LogAscii::use_json=T policy/protocols/conn/community-id-logging || break
done
~~~

Check the output of either run.

~~~bash
for sample in baseline investigation; do
  printf '\n%s\n' "$sample"
  wc -l "$RUN/zeek/$sample/"{conn,dns,http}.log
  jq -c '{uid, host, uri, method, status_code}' "$RUN/zeek/$sample/http.log"
done
~~~

**Command overview.** Zeek decodes each file to newline JSON in a separate directory. Podman reads the captures from a read-only mount and writes to the designated output directory with networking disabled. The Community ID policy adds a shared flow identifier to `conn.log`. `wc` counts rows and `jq` displays selected HTTP fields. Expect 6 connection, 3 DNS and 3 HTTP rows for the baseline. Expect 4 connection, 2 DNS and 2 HTTP rows for the investigation. One HTTP row should show `review.example.test`. Use that row's Zeek `uid` to look up its connection, then use the connection's Community ID for the Suricata pivot. The DNS lookup is a separate UDP flow. Correlate it by query, answer, client, and time.

In a real baseline, compare like-for-like windows, record maintenance periods and changes in packet volume, and break down results by segment, service, protocol, and time of day. A new hostname in a two-capture exercise is a test signal. Establish a longer, representative baseline before setting operational alert thresholds.

## 5. Test and tune the Suricata rule

Review the [offline YAML](../../configs/network-defense/suricata/http-offline.yaml.example) and [HTTP rule](../../configs/network-defense/suricata/http-review.rules). The rule requires an established client request with the exact HTTP host and URI. The YAML enables Community ID with seed `0`, matching Zeek's default. Its outputs are alerts, HTTP events, and flow records. It uses the package's classification data. If your package installs the classification or reference files elsewhere, set their approved paths with `--set classification-file=/approved/path` and `--set reference-config-file=/approved/path`.

~~~bash
SURICATA_CONFIG="$REPO/configs/network-defense/suricata/http-offline.yaml.example"
SURICATA_RULE="$REPO/configs/network-defense/suricata/http-review.rules"
mkdir -p "$RUN/suricata/"{check,baseline,investigation}
suricata -T -c "$SURICATA_CONFIG" -S "$SURICATA_RULE" -l "$RUN/suricata/check"

for sample in baseline investigation; do
  TZ=UTC suricata -r "$RUN/captures/$sample.pcap" -c "$SURICATA_CONFIG" \
    -S "$SURICATA_RULE" -l "$RUN/suricata/$sample" || break
done

for sample in baseline investigation; do
  printf '\n%s\n' "$sample"
  jq -cs '[.[] | select(.event_type == "alert" and .alert.signature_id == 1001001) |
    {timestamp, community_id, pcap_cnt, src_ip, src_port, dest_ip, dest_port,
     signature: .alert.signature, revision: .alert.rev}]' "$RUN/suricata/$sample/eve.json"
done
~~~

**Command overview.** `-T` checks the configuration and the single lab rule. `-r` reads packets offline, `-S` loads only the specified rules, and `-l` writes to the private output directory. Stop if the configuration test fails. Expect the baseline to decode HTTP with zero rule alerts and the investigation to produce one SID `1001001` alert. Confirm that both runs processed the expected packet counts. A missing or empty EVE file is a failed collection check.

To measure the benefit of narrowing a rule, copy it to the private run directory as a test variant. Remove only `http.host; content:"review.example.test"; startswith; endswith;`, change the message and use test SID `1001002`. Repeat the configuration test and the two replays in new output directories. The broad variant should also alert on the approved host's download in both captures. Record the number of benign and expected alerts for each variant. Keep the precise rule if it meets the expected results. For production rule changes, document the owner, tested rule version, rollback and retest before promotion.

## 6. Pivot and validate the exported file with YARA

Look up the alert's `community_id` in the same capture's Zeek `conn.log`. Confirm client/server addresses, ports, protocol and the time window. Compare the Suricata `pcap_cnt` to Wireshark's packet list. Stream reassembly can associate an alert with a later packet than the HTTP request. Do not join records from unrelated runs using the Community ID alone.

Extract only the synthetic HTTP objects from the specified streams. Both files have the same name, so export them to separate directories.

~~~bash
mkdir -p "$RUN/artifacts/"{control,candidate}
tshark -n -r "$RUN/captures/baseline.pcap" -Y 'tcp.port == 51002' \
  -w "$RUN/artifacts/control.pcapng"
tshark -n -r "$RUN/captures/investigation.pcap" -Y 'tcp.port == 51005' \
  -w "$RUN/artifacts/candidate.pcapng"
for sample in control candidate; do
  tshark -n -q -r "$RUN/artifacts/$sample.pcapng" \
    --export-objects "http,$RUN/artifacts/$sample" || break
  sha256sum "$RUN/artifacts/$sample/review.txt"
  yara -s "$REPO/rules/yara/lab_http_artifact.yar" "$RUN/artifacts/$sample/review.txt" || break
done
~~~

**Command overview.** TShark writes private filtered copies and extracts each response body. `sha256sum` records its fingerprint. `yara -s` reports a matching rule and string offsets. The control contains one marker and should produce no rule match. The candidate should match `LAB_Synthetic_HTTP_Artifact` and report both marker strings. This test validates a local classification rule against known bytes. Handle unknown files under the approved evidence process and avoid executing them.

## 7. Convert a separate Sysmon Sigma control to SPL

~~~bash
"$RUN/venv/bin/sigma" convert -t splunk -p splunk_windows \
  -o "$RUN/sysmon-review.spl" "$REPO/rules/sigma/lab_sysmon_review.yml" &&
  cat "$RUN/sysmon-review.spl"
~~~

**Command overview.** The Splunk backend and Windows mapping pipeline convert the Sigma rule and write the result to the private run directory. Check that it uses process creation `EventCode=1`, a `cmd.exe` image suffix and the command-line marker. Confirm these fields exist in your deployment before using the output.

On **WINHUNT01 only**, after verifying Sysmon and forwarding, run the two independent process controls in PowerShell. Record the UTC execution window and check Event Viewer under **Applications and Services Logs → Microsoft → Windows → Sysmon → Operational** for Event ID 1.

~~~powershell
cmd.exe /d /c 'echo LAB_SIGMA_CONTROL_MARKER'
cmd.exe /d /c 'echo LAB_SIGMA_REVIEW_MARKER'
~~~

**Summary.** `/d` disables AutoRun commands, `/c` runs the echo and closes the process, and `echo` prints an inert marker. In Splunk use the recorded time window and `index=sysmon host=WINHUNT01 sourcetype="XmlWinEventLog:Microsoft-Windows-Sysmon/Operational"` before the converted filter. Verify both markers are present in source events and only the review marker matches the rule. If the deployment exposes `EventID`, `process_path`, or `process_command_line`, review the local mapping before saving a search. Keep this separate from the packet finding. A process control generated on the VM and a synthetic packet session have independent origins.

## 8. Upload a small fixture to the existing Splunk index

Use this step only after verifying the current Splunk lab. The optional sensor/forwarder route is covered in [Splunk integration](SPLUNK_INTEGRATION.md). For this exercise, use a one-time upload into the existing `lab` index with no persistent input. Prepare only the fields needed for the case. The upload converts source event times to UTC seconds for consistent parsing and keeps the original higher-resolution evidence in the private source files.

~~~bash
REPLAY="$RUN/passive-$RUN_ID.json"
(
  set -e
  for sample in baseline investigation; do
    jq -c --arg run "$RUN_ID" --arg sample "$sample" '
      {timestamp: (.ts | floor | todateiso8601), run_id: $run, sample: $sample,
       record_type: "zeek_http", zeek_uid: .uid, http_host: .host, uri, status_code}
    ' "$RUN/zeek/$sample/http.log"
    jq -c --arg run "$RUN_ID" --arg sample "$sample" '
      {timestamp: (.ts | floor | todateiso8601), run_id: $run, sample: $sample,
       record_type: "zeek_conn", community_id, zeek_uid: .uid,
       src: .["id.orig_h"], src_port: .["id.orig_p"], dst: .["id.resp_h"],
       dst_port: .["id.resp_p"], proto}
    ' "$RUN/zeek/$sample/conn.log"
    jq -c --arg run "$RUN_ID" --arg sample "$sample" '
      select(.event_type == "alert" and .alert.signature_id == 1001001) |
      {timestamp: (.timestamp | if test("(Z|[+]00:?00)$") then .[0:19] + "Z"
        else error("Suricata output must use UTC") end),
       run_id: $run, sample: $sample, record_type: "suricata_alert", community_id,
       src: .src_ip, src_port, dst: .dest_ip, dst_port: .dest_port, proto,
       signature_id: .alert.signature_id, pcap_cnt}
    ' "$RUN/suricata/$sample/eve.json"
  done
) > "$REPLAY" && jq -s 'group_by([.sample,.record_type]) |
  map({sample: .[0].sample, type: .[0].record_type, rows: length})' "$REPLAY"
~~~

**Command overview.** `jq` selects a small set of fields, labels each row with its run, and prints counts per capture and record type. Expect 3 baseline HTTP rows, 6 baseline connection rows, 2 investigation HTTP rows, 4 investigation connection rows, and 1 investigation alert. Stop if preparation fails or the 16-row result differs.

1. On the private Splunk Web console, open **Add Data → Upload**, select the generated JSON file, and go to **Set Source Type**. If the browser runs on Windows, copy only this synthetic JSON to a restricted local directory or browse the WSL files through the Windows WSL share.
2. Select **`_json`** as the source type. In the preview, verify that each event occupies a single row, fields are present, and event time agrees with the first `timestamp` value after accounting for the UI time zone. If parsing differs, use the **Advanced** tab to set `INDEXED_EXTRACTIONS=JSON`, `TIMESTAMP_FIELDS=timestamp`, `TIME_FORMAT=%Y-%m-%dT%H:%M:%SZ`, `TZ=UTC` and `KV_MODE=none` in a separate source type saved as `lab:network:http-fixture`. Verify the preview again before indexing.
3. In **Input Settings** choose index **`lab`** and set the host to **`lab-http-fixture`**. In **Review**, check the destination and submit once. A repeat upload can duplicate events. Start a fresh run ID for a retest.
4. In Search, replace `REPLACE_RUN_ID` with the run directory name printed by `printf '%s\n' "$RUN_ID"`. Compare the same counts and event times with the local replay file. If counts or timestamps disagree, resolve the ingest issue before drawing findings.

~~~spl
index=lab host=lab-http-fixture earliest=-24h run_id="REPLACE_RUN_ID"
| eval expected_epoch=strptime(replace(timestamp,"Z$","+0000"),"%Y-%m-%dT%H:%M:%S%z")
| eval drift=abs(_time-expected_epoch)
| stats count as rows count(expected_epoch) as timestamps max(drift) as max_drift_seconds by sample record_type
~~~

Expect `timestamps=rows` and zero drift. Use the appropriate absolute search window if the test input was deliberately backdated.

## 9. Compare baseline and investigation in Splunk

~~~spl
index=lab host=lab-http-fixture earliest=-24h run_id="REPLACE_RUN_ID" record_type=zeek_http
| stats count(eval(sample="baseline")) as baseline count(eval(sample="investigation")) as investigation by http_host uri
| where baseline=0 AND investigation>0
~~~

The expected new pair is `review.example.test` and `/downloads/review.txt`. Find its `zeek_uid` in the HTTP rows, then compare it to the joined flow evidence.

~~~spl
index=lab host=lab-http-fixture earliest=-24h run_id="REPLACE_RUN_ID" sample=investigation
(record_type=zeek_conn OR (record_type=suricata_alert signature_id=1001001))
| where isnotnull(community_id)
| eval conn_time=if(record_type="zeek_conn",_time,null()), alert_time=if(record_type="suricata_alert",_time,null())
| stats count(conn_time) as connections count(alert_time) as alerts min(conn_time) as start min(alert_time) as alert_seen
    values(zeek_uid) as zeek_uid values(pcap_cnt) as frame by community_id src src_port dst dst_port
| where connections=1 AND alerts=1 AND abs(alert_seen-start)<=30
| convert ctime(start) ctime(alert_seen)
~~~

Expect one joined row for client port `51005`. A no-result query can indicate a missing feed, mismatched timestamps or a tuple change across NAT. Before using a wider correlation window, confirm the clock, sensor location, address translation, and packet coverage. In an approved real investigation, check the relevant firewall flow or NAT record and verify DNS, asset identity and the listener configuration with the owners. This fixture contains no firewall log, so the firewall pivot remains untested.

## 10. Document the case, evidence and retest

| Record | Evidence to capture in the private case file |
| --- | --- |
| Observation | UTC range, approved baseline hostname, new hostname, client/server tuple and HTTP response status |
| Validation | PCAP fingerprint, frame, Zeek UID, Suricata SID/revision and Community ID, YARA match and file fingerprint |
| Source limits | Capture point, known packet or protocol gaps, and the services or systems outside this observation |
| Owner follow-up | Check the DNS record, virtual-host binding, HTTP-to-HTTPS behavior, whether access from the client segment is intended, and which other paths share the listener |
| Recommendation and closure | Document the approved change, owner, due date, and retest with both the expected secure flow and the unwanted cleartext condition |

Copy the [validation worksheet](../../evidence/sanitized/network-defense-validation.md) into the private run directory and record the case. For CMMC practice, index the alert and triage evidence against the applicable monitoring objective in [CMMC Level 2](CMMC_LEVEL2.md). Document the remaining assessment evidence and scope. Apply your retention policy to generated captures, logs and upload copies, and publish only reviewed summaries.

## References

- [Zeek community ID customization](https://docs.zeek.org/en/current/customizations.html) explains how to add the shared flow identifier.
- [Wireshark TShark manual](https://www.wireshark.org/docs/man-pages/tshark.html) documents saved captures, display filters and HTTP object export.
- [Suricata EVE JSON output](https://docs.suricata.io/en/suricata-8.0.5/output/eve/eve-json-output.html) documents the alert data and Community ID options.
- [YARA command-line documentation](https://yara.readthedocs.io/en/latest/commandline.html) explains how to scan a file and show matching strings.
- [Sigma Getting Started](https://sigmahq.io/docs/guide/getting-started.html) explains the Splunk backend and Windows mapping pipeline.
- [Splunk source-type preview](https://help.splunk.com/en/splunk-enterprise/get-started/get-data-in/10.6/how-to-get-data-into-your-deployment/assign-the-correct-source-types-to-your-data) explains event and timestamp settings.
