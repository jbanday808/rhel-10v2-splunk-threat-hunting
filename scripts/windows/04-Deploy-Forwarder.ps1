#Requires -Version 5.1
#Requires -RunAsAdministrator
[CmdletBinding()]
param([string]$ProjectRoot = (Join-Path $PSScriptRoot '..\..'))
$ErrorActionPreference = 'Stop'
if ($env:COMPUTERNAME -ne 'WINHUNT01') { throw 'Run only inside WINHUNT01.' }
$ProjectRoot = (Resolve-Path -LiteralPath $ProjectRoot).Path
$ForwarderSource = Join-Path $ProjectRoot 'apps\LAB_UF_WINDOWS'
if (!(Test-Path -LiteralPath 'C:\SIEMLab\Public\ca.pem')) { throw 'Transfer and verify the public CA in Step 22 first.' }
$Forwarder = Get-CimInstance Win32_Service -Filter "Name='SplunkForwarder'"
if (!$Forwarder) { throw 'Install the Universal Forwarder using Step 25 first.' }
if ($Forwarder.StartName -ine 'NT SERVICE\SplunkForwarder') { throw 'Review the forwarder service account using Steps 25 and 26.' }

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
  -LiteralPath $ForwarderSource `
  -Destination "$UfHome\etc\apps" `
  -Recurse `
  -Force


icacls.exe "$UfHome\etc\auth\lab" /inheritance:r /grant:r `
  '*S-1-5-18:(OI)(CI)F' `
  '*S-1-5-32-544:(OI)(CI)F' `
  'NT SERVICE\SplunkForwarder:(OI)(CI)R'


Get-CimInstance Win32_Service `
  -Filter "Name='SplunkForwarder'" |
  Select-Object Name,StartName


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


& "$UfHome\bin\splunk.exe" btool check

& "$UfHome\bin\splunk.exe" btool inputs list --debug

& "$UfHome\bin\splunk.exe" btool outputs list --debug

Start-Service SplunkForwarder

Test-NetConnection splunk01.lab.test -Port 9997

Get-Content "$UfHome\var\log\splunk\splunkd.log" -Tail 50
