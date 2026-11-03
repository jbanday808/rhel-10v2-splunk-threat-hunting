**Step 26 — Deploy the forwarder configuration**

Inside the **Windows VM**:

```
$UfHome = 'C:\Program Files\SplunkUniversalForwarder'

Stop-Service SplunkForwarder

New-Item `
  -ItemType Directory `
  -Path "$UfHome\etc\auth\lab" `
  -Force | Out-Null

Copy-Item `
  -LiteralPath C:\SIEMLab\Public\ca.pem `
  -Destination "$UfHome\etc\auth\lab\ca.pem" `
  -Force

Copy-Item `
  -Path C:\SIEMLab\Source\apps\LAB_UF_WINDOWS `
  -Destination "$UfHome\etc\apps" `
  -Recurse `
  -Force
```

Set public-CA permissions:

```
icacls.exe "$UfHome\etc\auth\lab" /inheritance:r /grant:r `
  '*S-1-5-18:(OI)(CI)F' `
  '*S-1-5-32-544:(OI)(CI)F' `
  'NT SERVICE\SplunkForwarder:(OI)(CI)R'
```

Confirm the service account:

```
Get-CimInstance Win32_Service `
  -Filter "Name='SplunkForwarder'" |
  Select-Object Name,StartName
```

Add Event Log Readers membership if needed:

```
$Readers = Get-LocalGroup -SID 'S-1-5-32-573'

$ServiceSid = (
    [System.Security.Principal.NTAccount]'NT SERVICE\SplunkForwarder'
).Translate([System.Security.Principal.SecurityIdentifier])

$AlreadyMember = Get-LocalGroupMember -Group $Readers |
    Where-Object { $_.SID -eq $ServiceSid }

if (!$AlreadyMember) {
    Add-LocalGroupMember `
      -Group $Readers `
      -Member 'NT SERVICE\SplunkForwarder'
}
```

Check and start:

```
& "$UfHome\bin\splunk.exe" btool check

& "$UfHome\bin\splunk.exe" btool inputs list --debug

& "$UfHome\bin\splunk.exe" btool outputs list --debug

Start-Service SplunkForwarder

Test-NetConnection splunk01.lab.test -Port 9997

Get-Content "$UfHome\var\log\splunk\splunkd.log" -Tail 50
```

**Command overview:**

| Command                | Explanation                             |
| ---------------------- | --------------------------------------- |
| `Stop-Service`         | Pauses collection during configuration. |
| `Copy-Item`            | Copies the app and public CA.           |
| `icacls`               | Sets file permissions.                  |
| `Get-CimInstance`      | Checks the service account.             |
| `Add-LocalGroupMember` | Adds event-log reader membership.       |
| `btool`                | Checks configuration.                   |
| `Start-Service`        | Starts collection.                      |
| `Test-NetConnection`   | Checks the receiver’s port.             |
| `Get-Content -Tail`    | Displays recent messages.               |

A successful port check does not prove certificate validation. Confirm actual event delivery next.

---
