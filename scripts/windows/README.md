# Windows helpers

`Test-Project.ps1` is a read-only source-package check for the physical Windows host or CI.
The endpoint-changing scripts require administrator PowerShell and refuse to run unless the computer is named **WINHUNT01**. Perform the naming and network setup manually in Step 21 first.

| File | Guide step and prerequisites |
| --- | --- |
| `01-Initialize-EndpointFolders.ps1` | Step 22 folders inside the endpoint. Transfer the project and public CA separately. |
| `02-Enable-Auditing.ps1` | Step 23 audit policy and PowerShell logging. Preserves the first audit backup. |
| `03-Install-SysmonStandalone.ps1` | Step 24 fresh standalone installation only. Existing/built-in Sysmon uses the guide's update procedure. |
| `07-Install-UniversalForwarder.ps1` | Step 25 MSI installation. Supply the downloaded file and its vendor-published SHA-256. Follow the wizard settings in the guide. |
| `04-Deploy-Forwarder.ps1` | Step 26. Requires the forwarder and verified public CA at `C:\SIEMLab\Public\ca.pem`. |
| `05-Generate-HuntActivity.ps1` | Step 28. Creates the named disposable lab account, task, and marker activity. It stops if the account exists; the [manual existing-account path](../../docs/steps/28-generate-harmless-hunting-activity.md) is separate. Read the script first. |
| `06-Cleanup-TestObjects.ps1` | Step 46. Removes those named test objects and preserves the event logs. |

Example in WINHUNT01: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\windows\02-Enable-Auditing.ps1`.
Use the full guide for command explanations, service account choices, TLS verification, and actual event checks.
