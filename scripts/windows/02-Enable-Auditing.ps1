#Requires -Version 5.1
#Requires -RunAsAdministrator
$ErrorActionPreference = 'Stop'
if ($env:COMPUTERNAME -ne 'WINHUNT01') { throw 'Run only inside WINHUNT01.' }
function Invoke-LabNative {
    param([string]$File, [string[]]$Arguments)
    & $File @Arguments
    if ($LASTEXITCODE -ne 0) { throw "$File failed with exit code $LASTEXITCODE" }
}
New-Item -ItemType Directory -Path C:\SIEMLab\Evidence -Force | Out-Null
$Backup = 'C:\SIEMLab\Evidence\audit-policy-before.csv'
if (!(Test-Path -LiteralPath $Backup)) {
    Invoke-LabNative -File auditpol.exe -Arguments @('/backup', "/file:$Backup")
}
$Categories = @(
    '{0CCE9215-69AE-11D9-BED3-505054503030}',
    '{0CCE922B-69AE-11D9-BED3-505054503030}',
    '{0CCE9235-69AE-11D9-BED3-505054503030}',
    '{0CCE9237-69AE-11D9-BED3-505054503030}',
    '{0CCE9227-69AE-11D9-BED3-505054503030}'
)
foreach ($Category in $Categories) {
    Invoke-LabNative -File auditpol.exe -Arguments @('/set', "/subcategory:$Category", '/success:enable', '/failure:enable')
}
$AuditPath = 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Policies\System\Audit'
New-Item -Path $AuditPath -Force | Out-Null
New-ItemProperty -Path $AuditPath -Name ProcessCreationIncludeCmdLine_Enabled -PropertyType DWord -Value 1 -Force | Out-Null
New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Lsa' -Name SCENoApplyLegacyAuditPolicy -PropertyType DWord -Value 1 -Force | Out-Null
$LoggingPath = 'HKLM:\Software\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging'
New-Item -Path $LoggingPath -Force | Out-Null
New-ItemProperty -Path $LoggingPath -Name EnableScriptBlockLogging -PropertyType DWord -Value 1 -Force | Out-Null
Invoke-LabNative -File wevtutil.exe -Arguments @('sl','Microsoft-Windows-PowerShell/Operational','/e:true','/ms:134217728')
Invoke-LabNative -File wevtutil.exe -Arguments @('sl','Security','/ms:536870912')
Invoke-LabNative -File wevtutil.exe -Arguments @('sl','System','/ms:134217728')
Invoke-LabNative -File wevtutil.exe -Arguments @('sl','Application','/ms:134217728')
Write-Output 'Open a new PowerShell window before the hunting tests.'
