# Optional sensor Splunk Universal Forwarder — NOT INSTALLED

This is source template content for the proposed RHEL-SENSOR01 VM, NOT a running service.

- [local/inputs.conf](local/inputs.conf) requires authorized sanitized newline JSON files at private directories.
- No outputs.conf, secrets, private TLS keys, bind passwords, deployment tokens or installers are provided.
- Acquire Splunk UF from the verified vendor, confirm RHEL 10 support and review server-CA/hostname verification to splunk01.lab.test:9997.
- The current Splunk firewall may only allow WINHUNT01: obtain approved explicit source allowance for 172.25.250.40/32 before trying to send.
- Review parsing-tier timestamp handling and retention for old offline PCAP events.
- Do not upload raw PCAP to Splunk or GitHub; do not replace existing Windows or IdM services.

See [Splunk Integration](../../docs/network-defense/SPLUNK_INTEGRATION.md).
