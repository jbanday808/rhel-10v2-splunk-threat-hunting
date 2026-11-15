# Accept Windows sign-in success and failure records

**Status:** proposed check for the owned WINHUNT01 lab VM. Do not create extra failed attempts to satisfy a test: even one attempt can lock an account if earlier failures are near the policy threshold. No successful collection or intrusion is claimed here.

## Question and prerequisites

Can an analyst distinguish an **authorized successful sign-in** from one **intentional failed sign-in** in the Windows Security log and the `win_security` index? The [forwarder input](../../../apps/LAB_UF_WINDOWS/local/inputs.conf) maps the Security channel to `index=win_security`. [Step 23](../../steps/23-enable-windows-auditing-and-powershell-logging.md) describes audit settings; [Step 27](../../steps/27-verify-event-collection.md) checks collection. The pending forwarding/TLS investigation in [Step 45](../../steps/45-create-and-test-an-alert.md) must not be treated as resolved by this plan.

Only use the existing disposable-account exercise in [Step 28](../../steps/28-generate-harmless-hunting-activity.md): Step 28.7 tests the correct password, and Steps 28.14–28.15 review lockout policy before **one** intentionally incorrect password. Record the UTC times privately. If either part was skipped or failed, say so; do not repeat a login or weaken account policy for the report.

## Check the original events first

On WINHUNT01, inspect the local Security log for Event ID **4624** near the approved correct-password test and Event ID **4625** near the approved failed attempt. Then search Splunk with the matching window:

```spl
index=win_security host=WINHUNT01 earliest=-30m latest=now
| eval event_id=tonumber(coalesce(EventCode,EventID))
| where in(event_id,4624,4625)
| table _time _indextime host source sourcetype event_id TargetUserName TargetDomainName LogonType IpAddress WorkstationName Status SubStatus _raw
| sort 0 _time
```

**Search overview:** this stays in the configured Security index, displays both outcomes in event-time order, and keeps the original record available for private interpretation. Replace the relative window with the approved UTC bounds when needed. If the ID or named fields are only present in XML, record a field-extraction gap instead of calling the event absent. Keep account names, addresses, and raw events out of GitHub.

| Acceptance item | What to check |
| --- | --- |
| Local and indexed copies | Each permitted test has a local Security event and a matching searchable copy. |
| Correct identity | Compare `TargetUserName` **and** `TargetDomainName` with the disposable local account. `SubjectUserName` describes a different role in these events. |
| Outcome and context | 4624 means a successful logon event; 4625 records a failure. Read `LogonType`, failure status, and original XML before explaining the session. |
| Source limitation | `IpAddress` may be absent or local for a same-machine test. Do not invent a remote source or infer that a later success came from the earlier failed attempt. |

The correct-password attempt is a **benign positive control** for success auditing, and the single wrong-password attempt is a **benign positive control** for failure auditing. For a **nonmatching control**, compare an actually collected event for a different target account or host; it must not be joined to this disposable account merely because its timestamp is nearby. If that event is unavailable, mark the nonmatching control pending. The [failure-before-success hunt](../../../hunts/mitre-attack/02-failures-before-success.spl) requires additional source, account, and ordering review; these two safe tests do not validate that detection.

## Record the outcome

Keep the local and indexed event references, UTC test window, account-owner confirmation, LogonType, any missing source fields, and collection delay in private evidence. Mark each event family separately as **pass**, **pending**, or **inconclusive**. For a nontechnical update: “The lab can show a test sign-in and a test rejection if both records arrive. Those records do not mean the account was attacked.”

Use the [hunt report template](../templates/threat-hunt-report.md) for follow-up. Microsoft documents the different fields and meanings of [4624](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624) and [4625](https://learn.microsoft.com/windows/security/threat-protection/auditing/event-4625).
