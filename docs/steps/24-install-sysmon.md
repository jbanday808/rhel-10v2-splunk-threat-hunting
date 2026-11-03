**Step 24 — Install Sysmon**

Check for an existing installation:

```
Get-Service -Name Sysmon,Sysmon64 -ErrorAction SilentlyContinue

Get-WindowsOptionalFeature `
  -Online `
  -FeatureName Sysmon `
  -ErrorAction SilentlyContinue
```

If built-in Sysmon is active:

```
sysmon.exe -c C:\SIEMLab\Source\sysmon\sysmon.xml
```

If its feature is enabled but its service is not installed, use its existing executable with `-i` and the XML.

For a fresh VM without an active built-in or standalone instance:

```
Invoke-WebRequest `
  -Uri 'https://download.sysinternals.com/files/Sysmon.zip' `
  -OutFile C:\SIEMLab\Downloads\Sysmon.zip

Expand-Archive `
  -Path C:\SIEMLab\Downloads\Sysmon.zip `
  -DestinationPath C:\SIEMLab\Tools\Sysmon `
  -Force
```

Verify the executable:

```
$SysmonExe = 'C:\SIEMLab\Tools\Sysmon\Sysmon64.exe'

$Signature = Get-AuthenticodeSignature -FilePath $SysmonExe

$Signature | Format-List Status,SignerCertificate

if ($Signature.Status -ne 'Valid' -or
    $Signature.SignerCertificate.Subject -notmatch 'Microsoft') {
    throw 'Stop: the Sysmon signature did not validate.'
}
```

Install and verify:

```
& $SysmonExe -accepteula -i C:\SIEMLab\Source\sysmon\sysmon.xml

wevtutil.exe sl Microsoft-Windows-Sysmon/Operational /ms:268435456

Get-Service Sysmon64

Get-WinEvent `
  -LogName Microsoft-Windows-Sysmon/Operational `
  -MaxEvents 5 |
  Select-Object TimeCreated,Id
```

**Command overview:**

- `Invoke-WebRequest` downloads the package.
- `Expand-Archive` extracts it.
- `Get-AuthenticodeSignature` verifies the executable.
- `-i` installs Sysmon with the XML.
- `-c` updates an existing installation.
- `Get-WinEvent` checks generated records.

Use one Sysmon implementation. Microsoft documents both built-in and standalone options. [learn.microsoft.com](https://learn.microsoft.com/windows/security/operating-system-security/sysmon/how-to-enable-sysmon?utm_source=chatgpt.com)

---
