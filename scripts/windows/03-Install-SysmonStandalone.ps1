#Requires -Version 5.1
#Requires -RunAsAdministrator
[CmdletBinding()]
param([string]$ProjectRoot = (Join-Path $PSScriptRoot '..\..'))
$ErrorActionPreference = 'Stop'
if ($env:COMPUTERNAME -ne 'WINHUNT01') { throw 'Run only inside WINHUNT01.' }
if (Get-Service -Name Sysmon,Sysmon64 -ErrorAction SilentlyContinue) {
    throw 'An existing Sysmon service was found. Use the update procedure in Step 24.'
}
$Feature = Get-WindowsOptionalFeature -Online -FeatureName Sysmon -ErrorAction SilentlyContinue
if ($Feature -and $Feature.State -eq 'Enabled') {
    throw 'Built-in Sysmon is enabled. Follow Step 24 rather than installing a second implementation.'
}
$Config = Join-Path (Resolve-Path -LiteralPath $ProjectRoot).Path 'sysmon\sysmon.xml'
if (!(Test-Path -LiteralPath $Config)) { throw 'Sysmon XML is missing.' }
New-Item -ItemType Directory -Path C:\SIEMLab\Downloads,C:\SIEMLab\Tools -Force | Out-Null
Invoke-WebRequest -UseBasicParsing -Uri 'https://download.sysinternals.com/files/Sysmon.zip' -OutFile C:\SIEMLab\Downloads\Sysmon.zip
Expand-Archive -LiteralPath C:\SIEMLab\Downloads\Sysmon.zip -DestinationPath C:\SIEMLab\Tools\Sysmon -Force
$Exe = 'C:\SIEMLab\Tools\Sysmon\Sysmon64.exe'
$Signature = Get-AuthenticodeSignature -FilePath $Exe
if ($Signature.Status -ne 'Valid' -or $Signature.SignerCertificate.Subject -notmatch 'Microsoft') {
    throw 'The Sysmon executable signature did not validate.'
}
& $Exe -accepteula -i $Config
if ($LASTEXITCODE -ne 0) { throw "Sysmon installation failed: $LASTEXITCODE" }
wevtutil.exe sl Microsoft-Windows-Sysmon/Operational /ms:268435456
if ($LASTEXITCODE -ne 0) { throw 'Could not resize the Sysmon event log.' }
Get-Service -Name Sysmon64
