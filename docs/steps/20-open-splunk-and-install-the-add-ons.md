**Step 20 — Open Splunk and install the add-ons**

On the **physical Windows host**, use administrator PowerShell:

```
New-Item -ItemType Directory -Path C:\SIEMLab\Public -Force

scp.exe labadmin@172.25.250.10:/home/labadmin/siem-public/ca.cer C:\SIEMLab\Public\

Get-FileHash C:\SIEMLab\Public\ca.cer -Algorithm SHA256
```

Compare the hash with RHEL.

Import the public CA:

```
Import-Certificate `
  -FilePath C:\SIEMLab\Public\ca.cer `
  -CertStoreLocation Cert:\CurrentUser\Root
```

Update the server name:

```
$HostsFile = "$env:SystemRoot\System32\drivers\etc\hosts"

$HostsLines = Get-Content $HostsFile |
    Where-Object { $_ -notmatch 'splunk01\.lab\.test' }

$HostsLines = @($HostsLines) +
    '172.25.250.10 splunk01.lab.test splunk01'

Set-Content -Path $HostsFile -Value $HostsLines -Encoding Ascii

Start-Process 'https://splunk01.lab.test:8000'
```

**Command overview:**

- `Import-Certificate` trusts the verified public CA.
- `Get-Content` reads the hosts file.
- `Where-Object` removes the previous lab-name entry.
- `Set-Content` writes the updated entry.
- `Start-Process` opens Splunk.

In Splunk:

1. Sign in as `admin`.
2. Open **Apps → Manage Apps → Install app from file**.
3. Install the Microsoft Windows add-on.
4. Install the Sysmon add-on.
5. Restart when requested.
6. Open **Settings → Licensing**.
7. Record the allowance and expiry.

Splunk Enterprise Security is a separate product. This core lab uses Enterprise searches, dashboards, and alerts.

---
