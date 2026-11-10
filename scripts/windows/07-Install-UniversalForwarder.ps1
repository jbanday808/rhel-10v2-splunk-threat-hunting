#Requires -Version 5.1
#Requires -RunAsAdministrator
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$MsiPath,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-fA-F]{64}$')][string]$ExpectedSha256
)
$ErrorActionPreference = 'Stop'
if ($env:COMPUTERNAME -ne 'WINHUNT01') { throw 'Run only inside WINHUNT01.' }
if (Get-Service -Name SplunkForwarder -ErrorAction SilentlyContinue) { throw 'A forwarder already exists. Review Step 25.' }
$MsiPath = (Resolve-Path -LiteralPath $MsiPath).Path
if ((Get-FileHash -LiteralPath $MsiPath -Algorithm SHA256).Hash -ne $ExpectedSha256) {
    throw 'The MSI checksum differs from the official published checksum.'
}
$Install = Start-Process msiexec.exe -ArgumentList "/i `"$MsiPath`"" -Wait -PassThru
if ($Install.ExitCode -notin @(0,3010)) { throw "Installer exit code: $($Install.ExitCode)" }
Write-Output 'Use the Step 25 wizard settings, then deploy the configuration with Step 26.'
