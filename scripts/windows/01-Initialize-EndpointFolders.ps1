#Requires -Version 5.1
#Requires -RunAsAdministrator
$ErrorActionPreference = 'Stop'
if ($env:COMPUTERNAME -ne 'WINHUNT01') { throw 'Run only inside WINHUNT01 after Step 21.' }
@('Downloads','Source','Tools','Public','Evidence','TestFiles') | ForEach-Object {
    New-Item -ItemType Directory -Path (Join-Path 'C:\SIEMLab' $_) -Force | Out-Null
}
Write-Output 'Endpoint folders created. Transfer and verify the public CA using Step 22.'
