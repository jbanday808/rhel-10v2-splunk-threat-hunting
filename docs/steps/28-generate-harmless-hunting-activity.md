**Step 28 — Generate harmless hunting activity**

Run these commands only inside **WINHUNT01**, individually in the **same administrator Windows PowerShell window**. Its prompt begins with `PS`. The `$TestPassword` and `$LabCredential` variables are available only in that PowerShell session. Do not enter or share passwords in GitHub, screenshots, or chat. If a password prompt is cancelled or a command fails, stop; do not continue with values left from an earlier attempt.

This exercise has two account paths:

- **New account:** Complete Steps 28.2–28.3, skip Steps 28.4–28.5, then continue at Step 28.6 using the password entered in Step 28.2.
- **Existing disposable account:** Verify it in Step 28.1, skip Steps 28.2–28.3, and follow Steps 28.4–28.7 to reset and test its password. Use this path only after confirming that the existing account is the authorized disposable local lab account.

The optional `05-Generate-HuntActivity.ps1` helper still stops if `SIEMLabUser` exists; it does not perform the manual password reset. For shell or credential errors, see [PowerShell, Command Prompt, and lab credentials troubleshooting](../troubleshooting/windows-powershell-cmd-credentials.md).

## Step 28.1 — Confirm the guest and account

```powershell
$env:COMPUTERNAME
Get-LocalUser -Name 'SIEMLabUser' | Select-Object Name, Enabled, PrincipalSource, Description
```

**Command overview:** `$env:COMPUTERNAME` displays the computer name. `Get-LocalUser` checks the local test account and `Select-Object` shows its status and source. **Expected result:** The computer is `WINHUNT01`. If the account exists, confirm it is the enabled, disposable **local** lab account you intend to use. If Windows reports that the user was not found, use the new-account path. Investigate other errors before continuing. The LocalAccounts module requires 64-bit PowerShell on 64-bit Windows.

## Step 28.2 — Create a new disposable account, if absent

Skip this step when the account already exists. First run:

```powershell
if (Get-LocalUser -Name 'SIEMLabUser' -ErrorAction SilentlyContinue) {
    throw 'SIEMLabUser already exists. Review it before running this exercise.'
}
```

**Command overview:** `Get-LocalUser` checks for the account; `throw` stops this new-account check when it exists. **Expected result:** No message if the account is absent. If it exists, do not run the rest of Step 28.2; use the verified existing-account path.

Enter a temporary password:

```powershell
$TestPassword = Read-Host -Prompt 'Choose a temporary password for SIEMLabUser' -AsSecureString
```

**Command overview:** `Read-Host -AsSecureString` prompts without displaying the password and stores it in `$TestPassword`. **Expected result:** The prompt returns without displaying the password. Choose a nonempty password that meets local policy.

Create the account:

```powershell
New-LocalUser -Name 'SIEMLabUser' -Password $TestPassword -Description 'Disposable threat-hunting lab account' -ErrorAction Stop
```

**Command overview:** `New-LocalUser` creates the disposable local account using the entered password. **Expected result:** Windows reports the new account. If an error occurs, stop and resolve it before continuing; entering a password does not itself create or change an account.

## Step 28.3 — Generate a group-membership change, if using a new account

This optional lab action adds the newly created test account to the local Administrators group to generate a membership-change event. It grants administrator-group membership; use it only for the authorized disposable lab account and review the cleanup in Step 46. Skip this step for an existing account until its membership and the intended change have been reviewed.

```powershell
$Administrators = Get-LocalGroup -SID 'S-1-5-32-544'
Add-LocalGroupMember -Group $Administrators -Member 'SIEMLabUser' -ErrorAction Stop
```

**Command overview:** `Get-LocalGroup` finds the local Administrators group by SID. `Add-LocalGroupMember` adds the test account. **Expected result:** The command completes without an error. Windows may generate a group-membership event if the applicable audit policy is enabled. Stop on an error; do not assume membership changed.

## Step 28.4 — Enter a new password for an existing test account

For an **existing account only**, first confirm in Step 28.1 that `SIEMLabUser` is the authorized disposable local lab account. This step prepares a new password; it does not change Windows yet. Users who created the account in Step 28.2 should skip Steps 28.4–28.5.

```powershell
$TestPassword = Read-Host -Prompt 'Choose a new temporary password for SIEMLabUser' -AsSecureString
```

**Command overview:** `Read-Host -AsSecureString` prompts for a password without displaying it and stores it in `$TestPassword`. **Expected result:** A password prompt appears and returns to PowerShell. Choose a nonempty password that satisfies the local password policy.

## Step 28.5 — Apply the new password to the existing account

```powershell
Set-LocalUser -Name 'SIEMLabUser' -Password $TestPassword -ErrorAction Stop
```

**Command overview:** `Set-LocalUser` applies the entered password to the specified existing local account. `-ErrorAction Stop` reports a failure. **Expected result:** The command returns to the PowerShell prompt without an error. If it fails, stop and review the error before continuing. A successful password change does not itself prove that sign-in works.

This changes the account's password and can affect any other use of that account. Do not use it on an unverified account or an account connected to a Microsoft account.

## Step 28.6 — Build credentials from the same password

After a successful account creation in Step 28.2 **or** a successful password change in Step 28.5, run:

```powershell
$LabCredential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList "$env:COMPUTERNAME\SIEMLabUser", $TestPassword
```

