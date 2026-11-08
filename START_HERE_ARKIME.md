# Arkime Network Analysis Lab — Start Here

Add Arkime to the existing threat-hunting project as an **optional, separate RHEL 10 sensor**. Arkime indexes network-session metadata in OpenSearch and keeps packet files on disk so an analyst can investigate traffic. It does not automatically forward events to Splunk.

1. Read the [complete installation and deployment guide](docs/arkime/IMPLEMENTATION_GUIDE.md). It starts with a new, isolated VM, verified packages, local-only access and synthetic packet files.
2. Follow the [worked anomaly investigation](docs/arkime/INVESTIGATION.md) to compare the baseline and candidate captures, inspect the HTTP session and correlate matching evidence.
3. Record actual outcomes in the [sanitized validation template](evidence/sanitized/arkime-validation.md). Do not publish packets, credentials or real network details.
4. Review the [existing passive network defense guide](START_HERE_NETWORK_DEFENSE.md) and its [worked Zeek, Suricata and Splunk case](docs/network-defense/OFFLINE_HTTP_WALKTHROUGH.md).

**Status:** documentation and synthetic exercises only. Installation, service health, live network visibility and findings have not been validated on the home lab. No certification or production readiness is claimed.

The three existing VMs, their Splunk indexes and `/splunkdata` remain unchanged. The guide's fourth VM is optional. VMware NAT alone is not a network tap or mirror; live capture requires a separately authorized source of packets. Start with the offline exercise.
