# Splunk — Cobalt Strike–Associated Named-Pipe Hunt

Use the [complete Atomic Red Team validation guide](../../docs/splunk/COBALT_STRIKE_ATOMIC_VALIDATION.md) before running these optional searches. They use the existing `sysmon` index and `WINHUNT01` host, with no ES macros or new indexes. Paste one file into Splunk Web at a time.

| Search | Question | Expected check |
| --- | --- | --- |
| [00 — Telemetry health](00-pipe-telemetry-health.spl) | Are the relevant process and pipe events searchable, with pipe names extracted? | Distinguish missing events, missing fields and a hunt returning no matches. |
| [01 — Pipe candidates](01-default-pipe-candidates.spl) | Does a created/connected pipe match one of the selected default-style name patterns? | The lab `postex_a1b2c3d4` control should match; `SIEMLabControl_20261107` should be collected but not match. |
| [02 — Process context](02-process-context.spl) | Which process created or connected to a matching pipe? | Correlate on host and ProcessGuid; review any available process-creation event, image, parent and command line. |
| [03 — Synthetic pattern check](03-synthetic-pattern-self-test.spl) | Do the normalization and pattern expressions behave as expected in the local Splunk engine? | Twelve generated rows, all `PASS`; this does not test real telemetry. |

**Status:** candidate content. Windows execution, forwarding, SPL engine execution and detection coverage remain unvalidated in the home lab. The included Python unit tests exercise pattern boundaries; they are not Splunk integration tests.

The main searches include `earliest=-24h latest=now`, overriding the time picker's corresponding bounds. Change those modifiers deliberately for an older test. If `host` is different in the actual events, review and replace the host filter before searching. The queries accept `EventCode` or `EventID` and the documented pipe/process field aliases; validate field extraction first.

The normalization splits a pipe path at a backslash (`urldecode("%5C")`), selects the final component and converts it to lowercase. The pattern is anchored to the whole component and deliberately covers only hexadecimal `msagent_`, `postex_`, `postex_ssh_` suffixes and a decimal `MSSE-...-server` form. Other names and profile variants are outside scope. It is a review signal, not reliable product attribution.

A matching pipe can come from benign software or a simulation. Custom profiles can use different names and evade this small pattern set. The provided Sysmon fragment is similarly narrow; it is not full named-pipe visibility. Expand collection and hypotheses only after capacity, privacy and operational review.

The process-context search uses `eventstats`, whose memory limits can affect large result sets. A missing ProcessGuid excludes a row from that correlation; the base candidate search still shows it. Context may include other pipes used by the same process; it is not a separate classification of every pipe. An absent Event 1 may reflect an older process start, a short search window, collection gaps or missing fields. Do not join unrelated activity solely by PID.

For a penetration test, validate approved host, time, operator and actual indicators through the exercise owner. No PenTest team logs or indicators were supplied for this addition. Do not automatically label every hit as an authorized team or suppress a whole host/user.
