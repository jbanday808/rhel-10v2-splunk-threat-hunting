# Arkime — Network Baseline and Anomaly Analysis Playbook

Follow this playbook after the [installation guide](IMPLEMENTATION_GUIDE.md) and [worked HTTP case](INVESTIGATION.md). It turns captured sessions into an investigation: check coverage, compare a baseline, review a candidate, inspect packets and report the evidence.

**Status:** the expressions below were checked against Arkime 6.9.1's documented/source-defined fields. They still need validation in your installed Viewer and authorized dataset. They are candidate hunts, not proof that a malicious event occurred or an alert was delivered. Use autocomplete and a session's field menu to confirm the local field values.

## Step 1 — Select the correct dataset

| Source | Available test content | What it can demonstrate |
| --- | --- | --- |
| Existing generated PCAPs | HTTP and DNS, documentation addresses | Baseline/candidate comparison, DNS-to-HTTP review and saved-packet search |
| [Controlled local live test](CONTROLLED_LIVE_TEST.md) | Three local HTTP requests, tagged `arkime-local-control` | Capture from loopback through storage and reconstruction; no DNS test |
| Approved mirror/TAP | Only protocols and directions actually observed | Broader analysis after collection, access and security prerequisites are complete |

The generated HTTP/DNS fixtures contain no TLS, SMB or RDP sessions. Zero matches for those hunts in these fixtures are expected; they do not validate coverage for the missing protocols.

## Step 2 — Check collection quality before hunting

Open **Stats** and review the node, recent time, received packets, packet queue, packet drops, overload drops, database drops, free space, CPU and memory. Confirm the Viewer can retrieve saved packets. For offline imports, the capture process may have exited normally; use its completion output and resulting sessions rather than expecting a continually updating live counter.

Record capture direction, selected interface, VLAN/mirror source and any gaps. A running service or a reachable port alone does not show that a particular network segment is visible. If packets are missing or only one direction is present, record that limitation before interpreting traffic.

## Step 3 — Establish comparable time windows

Use the Viewer's time picker to select the baseline period and a separate review period. Record the actual UTC boundaries. Compare periods of the same duration and similar business activity, while accounting for changes in volume, maintenance and asset role. Do not compare ten minutes of test traffic to a full day without adjusting your interpretation.

For the offline fixture, use its generation timestamps. For the local live test, use the times recorded by `date -u`. Start narrow enough to separate runs but wide enough to include session completion. Retain the filters, data source and time window with your notes.

## Step 4 — Build a baseline using the Viewer

On **Sessions**, use this starting expression for the offline fixture:

```text
ip.src == 192.0.2.20
```

**Query overview:** This selects sessions initiated by the fixture client when Arkime has observed the normal connection direction. Inspect the actual tuple if a flow begins midstream.

Use **SPIView** to review the values and counts for source IP, destination IP, destination port, protocols, HTTP host and DNS host. Use **SPIGraph** to see how a selected field varies across the chosen time window. Use **Connections** to examine the relationships between peers. Record approved services and owners; frequency alone does not make a destination authorized.

For the generated baseline, expect only `updates.example.test` in HTTP. The later fixture introduces `review.example.test`. Those are exercise assumptions, not a production allowlist.

## Step 5 — Investigate a hostname outside the baseline

For the offline case:

```text
ip.src == 192.0.2.20 && http.host == review.example.test
```

For the controlled live case:

```text
tags == arkime-local-control && http.host == review.example.test
```

**Query overview:** The first selects the synthetic client and candidate HTTP host; the second uses the live test's tag. Inspect source and destination, ports, time, URI, method, status and reconstructed response. In the offline fixture the candidate request is `192.0.2.20:51005 → 192.0.2.10:80` for `/downloads/review.txt`. In the local live test both addresses are loopback and the server port is `18080`.

Ask whether the hostname, alias, application and cleartext service are authorized. The same IP may host several names; an IP match alone does not establish which service was used.

## Step 6 — Review HTTP failures and unexpected paths

```text
protocols == http && http.statuscode >= 400
```

**Query overview:** This finds HTTP sessions with error response codes for review. Look at the actual status codes, requests, client role and time distribution. Multiple requests or responses may be represented in one session, so a session count is not always a request count.