**Command overview:** `New-Object` creates a credential object from the local computer and account name plus the same secure password value. **Expected result:** PowerShell returns without displaying the password. If the command fails, stop and do not reuse an older credential object. This does not authenticate the account; the next step tests it. If you changed PowerShell windows or either earlier account operation failed, return to the appropriate path rather than using an old variable.

## Step 28.7 — Test the correct password

```powershell
Start-Process -FilePath "$env:SystemRoot\System32\cmd.exe" -ArgumentList '/k whoami' -WorkingDirectory "$env:SystemRoot\System32" -Credential $LabCredential -ErrorAction Stop
```

**Command overview:** `Start-Process` opens Command Prompt using the test credentials. `/k whoami` displays the account name and keeps the new window open. **Expected result:** A new window displays the local computer name and test account, for example `winhunt01\siemlabuser`. Capitalization may differ. Confirm the actual output before continuing.

If Windows reports an incorrect user name or password, a disabled/locked account, or a logon-right problem, stop and investigate with the [credential troubleshooting guide](../troubleshooting/windows-powershell-cmd-credentials.md). Do not repeatedly guess passwords or weaken policy. The successful creation of `$LabCredential` alone does not prove authentication succeeded.

## Step 28.8 — Close the test window

In the **new Command Prompt window**, run:

```cmd
exit
```

**Command overview:** `exit` closes the test Command Prompt. **Expected result:** Only that window closes; return to the original administrator PowerShell window for the remaining steps.

## Step 28.9 — Run a harmless encoded command

```powershell
$Payload = "Write-Output 'SIEM-LAB-ENCODED-TEST'"
$Encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($Payload))
powershell.exe -NoProfile -EncodedCommand $Encoded
```

**Command overview:** The first two commands encode a harmless marker; `powershell.exe -EncodedCommand` runs it. **Expected result:** `SIEM-LAB-ENCODED-TEST` is displayed. Relevant PowerShell and process events depend on local logging and audit settings.

## Step 28.10 — Generate a known network connection

```powershell
curl.exe --fail --silent --show-error 'https://example.com/' --output C:\SIEMLab\TestFiles\example.html
```

**Command overview:** `curl.exe` requests the public example page and writes it to the lab test folder. **Expected result:** The file is created if the folder, DNS, and approved outbound connectivity are available. If this fails, investigate the displayed network or file error separately.

## Step 28.11 — Register a harmless task

```powershell
$Action = New-ScheduledTaskAction -Execute "$env:SystemRoot\System32\cmd.exe" -Argument '/c echo SIEM-LAB-TASK-TEST'
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddHours(1)
Register-ScheduledTask -TaskName SIEMLab-HuntTest -Action $Action -Trigger $Trigger -Description 'Harmless SIEM hunting test'
```

**Command overview:** The first two commands define the marker action and trigger. `Register-ScheduledTask` registers the task. **Expected result:** Windows reports the new task. If the named task already exists, review it before making changes; do not overwrite an unrelated task.

## Step 28.12 — Start the task

```powershell
Start-ScheduledTask -TaskName SIEMLab-HuntTest
```

**Command overview:** `Start-ScheduledTask` starts the previously registered task. **Expected result:** The command returns without an error; inspect Task Scheduler history if the task's actual execution needs verification.

## Step 28.13 — Create an Application marker

```powershell
eventcreate.exe /T INFORMATION /ID 100 /L APPLICATION /SO SIEMLab /D 'SIEM-LAB-APPLICATION-TEST'
```

**Command overview:** `eventcreate.exe` writes an informational marker to the Application log. **Expected result:** The command reports success. Check Event Viewer if it reports an error.

## Step 28.14 — Prepare for one intentional failed login

Only proceed after the **correct-password test succeeded** in Step 28.7 and the failed-login exercise is authorized for the disposable account. Review the local account lockout policy first:

```powershell
net accounts
```

**Command overview:** `net accounts` displays local account policy, including the lockout threshold. **Expected result:** Review the actual policy and recent failed attempts. Even one more failed attempt can lock the account if previous failures are near the threshold. Do not change the policy to force the exercise; skip the failed-login test if the risk is unacceptable.

## Step 28.15 — Generate one intentional failed login

```powershell
runas.exe /user:.\SIEMLabUser cmd.exe
```

**Command overview:** `runas.exe` prompts for the local test account's password and attempts to start Command Prompt. **Expected result:** For this **intentional failed-login exercise**, enter an incorrect password **once**; an authentication error is expected. This is separate from the correct-password test in Step 28.7. Do not keep retrying, and do not share the password entered.

If logon auditing is enabled and the event is collected, Windows can generate Security event `4625`. Account creation (`4720`), group change (`4732`), process activity (`4688`), and scheduled task creation (`4698`) likewise depend on the actions performed and the relevant audit settings. An existing-account path does not create a new `4720` event merely by resetting its password.

Review the actual events in Splunk after forwarding is validated. [Step 46](46-remove-the-test-objects.md) and its cleanup helper remove the named account and other test objects; review what they will delete before running them, especially if reusing an existing disposable account. They do not restore a previous password.

## References

- [Microsoft Set-LocalUser](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.localaccounts/set-localuser?view=powershell-5.1): Explains how to change a local account password with a secure string.
- [Microsoft PSCredential constructor](https://learn.microsoft.com/en-us/dotnet/api/system.management.automation.pscredential.-ctor): Explains creating a credential from a user name and secure password.
- [Microsoft Start-Process](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/start-process?view=powershell-5.1): Explains starting a process using alternate credentials.
- [Microsoft account lockout threshold](https://learn.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/account-lockout-threshold): Explains the effect of failed sign-in attempts.
