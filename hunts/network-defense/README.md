# Network Defense — Splunk SPL Exercises (Unvalidated)

Requires actual network indexes, tested JSON ingestion and appropriate RBAC. Offline synthetic PCAPs have a fixed historical timestamp; use `earliest=0` to include test events once indexed with original event time.

- [01-baseline-service-matrix.spl](01-baseline-service-matrix.spl): Zeek service counts.
- [02-rare-dns-queries.spl](02-rare-dns-queries.spl): Rare observed DNS queries.
- [03-suricata-alert-triage.spl](03-suricata-alert-triage.spl): IDS alert reviews.
- [04-network-data-coverage.spl](04-network-data-coverage.spl): Last observed source timestamps.

These are query drafts; no alert is deployed or proven until tested against real authorized index data.
