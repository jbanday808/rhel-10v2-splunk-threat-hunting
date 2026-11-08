**Step 28 — Generate harmless hunting activity**

Run only inside **WINHUNT01**, in a new administrator PowerShell window.

If `SIEMLabUser` already exists or you need help with `Get-Credential` and a `Start-Process` command entered in Command Prompt, see [PowerShell, Command Prompt, and lab credentials troubleshooting](../troubleshooting/windows-powershell-cmd-credentials.md). Review the existing account before continuing; the exercise deliberately stops if the account exists.

Create the disposable account:

```
if (Get-LocalUser -Name SIEMLabUser -ErrorAction SilentlyContinue) {
    throw 'SIEMLabUser already exists. Review it before running this exercise.'
}

$TestPassword = Read-Host `
  'Choose a temporary password for SIEMLabUser' `
  -AsSecureString

New-LocalUser `
  -Name SIEMLabUser `
  -Password $TestPassword `
  -Description 'Disposable threat-hunting lab account'

$Administrators = Get-LocalGroup -SID 'S-1-5-32-544'

Add-LocalGroupMember `
  -Group $Administrators `
  -Member SIEMLabUser
```

Run an encoded command that only prints a marker:

```
$Payload = "Write-Output 'SIEM-LAB-ENCODED-TEST'"

$Encoded = [Convert]::ToBase64String(
    [Text.Encoding]::Unicode.GetBytes($Payload)
)

powershell.exe -NoProfile -EncodedCommand $Encoded
```

Generate a known network connection:

```
curl.exe --fail --silent --show-error `
  'https://example.com/' `
  --output C:\SIEMLab\TestFiles\example.html
```

Create a harmless task:

```
$Action = New-ScheduledTaskAction `
  -Execute "$env:SystemRoot\System32\cmd.exe" `
  -Argument '/c echo SIEM-LAB-TASK-TEST'

$Trigger = New-ScheduledTaskTrigger `
  -Once `
  -At (Get-Date).AddHours(1)

Register-ScheduledTask `
  -TaskName SIEMLab-HuntTest `
  -Action $Action `
  -Trigger $Trigger `
  -Description 'Harmless SIEM hunting test'

Start-ScheduledTask -TaskName SIEMLab-HuntTest
```

Create an Application marker:

```
eventcreate.exe /T INFORMATION /ID 100 /L APPLICATION `
  /SO SIEMLab /D 'SIEM-LAB-APPLICATION-TEST'
```

For one failed-login test:

```
runas.exe /user:.\SIEMLabUser cmd.exe
```

Enter an incorrect password **once** for the disposable account.

**Command overview:**

| Command                     | Explanation                                  |
| --------------------------- | -------------------------------------------- |
| `Read-Host -AsSecureString` | Requests the password without displaying it. |
| `New-LocalUser`             | Creates the test account.                    |
| `Add-LocalGroupMember`      | Creates a membership change.                 |
| `ToBase64String`            | Encodes the harmless command.                |
| `-EncodedCommand`           | Runs it.                                     |
| `curl.exe`                  | Creates a controlled network connection.     |
| `Register-ScheduledTask`    | Creates the test task.                       |
| `eventcreate`               | Writes an Application marker.                |
| `runas`                     | Makes the controlled login attempt.          |

Expected records include Security events `4720`, `4732`, `4688`, `4698`, and `4625`, plus PowerShell and Sysmon activity when the relevant policies generate them.

---
