# Optional Suricata passive review rules

These are **alert-only, offline examples** for the optional network-defense workstream. They support baseline review and passive vulnerability *hypotheses*; they do not establish a finding, authorize capture, or install a sensor. The existing [`local.rules`](local.rules) DNS marker and [`http-review.rules`](http-review.rules) worked HTTP exercise remain separate.

[`passive-review.rules.example`](passive-review.rules.example) uses the documentation ranges `192.0.2.0/24` (example clients) and `198.51.100.0/24` (example protected servers). It will not match the real lab's `172.25.250.0/24` traffic as written. For an approved use, copy the file to a **private** location, replace the ranges with the exact authorized client/server segments, check the capture point and rule direction, and review the local Suricata version and configuration. Do not put real network inventories, captures, credentials, or EVE logs in this repository.

## What each rule means

| SID | Candidate observation | Analyst check before reporting |
| --- | --- | --- |
| `1002001` | First DNS label is 45–63 characters | Compare to the domain baseline, CDN behavior, resolver logs, and other queries. Length is not entropy or exfiltration proof. The per-source five-minute alert limit hides repeat alert records; use DNS logs for counts. |
| `1002002` | A visible HTTP request contains `Authorization: Basic` | Confirm the service is really cleartext on the observed hop and review the approved encryption policy. Keep the authorization value private. Encrypted HTTPS without decryption is not visible to this rule. |
| `1002003`–`1002004` | Negotiated TLS 1.0 or 1.1 | Check both handshake directions, policy exceptions, client/server roles, and actual negotiated version. The rule uses `tls.version`, not the record-version field. |
| `1002005` | A visible certificate has passed its validity end date | Confirm the sensor saw the certificate, clock accuracy, server name, and service owner. This keyword checks the date; it does not validate trust or hostname. TLS 1.3 may hide certificates from a passive sensor. |
| `1002006` | SMBv1-formatted transaction on the example protected segment | Confirm the *selected* dialect with SMB logs and the server owner. Initial SMBv1 negotiation can upgrade to SMBv2; one match does not prove SMBv1 service is enabled. The five-minute limit is per address pair. |
| `1002007` | SYN from the example client segment to TCP/3389 on the example protected segment | Compare the source to approved administration paths and firewall/Windows logs. A SYN is an attempted connection, not a completed RDP session. The five-minute limit is per source. |
| `1002008` | `/.git/config` HTTP path returned status `200` in one transaction | Confirm the response body and virtual host privately with the service owner. A custom error page may return `200`; the rule does not prove the configuration file was exposed. |

The per-source limits reduce repeated alerts, not traffic or the need to measure it. They also mean alert counts cannot be used as total attempt counts. Compare alerts with Zeek, HTTP/DNS metadata, firewall records, packet loss, and the approved steady-state baseline.

## Offline checks

Run from the repository root on a workstation with Suricata, `jq`, and the approved package configuration. These commands do not open an interface or change a system rule file:

```bash
RULES="$PWD/configs/network-defense/suricata/passive-review.rules.example"
RUN="$(mktemp -d)"
mkdir -p "$RUN/replay"
suricata -T -c /etc/suricata/suricata.yaml -S "$RULES" -l "$RUN"
python3 scripts/network-defense/generate_synthetic_pcap.py --output "$RUN/short-dns.pcap"
suricata -r "$RUN/short-dns.pcap" \
  -c /etc/suricata/suricata.yaml -S "$RULES" -l "$RUN/replay"
jq -r 'select(.event_type == "alert" and .alert.signature_id >= 1002001
  and .alert.signature_id <= 1002008) |
  [.timestamp, .alert.signature_id] | @tsv' "$RUN/replay/eve.json"
```

**Command overview:** `-T` checks rule loading; the generator writes one short, harmless DNS query to a private temporary directory; `-r` replays that file without transmitting it; `jq` prints only the new rule IDs and times. **Expected negative control:** the short DNS marker should produce no `1002001`–`1002008` alerts. Check Suricata's exit status, processed packets, EVE file, and DNS decoding before treating zero alerts as a meaningful result. For an additional HTTP negative control, use the existing [worked HTTP exercise](../../../docs/network-defense/OFFLINE_HTTP_WALKTHROUGH.md), which requires its documented `dpkt` dependency.

For **positive controls**, use separately approved synthetic PCAPs and a fresh output directory per replay. Include a long DNS label; an HTTP Basic header containing only a disposable marker; TLS 1.0/1.1 negotiations and an expired test certificate; an SMBv1 transaction; a cross-segment RDP-port SYN; and a `/.git/config` HTTP transaction returning `200`. Pair each with a short DNS name, no Basic header, TLS 1.2/1.3, a valid test certificate, SMBv2, an approved or out-of-scope RDP path, and an HTTP `404` response. Check the expected SID **and absence of unintended SIDs**. The repository does not claim these positive controls or a live sensor test have been run.

Record the Suricata version, rule SHA/revision, capture hash, expected and observed SID counts, packet/flow coverage, false positives, analyst decision, owner feedback, and rollback plan in a private case file. Follow the [CONOPS](../../../docs/network-defense/CONOPS.md) and [detection triage guide](../../../docs/network-defense/DETECTIONS_AND_TESTING.md) before considering any operational change. Do not enable this file through `suricata-update` or copy it to `/etc/suricata/rules/` without an approved change.

## Keyword references

- [Suricata 8 rule headers and transaction direction](https://docs.suricata.io/en/suricata-8.0.5/rules/intro.html)
- [DNS query buffer](https://docs.suricata.io/en/suricata-8.0.5/rules/dns-keywords.html)
- [HTTP request/response buffers](https://docs.suricata.io/en/suricata-8.0.5/rules/http-keywords.html)
- [TLS version and certificate date](https://docs.suricata.io/en/suricata-8.0.5/rules/tls-keywords.html)
- [SMB version and negotiation caveat](https://docs.suricata.io/en/suricata-8.0.5/rules/smb-keywords.html)
- [Threshold behavior](https://docs.suricata.io/en/suricata-8.0.5/rules/thresholding.html)
