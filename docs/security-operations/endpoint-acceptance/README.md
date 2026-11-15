# Windows endpoint telemetry acceptance

These are small, read-only checks for the owned WINHUNT01 → Splunk lab path. The source files and harmless activities are examples; each result remains **pending** until its local event and indexed copy are observed. Keep real event details and screenshots in approved private storage.

| Check | What it answers |
| --- | --- |
| [Sysmon process creation](01-sysmon-process-create.md) | Can the analyst explain a new process using its original event and key fields? |

Start with [Step 27: verify event collection](../../steps/27-verify-event-collection.md). The [Windows forwarder input](../../../apps/LAB_UF_WINDOWS/local/inputs.conf) uses the existing `win_security`, `win_system`, `powershell`, and `sysmon` indexes; these cases do not add an index or claim that the open forwarding/TLS issue is resolved.
