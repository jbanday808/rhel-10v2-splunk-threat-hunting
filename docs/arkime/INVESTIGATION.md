# Worked Arkime Investigation — An Unexpected HTTP Host

Use this case after completing the [Arkime installation and offline import](IMPLEMENTATION_GUIDE.md#phase-4--generate-and-import-safe-test-traffic). All hostnames, packet contents and addresses are synthetic. This is an analysis exercise; it does not establish a real intrusion or live network visibility.

## The question

A client normally requests status information from `updates.example.test`. In a later test window, it requests a file from `review.example.test` using the same destination address. Is the second hostname expected, and what should an analyst ask the service owner?

| Fixture | Expected HTTP requests | Expected observation |
| --- | ---: | --- |
| `baseline.pcap` | 3 | All requests use `updates.example.test` |
| `investigation.pcap` | 2 | One request uses `updates.example.test`; one uses `review.example.test` |

The generator also writes DNS queries and responses. Both hosts resolve to `192.0.2.10`, so the IP address alone cannot distinguish the candidate from routine traffic. The synthetic client is `192.0.2.20`; the resolver is `192.0.2.30`. These are documentation addresses, not the home lab's actual IPs.

## Step 1 — Record the evidence boundary

Record the generation time, fixture hashes, Arkime version, sensor hostname and UTC investigation window in private notes. Confirm both imports finished without errors and that the Viewer is connected through the SSH tunnel. Set the Viewer time picker wide enough to include the fixture timestamps, which are generated several minutes before the command runs. If you ran the generator again, use the latest run's time window; multiple imports can add duplicate sessions.

## Step 2 — Find the HTTP sessions

In Arkime **Sessions**, enter:

```text
ip.src == 192.0.2.20 && ip.dst == 192.0.2.10
```

**Query overview:** `ip.src` filters the client, `ip.dst` filters the server, and `&&` requires both. Open the matching rows. Based on the generated input, expect three baseline and two investigation HTTP sessions if both captures were imported once and the window covers them. Record actual results instead of assuming the count. DNS traffic is a different flow to `192.0.2.30`.

If the Viewer does not return a session, first clear the expression, widen the time range, inspect the import output and verify database health. Direction and field names can differ in other captures; use the field autocomplete and inspect the actual session.

## Step 3 — Compare routine and candidate hosts

Search for the routine host:

```text
http.host == updates.example.test
```

Then search for the candidate host:

```text
http.host == review.example.test
```

**Query overview:** `http.host` selects the HTTP Host header decoded by Arkime. The candidate host is outside the fixture's deliberately defined baseline; it is not inherently malicious. If the parser or Viewer uses another field name in your version, inspect the session and use its field menu. Check the selected period and confirm that the host and client are visible.

Open the candidate row and record the observed source and destination addresses and ports, time, protocol, HTTP method, host, URI and response status. For the provided fixture, the expected TCP tuple is `192.0.2.20:51005 → 192.0.2.10:80`; the request is `GET /downloads/review.txt`, and the response is HTTP `200`. The candidate response body includes the inert marker `LAB_SYNTHETIC_HTTP_ARTIFACT`.

## Step 4 — Review the reconstructed session

Use the session's packet or data view to inspect the request and response. Confirm that the host header, file path and response belong to the **same** TCP session. Avoid treating an export or screenshot as safe to publish simply because this fixture is synthetic; confirm exactly what it contains first. Do not execute downloaded or unknown files.

**Interpretation:** HTTP is cleartext in this fixture, so the host, path and body are visible. HTTPS generally protects application content; do not claim that Arkime can see encrypted payloads without separately authorized decryption and valid keys.

## Step 5 — Check the associated DNS exchange

Search:

```text
dns.host == review.example.test
```

**Query overview:** `dns.host` selects a DNS hostname decoded by Arkime. Examine the query and response to verify that the test client asked the test resolver and received `192.0.2.10`. DNS and HTTP use separate network flows: correlate them using the name, time, client and answer, not an assumption that their session identifiers are the same.

## Step 6 — Correlate with Zeek, Suricata and Splunk

Run the repository's [offline HTTP walkthrough](../network-defense/OFFLINE_HTTP_WALKTHROUGH.md) on the **same fixture files and same time window** if you want Zeek and Suricata output. Its optional, one-time Splunk example uses the existing `lab` index and a sanitized synthetic JSON summary; it does not ingest Arkime automatically. Follow that walkthrough's private-file and upload instructions and record the actual `run_id` before searching.

For each tool, compare the observed UTC time, client and server IPs, ports, transport protocol and HTTP hostname. The Zeek and Suricata examples can calculate Community ID for supported flows with matching settings; Arkime's own session identifiers are different and must not be assumed equal. Account for different timestamp precision, orientation, NAT and missing packets. DNS and HTTP are different flows.

If the walkthrough's synthetic JSON has actually been uploaded, use its documented SPL and the selected run ID. A Splunk result does not prove that Arkime forwarded anything. If there is no upload, keep the correlation in your private notes instead of expecting a Splunk search result.

## Step 7 — Document the finding

Use the [sanitized validation template](../../evidence/sanitized/arkime-validation.md) and separate observation from interpretation:

- **Observed:** The fixture contains a cleartext HTTP request for `/downloads/review.txt` using a hostname outside the fixture baseline, followed by a `200` response.
- **Assessment:** This is a planned synthetic outlier. Its appearance validates the investigation workflow only if you actually observed it in your run.
- **Questions:** Is the hostname authorized? Is the alias expected? Should the service redirect clients to HTTPS? Did any other authorized systems use it during the review window?
- **Limitations:** Two small captures are not a representative production baseline. The exercise does not prove root cause, compromise, complete coverage or live capture.
- **Next step:** Ask the service owner to validate the hostname and encryption policy; document ownership, disposition, follow-up and any approved remediation.

## Additional hunt ideas

After a representative baseline is established and collection is authorized, use Arkime's fields and time picker to investigate:

| Hypothesis | What to compare | What could explain it |
| --- | --- | --- |
| New destination or DNS name | Asset role, destination, frequency and time of day | Deployment, software update, DNS change, or a finding needing review |
| Unexpected protocol or port | Protocol, endpoint role, connection timing and known services | Administrative activity, approved testing, misconfiguration, or suspicious use |
| Repeated short connections | Timing, destination, session duration and bytes | Scheduled software, health checks, monitoring, or activity needing further review |
| Unusual data transfer | Bytes sent and received, destination, peer role and maintenance window | Backups, updates, file transfer, or possible unauthorized transfer |

These are investigation hypotheses, not universal signatures or thresholds. Validate visibility, loss, context and the service owner's explanation before drawing a conclusion. Follow your incident-response process when evidence warrants escalation.

Continue with the [17-step anomaly analysis playbook](HUNTING_PLAYBOOK.md) for concrete protocol queries, baseline comparisons, graphs and saved-packet Hunt instructions. To verify a live interface with generated traffic first, use the [bounded local HTTP test](CONTROLLED_LIVE_TEST.md).
