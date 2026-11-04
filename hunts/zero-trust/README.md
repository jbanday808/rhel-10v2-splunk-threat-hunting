# Zero Trust Monitoring SPL — Read-only Lab Examples

These searches provide **visibility evidence**, not DoD Zero Trust compliance. They assume the documented six indexes and default or compatible Splunk field extractions. Update to the actual installed Splunk/add-on versions and log shapes. Every search must be run against actual authorized test data and assessed before claiming detection success.

| File | Purpose |
| --- | --- |
| [01-siem-data-coverage.spl](01-siem-data-coverage.spl) | Event counts and last seen by source |
| [02-windows-failed-logons.spl](02-windows-failed-logons.spl) | Windows failed authentication activity |
| [03-powershell-activity.spl](03-powershell-activity.spl) | PowerShell operational logs, source counts |
| [04-splunk-internal-errors.spl](04-splunk-internal-errors.spl) | Splunk internal warning/error activity |

**Important:** These are exploratory queries, not approved alerts and not autonomous response workflows. Inspect real field names before tuning. Never commit raw events or credential-bearing logs.
