# Software and generated files

Download and verify vendor software before installing it. Record exact versions in `versions.md`.

| Component | Official source |
| --- | --- |
| RHEL 10.2 ISO and packages | https://developers.redhat.com/products/rhel/download |
| Windows 11 ISO | https://www.microsoft.com/software-download/windows11 |
| Splunk Enterprise | https://www.splunk.com/en_us/downloads.html |
| Universal Forwarder | https://www.splunk.com/en_us/download/universal-forwarder.html |
| Windows and Sysmon add-ons | Use the official Splunkbase links in the full guide |
| NGINX add-on | https://help.splunk.com/en/supported-add-ons/splunk-supported-add-ons/nginx |
| Sysmon | https://learn.microsoft.com/sysinternals/downloads/sysmon |
| Git for Windows | https://git-scm.com/install/windows |
| GitHub CLI | https://cli.github.com/ |

Generate certificates and private keys on the VMs using Step 15 and the LDAP steps. Transfer only the verified public CA to the Windows endpoint. Configure Azure and GitHub IDs interactively using the OIDC appendix. Keep vendor installers, secrets, and raw evidence outside GitHub.
