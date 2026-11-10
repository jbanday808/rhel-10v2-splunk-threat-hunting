# Custom Suricata rules for passive vulnerability review

**Optional, offline-first IDS exercise.** The [12-rule pack](../../configs/network-defense/suricata/passive-review.rules) adds SIDs `1002001`-`1002012` without changing the existing DNS marker or HTTP worked case. It supports the Senior Cybersecurity Analyst responsibilities in the [draft CONOPS](CONOPS.md): protocol analysis, baseline comparison, anomaly triage, owner validation, reporting, and detection tuning. It does not demonstrate employment experience, clearance, operational deployment, or compliance.

These are **review signals**, not proof of compromise, a CVE, missing patches, or an exploitable host. No scanning, credential use, live capture, blocking, or automatic containment is performed. Keep real PCAPs, EVE records, credentials, protected network details, and case files out of public GitHub.

The [recorded offline replay](../../evidence/sanitized/network-defense-validation.md#custom-suricata-rule-pack-offline-replay) used Suricata **7.0.3** on a separate Linux analysis host. This is an observed test version, not a deployment recommendation or a claim that Suricata 8/RHEL 10 acceptance has run. Use an approved, supported release and repeat the matrix on the actual lab version before adoption.

## 1. Review the observation boundary

Execution host: an approved Linux analysis workstation or optional analysis VM, from the repository root as an unprivileged user. Use the approved Suricata installation in [SURICATA.md](SURICATA.md) or the [worked HTTP case](OFFLINE_HTTP_WALKTHROUGH.md). No service needs to run for saved-file analysis.

The [offline configuration](../../configs/network-defense/suricata/passive-offline.yaml.example) uses documentation addresses, **not the VMware addresses**:

| Variable | Fixture value | Required owner review before any separate operational use |
| --- | --- | --- |
| `HOME_NET` | `192.0.2.0/24` | All authorized internal segments visible at the capture point, including IPv6 where applicable |
| `EXTERNAL_NET` | `!$HOME_NET` | Means outside the defined boundary, not necessarily Internet or hostile |
| `DNS_SERVERS` | `192.0.2.30` | Approved resolvers, forwarders, and client roles; account for approved recursive-server traffic |

Use the fixture values unchanged for regression tests. Never copy this minimal YAML over an installed sensor configuration. Operational adoption requires an independently reviewed merge into the existing passive configuration, SID collision checks, capture authorization, and change approval. `-S` replaces the loaded ruleset for that process; it is appropriate for isolated replay, not an instruction to replace production feeds.

## 2. Understand each signal and its limits

Priority `2` means a policy/exposure review candidate; priority `3` is a lower-confidence activity review. Neither is an incident declaration.

| SID | Exact observation | Benign explanations, limits, and owner follow-up |
| --- | --- | --- |
| `1002001` | Decoded DNS query on TCP/UDP 53 to an address outside `DNS_SERVERS`; at most one alert/source/60 seconds | Approved forwarding, split DNS, or an incomplete resolver list. Verify resolver configuration and intended egress; not evidence of malicious DNS. DoH/DoT are outside this rule. |
| `1002002` | Five queries/source/60 seconds with a first label of 50-63 ASCII letters, digits, `_`, or `-`; at most one alert in that window | CDN tokens, telemetry, and security tools can match. Review query/response patterns, destination, client software, and the baseline. This is not entropy analysis or proof of tunneling/DGA. |
| `1002003` | HTTP/1.x request containing an actual `Authorization: Basic` header with a nonempty value | Approved lab or legacy service. Base64 is not encryption. Confirm the capture point is not downstream of approved TLS termination, identify the service owner, and review HTTPS enforcement. Do not copy header values into a case summary. |
| `1002004` | HTTP/1.x request containing `Proxy-Authorization: Basic` | Assess the client-to-proxy leg and approved proxy design; a CONNECT request can expose proxy credentials even if the subsequent tunnel is TLS. Review authentication and transport policy. |
| `1002005` | Exact HTTP `TRACE` request method | Diagnostics or approved testing. A request does not prove TRACE is enabled or a response reflects credentials. Review the response and server policy before recommending a change. |
| `1002006` | ServerHello selects TLS 1.0, directed to a `HOME_NET` client | Legacy client/service compatibility. Confirm the selected version and service configuration; recommend owner-approved modern TLS migration. A legacy ClientHello or record-layer version alone is not sufficient. |
| `1002007` | ServerHello selects TLS 1.1, directed to a `HOME_NET` client | Same validation as TLS 1.0. Encrypted application content, patch state, and certificate-chain trust are not assessed. |
| `1002008` | NBSS-framed SMBv1 client request other than SMB_COM_NEGOTIATE on TCP/445 | Legacy service/client or isolated compatibility testing. Validate server acceptance and asset configuration. An SMB1-formatted initial negotiate can select SMB2, so that command is deliberately excluded. |
| `1002009` | Decoded SMB from `HOME_NET` to `EXTERNAL_NET`; at most one alert/source/60 seconds | Approved cross-segment file service or an incomplete boundary. Review peer ownership, firewall policy, authentication logs, and change tickets. No SMB signing/encryption conclusion is made. |
| `1002010` | Server TCP/3389 response selects Standard RDP Security (`selectedProtocol=0`) | Legacy compatibility. Validate this session with the owner and review TLS/NLA policy; it does not establish a specific RDP vulnerability. |
| `1002011` | Server TCP/3389 response selects TLS-only RDP (`selectedProtocol=1`), not CredSSP | This negotiation did not select NLA/CredSSP. It does not prove the server never supports NLA, a successful login, or a particular account exposure. Confirm client and server settings. |
| `1002012` | Decoded RDP from `HOME_NET` to `EXTERNAL_NET`; at most one alert/source/60 seconds | Approved gateway, support session, or an incomplete boundary. Validate access authorization, peer inventory, Windows logon evidence, and segmentation policy. |

The SMBv1 and two RDP response signatures inspect reassembled TCP bytes at fixed offsets in the first NBSS/TPKT record. They are intentionally limited to TCP/445 and server TCP/3389 respectively; alternate ports, later/coalesced records, midstream capture, or missing stream beginnings can evade them. They are not general SMB or RDP parsers. The egress rules instead require Suricata protocol identification. TLS rules inspect server-to-client negotiation for internal clients, not every internal server serving external clients.

HTTPS application headers, encrypted SMB/RDP payloads, TLS 1.3 certificates, DNS encryption, asymmetric visibility, and packet loss limit inference. A TAP/SPAN must actually deliver authorized traffic; VMware VMnet8 NAT is not a mirror. These examples do not establish network-wide coverage.

## 3. Generate safe positive and negative controls

The standard-library [generator](../../scripts/network-defense/generate_passive_fixtures.py) writes documentation-address packets to disk only. HTTP authorization values are inert, deliberately non-credential placeholders; no password is supplied or decoded. TLS examples stop after hello messages, SMB examples negotiate or echo, and RDP examples stop at negotiation. Nothing connects to these addresses.

~~~bash
umask 077
REPO="$PWD"
mkdir -p "$HOME/network-lab"
RUN=$(mktemp -d "$HOME/network-lab/passive-rules-XXXXXXXX")
python3 scripts/network-defense/generate_passive_fixtures.py "$RUN/captures"
suricata -V
~~~

**Command overview:** Create a private run directory outside Git, generate independent controls and an `expected-alerts.json` manifest with packet totals and SHA-256 values, and record the actual engine version. The default packet timestamp is fixed for reproducibility. Use `--start-epoch` with a reviewed UTC epoch for a separate ingestion exercise; backdated fixtures may be outside Splunk retention/search windows.

**Summary:** Each capture is independent so source-based threshold state cannot leak between cases. The writer refuses repository paths (including symlink destinations), existing output directories, and invalid start times.

## 4. Check syntax and replay one capture

~~~bash
CONFIG="$REPO/configs/network-defense/suricata/passive-offline.yaml.example"
RULES="$REPO/configs/network-defense/suricata/passive-review.rules"
mkdir "$RUN/check" "$RUN/dns-long-five"
suricata -T -c "$CONFIG" -S "$RULES" -l "$RUN/check"
~~~

**Command overview:** `-T` must load all 12 rules without rule failures before continuing. Use the installed package's classification/reference files; if their paths differ, supply the approved `--set classification-file=/approved/path` and `--set reference-config-file=/approved/path` to both commands.

~~~bash
TZ=UTC suricata --runmode single -r "$RUN/captures/dns-long-five.pcap" \
  -c "$CONFIG" -S "$RULES" -l "$RUN/dns-long-five"
python3 scripts/network-defense/summarize_network_logs.py \
  "$RUN/dns-long-five/eve.json" --type suricata
~~~

**Summary:** `-r` reads only the saved capture, `-l` isolates output, and the summarizer prints aggregate event counts without payloads. Expect one alert with SID `1002002` on the fifth query; inspect the private EVE file to verify the SID, timestamp, revision, Community ID, and flow packet totals. Do not infer the correct SID from the aggregate count alone.

Run the complete matrix with the existing unittest runner:

~~~bash
SURICATA_BIN="$(command -v suricata)" \
  python3 -B -m unittest discover -s tests -p test_network_defense.py -v
~~~

**Command overview:** The replay test runs `-T`, then a fresh offline process per capture. It compares **all** alert SIDs and exact counts to ground truth, verifies protocol identification, and checks that flow packet totals equal the fixture packet totals, so an empty/failed replay cannot pass as a clean negative. Without Suricata, the engine test is explicitly skipped; fixture/source checks alone do not validate detections. If `command -v suricata` fails, install the approved analyzer before claiming the replay ran.

Controls include approved versus unapproved DNS over UDP and TCP, four versus five long-label queries, 49/50/63-character boundaries, 61-second spacing, separate sources, Basic versus Bearer/empty values and unrelated headers, proxy/origin separation, TRACE versus GET, TLS 1.2/1.3 and rejected legacy client offers, SMB1-to-SMB2 negotiation, internal/external peers, CredSSP selections `2`/`8`, RDP failure versus success messages, and a response split across TCP segments.

## 5. Triage, measure, and tune under the CONOPS

Record the private capture hash, UTC interval, sensor/tool versions, SID/revision, tuple, relevant frame/stream, Community ID, capture gaps, baseline comparison, benign alternatives, confidence, owner, and disposition. Pivot to Zeek using Community ID plus tuple/time; retain Zeek UID for protocol logs. Confirm suspected configuration faults with the administrator rather than promoting a packet-only hypothesis to a confirmed vulnerability.

If sanitized EVE fixtures are separately approved for the existing `lab` index, verify JSON fields, event time, retention, and source labeling before using this example. Replace the source-type placeholder with the locally verified mapping; no new index or forwarding change is required by this pack.

~~~spl
index=lab sourcetype="REPLACE_WITH_VERIFIED_EVE_SOURCETYPE" earliest=-24h event_type=alert
| spath path=alert.signature_id output=sid
| spath path=alert.signature output=signature
| spath path=alert.rev output=revision
| where sid>=1002001 AND sid<=1002012
| stats count as alerts min(_time) as first_seen max(_time) as last_seen
    values(community_id) as community_ids by sid revision signature src_ip dest_ip
~~~

For private triage, use the actual fixture time range rather than `-24h` for fixed-time captures. Preserve raw evidence privately and publish only reviewed aggregates.

Measure fixture detection recall (expected cases detected / expected cases), false-positive controls, decoded/expected packets, reviewed-alert precision, duplicate rate, triage turnaround, and ingestion latency **only when ingestion is actually tested**. Source-based alert limits can hide additional destinations, and burst thresholds can aggregate multiple applications on a shared source/NAT address. These example thresholds are not learned baselines or approved performance targets.

Tune `HOME_NET` and resolver roles before thresholds. Keep peer exceptions narrowly scoped and owner-approved; do not globally suppress SMB/RDP or disable a protocol parser to reduce noise. Preserve the prior rule revision, replay the same controls after changes, and record expected/observed results, reviewer, evidence ID, and retest date. Never tune against protected traffic on public infrastructure.

Route suspected incidents through the [incident workflow](../security-operations/INCIDENT_MANAGEMENT.md) and configuration findings through the [vulnerability workflow](../security-operations/VULNERABILITY_MANAGEMENT.md). Proposed NIST SP 800-53 links include SI-4 (monitoring), CA-7 (continuous monitoring), and RA-5 (vulnerability monitoring); these are illustrative evidence relationships, not RMF authorization, DoD acceptance, or CMMC certification.

**Rollback:** Offline runs install no rules or service changes; stop only the replay process you started and retain/dispose of its named private run directory under the approved retention policy. For a separately approved sensor change, restore only the added rule/config entries from the reviewed backup, run `-T`, and confirm existing passive feeds and core lab services remain unaffected. Live deployment and owner acceptance remain **Pending**.

## References

- [OISF rule syntax](https://docs.suricata.io/en/suricata-7.0.3/rules/intro.html), [DNS buffers](https://docs.suricata.io/en/suricata-7.0.3/rules/dns-keywords.html), [HTTP buffers](https://docs.suricata.io/en/suricata-7.0.3/rules/http-keywords.html), [TLS negotiation](https://docs.suricata.io/en/suricata-7.0.3/rules/tls-keywords.html), and [threshold semantics](https://docs.suricata.io/en/suricata-7.0.3/rules/thresholding.html).
- [Microsoft RDP protocol specification](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-rdpbcgr/) defines the RDP Negotiation Response and selected security protocol values.
- [RFC 8996](https://www.rfc-editor.org/rfc/rfc8996.html) deprecates TLS 1.0 and 1.1; [RFC 7617](https://www.rfc-editor.org/rfc/rfc7617.html) describes HTTP Basic authentication and its transport limitations.
