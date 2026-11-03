**Step 23 — Enable Windows auditing and PowerShell logging**

Inside the **Windows VM**, use administrator PowerShell:

```
auditpol.exe /backup /file:C:\SIEMLab\Evidence\audit-policy-before.csv
```

Enable audit categories:

```
$AuditCategories = @(
    '{0CCE9215-69AE-11D9-BED3-505054503030}',
    '{0CCE922B-69AE-11D9-BED3-505054503030}',
    '{0CCE9235-69AE-11D9-BED3-505054503030}',
    '{0CCE9237-69AE-11D9-BED3-505054503030}',
    '{0CCE9227-69AE-11D9-BED3-505054503030}'
)

foreach ($Category in $AuditCategories) {
    auditpol.exe /set "/subcategory:$Category" /success:enable /failure:enable
}
```

These cover sign-ins, process creation, account changes, group changes, and other object access such as scheduled-task auditing.

Enable command-line information:

```
$AuditPath = 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Policies\System\Audit'

New-Item -Path $AuditPath -Force | Out-Null

New-ItemProperty `
  -Path $AuditPath `
  -Name ProcessCreationIncludeCmdLine_Enabled `
  -PropertyType DWord `
  -Value 1 `
  -Force | Out-Null
```

Enable advanced audit-policy precedence:

```
New-ItemProperty `
  -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Lsa' `
  -Name SCENoApplyLegacyAuditPolicy `
  -PropertyType DWord `
  -Value 1 `
  -Force | Out-Null
```

Enable PowerShell script logging:

```
$PowerShellPath = 'HKLM:\Software\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging'

New-Item -Path $PowerShellPath -Force | Out-Null

New-ItemProperty `
  -Path $PowerShellPath `
  -Name EnableScriptBlockLogging `
  -PropertyType DWord `
  -Value 1 `
  -Force | Out-Null
```

Enable and resize event logs:

```
wevtutil.exe sl Microsoft-Windows-PowerShell/Operational /e:true /ms:134217728

wevtutil.exe sl Security /ms:536870912

wevtutil.exe sl System /ms:134217728

wevtutil.exe sl Application /ms:134217728
```

**Command overview:**

| Command            | Explanation                        |
| ------------------ | ---------------------------------- |
| `auditpol /backup` | Saves original audit settings.     |
| `auditpol /set`    | Enables selected activity records. |
| `New-Item`         | Creates a settings location.       |
| `New-ItemProperty` | Sets the logging option.           |
| `wevtutil sl`      | Enables or resizes event logs.     |

Windows requires the command-line policy to include command details in Event 4688. [learn.microsoft.com](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/auditpol?utm_source=chatgpt.com)

Open a new PowerShell window before later tests.

---
