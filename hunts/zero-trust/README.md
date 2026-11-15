# Zero Trust Monitoring SPL — Read-only Lab Examples

These searches provide **visibility evidence**, not DoD Zero Trust compliance. They assume the documented six indexes and default or compatible Splunk field extractions. Update to the actual installed Splunk/add-on versions and log shapes. Every search must be run against actual authorized test data and assessed before claiming detection success.

| File | Purpose |
| --- | --- |
| [01-siem-data-coverage.spl](01-siem-data-coverage.spl) | Expected lab index/host pairs, including missing sources; [synthetic control](fixtures/01-expected-source-gaps.md) |
| [02-windows-failed-logons.spl](02-windows-failed-logons.spl) | Failed sign-ins by domain, target, source, and logon type; [synthetic control](fixtures/02-failed-logon-identity-scope.md) |
| [03-powershell-activity.spl](03-powershell-activity.spl) | Separate module 4103 and script-block 4104 coverage; [synthetic control](fixtures/03-powershell-event-types.md) |
| [04-splunk-internal-errors.spl](04-splunk-internal-errors.spl) | Splunk internal warning/error activity |

**Important:** These are exploratory queries, not approved alerts and not autonomous response workflows. Inspect real field names before tuning. Never commit raw events or credential-bearing logs.
