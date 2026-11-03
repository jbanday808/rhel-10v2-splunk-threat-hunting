**Step 46 — Remove the test objects**

Inside **WINHUNT01**:

```
Stop-ScheduledTask `
  -TaskName SIEMLab-HuntTest `
  -ErrorAction SilentlyContinue

Unregister-ScheduledTask `
  -TaskName SIEMLab-HuntTest `
  -Confirm:$false

$Administrators = Get-LocalGroup -SID 'S-1-5-32-544'

Remove-LocalGroupMember `
  -Group $Administrators `
  -Member SIEMLabUser

Remove-LocalUser -Name SIEMLabUser

Remove-Item `
  -LiteralPath C:\SIEMLab\TestFiles\example.html `
  -Force `
  -ErrorAction SilentlyContinue
```

**Command overview:**

- `Stop-ScheduledTask` stops the task.
- `Unregister-ScheduledTask` removes it.
- `Remove-LocalGroupMember` removes temporary administrator membership.
- `Remove-LocalUser` deletes the disposable account.
- `Remove-Item` deletes the test download.

Keep the event records for investigation notes.

---