The provided fixtures use successful `200` responses; expect no errors from a clean single-fixture run. In another authorized dataset, failures might come from a changed URL, expired authentication, a broken application or suspicious requests. Verify the owner explanation and exact requests before escalating.

## Step 7 — Investigate repeated DNS failures

```text
protocols == dns && dns.status == NXDOMAIN
```

**Query overview:** `NXDOMAIN` is a DNS response reporting that the requested name does not exist. Review the source clients, requested names, timing, counts and resolver. Use SPIView to identify clients and names that dominate the selected period, then compare against a similar baseline window.

The generated fixtures use valid A-record answers, so this hunt should not match them. Stale software configuration, search suffixes and typographical errors can also produce failures. An unusual number of failed names is a lead for investigation, not a diagnosis of malware.

## Step 8 — Review unusual DNS query types

```text
protocols == dns && dns.query.type == TXT
```

**Query overview:** This selects TXT queries decoded by Arkime. Review names, clients, response sizes, frequency and approved services. TXT is used legitimately, including email and domain-verification functions. A TXT query alone is not evidence of a tunnel.

The existing fixtures contain A-record lookups; they are not a positive test for this hunt. Obtain an approved representative sample before evaluating whether the pattern is unusual for a real asset.

## Step 9 — Identify legacy TLS candidates

```text
protocols == tls && (tls.version == SSLv3 || tls.version == TLSv1 || tls.version == TLSv1.1)
```

**Query overview:** This selects decoded sessions reporting the listed older TLS/SSL versions. Inspect the actual handshake, server/client roles, negotiated information and service owner. Encrypted sessions do not reveal application payload by default. Missing handshakes or asymmetric capture may prevent a version from being recorded.

The supplied HTTP fixtures cannot validate this hunt. On an approved dataset, document the observed protocol, affected service, operational constraints and the owner's plan for supported encryption. Do not claim an exploitable weakness solely from a banner or an incomplete negotiation.

## Step 10 — Review candidate SMB and RDP connections

For common SMB service ports:

```text
port.dst == 445 || port.dst == 139
```

For the common RDP service port:

```text
port.dst == 3389
```

**Query overview:** These select destination ports commonly associated with the services. Confirm the decoded protocol and asset roles; a port number alone does not identify the application, its security settings or a user's authentication result. Nonstandard ports and encrypted tunnels can also reduce coverage.

Compare the communicating hosts with approved administration and file-service patterns. To confirm process or sign-in activity, use separately collected endpoint logs with a matching time window. The synthetic HTTP/DNS fixture does not include these protocols.

## Step 11 — Review a client contacting many peers

Filter Sessions to the client being investigated. For the provided fixture this is:

```text
ip.src == 192.0.2.20
```

Open **Connections** with the same time and expression, then examine destination IP and destination-port relationships. Compare the number and role of peers with the client's baseline. Use SPIView to review the underlying values, then open individual sessions to validate the graph.

A software inventory agent, monitoring tool or administrative workstation can legitimately contact many peers. A fan-out pattern requires context; missing SYNs, NAT and merged views can also affect the apparent direction. Do not initiate a scan to reproduce it in this exercise.

## Step 12 — Review repeated connection timing

Select the client and destination found in a candidate, choose a consistent time window and examine the session timeline and SPIGraph. Look for repeated short sessions, changes in frequency, and whether the pattern aligns with maintenance or scheduled software.

A repeating pattern can come from health checks, updates or monitoring. Do not label it command-and-control solely because it repeats. Record the interval estimate, observed session count, supporting protocol details and alternative explanations. The small fixtures have intentionally scheduled timestamps and are not a realistic beaconing benchmark.

## Step 13 — Review unusual transfer volume

On Sessions and its timeline, compare **Bytes** and **Databytes**, including source and destination directions. Compare the same asset role and similar-duration windows; inspect individual sessions that account for a change. Link the bytes to observed peers and authorized file transfers, updates or backups.

These metrics describe captured network activity. They do not, by themselves, show which user initiated it, whether content was sensitive, or whether a transfer was unauthorized. Packet loss, retransmissions, encryption and session boundaries limit the conclusion. Choose any operational threshold from a representative baseline and document why it fits the service.

