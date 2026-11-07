# Windows 11 STIG V2R11 — rule reference CC

This reference reproduces the **check and fix** text from the user-supplied, unclassified manual XCCDF (Release: 11 Benchmark Date: 30 Sep 2026). It contains 77 rules. Line-end whitespace is normalized for readability. The source is a version-specific reference: confirm the required release and use the official benchmark and your assessor’s applicability decision. All targets, evidence and assessment statuses remain unverified.

Read the implementation guide, back up the system, and obtain approval before making changes. The source fix text can contain commands or settings that change the system; do not run them blindly. In a managed system use the approved policy owner and source.

| Rule | Severity | Title |
| --- | --- | --- |
| [WN11-CC-000005](#wn11-cc-000005) | medium | Camera access from the lock screen must be disabled. |
| [WN11-CC-000007](#wn11-cc-000007) | medium | Windows 11 must cover or disable the built-in or attached camera when not in use. |
| [WN11-CC-000010](#wn11-cc-000010) | medium | The display of slide shows on the lock screen must be disabled. |
| [WN11-CC-000020](#wn11-cc-000020) | medium | IPv6 source routing must be configured to highest protection. |
| [WN11-CC-000025](#wn11-cc-000025) | medium | The system must be configured to prevent IP source routing. |
| [WN11-CC-000030](#wn11-cc-000030) | low | The system must be configured to prevent Internet Control Message Protocol (ICMP) redirects from overriding Open Shortest Path First (OSPF) generated routes. |
| [WN11-CC-000035](#wn11-cc-000035) | low | The system must be configured to ignore NetBIOS name release requests except from WINS servers. |
| [WN11-CC-000037](#wn11-cc-000037) | medium | Local administrator accounts must have their privileged token filtered to prevent elevated privileges from being used over the network on domain systems. |
| [WN11-CC-000038](#wn11-cc-000038) | medium | WDigest Authentication must be disabled. |
| [WN11-CC-000039](#wn11-cc-000039) | medium | Run as different user must be removed from context menus. |
| [WN11-CC-000040](#wn11-cc-000040) | medium | Insecure logons to an SMB server must be disabled. |
| [WN11-CC-000044](#wn11-cc-000044) | medium | Internet connection sharing must be disabled. |
| [WN11-CC-000050](#wn11-cc-000050) | medium | Hardened UNC Paths must be defined to require mutual authentication and integrity for at least the \\*\SYSVOL and \\*\NETLOGON shares. |
| [WN11-CC-000052](#wn11-cc-000052) | medium | Windows 11 must be configured to prioritize ECC Curves with longer key lengths first. |
| [WN11-CC-000055](#wn11-cc-000055) | medium | Simultaneous connections to the internet or a Windows domain must be limited. |
| [WN11-CC-000060](#wn11-cc-000060) | medium | Connections to non-domain networks when connected to a domain authenticated network must be blocked. |
| [WN11-CC-000066](#wn11-cc-000066) | medium | Command line data must be included in process creation events. |
| [WN11-CC-000068](#wn11-cc-000068) | medium | Windows 11 must be configured to enable Remote host allows delegation of non-exportable credentials. |
| [WN11-CC-000070](#wn11-cc-000070) | medium | Virtualization-Based Security (VBS) must be enabled on Windows 11 with the platform security level configured to Secure Boot or Secure Boot with DMA Protection. |
| [WN11-CC-000075](#wn11-cc-000075) | high | Credential Guard must be running on Windows 11 systems. |
| [WN11-CC-000080](#wn11-cc-000080) | medium | Virtualization-based protection of code integrity must be enabled. |
| [WN11-CC-000085](#wn11-cc-000085) | medium | Early Launch Antimalware, Boot-Start Driver Initialization Policy must prevent boot drivers. |
| [WN11-CC-000090](#wn11-cc-000090) | medium | Group Policy objects must be reprocessed even if they have not changed. |
| [WN11-CC-000100](#wn11-cc-000100) | medium | Downloading print driver packages over HTTP must be prevented. |
| [WN11-CC-000105](#wn11-cc-000105) | medium | Web publishing and online ordering wizards must be prevented from downloading a list of providers. |
| [WN11-CC-000110](#wn11-cc-000110) | medium | Printing over HTTP must be prevented. |
| [WN11-CC-000115](#wn11-cc-000115) | medium | Systems must at least attempt device authentication using certificates. |
| [WN11-CC-000120](#wn11-cc-000120) | medium | The network selection user interface (UI) must not be displayed on the logon screen. |
| [WN11-CC-000130](#wn11-cc-000130) | medium | Local users on domain-joined computers must not be enumerated. |
| [WN11-CC-000145](#wn11-cc-000145) | medium | Users must be prompted for a password on resume from sleep (on battery). |
| [WN11-CC-000150](#wn11-cc-000150) | medium | The user must be prompted for a password on resume from sleep (plugged in). |
| [WN11-CC-000155](#wn11-cc-000155) | high | Solicited Remote Assistance must not be allowed. |
| [WN11-CC-000165](#wn11-cc-000165) | medium | Unauthenticated RPC clients must be restricted from connecting to the RPC server. |
| [WN11-CC-000170](#wn11-cc-000170) | low | The setting to allow Microsoft accounts to be optional for modern style apps must be enabled. |
| [WN11-CC-000175](#wn11-cc-000175) | low | The Application Compatibility Program Inventory must be prevented from collecting data and sending the information to Microsoft. |
| [WN11-CC-000180](#wn11-cc-000180) | high | Autoplay must be turned off for non-volume devices. |
| [WN11-CC-000185](#wn11-cc-000185) | high | The default autorun behavior must be configured to prevent autorun commands. |
| [WN11-CC-000190](#wn11-cc-000190) | high | Autoplay must be disabled for all drives. |
| [WN11-CC-000195](#wn11-cc-000195) | medium | Enhanced anti-spoofing for facial recognition must be enabled on Windows 11. |
| [WN11-CC-000200](#wn11-cc-000200) | medium | Administrator accounts must not be enumerated during elevation. |
| [WN11-CC-000204](#wn11-cc-000204) | medium | Enhanced diagnostic data must be limited to the minimum required to support Windows Analytics. |
| [WN11-CC-000205](#wn11-cc-000205) | medium | Windows Telemetry must not be configured to Full. |
| [WN11-CC-000206](#wn11-cc-000206) | low | Windows Update must not obtain updates from other PCs on the internet. |
| [WN11-CC-000210](#wn11-cc-000210) | medium | The Microsoft Defender SmartScreen for Explorer must be enabled. |
| [WN11-CC-000215](#wn11-cc-000215) | medium | Explorer Data Execution Prevention must be enabled. |
| [WN11-CC-000220](#wn11-cc-000220) | low | File Explorer heap termination on corruption must be disabled. |
| [WN11-CC-000225](#wn11-cc-000225) | medium | File Explorer shell protocol must run in protected mode. |
| [WN11-CC-000252](#wn11-cc-000252) | medium | Windows 11 must be configured to disable Windows Game Recording and Broadcasting. |
| [WN11-CC-000255](#wn11-cc-000255) | medium | The use of a hardware security device with Windows Hello for Business must be enabled. |
| [WN11-CC-000260](#wn11-cc-000260) | medium | Windows 11 must be configured to require a minimum PIN length of six characters or greater. |
| [WN11-CC-000270](#wn11-cc-000270) | medium | Passwords must not be saved in the Remote Desktop Client. |
| [WN11-CC-000275](#wn11-cc-000275) | medium | Local drives must be prevented from sharing with Remote Desktop Session Hosts. |
| [WN11-CC-000280](#wn11-cc-000280) | medium | Remote Desktop Services must always prompt a client for passwords upon connection. |
| [WN11-CC-000285](#wn11-cc-000285) | medium | The Remote Desktop Session Host must require secure RPC communications. |
| [WN11-CC-000290](#wn11-cc-000290) | medium | Remote Desktop Services must be configured with the client connection encryption set to the required level. |
| [WN11-CC-000295](#wn11-cc-000295) | medium | Attachments must be prevented from being downloaded from RSS feeds. |
| [WN11-CC-000300](#wn11-cc-000300) | medium | Basic authentication for RSS feeds over HTTP must not be used. |
| [WN11-CC-000305](#wn11-cc-000305) | medium | Indexing of encrypted files must be turned off. |
| [WN11-CC-000310](#wn11-cc-000310) | medium | Users must be prevented from changing installation options. |
| [WN11-CC-000315](#wn11-cc-000315) | high | The Windows Installer feature "Always install with elevated privileges" must be disabled. |
| [WN11-CC-000320](#wn11-cc-000320) | medium | Users must be notified if a web-based program attempts to install software. |
| [WN11-CC-000325](#wn11-cc-000325) | medium | Automatically signing in the last interactive user after a system-initiated restart must be disabled. |
| [WN11-CC-000326](#wn11-cc-000326) | medium | PowerShell script block logging must be enabled on Windows 11. |
| [WN11-CC-000327](#wn11-cc-000327) | medium | PowerShell Transcription must be enabled on Windows 11. |
| [WN11-CC-000330](#wn11-cc-000330) | high | The Windows Remote Management (WinRM) client must not use Basic authentication. |
| [WN11-CC-000335](#wn11-cc-000335) | medium | The Windows Remote Management (WinRM) client must not allow unencrypted traffic. |
| [WN11-CC-000345](#wn11-cc-000345) | high | The Windows Remote Management (WinRM) service must not use Basic authentication. |
| [WN11-CC-000350](#wn11-cc-000350) | medium | The Windows Remote Management (WinRM) service must not allow unencrypted traffic. |
| [WN11-CC-000355](#wn11-cc-000355) | medium | The Windows Remote Management (WinRM) service must not store RunAs credentials. |
| [WN11-CC-000360](#wn11-cc-000360) | medium | The Windows Remote Management (WinRM) client must not use Digest authentication. |
| [WN11-CC-000365](#wn11-cc-000365) | medium | Windows 11 must be configured to prevent Windows apps from being activated by voice while the system is locked. |
| [WN11-CC-000370](#wn11-cc-000370) | medium | The convenience PIN for Windows 11 must be disabled. |
| [WN11-CC-000385](#wn11-cc-000385) | medium | Windows Ink Workspace must be configured to disallow access above the lock. |
| [WN11-CC-000390](#wn11-cc-000390) | low | Windows 11 must be configured to prevent users from receiving suggestions for third-party or additional applications. |
| [WN11-CC-000391](#wn11-cc-000391) | medium | Internet Explorer must be disabled for Windows 11. |
| [WN11-CC-000063](#wn11-cc-000063) | medium | Windows 11 systems must use either Group Policy or an approved Mobile Device Management (MDM) product to enforce STIG compliance. |
| [WN11-CC-000366](#wn11-cc-000366) | medium | Windows 11 must be configured to prevent Windows apps from being activated by voice. |

<a id="wn11-cc-000005"></a>

## WN11-CC-000005 — Camera access from the lock screen must be disabled.

- Group: `V-253350`; rule revision: `SV-253350r958478_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the device does not have a camera, this is NA.

If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\Personalization\

Value Name: NoLockScreenCamera

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
If the device does not have a camera, this is NA.

Configure the policy value for Computer Configuration >> Administrative Templates >> Control Panel >> Personalization >> "Prevent enabling lock screen camera" to "Enabled".
~~~~~


<a id="wn11-cc-000007"></a>

## WN11-CC-000007 — Windows 11 must cover or disable the built-in or attached camera when not in use.

- Group: `V-253351`; rule revision: `SV-253351r1106508_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the device or operating system does not have a camera installed, this requirement is not applicable.

This requirement is not applicable to mobile devices (smartphones and tablets), where the use of the camera is a local authorizing official (AO) decision.

This requirement is not applicable to dedicated VTC suites located in approved VTC locations that are centrally managed.

For an external camera, if there is not a method for the operator to manually disconnect camera at the end of collaborative computing sessions, this is a finding.

For a built-in camera, the camera must be protected by a camera cover (e.g. laptop camera cover slide) when not in use. If the built-in camera is not protected with a camera cover, or if the built-in
camera is not disabled in the bios, this is a finding.

If the camera is not disconnected or covered, the following registry entry is required:

Registry Hive: HKEY_LOCAL_MACHINE
RegistryPath\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam

Value Name: Value                                                                             Value Data: Deny

If "Value Name" is set to a value other than "Deny" and the collaborative computing device has not been authorized for use, this is a finding.
~~~~~

### Source fix text

~~~~~text
If the camera is not disconnected or covered, the following registry entry is required.

Registry Hive: HKEY_LOCAL_MACHINE
RegistryPath\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam

Value Name: Value                                                                            Value Data: Deny
~~~~~


<a id="wn11-cc-000010"></a>

## WN11-CC-000010 — The display of slide shows on the lock screen must be disabled.

- Group: `V-253352`; rule revision: `SV-253352r958478_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\Personalization\

Value Name: NoLockScreenSlideshow

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Control Panel >> Personalization >> "Prevent enabling lock screen slide show" to "Enabled".
~~~~~


<a id="wn11-cc-000020"></a>

## WN11-CC-000020 — IPv6 source routing must be configured to highest protection.

- Group: `V-253353`; rule revision: `SV-253353r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Services\Tcpip6\Parameters\

Value Name: DisableIpSourceRouting

Value Type: REG_DWORD
Value: 2
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> MSS (Legacy) >> "MSS: (DisableIPSourceRouting IPv6) IP source routing protection level (protects against packet spoofing)" to "Highest protection, source routing is completely disabled".

This policy setting requires the installation of the MSS-Legacy custom templates included with the STIG package. "MSS-Legacy.admx" and "MSS-Legacy.adml" must be copied to the \Windows\PolicyDefinitions and \Windows\PolicyDefinitions\en-US directories respectively.
~~~~~


<a id="wn11-cc-000025"></a>

## WN11-CC-000025 — The system must be configured to prevent IP source routing.

- Group: `V-253354`; rule revision: `SV-253354r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\

Value Name: DisableIPSourceRouting

Value Type: REG_DWORD
Value: 2
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> MSS (Legacy) >> "MSS: (DisableIPSourceRouting) IP source routing protection level (protects against packet spoofing)" to "Highest protection, source routing is completely disabled".

This policy setting requires the installation of the MSS-Legacy custom templates included with the STIG package. "MSS-Legacy.admx" and "MSS-Legacy.adml" must be copied to the \Windows\PolicyDefinitions and \Windows\PolicyDefinitions\en-US directories respectively.
~~~~~


<a id="wn11-cc-000030"></a>

## WN11-CC-000030 — The system must be configured to prevent Internet Control Message Protocol (ICMP) redirects from overriding Open Shortest Path First (OSPF) generated routes.

- Group: `V-253355`; rule revision: `SV-253355r1268251_rule`; source severity: **low**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\

Value Name: EnableICMPRedirect

Value Type: REG_DWORD
Value: 0
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> MSS (Legacy) >> "MSS: (EnableICMPRedirect) Allow ICMP redirects to override OSPF generated routes" to "Disabled".

This policy setting requires the installation of the MSS-Legacy custom templates included with the STIG package. "MSS-Legacy.admx" and "MSS-Legacy.adml" must be copied to the \Windows\PolicyDefinitions and \Windows\PolicyDefinitions\en-US directories respectively.
~~~~~


<a id="wn11-cc-000035"></a>

## WN11-CC-000035 — The system must be configured to ignore NetBIOS name release requests except from WINS servers.

- Group: `V-253356`; rule revision: `SV-253356r958902_rule`; source severity: **low**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Services\Netbt\Parameters\

Value Name: NoNameReleaseOnDemand

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> MSS (Legacy) >> "MSS: (NoNameReleaseOnDemand) Allow the computer to ignore NetBIOS name release requests except from WINS servers" to "Enabled".

This policy setting requires the installation of the MSS-Legacy custom templates included with the STIG package. "MSS-Legacy.admx" and "MSS-Legacy.adml" must be copied to the \Windows\PolicyDefinitions and \Windows\PolicyDefinitions\en-US directories respectively.
~~~~~


<a id="wn11-cc-000037"></a>

## WN11-CC-000037 — Local administrator accounts must have their privileged token filtered to prevent elevated privileges from being used over the network on domain systems.

- Group: `V-253357`; rule revision: `SV-253357r958518_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the system is not a member of a domain, this is NA.

If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\

Value Name: LocalAccountTokenFilterPolicy

Value Type: REG_DWORD
Value: 0x00000000 (0)
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> MS Security Guide >> "Apply UAC restrictions to local accounts on network logons" to "Enabled".

This policy setting requires the installation of the SecGuide custom templates included with the STIG package. "SecGuide.admx" and "SecGuide.adml" must be copied to the \Windows\PolicyDefinitions and \Windows\PolicyDefinitions\en-US directories respectively.
~~~~~


<a id="wn11-cc-000038"></a>

## WN11-CC-000038 — WDigest Authentication must be disabled.

- Group: `V-253358`; rule revision: `SV-253358r958478_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Control\SecurityProviders\Wdigest\

Value Name: UseLogonCredential

Type: REG_DWORD
Value: 0x00000000 (0)
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> MS Security Guide >> "WDigest Authentication (disabling may require KB2871997)" to "Disabled".

The patch referenced in the policy title is not required for Windows 11.

This policy setting requires the installation of the SecGuide custom templates included with the STIG package. "SecGuide.admx" and "SecGuide.adml" must be copied to the \Windows\PolicyDefinitions and \Windows\PolicyDefinitions\en-US directories respectively.
~~~~~


<a id="wn11-cc-000039"></a>

## WN11-CC-000039 — Run as different user must be removed from context menus.

- Group: `V-253359`; rule revision: `SV-253359r958478_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry values do not exist or are not configured as specified, this is a finding.
The policy configures the same Value Name, Type and Value under four different registry paths.

Registry Hive: HKEY_LOCAL_MACHINE
Registry Paths:
\SOFTWARE\Classes\batfile\shell\runasuser\
\SOFTWARE\Classes\cmdfile\shell\runasuser\
\SOFTWARE\Classes\exefile\shell\runasuser\
\SOFTWARE\Classes\mscfile\shell\runasuser\

Value Name: SuppressionPolicy

Type: REG_DWORD
Value: 0x00001000 (4096)
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> MS Security Guide >> "Remove "Run as Different User" from context menus" to "Enabled".

This policy setting requires the installation of the SecGuide custom templates included with the STIG package. "SecGuide.admx" and "SecGuide.adml" must be copied to the \Windows\PolicyDefinitions and \Windows\PolicyDefinitions\en-US directories respectively.
~~~~~


<a id="wn11-cc-000040"></a>

## WN11-CC-000040 — Insecure logons to an SMB server must be disabled.

- Group: `V-253360`; rule revision: `SV-253360r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\LanmanWorkstation\

Value Name: AllowInsecureGuestAuth

Type: REG_DWORD
Value: 0x00000000 (0)
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Network >> Lanman Workstation >> "Enable insecure guest logons" to "Disabled".
~~~~~


<a id="wn11-cc-000044"></a>

## WN11-CC-000044 — Internet connection sharing must be disabled.

- Group: `V-253361`; rule revision: `SV-253361r958478_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\Network Connections\

Value Name: NC_ShowSharedAccessUI

Type: REG_DWORD
Value: 0x00000000 (0)
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Network >> Network Connections >> "Prohibit use of Internet Connection Sharing on your DNS domain network" to "Enabled".
~~~~~


<a id="wn11-cc-000050"></a>

## WN11-CC-000050 — Hardened UNC Paths must be defined to require mutual authentication and integrity for at least the \\*\SYSVOL and \\*\NETLOGON shares.

- Group: `V-253362`; rule revision: `SV-253362r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
This requirement is applicable to domain-joined systems, for standalone systems this is NA.

If the following registry values do not exist or are not configured as specified, this is a finding.

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\NetworkProvider\HardenedPaths\

Value Name: \\*\NETLOGON
Value Type: REG_SZ
Value: RequireMutualAuthentication=1, RequireIntegrity=1

Value Name: \\*\SYSVOL
Value Type: REG_SZ
Value: RequireMutualAuthentication=1, RequireIntegrity=1

Additional entries would not be a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Network >> Network Provider >> "Hardened UNC Paths" to "Enabled" with at least the following configured in "Hardened UNC Paths:" (click the "Show" button to display).

Value Name: \\*\SYSVOL
Value: RequireMutualAuthentication=1, RequireIntegrity=1

Value Name: \\*\NETLOGON
Value: RequireMutualAuthentication=1, RequireIntegrity=1
~~~~~


<a id="wn11-cc-000052"></a>

## WN11-CC-000052 — Windows 11 must be configured to prioritize ECC Curves with longer key lengths first.

- Group: `V-253363`; rule revision: `SV-253363r1268232_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Cryptography\Configuration\SSL\00010002\

Value Name: EccCurves

Value Type: REG_MULTI_SZ
Value: NistP384 NistP256
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Network >> SSL Configuration Settings >> "ECC Curve Order" to "Enabled" with "ECC Curve Order:" including the following in the order listed:

NistP384
NistP256
~~~~~


<a id="wn11-cc-000055"></a>

## WN11-CC-000055 — Simultaneous connections to the internet or a Windows domain must be limited.

- Group: `V-253364`; rule revision: `SV-253364r1268254_rule`; source severity: **medium**.

### Source check text

~~~~~text
The default behavior for "Minimize the number of simultaneous connections to the Internet or a Windows Domain" is "Enabled".

If it exists and is configured with a value of "0", this is a finding.

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\WcmSvc\GroupPolicy\

Value Name: fMinimizeConnections

Value Type: REG_DWORD
Value: 3 (or if the Value Name does not exist)
~~~~~

### Source fix text

~~~~~text
The default behavior for "Minimize the number of simultaneous connections to the Internet or a Windows Domain" is "Enabled".

If this needs to be corrected, configure the policy value for Computer Configuration >> Administrative Templates >> Network >> Windows Connection Manager >> "Minimize the number of simultaneous connections to the Internet or a Windows Domain" to "Enabled".  Under "Options", set "Minimize Policy Options" to "3 = Prevent Wi-Fi When on Ethernet".
~~~~~


<a id="wn11-cc-000060"></a>

## WN11-CC-000060 — Connections to non-domain networks when connected to a domain authenticated network must be blocked.

- Group: `V-253365`; rule revision: `SV-253365r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\WcmSvc\GroupPolicy\

Value Name: fBlockNonDomain

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Network >> Windows Connection Manager >> "Prohibit connection to non-domain networks when connected to domain authenticated network" to "Enabled".
~~~~~


<a id="wn11-cc-000066"></a>

## WN11-CC-000066 — Command line data must be included in process creation events.

- Group: `V-253367`; rule revision: `SV-253367r958422_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\Audit\

Value Name: ProcessCreationIncludeCmdLine_Enabled

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> System >> Audit Process Creation >> "Include command line in process creation events" to "Enabled".
~~~~~


<a id="wn11-cc-000068"></a>

## WN11-CC-000068 — Windows 11 must be configured to enable Remote host allows delegation of non-exportable credentials.

- Group: `V-253368`; rule revision: `SV-253368r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\CredentialsDelegation\

Value Name: AllowProtectedCreds

Type: REG_DWORD
Value: 0x00000001 (1)
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> System >> Credentials Delegation >> "Remote host allows delegation of non-exportable credentials" to "Enabled".
~~~~~


<a id="wn11-cc-000070"></a>

## WN11-CC-000070 — Virtualization-Based Security (VBS) must be enabled on Windows 11 with the platform security level configured to Secure Boot or Secure Boot with DMA Protection.

- Group: `V-253369`; rule revision: `SV-253369r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
Confirm VBS is enabled and running with Secure Boot or Secure Boot and DMA Protection.

If there are documented operational mission needs to disable VBS, this may be reduced to a CAT III finding.

Run "PowerShell" with elevated privileges (run as administrator).

Enter the following:

"Get-CimInstance -ClassName Win32_DeviceGuard -Namespace root\Microsoft\Windows\DeviceGuard"

If "RequiredSecurityProperties" does not include a value of "2" indicating "Secure Boot" (e.g., "{1, 2}"), this is a finding.

If "Secure Boot and DMA Protection" is configured, "3" will also be displayed in the results (e.g., "{1, 2, 3}").

If "VirtualizationBasedSecurityStatus" is not a value of "2" indicating "Running", this is a finding.

Alternately:

Run "System Information".

Under "System Summary", verify the following:

If "Device Guard virtualization-based security" does not display "Running", this is a finding.

If "Device Guard Required Security Properties" does not display "Base Virtualization Support, Secure Boot", this is a finding.

If "Secure Boot and DMA Protection" is configured, "DMA Protection" will also be displayed (e.g., "Base Virtualization Support, Secure Boot, DMA Protection").

The policy settings referenced in the Fix section will configure the following registry values. However, due to hardware requirements, the registry values alone do not ensure proper function.

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\DeviceGuard\

Value Name: EnableVirtualizationBasedSecurity
Value Type: REG_DWORD
Value: 1

Value Name: RequirePlatformSecurityFeatures
Value Type: REG_DWORD
Value: 1 (Secure Boot only) or 3 (Secure Boot and DMA Protection)

A Microsoft article on the Credential Guard system requirement can be found at the following link:

https://technet.microsoft.com/en-us/itpro/windows/keep-secure/credential-guard-requirements
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> System >> Device Guard >> "Turn On virtualization-based Security" to "Enabled" with "Secure Boot" or "Secure Boot and DMA Protection" selected for "Select Platform Security Level:".

A Microsoft article on Credential Guard system requirement can be found at the following link.
https://technet.microsoft.com/en-us/itpro/windows/keep-secure/credential-guard-requirements
~~~~~


<a id="wn11-cc-000075"></a>

## WN11-CC-000075 — Credential Guard must be running on Windows 11 systems.

- Group: `V-253370`; rule revision: `SV-253370r1268251_rule`; source severity: **high**.

### Source check text

~~~~~text
Confirm Credential Guard is running.

Run "PowerShell" with elevated privileges (run as administrator).

Enter the following:

"Get-CimInstance -ClassName Win32_DeviceGuard -Namespace root\Microsoft\Windows\DeviceGuard"

If "SecurityServicesRunning" does not include a value of "1" (e.g., "{1, 2}"), this is a finding.

Alternately:

Run "System Information".

Under "System Summary", verify the following:

If "virtualization-based Services Running" does not list "Credential Guard", this is a finding.

The policy settings referenced in the Fix section will configure the following registry value. However, due to hardware requirements, the registry value alone does not ensure proper function.

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\DeviceGuard\

Value Name: LsaCfgFlags
Value Type: REG_DWORD
Value: 0x00000001 (1) (Enabled with UEFI lock)
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> System >> Device Guard >> "Turn On virtualization-based Security" to "Enabled" with "Enabled with UEFI lock" selected for "Credential Guard Configuration:".

A Microsoft TechNet article on Credential Guard, including system requirement details, can be found at the following link:

https://docs.microsoft.com/en-us/windows/access-protection/credential-guard/credential-guard
~~~~~


<a id="wn11-cc-000080"></a>

## WN11-CC-000080 — Virtualization-based protection of code integrity must be enabled.

- Group: `V-253371`; rule revision: `SV-253371r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
Confirm virtualization-based protection of code integrity.

If there are documented operational mission needs to disable code integrity, this may be reduced to a CAT II finding.

Run "PowerShell" with elevated privileges (run as administrator).

Enter the following:

"Get-CimInstance -ClassName Win32_DeviceGuard -Namespace root\Microsoft\Windows\DeviceGuard"

If "SecurityServicesRunning" does not include a value of "2" (e.g., "{1, 2}"), this is a finding.

Alternately:

Run "System Information".

Under "System Summary", verify the following:

If "Virtualization-based Security Services Running" does not list "Hypervisor enforced Code Integrity", this is a finding.

The policy settings referenced in the Fix section will configure the following registry value. However, due to hardware requirements, the registry value alone does not ensure proper function.

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\DeviceGuard\

Value Name: HypervisorEnforcedCodeIntegrity
Value Type: REG_DWORD
Value: 0x00000001 (1) (Enabled with UEFI lock), or 0x00000002 (2) (Enabled without lock)
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> System >> Device Guard >> "Turn On virtualization-based Security" to "Enabled" with "Enabled with UEFI lock" or "Enabled without lock" selected for "virtualization-based Protection of Code Integrity:".

"Enabled with UEFI lock" is preferred as more secure; however, it cannot be turned off remotely through a group policy change if there is an issue.

"Enabled without lock" will allow this to be turned off remotely while testing for issues.
~~~~~


<a id="wn11-cc-000085"></a>

## WN11-CC-000085 — Early Launch Antimalware, Boot-Start Driver Initialization Policy must prevent boot drivers.

- Group: `V-253372`; rule revision: `SV-253372r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
The default behavior is for Early Launch Antimalware - Boot-Start Driver Initialization policy is to enforce "Good, unknown and bad but critical" (preventing "bad").

If the registry value name below does not exist, this is a finding.

If it exists and is configured with a value of "7", this is a finding.

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Policies\EarlyLaunch\

Value Name: DriverLoadPolicy

Value Type: REG_DWORD
Value: 1, 3, or 8

Possible values for this setting are:
8 - Good only
1 - Good and unknown
3 - Good, unknown and bad but critical
7 - All (which includes "Bad" and would be a finding)
~~~~~

### Source fix text

~~~~~text
Ensure that Early Launch Antimalware - Boot-Start Driver Initialization policy is set to enforce "Good, unknown and bad but critical" (preventing "bad").

To correct this, configure the policy value for Computer Configuration >> Administrative Templates >> System >> Early Launch Antimalware >> "Boot-Start Driver Initialization Policy" to "Enabled with "Good, unknown and bad but critical" selected.
~~~~~


<a id="wn11-cc-000090"></a>

## WN11-CC-000090 — Group Policy objects must be reprocessed even if they have not changed.

- Group: `V-253373`; rule revision: `SV-253373r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\Group Policy\{35378EAC-683F-11D2-A89A-00C04FBBCFA2}

Value Name: NoGPOListChanges

Value Type: REG_DWORD
Value: 0
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> System >> Group Policy >> "Configure registry policy processing" to "Enabled" and select the option "Process even if the Group Policy objects have not changed".
~~~~~


<a id="wn11-cc-000100"></a>

## WN11-CC-000100 — Downloading print driver packages over HTTP must be prevented.

- Group: `V-253374`; rule revision: `SV-253374r958478_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows NT\Printers\

Value Name: DisableWebPnPDownload

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> System >> Internet Communication Management >> Internet Communication settings >> "Turn off downloading of print drivers over HTTP" to "Enabled".
~~~~~


<a id="wn11-cc-000105"></a>

## WN11-CC-000105 — Web publishing and online ordering wizards must be prevented from downloading a list of providers.

- Group: `V-253375`; rule revision: `SV-253375r958478_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\

Value Name: NoWebServices

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> System >> Internet Communication Management >> Internet Communication settings >> "Turn off Internet download for Web publishing and online ordering wizards" to "Enabled".
~~~~~


<a id="wn11-cc-000110"></a>

## WN11-CC-000110 — Printing over HTTP must be prevented.

- Group: `V-253376`; rule revision: `SV-253376r958478_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows NT\Printers\

Value Name: DisableHTTPPrinting

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> System >> Internet Communication Management >> Internet Communication settings >> "Turn off printing over HTTP" to "Enabled".
~~~~~


<a id="wn11-cc-000115"></a>

## WN11-CC-000115 — Systems must at least attempt device authentication using certificates.

- Group: `V-253377`; rule revision: `SV-253377r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
This requirement is applicable to domain-joined systems, for standalone systems this is NA.

The default behavior for "Support device authentication using certificate" is "Automatic".

If it exists and is configured with a value of "0", this is a finding.

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\Kerberos\Parameters\

Value Name: DevicePKInitEnabled
Value Type: REG_DWORD
Value: 1 (or if the Value Name does not exist)
~~~~~

### Source fix text

~~~~~text
This requirement is applicable to domain-joined systems, for standalone systems this is NA.

The default behavior for "Support device authentication using certificate" is "Automatic".

To correct this, configured the policy value for Computer Configuration >> Administrative Templates >> System >> Kerberos >> "Support device authentication using certificate" to "Not Configured or "Enabled" with either option selected in "Device authentication behavior using certificate:".
~~~~~


<a id="wn11-cc-000120"></a>

## WN11-CC-000120 — The network selection user interface (UI) must not be displayed on the logon screen.

- Group: `V-253378`; rule revision: `SV-253378r958478_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\System\

Value Name: DontDisplayNetworkSelectionUI

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> System >> Logon >> "Do not display network selection UI" to "Enabled".
~~~~~


<a id="wn11-cc-000130"></a>

## WN11-CC-000130 — Local users on domain-joined computers must not be enumerated.

- Group: `V-253379`; rule revision: `SV-253379r958478_rule`; source severity: **medium**.

### Source check text

~~~~~text
This requirement is applicable to domain-joined systems, for standalone systems this is NA.

If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\System\

Value Name: EnumerateLocalUsers

Value Type: REG_DWORD
Value: 0
~~~~~

### Source fix text

~~~~~text
This requirement is applicable to domain-joined systems, for standalone systems this is NA.

Configure the policy value for Computer Configuration >> Administrative Templates >> System >> Logon >> "Enumerate local users on domain-joined computers" to "Disabled".
~~~~~


<a id="wn11-cc-000145"></a>

## WN11-CC-000145 — Users must be prompted for a password on resume from sleep (on battery).

- Group: `V-253380`; rule revision: `SV-253380r1051049_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Power\PowerSettings\0e796bdb-100d-47d6-a2d5-f7d2daa51f51\

Value Name: DCSettingIndex

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> System >> Power Management >> Sleep Settings >> "Require a password when a computer wakes (on battery)" to "Enabled".
~~~~~


<a id="wn11-cc-000150"></a>

## WN11-CC-000150 — The user must be prompted for a password on resume from sleep (plugged in).

- Group: `V-253381`; rule revision: `SV-253381r1051050_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Power\PowerSettings\0e796bdb-100d-47d6-a2d5-f7d2daa51f51\

Value Name: ACSettingIndex

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> System >> Power Management >> Sleep Settings >> "Require a password when a computer wakes (plugged in)" to "Enabled".
~~~~~


<a id="wn11-cc-000155"></a>

## WN11-CC-000155 — Solicited Remote Assistance must not be allowed.

- Group: `V-253382`; rule revision: `SV-253382r1268233_rule`; source severity: **high**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows NT\Terminal Services\

Value Name: fAllowToGetHelp

Value Type: REG_DWORD
Value: 0
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> System >> Remote Assistance >> "Configure Solicited Remote Assistance" to "Disabled".
~~~~~


<a id="wn11-cc-000165"></a>

## WN11-CC-000165 — Unauthenticated RPC clients must be restricted from connecting to the RPC server.

- Group: `V-253383`; rule revision: `SV-253383r971545_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows NT\Rpc\

Value Name: RestrictRemoteClients

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> System >> Remote Procedure Call >> "Restrict Unauthenticated RPC clients" to "Enabled" and "Authenticated".
~~~~~


<a id="wn11-cc-000170"></a>

## WN11-CC-000170 — The setting to allow Microsoft accounts to be optional for modern style apps must be enabled.

- Group: `V-253384`; rule revision: `SV-253384r1268251_rule`; source severity: **low**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\

Value Name: MSAOptional

Value Type: REG_DWORD
Value: 0x00000001 (1)
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> App Runtime >> "Allow Microsoft accounts to be optional" to "Enabled".
~~~~~


<a id="wn11-cc-000175"></a>

## WN11-CC-000175 — The Application Compatibility Program Inventory must be prevented from collecting data and sending the information to Microsoft.

- Group: `V-253385`; rule revision: `SV-253385r958478_rule`; source severity: **low**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\AppCompat\

Value Name: DisableInventory

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Application Compatibility >> "Turn off Inventory Collector" to "Enabled".
~~~~~


<a id="wn11-cc-000180"></a>

## WN11-CC-000180 — Autoplay must be turned off for non-volume devices.

- Group: `V-253386`; rule revision: `SV-253386r958804_rule`; source severity: **high**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\Explorer\

Value Name: NoAutoplayfornonVolume

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> AutoPlay Policies >> "Disallow Autoplay for non-volume devices" to "Enabled".
~~~~~


<a id="wn11-cc-000185"></a>

## WN11-CC-000185 — The default autorun behavior must be configured to prevent autorun commands.

- Group: `V-253387`; rule revision: `SV-253387r958804_rule`; source severity: **high**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\

Value Name: NoAutorun

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> AutoPlay Policies >> "Set the default behavior for AutoRun" to "Enabled:Do not execute any autorun commands".
~~~~~


<a id="wn11-cc-000190"></a>

## WN11-CC-000190 — Autoplay must be disabled for all drives.

- Group: `V-253388`; rule revision: `SV-253388r958804_rule`; source severity: **high**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Microsoft\Windows\CurrentVersion\policies\Explorer\

Value Name: NoDriveTypeAutoRun

Value Type: REG_DWORD
Value: 0x000000ff (255)

Note: If the value for NoDriveTypeAutorun is entered manually, it must be entered as "ff" when Hexadecimal is selected, or "255" with Decimal selected. Using the policy value specified in the Fix section will enter it correctly.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> AutoPlay Policies >> "Turn off AutoPlay" to "Enabled:All Drives".
~~~~~


<a id="wn11-cc-000195"></a>

## WN11-CC-000195 — Enhanced anti-spoofing for facial recognition must be enabled on Windows 11.

- Group: `V-253389`; rule revision: `SV-253389r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Biometrics\FacialFeatures\   (For GPO-managed systems)
Or
Registry Path: \SOFTWARE\Microsoft\Policies\PassportForWork\Biometrics\   (For Intune-managed systems)

Value Name: EnhancedAntiSpoofing
Or
Value Name: FacialFeaturesUseEnhancedAntiSpoofing  (For Intune-managed systems)

Value Type: REG_DWORD
Value: 0x00000001 (1)
~~~~~

### Source fix text

~~~~~text
For GPO-managed systems:

Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Biometrics >> Facial Features >> "Configure enhanced anti-spoofing" to "Enabled".

For Intune-managed systems:

Revise the Intune policy to enable enhanced anti-spoofing for Facial Features.
~~~~~


<a id="wn11-cc-000200"></a>

## WN11-CC-000200 — Administrator accounts must not be enumerated during elevation.

- Group: `V-253391`; rule revision: `SV-253391r958518_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\CredUI\

Value Name: EnumerateAdministrators

Value Type: REG_DWORD
Value: 0
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Credential User Interface >> "Enumerate administrator accounts on elevation" to "Disabled".
~~~~~


<a id="wn11-cc-000204"></a>

## WN11-CC-000204 — Enhanced diagnostic data must be limited to the minimum required to support Windows Analytics.

- Group: `V-253392`; rule revision: `SV-253392r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
If "Enhanced" level is enabled for telemetry, this must be configured. If "Security" or "Basic" are configured, this is NA. (See WN11-CC-000205).

If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\DataCollection\

Value Name: LimitEnhancedDiagnosticDataWindowsAnalytics

Type: REG_DWORD
Value: 0x00000001 (1)
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Data Collection and Preview Builds >> "Limit optional diagnostic data for Windows Analytics" to "Enabled" with "Enable Desktop Analytics collection" selected in "Options:".
~~~~~


<a id="wn11-cc-000205"></a>

## WN11-CC-000205 — Windows Telemetry must not be configured to Full.

- Group: `V-253393`; rule revision: `SV-253393r1256676_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\DataCollection\

Value Name: AllowTelemetry

Type: REG_DWORD
Value: 0x00000000 (0) (Security)
0x00000001 (1) (Basic)
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Data Collection and Preview Builds >> "Allow Diagnostic Data" to "Enabled" with "Send required diagnostic data" selected in "Options:".
~~~~~


<a id="wn11-cc-000206"></a>

## WN11-CC-000206 — Windows Update must not obtain updates from other PCs on the internet.

- Group: `V-253394`; rule revision: `SV-253394r1268251_rule`; source severity: **low**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\DeliveryOptimization\

Value Type: REG_DWORD
Value: 0x00000000 (0) - No peering (HTTP Only)
0x00000001 (1) - Peers on same NAT only (LAN)
0x00000002 (2) - Local Network / Private group peering (Group)
0x00000063 (99) - Simple download mode, no peering (Simple)
0x00000064 (100) - Bypass mode, Delivery Optimization not used (Bypass)

A value of 0x00000003 (3), Internet, is a finding.

Standalone systems (configured in Settings):

If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Microsoft\Windows\CurrentVersion\DeliveryOptimization\Config\

Value Name: DODownloadMode

Value Type: REG_DWORD
Value: 0x00000000 (0) - Off
0x00000001 (1) - LAN
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Delivery Optimization >> "Download Mode" to "Enabled" with any option except "Internet" selected.

Acceptable selections include:
Bypass (100)
Group (2)
HTTP only (0)
LAN (1)
Simple (99)
~~~~~


<a id="wn11-cc-000210"></a>

## WN11-CC-000210 — The Microsoft Defender SmartScreen for Explorer must be enabled.

- Group: `V-253395`; rule revision: `SV-253395r958478_rule`; source severity: **medium**.

### Source check text

~~~~~text
This is applicable to unclassified systems, for other systems this is NA.

If the following registry values do not exist or are not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\System\

Value Name: EnableSmartScreen

Value Type: REG_DWORD
Value: 0x00000001 (1)

And

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\System\

Value Name: ShellSmartScreenLevel

Value Type: REG_SZ
Value: Block
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> File Explorer >> "Configure Windows Defender SmartScreen" to "Enabled" with "Warn and prevent bypass" selected.

Windows 11 includes duplicate policies for this setting. It can also be configured under Computer Configuration >> Administrative Templates >> Windows Components >> Windows Defender SmartScreen >> Explorer.
~~~~~


<a id="wn11-cc-000215"></a>

## WN11-CC-000215 — Explorer Data Execution Prevention must be enabled.

- Group: `V-253396`; rule revision: `SV-253396r958928_rule`; source severity: **medium**.

### Source check text

~~~~~text
The default behavior is for data execution prevention to be turned on for file explorer.

If it exists and is configured with a value of "1", this is a finding.

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\Explorer\

Value Name: NoDataExecutionPrevention

Value Type: REG_DWORD
Value: 0 (or if the Value Name does not exist)
~~~~~

### Source fix text

~~~~~text
The default behavior is for data execution prevention to be turned on for file explorer.

To correct this, configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> File Explorer >> "Turn off Data Execution Prevention for Explorer" to "Not Configured" or "Disabled".
~~~~~


<a id="wn11-cc-000220"></a>

## WN11-CC-000220 — File Explorer heap termination on corruption must be disabled.

- Group: `V-253397`; rule revision: `SV-253397r958902_rule`; source severity: **low**.

### Source check text

~~~~~text
The default behavior is for File Explorer heap termination on corruption to be enabled.

If it exists and is configured with a value of "1", this is a finding.

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\Explorer\

Value Name: NoHeapTerminationOnCorruption

Value Type: REG_DWORD
Value: 0x00000000 (0) (or if the Value Name does not exist)
~~~~~

### Source fix text

~~~~~text
The default behavior is for File Explorer heap termination on corruption to be enabled.

To correct this, configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> File Explorer >> "Turn off heap termination on corruption" to "Not Configured" or "Disabled".
~~~~~


<a id="wn11-cc-000225"></a>

## WN11-CC-000225 — File Explorer shell protocol must run in protected mode.

- Group: `V-253398`; rule revision: `SV-253398r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
The default behavior is for shell protected mode to be turned on for file explorer.

If it exists and is configured with a value of "1", this is a finding.

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\

Value Name: PreXPSP2ShellProtocolBehavior

Value Type: REG_DWORD
Value: 0 (or if the Value Name does not exist)
~~~~~

### Source fix text

~~~~~text
The default behavior is for shell protected mode to be turned on for file explorer.

To correct this, configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> File Explorer >> "Turn off shell protocol protected mode" to "Not Configured" or "Disabled".
~~~~~


<a id="wn11-cc-000252"></a>

## WN11-CC-000252 — Windows 11 must be configured to disable Windows Game Recording and Broadcasting.

- Group: `V-253399`; rule revision: `SV-253399r1259989_rule`; source severity: **medium**.

### Source check text

~~~~~text
This is NA for Windows 11 LTSC.

If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\GameDVR\  (For GPO-managed systems)
Or
Registry Path: \SOFTWARE\Microsoft\PolicyManager\current\device\ApplicationManagement  (For Intune-managed systems)

Value Name: AllowGameDVR

Type: REG_DWORD
Value: 0x00000000 (0)
~~~~~

### Source fix text

~~~~~text
For GPO-managed systems:
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Windows Game Recording and Broadcasting >> "Enables or disables Windows Game Recording and Broadcasting" to "Disabled".

For Intune-managed systems:
Revise the Intune policy to disable Windows Game Recording and Broadcasting.
~~~~~


<a id="wn11-cc-000255"></a>

## WN11-CC-000255 — The use of a hardware security device with Windows Hello for Business must be enabled.

- Group: `V-253400`; rule revision: `SV-253400r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
Virtual desktop implementations currently may not support the use of TPMs. For virtual desktop implementations where the virtual desktop instance is deleted or refreshed upon logoff, this is NA.

If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\PassportForWork\

Value Name: RequireSecurityDevice

Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Windows Hello for Business >> "Use a hardware security device" to "Enabled".
~~~~~


<a id="wn11-cc-000260"></a>

## WN11-CC-000260 — Windows 11 must be configured to require a minimum PIN length of six characters or greater.

- Group: `V-253401`; rule revision: `SV-253401r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\PassportForWork\PINComplexity\  (For GPO-managed systems)
Or
Registry Path: \SOFTWARE\Microsoft\Policies\PassportForWork\[guid]\device\policies\PINComplexity  (For Intune-managed systems)

Value Name: MinimumPINLength

Type: REG_DWORD
Value: 6 (or greater)
~~~~~

### Source fix text

~~~~~text
For GPO-managed systems:

Configure the policy value for Computer Configuration >> Administrative Templates >> System >> PIN Complexity >> "Minimum PIN length" to "6" or greater.

For Intune-managed systems:

Revise the Intune policy to set the minimum PIN length to "6" or greater.
~~~~~


<a id="wn11-cc-000270"></a>

## WN11-CC-000270 — Passwords must not be saved in the Remote Desktop Client.

- Group: `V-253402`; rule revision: `SV-253402r1051051_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows NT\Terminal Services\

Value Name: DisablePasswordSaving

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Remote Desktop Services >> Remote Desktop Connection Client >> "Do not allow passwords to be saved" to "Enabled".
~~~~~


<a id="wn11-cc-000275"></a>

## WN11-CC-000275 — Local drives must be prevented from sharing with Remote Desktop Session Hosts.

- Group: `V-253403`; rule revision: `SV-253403r1268233_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows NT\Terminal Services\

Value Name: fDisableCdm

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Remote Desktop Services >> Remote Desktop Session Host >> Device and Resource Redirection >> "Do not allow drive redirection" to "Enabled".
~~~~~


<a id="wn11-cc-000280"></a>

## WN11-CC-000280 — Remote Desktop Services must always prompt a client for passwords upon connection.

- Group: `V-253404`; rule revision: `SV-253404r1051052_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows NT\Terminal Services\

Value Name: fPromptForPassword

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Remote Desktop Services >> Remote Desktop Session Host >> Security >> "Always prompt for password upon connection" to "Enabled".
~~~~~


<a id="wn11-cc-000285"></a>

## WN11-CC-000285 — The Remote Desktop Session Host must require secure RPC communications.

- Group: `V-253405`; rule revision: `SV-253405r1268237_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows NT\Terminal Services\

Value Name: fEncryptRPCTraffic

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Remote Desktop Services >> Remote Desktop Session Host >> Security "Require secure RPC communication" to "Enabled".
~~~~~


<a id="wn11-cc-000290"></a>

## WN11-CC-000290 — Remote Desktop Services must be configured with the client connection encryption set to the required level.

- Group: `V-253406`; rule revision: `SV-253406r1268222_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows NT\Terminal Services\

Value Name: MinEncryptionLevel

Value Type: REG_DWORD
Value: 3
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Remote Desktop Services >> Remote Desktop Session Host >> Security >> "Set client connection encryption level" to "Enabled" and "High Level".
~~~~~


<a id="wn11-cc-000295"></a>

## WN11-CC-000295 — Attachments must be prevented from being downloaded from RSS feeds.

- Group: `V-253407`; rule revision: `SV-253407r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Internet Explorer\Feeds\

Value Name: DisableEnclosureDownload

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> RSS Feeds >> "Prevent downloading of enclosures" to "Enabled".
~~~~~


<a id="wn11-cc-000300"></a>

## WN11-CC-000300 — Basic authentication for RSS feeds over HTTP must not be used.

- Group: `V-253408`; rule revision: `SV-253408r958478_rule`; source severity: **medium**.

### Source check text

~~~~~text
The default behavior is for the Windows RSS platform to not use Basic authentication over HTTP connections.

If it exists and is configured with a value of "1", this is a finding.

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Internet Explorer\Feeds\

Value Name: AllowBasicAuthInClear

Value Type: REG_DWORD
Value: 0 (or if the Value Name does not exist)
~~~~~

### Source fix text

~~~~~text
The default behavior is for the Windows RSS platform to not use Basic authentication over HTTP connections.

To correct this, configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> RSS Feeds >> "Turn on Basic feed authentication over HTTP" to "Not Configured" or "Disabled".
~~~~~


<a id="wn11-cc-000305"></a>

## WN11-CC-000305 — Indexing of encrypted files must be turned off.

- Group: `V-253409`; rule revision: `SV-253409r1210297_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\Windows Search\  (For GPO-managed systems)
Or
Registry Path: \Software\Microsoft\Policymanager\current\device\search  (For Intune-managed systems)

Value Name: AllowIndexingEncryptedStoresOrItems

Value Type: REG_DWORD
Value: 0
~~~~~

### Source fix text

~~~~~text
For GPO-managed systems:

Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Search >> "Allow indexing of encrypted files" to "Disabled".

For Intune-managed systems:

Revise the Intune policy to disable indexing of encrypted files.
~~~~~


<a id="wn11-cc-000310"></a>

## WN11-CC-000310 — Users must be prevented from changing installation options.

- Group: `V-253410`; rule revision: `SV-253410r1051053_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\Installer\

Value Name: EnableUserControl

Value Type: REG_DWORD
Value: 0
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Windows Installer >> "Allow user control over installs" to "Disabled".
~~~~~


<a id="wn11-cc-000315"></a>

## WN11-CC-000315 — The Windows Installer feature "Always install with elevated privileges" must be disabled.

- Group: `V-253411`; rule revision: `SV-253411r1051054_rule`; source severity: **high**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\Installer\

Value Name: AlwaysInstallElevated

Value Type: REG_DWORD
Value: 0
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Windows Installer >> "Always install with elevated privileges" to "Disabled".
~~~~~


<a id="wn11-cc-000320"></a>

## WN11-CC-000320 — Users must be notified if a web-based program attempts to install software.

- Group: `V-253412`; rule revision: `SV-253412r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
The default behavior is for Internet Explorer to warn users and select whether to allow or refuse installation when a web-based program attempts to install software on the system.

If it exists and is configured with a value of "1", this is a finding.

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\Installer\

Value Name: SafeForScripting

Value Type: REG_DWORD
Value: 0 (or if the Value Name does not exist)
~~~~~

### Source fix text

~~~~~text
The default behavior is for Internet Explorer to warn users and select whether to allow or refuse installation when a web-based program attempts to install software on the system.

To correct this, configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Windows Installer >> "Prevent Internet Explorer security prompt for Windows Installer scripts" to "Not Configured" or "Disabled".
~~~~~


<a id="wn11-cc-000325"></a>

## WN11-CC-000325 — Automatically signing in the last interactive user after a system-initiated restart must be disabled.

- Group: `V-253413`; rule revision: `SV-253413r991591_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\

Value Name: DisableAutomaticRestartSignOn

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Windows Logon Options >> "Sign-in last interactive user automatically after a system-initiated restart" to "Disabled".
~~~~~


<a id="wn11-cc-000326"></a>

## WN11-CC-000326 — PowerShell script block logging must be enabled on Windows 11.

- Group: `V-253414`; rule revision: `SV-253414r958422_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging\

Value Name: EnableScriptBlockLogging

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Windows PowerShell >> "Turn on PowerShell Script Block Logging" to "Enabled".
~~~~~


<a id="wn11-cc-000327"></a>

## WN11-CC-000327 — PowerShell Transcription must be enabled on Windows 11.

- Group: `V-253415`; rule revision: `SV-253415r1259992_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\PowerShell\Transcription\

Value Name: EnableTranscripting

Value Type: REG_DWORD
Value: 1

The location used for log storage must be a write-only, restricted directory (preferably a network share) that security personnel can access. The registry value setting for "Transcript output directory" is set by the GPO to "C:\ProgramData\PS_Transcript". That directory allows Read, Modify, and Delete access by standard (nonprivileged) user accounts. Either a different directory that has appropriate access permissions must be configured (see Fix text), or the permissions for the existing Transcript output directory must be configured appropriately.

If the directory used to store the PowerShell transcription log files (Transcript output directory) permits read or modify access by nonprivileged users, this is a finding.

If the output directory set by the GPO is preferred, the access permissions must be revised to ensure the PowerShell Transcription log files are accessible only to the Administrator and System accounts.

To review permissions of the output directory, enter the following commands.
Open "Command Prompt (Admin)".

[Enter "icacls" followed by the directory configured to store PowerShell Transcription logs:]
icacls C:\ProgramData\PS_Transcript

If log files currently reside in the output directory, issue the following:
icacls C:\ProgramData\PS_Transcript\*.*

The results must be displayed as below:
NT AUTHORITY\SYSTEM:(OI)(CI)(IO)(F)
BUILTIN\Administrators:(OI)(CI)(IO)(F)
*NT AUTHORITY\Authenticated Users:(OI)(CI)(WD,AD)
*BUILTIN\Users:(OI)(CI)(WD,AD)
*Note: The standard user accounts may differ based on the system's purpose/role and Active Directory structure.

If the directory used to store PowerShell Transcription logs is not configured to provide Full Control access to Administrative and System accounts while permitting write-only access for standard user accounts, this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Windows PowerShell >> "Turn on PowerShell Transcription" to "Enabled".

If a centralized (versus local) Transcript output directory is preferred, configure the Transcript output directory to point to a Central Log Server or another secure location to prevent user Read, Modify, and Delete access by nonprivileged accounts.

Ensure the selected directory is write-only with Full Control access granted to Administrator and System accounts.

Enter the following registry value:
Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\PowerShell\Transcription
*Value Name: OutputDirectory
Value Type: REG_SZ (String Value)

* Note: "OutputDirectory" value should be: "[custom directory path (e.g., I:\UserX_PowerShellTranscripts)]"

If the folder configured (in the registry) as the Transcript output directory is not configured to provide Full Control access to Administrative and System accounts, while permitting WD, AD access for standard user accounts, issue the following commands:
Open "Command Prompt (Admin)".
1. If the directory configured to store PowerShell Transcription logs does not exist:
mkdir C:\ProgramData\PS_Transcript
2. Assign appropriate permissions to Administrators group and System account:
icacls "C:\ProgramData\PS_Transcript" /inheritance:r /grant:r "Administrators:(OI)(CI)(F)" /grant:r "SYSTEM":(OI)(CI)(F)
3. Assign appropriate permissions to user groups:
icacls "C:\ProgramData\PS_Transcript" /grant:r "Users":(OI)(CI)(WD,AD) /t /c
icacls "C:\ProgramData\PS_Transcript" /grant:r "Authenticated Users":(OI)(CI)(WD,AD) /t /c
~~~~~


<a id="wn11-cc-000330"></a>

## WN11-CC-000330 — The Windows Remote Management (WinRM) client must not use Basic authentication.

- Group: `V-253416`; rule revision: `SV-253416r958510_rule`; source severity: **high**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\WinRM\Client\

Value Name: AllowBasic

Value Type: REG_DWORD
Value: 0
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Windows Remote Management (WinRM) >> WinRM Client >> "Allow Basic authentication" to "Disabled".
~~~~~


<a id="wn11-cc-000335"></a>

## WN11-CC-000335 — The Windows Remote Management (WinRM) client must not allow unencrypted traffic.

- Group: `V-253417`; rule revision: `SV-253417r958848_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\WinRM\Client\

Value Name: AllowUnencryptedTraffic

Value Type: REG_DWORD
Value: 0
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Windows Remote Management (WinRM) >> WinRM Client >> "Allow unencrypted traffic" to "Disabled".
~~~~~


<a id="wn11-cc-000345"></a>

## WN11-CC-000345 — The Windows Remote Management (WinRM) service must not use Basic authentication.

- Group: `V-253418`; rule revision: `SV-253418r958510_rule`; source severity: **high**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\WinRM\Service\

Value Name: AllowBasic

Value Type: REG_DWORD
Value: 0
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Windows Remote Management (WinRM) >> WinRM Service >> "Allow Basic authentication" to "Disabled".

Severity Override Guidance: The AO can allow the severity override if they have reviewed the overall protection. This would only be allowed temporarily for implementation as documented and approved.
....
Allowing Basic authentication to be used for the sole creation of Office 365 DoD tenants.
....
A documented mechanism and or script that can disable Basic authentication once administration completes.
....
Use of a Privileged Access Workstation (PAW) and adherence to the Clean Source principle for administration.
~~~~~


<a id="wn11-cc-000350"></a>

## WN11-CC-000350 — The Windows Remote Management (WinRM) service must not allow unencrypted traffic.

- Group: `V-253419`; rule revision: `SV-253419r958850_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\WinRM\Service\

Value Name: AllowUnencryptedTraffic

Value Type: REG_DWORD
Value: 0
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Windows Remote Management (WinRM) >> WinRM Service >> "Allow unencrypted traffic" to "Disabled".
~~~~~


<a id="wn11-cc-000355"></a>

## WN11-CC-000355 — The Windows Remote Management (WinRM) service must not store RunAs credentials.

- Group: `V-253420`; rule revision: `SV-253420r1051055_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\WinRM\Service\

Value Name: DisableRunAs

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Windows Remote Management (WinRM) >> WinRM Service >> "Disallow WinRM from storing RunAs credentials" to "Enabled".
~~~~~


<a id="wn11-cc-000360"></a>

## WN11-CC-000360 — The Windows Remote Management (WinRM) client must not use Digest authentication.

- Group: `V-253421`; rule revision: `SV-253421r958510_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\WinRM\Client\

Value Name: AllowDigest

Value Type: REG_DWORD
Value: 0
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Windows Remote Management (WinRM) >> WinRM Client >> "Disallow Digest authentication" to "Enabled".
~~~~~


<a id="wn11-cc-000365"></a>

## WN11-CC-000365 — Windows 11 must be configured to prevent Windows apps from being activated by voice while the system is locked.

- Group: `V-253422`; rule revision: `SV-253422r1270952_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\AppPrivacy\
Value Name: LetAppsActivateWithVoiceAboveLock

Type: REG_DWORD
Value: 0x00000002 (2)
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> App Privacy >> "Let Windows apps activate with voice while the system is locked" to "Enabled" with Default for all Apps: set to "Force Deny".
~~~~~


<a id="wn11-cc-000370"></a>

## WN11-CC-000370 — The convenience PIN for Windows 11 must be disabled.

- Group: `V-253423`; rule revision: `SV-253423r958478_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \Software\Policies\Microsoft\Windows\System

Value Name: AllowDomainPINLogon
Value Type: REG_DWORD
Value data: 0
~~~~~

### Source fix text

~~~~~text
Disable the convenience PIN sign-in.

To correct this, configure the policy value for Computer Configuration >> Administrative Templates >> System >> Logon >> Set "Turn on convenience PIN sign-in" to "Disabled".
~~~~~


<a id="wn11-cc-000385"></a>

## WN11-CC-000385 — Windows Ink Workspace must be configured to disallow access above the lock.

- Group: `V-253424`; rule revision: `SV-253424r1210299_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\WindowsInkWorkspace  (For GPO-managed systems)
Or
Registry Path: \SOFTWARE\Microsoft\PolicyManager\current\device\WindowsInkWorkspace  (For Intune-managed systems)

Value Name: AllowWindowsInkWorkspace
Value Type: REG_DWORD
Value data: 1
~~~~~

### Source fix text

~~~~~text
Disable the convenience PIN sign-in.

For GPO-managed systems:

Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Windows Ink Workspace >> Set "Allow Windows Ink Workspace" to "Enabled and set Options On, but disallow access above lock".

For Intune-managed systems:

Set the Windows Ink Workspace Policy to disallow access above lock.
~~~~~


<a id="wn11-cc-000390"></a>

## WN11-CC-000390 — Windows 11 must be configured to prevent users from receiving suggestions for third-party or additional applications.

- Group: `V-253425`; rule revision: `SV-253425r1259997_rule`; source severity: **low**.

### Source check text

~~~~~text
Note: This Check must be performed for each interactive user profile on the system.
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_CURRENT_USER
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\CloudContent\

Value Name: DisableThirdPartySuggestions

Type: REG_DWORD
Value: 0x00000001 (1)

Note: This requirement is applicable to profiles for interactive logins. It is not applicable for Service accounts.

To determine the system's enabled user profiles:
Run "PowerShell" as an administrator.

Execute the following command:
Get-LocalUser | Where-Object {$_.Enabled -eq $true}
~~~~~

### Source fix text

~~~~~text
For each user profile on the system, configure the policy value for User Configuration >> Administrative Templates. >> Windows Components >> Cloud Content >> "Do not suggest third-party content in Windows spotlight" to "Enabled".
~~~~~


<a id="wn11-cc-000391"></a>

## WN11-CC-000391 — Internet Explorer must be disabled for Windows 11.

- Group: `V-256893`; rule revision: `SV-256893r958552_rule`; source severity: **medium**.

### Source check text

~~~~~text
Determine if IE11 is installed or enabled on Windows 11 semi-annual channel.

If IE11 is installed or not disabled on Windows 11 semi-annual channel, this is a finding.

If IE11 is installed on an unsupported operating system and is enabled or installed, this is a finding.

For more information, visit: https://learn.microsoft.com/en-us/lifecycle/faq/internet-explorer-microsoft-edge#what-is-the-lifecycle-policy-for-internet-explorer-
~~~~~

### Source fix text

~~~~~text
For Windows 11 semi-annual channel, remove or disable the IE11 application.

To disable IE11 as a standalone browser:

Set the policy value for "Computer Configuration/Administrative Templates/Windows Components/Internet Explorer/Disable Internet Explorer 11 as a standalone browser" to "Enabled" with the option value set to "Never".
~~~~~


<a id="wn11-cc-000063"></a>

## WN11-CC-000063 — Windows 11 systems must use either Group Policy or an approved Mobile Device Management (MDM) product to enforce STIG compliance.

- Group: `V-268318`; rule revision: `SV-268318r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the Windows 11 system is receiving policy from either group Policy or an MDM with the following steps:

From a command line or PowerShell:

gpresult /R
OS Configuration: Member Workstation

If the system OS Configuration is set to "Member Workstation", the system is being managed by GPO.

If the system OS Configuration is set to "Standalone Workstation" and is not being managed by GPO, ask the administrator to indicate which MDM is managing the device.

Issue to the following for Intune. Note: Intune must be running at time of command.

From PowerShell: Get-Service -Name "IntuneManagementExtension"

This should return the following result:

Status = Running, Name = IntuneManagementExtension, DisplayName = Microsoft Intune Management Extension

If Intune is not installed, the response will include "ObjectNotFound" and/or "NoServiceFoundForGivenName".

If the Windows 11 system is not receiving policy from either group Policy or an MDM (that is running), this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the Windows 11 system to use either Group Policy or an approved MDM product to enforce STIG compliance.
~~~~~


<a id="wn11-cc-000366"></a>

## WN11-CC-000366 — Windows 11 must be configured to prevent Windows apps from being activated by voice.

- Group: `V-289260`; rule revision: `SV-289260r1270955_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\AppPrivacy\
Value Name: LetAppsActivateWithVoice

Type: REG_DWORD
Value: 0x00000002 (2)
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> App Privacy>>"Let Windows apps activate with voice" to "Enabled" with Default for all Apps set to "Force Deny".
~~~~~
