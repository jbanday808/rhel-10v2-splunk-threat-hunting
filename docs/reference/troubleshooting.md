# Troubleshooting guide

| Symptom | First checks |
| --- | --- |
| Cannot reach VM | VMware VMnet8, IP, gateway and firewall zone |
| RHEL updates fail | DNS resolution, NAT, Red Hat subscription/repository |
| Splunk will not start | `/splunkdata` mount, free space, ownership, certs, `journalctl`, `btool` |
| Forwarded Windows data absent or `wrong version number` on TCP 9997 | [Forwarder TLS and KV service troubleshooting](../troubleshooting/splunk-forwarder-tls-and-kv-service.md): check active output settings, CA, fresh logs and indexed events |
| KV service connection refused or startup warnings | [Review KV service status and startup messages](../troubleshooting/splunk-forwarder-tls-and-kv-service.md#5-investigate-the-separate-kv-service-and-startup-warnings) separately from forwarding TLS |
| `Start-Process` is not recognized or a lab credential prompt is confusing | [PowerShell, Command Prompt, and lab credentials](../troubleshooting/windows-powershell-cmd-credentials.md): check the shell, session variable, account and new window |
| Sysmon fields empty | Compatible Sysmon add-on, XML sourcetype, field mapping |
| Custom lab fields missing | `props.conf`, `REPORT-lab-fields`, `transforms.conf` and sample format |
| IdM login fails | IdM DNS, TCP 636, trusted CA, LDAP group mapping, local admin recovery |
| Indexed data disappears | Age/size retention and event-log rollover |

Keep SELinux enforcing. Do **not** reformat a data disk to repair Splunk startup. Do **not** publish private error logs. Verify results directly on lab systems.
