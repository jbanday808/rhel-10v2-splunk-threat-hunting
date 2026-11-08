# Cobalt Strike–Associated Pipe Hunt — Validation Template

**Status: not performed in the user's lab.** Keep the real test record and source events in approved private storage. Publish only reviewed, sanitized outcomes.

| Check | Planned expected result | Actual / date / reviewer |
| --- | --- | --- |
| Scope | Owned WINHUNT01, exercise owner and UTC window documented | Not tested |
| Source | Pinned Atomic YAML hash and selected GUID reviewed | Not tested |
| Telemetry | Approved Sysmon pipe-rule merge, rollback file and forwarding verified | Not tested |
| SPL self-test | All 12 synthetic cases pass in Splunk Web | Not tested |
| Negative control | Event 17 for SIEMLabControl_20261107 is locally present and indexed, but absent from the candidate hunt | Not tested |
| Positive control | Event 17 for postex_a1b2c3d4 is locally present, indexed and returned by the hunt | Not tested |
| Process context | Host/ProcessGuid pivot reviewed, including missing Event 1 or field gaps | Not tested |
| Event 18 | Not expected from the selected server-only Atomic test; evaluated separately if observed | Not tested |
| Cleanup | Atomic returns and disposes its pipe; reviewed Sysmon rollback applied or monitoring change retained with approval | Not tested |
| Disposition | Simulation recorded; any actual PenTest activity independently validated | Not tested |

A successful Atomic exit, local event, indexed event, SPL match and alert delivery are separate outcomes. This exercise does not run a Cobalt Strike Beacon or prove command-and-control, lateral movement, injection or full Cobalt Strike detection coverage.
