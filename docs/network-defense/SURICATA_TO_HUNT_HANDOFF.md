# From a Suricata rule match to a reviewable hunt

**Status:** proposed analyst handoff for the repository's 12 **alert-only** passive rules (`1002001`–`1002012`). The [rule guide](SURICATA_CUSTOM_RULES.md#2-understand-each-signal-and-its-limits) defines what each SID actually matches. Recorded offline replay on a separate Linux host does not establish a deployed RHEL sensor, complete network visibility, or a live Splunk alert.

## First confirm what fired

In the approved private EVE record, note the UTC time, `alert.signature_id`, `alert.rev`, `alert.signature`, `alert.action`, source/destination tuple, protocol, `flow_id`, and any `community_id` or `pcap_cnt`. Verify the rule revision and `HOME_NET`, `EXTERNAL_NET`, and `DNS_SERVERS` values used for that run. An `allowed` action and an alert-only rule are an observation, **not** evidence the traffic was blocked.

Use the original private capture to inspect the packet or reassembled stream. `pcap_cnt` can locate the alerting packet in offline replay; it may be later than the first relevant request because a signature can match after reassembly. If a Zeek log exists for the **same capture**, compare Community ID, both addresses and ports, transport, and time. Keep Zeek's `uid` for Zeek-internal pivots; Suricata's `flow_id` is not a Zeek UID. Do not join unrelated runs just because synthetic tuples or Community IDs repeat.

## Choose the next question by rule family

| SIDs | Narrow hunt question | Necessary control or owner check |
| --- | --- | --- |
| `1002001`–`1002002` (DNS) | Was a resolver outside the approved list used, or were long labels repeated by one client? | Compare approved-resolver, four-query, short-label, spaced-query and separate-source controls from the [fixture matrix](SURICATA_CUSTOM_RULES.md#3-generate-safe-positive-and-negative-controls). Ask the DNS/endpoint owner about legitimate forwarding or software. |
| `1002003`–`1002005` (HTTP) | Was a cleartext Basic authorization header or TRACE **request** observed? | Compare Bearer, empty/unrelated header, and GET controls. Ask the service/proxy owner about transport policy and the response; never copy header values to a public report. |
| `1002006`–`1002007` (TLS) | Which older version did the **server select** for this session? | Compare modern and rejected-client handshakes. Confirm service configuration with the owner; a client offer alone does not prove the server accepted it. |
| `1002008`–`1002009` (SMB) | Was a non-negotiate SMBv1 request or decoded SMB across the reviewed boundary observed? | Compare SMB1-to-SMB2 negotiation and internal-peer controls. Confirm server acceptance, asset role and the real network boundary. |
| `1002010`–`1002012` (RDP) | What negotiation response or cross-boundary RDP flow was actually observed? | Compare CredSSP, failed, client-offer and internal-peer controls. Ask Windows/network owners about approved support routes and settings; a flow is not a logon. |

The family questions are starting points, not a claim that every rule fires on every deployment. If a positive capture does not produce its expected alert, or a nonmatching control alerts, record the rule/version/field failure before forwarding a security finding. An empty event list is **inconclusive** until packet visibility, rule loading, parser output and time coverage are checked. The [network validation worksheet](../../evidence/sanitized/network-defense-validation.md) holds the test status.

## Package the handoff

Give the next analyst or owner a short private record: question; SID and revision; exact run/capture hash; UTC interval; tuple and packet/flow reference; matched and nonmatching controls; collection gaps; benign explanations; person who can verify the system setting; and the decision needed. The optional [Splunk aggregate search](SURICATA_CUSTOM_RULES.md#5-triage-measure-and-tune-under-the-conops) is for a separately verified fixture upload to the existing `lab` index, not proof of a configured network feed. Keep raw EVE, PCAP, credentials and customer identifiers out of GitHub.

**Worked synthetic handoff:** SID `1002002` is expected from the fixture `dns-long-five`, while `dns-long-four`, `dns-label-49`, `dns-long-spaced`, and `dns-separate-sources` should not alert. The next question is whether one approved client's repeated long labels are normal for its software. A private replay must confirm the actual alerts and packet counts; the source manifest alone does not prove the analyzer ran.

**Plain-language briefing:** “A rule marked a network pattern for review. We checked whether the monitoring point saw it correctly and whether normal activity can explain it. The system owner will help decide what it means.”

Sources: [Suricata EVE alert and packet fields](https://docs.suricata.io/en/suricata-8.0.4/output/eve/eve-json-format.html) and [Zeek Community ID support](https://docs.zeek.org/en/current/customizations.html).
