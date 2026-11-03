---
applyTo: "apps/**/*.conf"
---
# Splunk-specific instructions

Use supported stanza names and precise `.conf` filenames. Keep server inputs separate from Windows Universal Forwarder inputs. SPL searches should include explicit indexes and practical time windows. Do not silently enable new data sources, replace existing index configurations, or widen role permissions. Explain any change to TLS, parser, role mappings, retention, or index routing. Test against the installed Splunk build using `btool` and an isolated lab before deployment.
