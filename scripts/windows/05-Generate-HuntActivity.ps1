#Requires -Version 5.1
#Requires -RunAsAdministrator
$ErrorActionPreference = 'Stop'
if ($env:COMPUTERNAME -ne 'WINHUNT01') { throw 'Run only inside WINHUNT01.' }
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


$Payload = "Write-Output 'SIEM-LAB-ENCODED-TEST'"

$Encoded = [Convert]::ToBase64String(
    [Text.Encoding]::Unicode.GetBytes($Payload)
)

powershell.exe -NoProfile -EncodedCommand $Encoded


curl.exe --fail --silent --show-error `
  'https://example.com/' `
  --output C:\SIEMLab\TestFiles\example.html


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


eventcreate.exe /T INFORMATION /ID 100 /L APPLICATION `
  /SO SIEMLab /D 'SIEM-LAB-APPLICATION-TEST'


runas.exe /user:.\SIEMLabUser cmd.exe
