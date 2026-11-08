# Arkime Network Analysis Lab — Start Here

Add Arkime to the existing threat-hunting project as an **optional, separate RHEL 10 sensor**. Arkime indexes network-session metadata in OpenSearch and keeps packet files on disk so an analyst can investigate traffic. It does not automatically forward events to Splunk.

| Order | Guide | Outcome to verify |
| --- | --- | --- |
| 1 | [38-step installation and deployment guide](docs/arkime/IMPLEMENTATION_GUIDE.md) | Matching verified packages, separate data storage, authenticated database, restricted Viewer and offline imports |
| 2 | [Worked HTTP anomaly investigation](docs/arkime/INVESTIGATION.md) | Routine and candidate sessions reviewed against the synthetic baseline |
| 3 | [Optional controlled live capture](docs/arkime/CONTROLLED_LIVE_TEST.md) | Three local HTTP transactions captured, stored and reconstructed without a VMware mirror |
| 4 | [Network baseline and anomaly playbook](docs/arkime/HUNTING_PLAYBOOK.md) | HTTP, DNS, TLS and service-port hunts; graphs, packet-content search and periodic review tagging |
| 5 | [Sanitized validation template](evidence/sanitized/arkime-validation.md) | Actual results, coverage, limitations and reviewer recorded after testing |

Each procedure includes commands or Viewer actions, a short explanation and expected observations. Use the broader protocol hunts only with approved traffic that contains those protocols; the supplied fixtures cover HTTP and DNS. The lab's demo database security is limited to synthetic data. Complete the documented security and capture prerequisites before collecting an external network.

For cross-tool comparison, use the [existing passive network defense guide](START_HERE_NETWORK_DEFENSE.md) and its [worked Zeek, Suricata and Splunk case](docs/network-defense/OFFLINE_HTTP_WALKTHROUGH.md) on the same fixtures.

**Status:** documentation and synthetic exercises only. Installation, service health, live network visibility and findings have not been validated on the home lab. No certification or production readiness is claimed.

The three existing VMs, their Splunk indexes and `/splunkdata` remain unchanged. The guide's fourth VM is optional. VMware NAT alone is not a network tap or mirror; live capture requires a separately authorized source of packets. Start with the offline exercise.