## Step 14 — Search saved packet content using Hunt

This is a bounded positive/negative test using the existing **offline HTTP fixtures**, not the different local-live marker. The Viewer must be able to read the managed PCAPs. Enable `cronQueries=true` on the one designated Viewer as described in [Step 31.1](IMPLEMENTATION_GUIDE.md#step-311--optionally-test-a-periodic-detection), and use an Arkime account allowed to run packet searches.

1. In **Sessions**, select the fixture time window and `ip.src == 192.0.2.20 && ip.dst == 192.0.2.10`. Confirm the small number of HTTP sessions before proceeding.
2. Open **Hunt**, then **Create a packet search job**.
3. Name it `lab-http-marker`, enter a description, and set the maximum packets examined per session to `100`, which is sufficient for these tiny fixtures.
4. Search for `LAB_SYNTHETIC_HTTP_ARTIFACT` using **case-sensitive ASCII** and **reassembled** packets. Search both source and destination directions. Leave notifiers unselected.
5. Submit the job and review its completed status, errors and matching sessions. For one clean import, expect the candidate HTTP session to match and the routine HTTP sessions not to match.
6. Open a matching session and inspect its response bytes. Record job status and packet availability. Missing or expired PCAPs, a failed job, or a truncated search is an incomplete test.

**Overview:** A session expression selects metadata. Hunt examines saved packet content within those selected sessions. A completed, verified match is stronger evidence than assuming that a host filter searched response bodies. The marker is inert exercise text and is not a general malware signature. For unknown files, follow approved handling and avoid execution.

## Step 15 — Test periodic review tagging

Use the existing [periodic-query procedure](IMPLEMENTATION_GUIDE.md#step-311--optionally-test-a-periodic-detection) with the verified host expression. It tags matches and lets you inspect last-run information and counts. Validate the candidate **and** routine controls, check failures, and disable the exercise query afterwards.

A periodic expression is a defined review rule. It does not learn a baseline automatically. Notification delivery needs its own configured destination and an observed test; a tag or match count is not confirmation that a message reached anyone.

## Step 16 — Correlate with other tools

Use the [worked Zeek/Suricata/Splunk case](../network-defense/OFFLINE_HTTP_WALKTHROUGH.md) on the same fixture files if you need a cross-tool exercise. Match UTC time, source/destination IPs, ports, transport and HTTP host/path. Use tool-specific IDs only within their documented scope. Verify Community ID generation and settings before using it; it does not make unrelated runs or DNS and HTTP the same flow.

The optional Splunk upload in that walkthrough uses the existing `lab` index and synthetic summaries. This Arkime deployment has no automatic Splunk ingestion. For real endpoint correlation, verify the source log, timestamp and field extraction before using a Splunk result as supporting evidence.

## Step 17 — Report and disposition the finding

Record the question, data source, collection limits, exact filters and UTC window, observed sessions, packet review, alternatives, owner validation and next action. Use the [sanitized validation template](../../evidence/sanitized/arkime-validation.md), and keep raw packets and identifying details in approved private storage.

An example conclusion for the fixture is: “The reviewed synthetic capture contains an HTTP download using a hostname outside the exercise baseline. The request and response were observed in the same session. The exercise validates this review workflow only; it does not establish compromise or complete network visibility.” Use this conclusion only after observing those results in your own test.

## References

- [Arkime Viewer Help at v6.9.1](https://github.com/arkime/arkime/blob/v6.9.1/viewer/vueapp/src/components/help/Help.vue): Session views, graphs, statistics and saved-packet Hunt controls.
- [Arkime v6.9.1 HTTP parser](https://github.com/arkime/arkime/blob/v6.9.1/capture/parsers/http.c): HTTP host, URI and response-code field definitions.
- [Arkime v6.9.1 DNS parser](https://github.com/arkime/arkime/blob/v6.9.1/capture/parsers/dns.c): DNS name, query-type and response-status field definitions.
- [Arkime v6.9.1 TLS parser](https://github.com/arkime/arkime/blob/v6.9.1/capture/parsers/tls.c): TLS version values and parsing behavior.
- [Arkime settings](https://arkime.com/settings): Configuration, periodic queries and capture options.
