#Requires -Version 5.1
[CmdletBinding()]
param(
    [string]$Root = (Join-Path $PSScriptRoot '..\..'),
    [switch]$VerifyManifest
)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path -LiteralPath $Root).Path
$Required = @(
    'README.md', 'start-here\START_HERE_WINDOWS.md', '.gitignore', '.gitattributes',
    'apps\LAB_SIEM\local\indexes.conf',
    'apps\LAB_SIEM\local\inputs.conf', 'apps\LAB_SIEM\local\props.conf',
    'configs\redaction\inputs.conf.example', 'configs\redaction\props.conf.example',
    'scripts\rhel\install-redaction-lab.sh', 'scripts\rhel\generate-redaction-marker.sh',
    'scripts\merge_redaction_config.py', 'tests\test_redaction.py',
    'configs\hec\inputs.conf.example', 'scripts\rhel\send-hec-event.sh',
    'examples\hec\event.json', 'hunts\12-hec-ingestion-check.spl',
    'apps\LAB_UF_WINDOWS\local\outputs.conf',
    'apps\Splunk_TA_nginx\local\inputs.conf',
    'sysmon\sysmon.xml', 'configs\nginx\nginx.conf',
    '.github\workflows\validate-project.yml',
    '.github\workflows\oidc-claims.yml',
    '.github\workflows\azure-oidc.yml'
)
foreach ($Relative in $Required) {
    if (!(Test-Path -LiteralPath (Join-Path $Root $Relative) -PathType Leaf)) {
        throw "Missing required file: $Relative"
    }
}
$Failures = New-Object 'System.Collections.Generic.List[string]'
Get-ChildItem -LiteralPath (Join-Path $Root 'scripts') -Recurse -Filter '*.ps1' | ForEach-Object {
    $Tokens = $null
    $ParseErrors = $null
    $null = [System.Management.Automation.Language.Parser]::ParseFile(
        $_.FullName, [ref]$Tokens, [ref]$ParseErrors
    )
    foreach ($Issue in $ParseErrors) {
        $Failures.Add("$($_.FullName): $($Issue.Message)")
    }
}
Get-ChildItem -LiteralPath $Root -Recurse -Filter '*.xml' | Where-Object {
    $_.FullName -notmatch '[\\/]\.git[\\/]'
} | ForEach-Object {
    try { $null = [xml](Get-Content -LiteralPath $_.FullName -Raw) }
    catch { $Failures.Add("XML parse failed: $($_.Exception.Message)") }
}
$StepCount = @(Get-ChildItem -LiteralPath (Join-Path $Root 'docs\steps') -Filter '*.md' | Where-Object {
    $_.Name -match '^\d{2}-'
}).Count
if ($StepCount -ne 52) { $Failures.Add('Expected 52 numbered step files.') }
if ($VerifyManifest) {
    $Manifest = Get-Content -LiteralPath (Join-Path $Root 'FILE_MANIFEST.json') -Raw | ConvertFrom-Json
    foreach ($Entry in $Manifest.files) {
        $Relative = $Entry.path.Replace('/', [IO.Path]::DirectorySeparatorChar)
        $Full = [IO.Path]::GetFullPath((Join-Path $Root $Relative))
        $Prefix = $Root.TrimEnd([IO.Path]::DirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar
        if (!$Full.StartsWith($Prefix, [StringComparison]::OrdinalIgnoreCase)) {
            $Failures.Add("Manifest path outside project: $($Entry.path)")
            continue
        }
        if (!(Test-Path -LiteralPath $Full -PathType Leaf)) {
            $Failures.Add("Missing manifest file: $($Entry.path)")
            continue
        }
        $Actual = (Get-FileHash -LiteralPath $Full -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($Actual -ne $Entry.sha256) { $Failures.Add("Initial file hash changed: $($Entry.path)") }
    }
}
if ($Failures.Count -gt 0) { throw ($Failures -join [Environment]::NewLine) }
Write-Output 'Source validation passed. Live lab validation remains separate.'
