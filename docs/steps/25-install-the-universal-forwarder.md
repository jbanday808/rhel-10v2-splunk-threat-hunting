**Step 25 — Install the Universal Forwarder**

Inside the **Windows VM**, download the compatible MSI:

```
$UfMsi = Read-Host 'Full path to the Universal Forwarder MSI'

Get-FileHash -LiteralPath $UfMsi -Algorithm SHA256
```

After checksum verification:

```
Start-Process msiexec.exe `
  -ArgumentList "/i `"$UfMsi`"" `
  -Wait
```

In the wizard:

1. Select **Splunk Enterprise**.
2. Keep `C:\Program Files\SplunkUniversalForwarder`.
3. Use `NT SERVICE\SplunkForwarder`.
4. Create the forwarder administrator credentials.
5. Leave deployment-server and receiving-indexer fields blank.
6. Leave event collection unchecked because your app defines it.
7. Complete installation.

Splunk documents the virtual account as its least-privileged Windows forwarder account. [help.splunk.com](https://help.splunk.com/en/splunk-enterprise/forward-and-process-data/universal-forwarder-manual/10.6/install-the-universal-forwarder/install-a-windows-universal-forwarder?utm_source=chatgpt.com)

---
