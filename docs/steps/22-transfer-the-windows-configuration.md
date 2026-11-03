**Step 22 — Transfer the Windows configuration**

On **RHEL**:

```
cd "$HOME/rhel-splunk-threat-hunting"

tar -czf "$HOME/endpoint-config.tgz" \
  apps/LAB_UF_WINDOWS \
  sysmon
```

**Command overview:** `tar -czf` packages the forwarding settings and Sysmon rules.

Inside the **Windows VM**:

```
New-Item -ItemType Directory -Force -Path `
  C:\SIEMLab\Downloads, `
  C:\SIEMLab\Source, `
  C:\SIEMLab\Tools, `
  C:\SIEMLab\Public, `
  C:\SIEMLab\Evidence, `
  C:\SIEMLab\TestFiles
```

Check the SSH client:

```
Get-Command scp.exe
```

If missing:

```
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
```

Transfer and extract:

```
scp.exe labadmin@172.25.250.10:/home/labadmin/endpoint-config.tgz C:\SIEMLab\Downloads\

tar.exe -xzf C:\SIEMLab\Downloads\endpoint-config.tgz -C C:\SIEMLab\Source

scp.exe labadmin@172.25.250.10:/home/labadmin/siem-public/ca.pem C:\SIEMLab\Public\

scp.exe labadmin@172.25.250.10:/home/labadmin/siem-public/ca.cer C:\SIEMLab\Public\

Get-FileHash C:\SIEMLab\Public\ca.pem,C:\SIEMLab\Public\ca.cer -Algorithm SHA256
```

Compare certificate hashes with RHEL.

Update the server name:

```
$HostsFile = "$env:SystemRoot\System32\drivers\etc\hosts"

$HostsLines = Get-Content $HostsFile |
    Where-Object { $_ -notmatch 'splunk01\.lab\.test' }

$HostsLines = @($HostsLines) +
    '172.25.250.10 splunk01.lab.test splunk01'

Set-Content -Path $HostsFile -Value $HostsLines -Encoding Ascii
```

**Command overview:**

- `New-Item` creates folders.
- `scp` copies files securely.
- `tar.exe -xzf` extracts them.
- `Get-FileHash` checks transferred certificates.
- The hosts-file commands update local name resolution.

---
