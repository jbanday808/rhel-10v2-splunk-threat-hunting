# Troubleshoot Start-Process, Command Prompt, and lab credentials

This guide addresses the following error reported while running a lab command:

```text
'Start-Process' is not recognized as an internal or external command,
operable program or batch file.
```

The command was entered at a `C:\Windows\System32>` **Command Prompt** prompt. `Start-Process` is a **PowerShell cmdlet**, so Command Prompt does not recognize it as a command. The later `Get-Credential` prompt was run from PowerShell and is the correct way to prepare the credential object.

**Status:** The reported credential prompt was displayed successfully. The supplied output does not establish that the password was accepted or that the new process started as the intended user. Verify those steps below.

Use this guide only on the authorized **WINHUNT01** lab guest with its disposable test account. Never enter an actual password in a command, screenshot, GitHub file, or chat message.

## Step 1 — Identify your current window

Look at the prompt before entering a command:

| Prompt example | Shell | What to enter |
| --- | --- | --- |
| `C:\Windows\System32>` | Command Prompt (`cmd.exe`) | Command Prompt commands or `powershell.exe` to start PowerShell. |
| `PS C:\Windows\System32>` | Windows PowerShell | PowerShell commands such as `Get-Credential` and `Start-Process`. |

If you still have the PowerShell window where you ran `Get-Credential`, return to **that same window**. The `$LabCredential` variable is local to the PowerShell session in which it was created. It is not automatically shared with Command Prompt, another tab, or a newly opened PowerShell window.

The `Start-Process` command that failed at the Command Prompt was not executed by PowerShell. Do not assume it started a process.

## Step 2 — Open Windows PowerShell if needed

If you are at the Command Prompt and need a PowerShell session, enter:

```cmd
powershell.exe -NoLogo
```

**Command overview:** `powershell.exe` starts Windows PowerShell; `-NoLogo` hides the startup banner. **Expected result:** The prompt begins with `PS`, for example `PS C:\Windows\System32>`.

Starting PowerShell this way inherits the account and elevation of the existing Command Prompt. It does not restore variables from another PowerShell session or automatically give administrator rights. If the previous Command Prompt was opened as the test user, the new PowerShell session uses that user's context. To work from an administrator session, open Windows PowerShell as administrator using Windows Terminal or the Start menu, as permitted in the lab.

## Step 3 — Check the disposable account

In PowerShell on WINHUNT01:

```powershell
Get-LocalUser -Name 'SIEMLabUser' | Select-Object Name, Enabled
```

**Command overview:** `Get-LocalUser` finds the named local account. `Select-Object` displays its name and whether it is enabled. **Expected result:** The intended account appears and `Enabled` is `True`. If it is absent or disabled, review the authorized account setup with the lab owner before proceeding.

If `New-LocalUser` reports that the user already exists, the Step 28 new-account check and the lab helper intentionally stop for review. The updated [Step 28](../steps/28-generate-harmless-hunting-activity.md) provides a separate manual password-reset path for the verified, authorized disposable local lab account. Do not automatically recreate, delete, enable, or reset an unverified account. `Get-LocalUser` is not available in 32-bit PowerShell on a 64-bit Windows system; use an approved 64-bit Windows PowerShell session.

## Step 4 — Create or reuse the credential object

If `$LabCredential` was created in this same PowerShell window, proceed to Step 5. Otherwise run:

```powershell
$LabCredential = Get-Credential -UserName "$env:COMPUTERNAME\SIEMLabUser" `
    -Message 'Enter the current SIEMLabUser password'
