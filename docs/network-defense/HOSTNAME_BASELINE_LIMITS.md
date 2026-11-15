# A new hostname on a familiar server

**Status:** proposed interpretation exercise. The [offline HTTP walkthrough](OFFLINE_HTTP_WALKTHROUGH.md) provides a **cleartext HTTP** positive and control. It does not contain a TLS handshake, so it cannot validate an SNI hunt. Any TLS review needs a separately approved capture and an observed parser result.

## Ask what changed

Several hostnames can share one address. Ask: **“Did this client contact a hostname outside its approved baseline, and can the service owner explain it?”** A name seen in a request or handshake is a lead, not proof that a different server, malicious site, or protected content was reached.

## Use the provided HTTP control first

1. Generate and keep the two private synthetic captures as described in the [worked HTTP case](OFFLINE_HTTP_WALKTHROUGH.md#2-generate-and-verify-the-captures). Record their hashes and UTC windows.
2. In Wireshark, open the baseline capture and filter `http.host == "updates.example.test"`. Review the client, destination, port, request URI, and response. Then open the investigation capture and filter `http.host == "review.example.test"`.
3. Confirm the candidate is the exercise's client port `51005`, to the same example destination and path as the control. Compare the actual HTTP Host header, not just the destination IP. The expected candidate was deliberately added to the synthetic capture; it is **not** an observed compromise.
4. Check the original frame and response before reporting. A displayed hostname without a complete request/response is weaker evidence than the worked fixture's reconstructed stream.

**Expected testable result:** the approved hostname appears in the baseline; the review hostname appears only in the investigation capture. If either file or parser output is missing, record a failed exercise rather than a clean hunt.

## Treat TLS as a separate evidence path

With a separately authorized TLS PCAP that includes the client handshake, `tls.handshake.extensions_server_name` can show a visible Server Name Indication value in Wireshark. Check the actual client, server, time, and parser field before using it as a baseline clue. Do **not** apply this test to the repository's HTTP-only fixture and report a zero result as TLS coverage.

| Observation | Supported reading | Important limit |
| --- | --- | --- |
| `http.host` in the supplied cleartext HTTP fixture | A hostname claimed in the visible request | It does not prove the server was authorized or a download was safe. |
| Visible TLS SNI in an approved handshake | A hostname offered by a client for that connection | It does not reveal HTTPS URL, request body, response, or account identity. |
| No visible SNI | A field was unavailable in the observed capture | Missing handshake, parser limits, or Encrypted Client Hello may explain it; do not infer no website was contacted. |
| Same destination IP with two hostnames | Shared address is plausible | An IP-only match cannot decide which virtual host was used. |

Use comparable periods and asset roles before deciding a name is unusual. CDNs, shared hosting, redirects, software updates, and approved testing are ordinary alternatives. Confirm the hostname, alias, application, and expected change with the service owner. DNS and an HTTP/TLS connection are distinct flows; associate them only after checking client, answer, time, and any NAT or resolver boundary.

## Explain the limit plainly

Keep PCAPs, full names, and endpoint context private. In the [network validation worksheet](../../evidence/sanitized/network-defense-validation.md), record capture and parser versions, baseline window, candidate frame/flow, owner response, and missing visibility. A plain-language update is: “A lab client used a different name for a familiar address. We can see that name in this test request, but the service owner must explain whether it was expected.”

Sources: [Wireshark HTTP fields](https://www.wireshark.org/docs/dfref/h/http.html), [Wireshark TLS SNI field](https://www.wireshark.org/docs/dfref/t/tls.html), and [TLS Encrypted Client Hello](https://www.rfc-editor.org/rfc/rfc9849.html).
