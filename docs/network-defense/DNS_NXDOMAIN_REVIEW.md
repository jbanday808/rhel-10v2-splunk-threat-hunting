# Repeated missing DNS names: a careful review

**Status:** proposed, read-only hunt using an approved private capture or Zeek `dns.log`. The repository's generated HTTP/DNS fixture has valid answers, so it is a **nonmatching control**, not a positive NXDOMAIN test. No live DNS feed into Splunk or completed investigation is claimed.

## Ask the question

An NXDOMAIN response means the requested name did not exist according to the responding DNS server. Ask: **“Why did this client ask for several missing names in this window, and is that normal for its role?”** A mistyped address, old configuration, search suffix, or offline application can create failures. A large count alone does not establish malware or DNS tunneling.

## Check the data before counting

1. Agree on the client, resolver, UTC window, and private evidence location. Confirm the sensor actually saw DNS **responses** from the relevant resolver. Query-only capture cannot establish an NXDOMAIN response.
2. In Wireshark, use `dns.flags.response == 1 && dns.flags.rcode == 3` to view NXDOMAIN responses in the approved PCAP. Verify the reply's client/resolver addresses, queried name, transaction ID, and time against its request. The numeric response code `3` represents NXDOMAIN.
3. If Zeek JSON logs were produced from the **same** capture, check the installed schema for `query`, `rcode_name`, `id.orig_h`, and `id.resp_h`. For a named private file, this read-only command lists candidate rows:

   ```bash
   jq -r 'select(.rcode_name == "NXDOMAIN") | [.ts, .["id.orig_h"], .["id.resp_h"], .query] | @tsv' /private/approved-run/dns.log
   ```

   **Command overview:** `jq` reads existing JSON lines and prints time, client, resolver, and name for NXDOMAIN events. Replace the example private path with the approved log path. **Expected testable result:** rows correspond to the reviewed response packets; if fields or times disagree, resolve parsing or capture coverage before hunting.
4. Group failures by client and a short, agreed time window. Count both responses and **distinct** names. Compare with a similar normal period for the same client and resolver; account for software updates, browser search suffixes, and maintenance.
5. Ask the endpoint or DNS owner what process was active and whether the names belong to an approved application. DNS alone may not identify the requesting process. Record missing endpoint evidence as a limit, not as proof of a threat.

| Synthetic comparison | Interpretation to test | Control |
| --- | --- | --- |
| One example client asks for four different nonexistent names in a minute | Needs owner review if unusual for that client | Check a comparable normal window and the endpoint application. |
| A second client repeats one misspelled printer name | Likely configuration or typo candidate | Confirm the printer setting; do not count repeats as four distinct destinations. |
| The repository's existing HTTP/DNS capture returns valid A answers | Nonmatching control | A zero-NXDOMAIN result is expected for **that fixture only**. |

The [Arkime playbook](../arkime/HUNTING_PLAYBOOK.md#step-7--investigate-repeated-dns-failures) offers a Viewer pivot when Arkime has an approved dataset. Its session count is not necessarily a DNS request count. The [rare DNS search](../../hunts/network-defense/02-rare-dns-queries.spl) uses a **proposed** `net_zeek` index; the core lab has only six indexes, so do not run it as if that feed were configured.

## Explain the result

Privately record the capture hash, resolver, client, UTC window, response and unique-name counts, baseline comparison, endpoint-owner explanation, and gaps in the [network validation worksheet](../../evidence/sanitized/network-defense-validation.md). A correct plain-language update is: “This computer asked for several names the DNS server could not find. We are checking whether an ordinary application or configuration caused them.” If the response side was not captured, call the outcome **inconclusive**.

Sources: [Zeek DNS log fields](https://docs.zeek.org/en/current/reference/logs/dns.html) and [Wireshark DNS filter fields](https://www.wireshark.org/docs/dfref/d/dns.html).
