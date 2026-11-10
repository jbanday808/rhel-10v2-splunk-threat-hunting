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
| Arkime downloads (optional RHEL 10.2 sensor) | https://arkime.com/downloads |
| Arkime 6.9.1 EL10 RPM and SHA-256 (version used in the optional guide) | https://github.com/arkime/arkime/releases/tag/v6.9.1 |
| OpenSearch RPM and signature (Arkime session database) | https://opensearch.org/artifacts/by-version/ |
| Git for Windows | https://git-scm.com/install/windows |
| GitHub CLI | https://cli.github.com/ |

For the optional Arkime sensor, choose a package matching the VM's operating system and CPU architecture. Verify the Arkime RPM against the digest on its release page and the OpenSearch RPM against its vendor signature before installation. The [Arkime installation guide](../arkime/IMPLEMENTATION_GUIDE.md) documents the versioned downloads, checks, and setup; confirm compatible versions before use.

Generate certificates and private keys on the VMs using Step 15 and the LDAP steps. Transfer only the verified public CA to the Windows endpoint. Configure Azure and GitHub IDs interactively using the OIDC appendix. Keep vendor installers, secrets, and raw evidence outside GitHub.