```

**Command overview:** `$env:COMPUTERNAME` identifies the local computer. `Get-Credential` prompts for the local test account's password and stores a credential object in `$LabCredential` for this session. **Expected result:** A credential prompt appears. Enter the **current password for the existing test account**. Do not share or record it.

If the prompt closes after you enter a password, that means the object was collected. `Get-Credential` does **not** set or reset the account password and does not by itself confirm that the password is correct. For example, if account creation failed because the account already existed, the password previously typed for a new account was not automatically applied to the existing account.

## Step 5 — Confirm a credential object is available

In the **same PowerShell session**, run:

```powershell
$LabCredential -is [System.Management.Automation.PSCredential]
```

**Command overview:** `-is` checks whether the variable contains a PowerShell credential object. **Expected result:** `True`. If the prompt was cancelled, the variable is empty, or a different session was opened, return to Step 4. `True` confirms the object type; it does not authenticate the password.

## Step 6 — Start the test window from PowerShell

In the **same PowerShell window**, run:

```powershell
if ($LabCredential -is [System.Management.Automation.PSCredential]) {
    Start-Process -FilePath "$env:SystemRoot\System32\cmd.exe" `
        -ArgumentList '/k whoami' `
        -WorkingDirectory "$env:SystemRoot\System32" `
        -Credential $LabCredential `
        -ErrorAction Stop
} else {
    Write-Host 'No credential object in this session. Run Get-Credential again.'
}
```

**Command overview:**

- `if` checks that the credential object is present before starting a process.
- `Start-Process` starts a program from PowerShell.
- `-FilePath` selects the Windows Command Prompt executable.
- `-ArgumentList '/k whoami'` runs `whoami` and leaves the new window open.
- `-WorkingDirectory` selects the Windows System32 directory.
- `-Credential $LabCredential` supplies the test account's credential object.
- `-ErrorAction Stop` displays a terminating error if PowerShell cannot start the process.

**Expected result:** A new Command Prompt window opens and `whoami` displays the local computer name followed by `\SIEMLabUser`, subject to Windows capitalization. If no window appears or an error is displayed, follow Step 8. Starting the process has not been verified until you observe the actual result.

## Step 7 — Use and close the new window

The new window is **Command Prompt**, so its prompt is expected to look like `C:\Windows\System32>`. To confirm its identity again, enter:

```cmd
whoami
```

**Command overview:** `whoami` displays the account running the current window. **Expected result:** The output identifies the intended local test account. It does not by itself prove administrator privileges or Splunk event delivery.

To close only this test Command Prompt window, enter:

```cmd
exit
```

**Command overview:** `exit` closes the current Command Prompt session. **Expected result:** The test window closes and the original PowerShell window remains available.

If you want to run PowerShell commands inside the test window, you may first run `powershell.exe -NoLogo` there. That new PowerShell session runs in the test window's account context and does not inherit the earlier `$LabCredential` variable. Do not type `Start-Process` directly at the `C:\...>` Command Prompt.

## Step 8 — Troubleshoot a failed launch

| Symptom | What to check |
| --- | --- |
| `Start-Process` is not recognized | Verify that the prompt begins with `PS`; return to PowerShell and use the credential in that session. |
| The credential object check returns `False` | The prompt was cancelled, the variable was not set, or this is a different PowerShell session. Run Step 4 again. |
| The user name or password is rejected | Confirm the local account and its current password through the authorized process. For the verified disposable account, [Step 28](../steps/28-generate-harmless-hunting-activity.md) documents a manual reset and a correct-password test. Avoid repeated attempts that could trigger a lockout. |
| The account already exists | Confirm it is the authorized disposable local lab account. The new-account block and helper stop rather than changing it automatically; use the separate manual path in Step 28 if a reset is needed. |
| A logon-right or policy error appears | Review local security policy and account restrictions with the responsible administrator. Do not weaken STIG or domain policy just to force the test to work. |
| No window is visible | Check for an error in the original PowerShell window and look for the new window in the taskbar. Do not claim success until `whoami` confirms the intended identity. |
| An error specifically identifies the Secondary Logon service | Inspect the service with the command below, and follow the approved service-management procedure if a change is required. |

```powershell
Get-CimInstance Win32_Service -Filter "Name='seclogon'" |
    Select-Object Name, State, StartMode
```

**Command overview:** `Get-CimInstance` reads the Secondary Logon service's current state and startup mode. **Expected result:** Record the reported state. This command does not change the service; assess any change with the lab owner and applicable policy.

## Step 9 — Optionally review the lab's security events

If logon auditing and forwarding are already configured, review recent events in Splunk:

```spl
index=win_security host=WINHUNT01 earliest=-15m (EventCode=4624 OR EventCode=4625)
| table _time host EventCode _raw
| head 20
```

**Search overview:** `index` and `host` select the intended lab data; `EventCode` filters for successful and failed logon events; `table` and `head` limit the results. **Expected result:** If the relevant events were generated, forwarded, indexed, and have this field extraction, compare their times with the test. Event fields and timestamps may differ, and no result alone does not prove that the login failed. Inspect local Windows Security logs, audit policy, forwarding, time range, and actual field names if necessary. Keep raw event details private.

Merely displaying `Get-Credential` is not evidence that a logon occurred. The original Command Prompt error likewise does not prove an authentication attempt was made.

## References

- [Microsoft Start-Process](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/start-process?view=powershell-5.1): Explains starting a process, specifying its working directory, and using alternate credentials.
- [Microsoft Get-Credential](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/get-credential?view=powershell-5.1): Explains the credential prompt and PowerShell credential objects.
- [Microsoft Get-LocalUser](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.localaccounts/get-localuser?view=powershell-5.1): Explains how to inspect a local account and the 64-bit PowerShell requirement.
- [Lab Step 28](../steps/28-generate-harmless-hunting-activity.md): Describes the authorized disposable account and hunting activity exercise.
