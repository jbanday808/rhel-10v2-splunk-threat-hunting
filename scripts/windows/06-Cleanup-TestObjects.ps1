#Requires -Version 5.1
#Requires -RunAsAdministrator
$ErrorActionPreference = 'Stop'
if ($env:COMPUTERNAME -ne 'WINHUNT01') { throw 'Run only inside WINHUNT01.' }
$Task = Get-ScheduledTask -TaskName SIEMLab-HuntTest -ErrorAction SilentlyContinue
if ($Task) {
    Stop-ScheduledTask -TaskName SIEMLab-HuntTest -ErrorAction SilentlyContinue
    Unregister-ScheduledTask -TaskName SIEMLab-HuntTest -Confirm:$false
}
if (Get-LocalUser -Name SIEMLabUser -ErrorAction SilentlyContinue) {
    $Admins = Get-LocalGroup -SID 'S-1-5-32-544'
    Remove-LocalGroupMember -Group $Admins -Member SIEMLabUser -ErrorAction SilentlyContinue
    Remove-LocalUser -Name SIEMLabUser
}
Remove-Item -LiteralPath C:\SIEMLab\TestFiles\example.html -Force -ErrorAction SilentlyContinue
Write-Output 'Disposable test objects removed. Event records remain for investigation.'
