**Step 4 — Download and verify the software**

Download:

1. RHEL 10.2 x86_64 ISO.
2. Windows 11 x64 ISO.
3. Splunk Enterprise Linux x64 `.tgz`.
4. Compatible Windows x64 Universal Forwarder `.msi`.
5. Splunk Add-on for Microsoft Windows.
6. Splunk Add-on for Sysmon.
7. For the optional analysis VM, Kali Linux installer ISO or official VMware image (choose one).

Official pages:

- [Red Hat Enterprise Linux](https://developers.redhat.com/products/rhel/download)
- [Windows 11](https://www.microsoft.com/software-download/windows11)
- [Splunk Enterprise](https://www.splunk.com/en_us/download/splunk-enterprise.html)
- [Universal Forwarder](https://www.splunk.com/en_us/download/universal-forwarder.html)
- [Microsoft Windows add-on](https://splunkbase.splunk.com/app/742?utm_source=chatgpt.com)
- [Sysmon add-on](https://splunkbase.splunk.com/app/5709?utm_source=chatgpt.com)
- [Kali Linux official downloads](https://www.kali.org/get-kali/)

Choose add-on releases that explicitly support your selected Splunk version. [splunkbase.splunk.com](https://splunkbase.splunk.com/app/742?utm_source=chatgpt.com)

On your **physical Windows computer**, check downloaded files with PowerShell:

```
$Download = Read-Host 'Enter the full path to the downloaded file'

Get-FileHash -LiteralPath $Download -Algorithm SHA256
```

**Command overview:**

- `Read-Host` asks for the file location.
- `Get-FileHash` calculates its fingerprint.
- `SHA256` selects the fingerprint method.

Compare the complete result with the vendor’s published checksum.

For Kali, follow the official download page's integrity and authenticity instructions for the **specific image** you chose. Keep its exact release and checksum in your private installation notes. The [Kali workstation guide](../network-defense/KALI_DEPLOYMENT.md) covers the optional tool installation and offline validation; these tools do not change the six existing Splunk indexes.

---
