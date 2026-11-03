# Troubleshooting guide

| Symptom | First checks |
| --- | --- |
| Cannot reach VM | VMware VMnet8, IP, gateway and firewall zone |
| RHEL updates fail | DNS resolution, NAT, Red Hat subscription/repository |
| Splunk will not start | `/splunkdata` mount, free space, ownership, certs, `journalctl`, `btool` |
| Forwarded Windows data absent | Windows event channels, UF service, TLS CA and Splunk receiver TCP 9997 |
| Sysmon fields empty | Compatible Sysmon add-on, XML sourcetype, field mapping |
| Custom lab fields missing | `props.conf`, `REPORT-lab-fields`, `transforms.conf` and sample format |
| IdM login fails | IdM DNS, TCP 636, trusted CA, LDAP group mapping, local admin recovery |
| Indexed data disappears | Age/size retention and event-log rollover |

Keep SELinux enforcing. Do **not** reformat a data disk to repair Splunk startup. Do **not** publish private error logs. Verify results directly on lab systems.
