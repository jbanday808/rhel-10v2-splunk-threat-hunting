# Windows 11 STIG V2R11 — rule reference SO

This reference reproduces the **check and fix** text from the user-supplied, unclassified manual XCCDF (Release: 11 Benchmark Date: 30 Sep 2026). It contains 43 rules. Line-end whitespace is normalized for readability. The source is a version-specific reference: confirm the required release and use the official benchmark and your assessor’s applicability decision. All targets, evidence and assessment statuses remain unverified.

Read the implementation guide, back up the system, and obtain approval before making changes. The source fix text can contain commands or settings that change the system; do not run them blindly. In a managed system use the approved policy owner and source.

| Rule | Severity | Title |
| --- | --- | --- |
| [WN11-SO-000010](#wn11-so-000010) | medium | The built-in guest account must be disabled. |
| [WN11-SO-000015](#wn11-so-000015) | medium | Local accounts with blank passwords must be restricted to prevent access from the network. |
| [WN11-SO-000020](#wn11-so-000020) | medium | The built-in administrator account must be renamed. |
| [WN11-SO-000025](#wn11-so-000025) | medium | The built-in guest account must be renamed. |
| [WN11-SO-000030](#wn11-so-000030) | medium | Audit policy using subcategories must be enabled. |
| [WN11-SO-000035](#wn11-so-000035) | medium | Outgoing secure channel traffic must be encrypted or signed. |
| [WN11-SO-000040](#wn11-so-000040) | medium | Outgoing secure channel traffic must be encrypted. |
| [WN11-SO-000045](#wn11-so-000045) | medium | Outgoing secure channel traffic must be signed. |
| [WN11-SO-000050](#wn11-so-000050) | low | The computer account password must not be prevented from being reset. |
| [WN11-SO-000055](#wn11-so-000055) | low | The maximum age for machine account passwords must be configured to 30 days or less. |
| [WN11-SO-000060](#wn11-so-000060) | medium | The system must be configured to require a strong session key. |
| [WN11-SO-000070](#wn11-so-000070) | medium | The machine inactivity limit must be set to 15 minutes, locking the system with the screensaver. |
| [WN11-SO-000075](#wn11-so-000075) | medium | The required legal notice must be configured to display before console logon. |
| [WN11-SO-000085](#wn11-so-000085) | low | Caching of logon credentials must be limited. |
| [WN11-SO-000095](#wn11-so-000095) | medium | The Smart Card removal option must be configured to Force Logoff or Lock Workstation. |
| [WN11-SO-000100](#wn11-so-000100) | medium | The Windows SMB client must be configured to always perform SMB packet signing. |
| [WN11-SO-000110](#wn11-so-000110) | medium | Unencrypted passwords must not be sent to third-party SMB Servers. |
| [WN11-SO-000120](#wn11-so-000120) | medium | The Windows SMB server must be configured to always perform SMB packet signing. |
| [WN11-SO-000140](#wn11-so-000140) | high | Anonymous SID/Name translation must not be allowed. |
| [WN11-SO-000145](#wn11-so-000145) | high | Anonymous enumeration of SAM accounts must not be allowed. |
| [WN11-SO-000150](#wn11-so-000150) | high | Anonymous enumeration of shares must be restricted. |
| [WN11-SO-000160](#wn11-so-000160) | medium | The system must be configured to prevent anonymous users from having the same rights as the Everyone group. |
| [WN11-SO-000165](#wn11-so-000165) | high | Anonymous access to Named Pipes and Shares must be restricted. |
| [WN11-SO-000167](#wn11-so-000167) | medium | Remote calls to the Security Account Manager (SAM) must be restricted to Administrators. |
| [WN11-SO-000180](#wn11-so-000180) | medium | NTLM must be prevented from falling back to a Null session. |
| [WN11-SO-000185](#wn11-so-000185) | medium | PKU2U authentication using online identities must be prevented. |
| [WN11-SO-000190](#wn11-so-000190) | medium | Kerberos encryption types must be configured to prevent the use of DES and RC4 encryption suites. |
| [WN11-SO-000195](#wn11-so-000195) | high | The system must be configured to prevent the storage of the LAN Manager hash of passwords. |
| [WN11-SO-000205](#wn11-so-000205) | high | The LanMan authentication level must be set to send NTLMv2 response only, and to refuse LM and NTLM. |
| [WN11-SO-000210](#wn11-so-000210) | medium | The system must be configured to the required LDAP client signing level. |
| [WN11-SO-000215](#wn11-so-000215) | medium | The system must be configured to meet the minimum session security requirement for NTLM SSP based clients. |
| [WN11-SO-000220](#wn11-so-000220) | medium | The system must be configured to meet the minimum session security requirement for NTLM SSP based servers. |
| [WN11-SO-000230](#wn11-so-000230) | medium | The system must be configured to use FIPS-compliant algorithms for encryption, hashing, and signing. |
| [WN11-SO-000240](#wn11-so-000240) | low | The default permissions of global system objects must be increased. |
| [WN11-SO-000245](#wn11-so-000245) | medium | User Account Control approval mode for the built-in Administrator must be enabled. |
| [WN11-SO-000250](#wn11-so-000250) | medium | User Account Control must prompt administrators for consent on the secure desktop. |
| [WN11-SO-000251](#wn11-so-000251) | medium | Windows 11 must use multifactor authentication for local and network access to privileged and nonprivileged accounts. |
| [WN11-SO-000255](#wn11-so-000255) | medium | User Account Control must automatically deny elevation requests for standard users. |
| [WN11-SO-000260](#wn11-so-000260) | medium | User Account Control must be configured to detect application installations and prompt for elevation. |
| [WN11-SO-000265](#wn11-so-000265) | medium | User Account Control must only elevate UIAccess applications that are installed in secure locations. |
| [WN11-SO-000270](#wn11-so-000270) | medium | User Account Control must run all administrators in Admin Approval Mode, enabling UAC. |
| [WN11-SO-000275](#wn11-so-000275) | medium | User Account Control must virtualize file and registry write failures to per-user locations. |
| [WN11-SO-000280](#wn11-so-000280) | medium | Passwords for enabled local Administrator accounts must be changed at least every 180 days. |

<a id="wn11-so-000010"></a>

## WN11-SO-000010 — The built-in guest account must be disabled.

- Group: `V-253433`; rule revision: `SV-253433r958504_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options.

If the value for "Accounts: Guest account status" is not set to "Disabled", this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Accounts: Guest account status" to "Disabled".
~~~~~


<a id="wn11-so-000015"></a>

## WN11-SO-000015 — Local accounts with blank passwords must be restricted to prevent access from the network.

- Group: `V-253434`; rule revision: `SV-253434r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Control\Lsa\

Value Name: LimitBlankPasswordUse

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Accounts: Limit local account use of blank passwords to console logon only" to "Enabled".
~~~~~


<a id="wn11-so-000020"></a>

## WN11-SO-000020 — The built-in administrator account must be renamed.

- Group: `V-253435`; rule revision: `SV-253435r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options.

If the value for "Accounts: Rename administrator account" is set to "Administrator", this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Accounts: Rename administrator account" to a name other than "Administrator".
~~~~~


<a id="wn11-so-000025"></a>

## WN11-SO-000025 — The built-in guest account must be renamed.

- Group: `V-253436`; rule revision: `SV-253436r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options.

If the value for "Accounts: Rename guest account" is set to "Guest", this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Accounts: Rename guest account" to a name other than "Guest".
~~~~~


<a id="wn11-so-000030"></a>

## WN11-SO-000030 — Audit policy using subcategories must be enabled.

- Group: `V-253437`; rule revision: `SV-253437r1268225_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Control\Lsa\

Value Name: SCENoApplyLegacyAuditPolicy

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Audit: Force audit policy subcategory settings (Windows Vista or later) to override audit policy category settings" to "Enabled".
~~~~~


<a id="wn11-so-000035"></a>

## WN11-SO-000035 — Outgoing secure channel traffic must be encrypted or signed.

- Group: `V-253438`; rule revision: `SV-253438r958908_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Services\Netlogon\Parameters\

Value Name: RequireSignOrSeal

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Domain member: Digitally encrypt or sign secure channel data (always)" to "Enabled".
~~~~~


<a id="wn11-so-000040"></a>

## WN11-SO-000040 — Outgoing secure channel traffic must be encrypted.

- Group: `V-253439`; rule revision: `SV-253439r958908_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Services\Netlogon\Parameters\

Value Name: SealSecureChannel

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Domain member: Digitally encrypt secure channel data (when possible)" to "Enabled".
~~~~~


<a id="wn11-so-000045"></a>

## WN11-SO-000045 — Outgoing secure channel traffic must be signed.

- Group: `V-253440`; rule revision: `SV-253440r958908_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Services\Netlogon\Parameters\

Value Name: SignSecureChannel

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Domain member: Digitally sign secure channel data (when possible)" to "Enabled".
~~~~~


<a id="wn11-so-000050"></a>

## WN11-SO-000050 — The computer account password must not be prevented from being reset.

- Group: `V-253441`; rule revision: `SV-253441r1268251_rule`; source severity: **low**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Services\Netlogon\Parameters\

Value Name: DisablePasswordChange

Value Type: REG_DWORD
Value: 0
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Domain member: Disable machine account password changes" to "Disabled".
~~~~~


<a id="wn11-so-000055"></a>

## WN11-SO-000055 — The maximum age for machine account passwords must be configured to 30 days or less.

- Group: `V-253442`; rule revision: `SV-253442r1268251_rule`; source severity: **low**.

### Source check text

~~~~~text
(remove)This is the default configuration for this setting (30 days).

If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Services\Netlogon\Parameters\

Value Name: MaximumPasswordAge

Value Type: REG_DWORD
Value: 0x0000001e (30) (or less, excluding 0)
~~~~~

### Source fix text

~~~~~text
This is the default configuration for this setting (30 days).

Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Domain member: Maximum machine account password age" to "30" or less (excluding 0 which is unacceptable).
~~~~~


<a id="wn11-so-000060"></a>

## WN11-SO-000060 — The system must be configured to require a strong session key.

- Group: `V-253443`; rule revision: `SV-253443r958908_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Services\Netlogon\Parameters\

Value Name: RequireStrongKey

Value Type: REG_DWORD
Value: 1

Warning: This setting may prevent a system from being joined to a domain if not configured consistently between systems.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Domain member: Require strong (Windows 2000 or Later) session key" to "Enabled".
~~~~~


<a id="wn11-so-000070"></a>

## WN11-SO-000070 — The machine inactivity limit must be set to 15 minutes, locking the system with the screensaver.

- Group: `V-253444`; rule revision: `SV-253444r958636_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\

Value Name: InactivityTimeoutSecs

Value Type: REG_DWORD
Value: 0x00000384 (900) (or less, excluding "0" which is effectively disabled)
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Interactive logon: Machine inactivity limit" to "900" seconds" or less, excluding "0" which is effectively disabled.
~~~~~


<a id="wn11-so-000075"></a>

## WN11-SO-000075 — The required legal notice must be configured to display before console logon.

- Group: `V-253445`; rule revision: `SV-253445r1268218_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:
Note: If configuring this policy via a Policy Configuration Service Provider (CSP), additional steps are needed (see Fix Text).

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\

Value Name: LegalNoticeText

Value Type: REG_SZ
Value:
You are accessing a U.S. Government (USG) Information System (IS) that is provided for USG-authorized use only.

By using this IS (which includes any device attached to this IS), you consent to the following conditions:

-The USG routinely intercepts and monitors communications on this IS for purposes including, but not limited to, penetration testing, COMSEC monitoring, network operations and defense, personnel misconduct (PM), law enforcement (LE), and counterintelligence (CI) investigations.

-At any time, the USG may inspect and seize data stored on this IS.

-Communications using, or data stored on, this IS are not private, are subject to routine monitoring, interception, and search, and may be disclosed or used for any USG-authorized purpose.

-This IS includes security measures (e.g., authentication and access controls) to protect USG interests--not for your personal benefit or privacy.

-Notwithstanding the above, using this IS does not constitute consent to PM, LE or CI investigative searching or monitoring of the content of privileged communications, or work product, related to personal representation or services by attorneys, psychotherapists, or clergy, and their assistants. Such communications and work product are private and confidential. See User Agreement for details.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Interactive logon: Message text for users attempting to log on" to the following.

You are accessing a U.S. Government (USG) Information System (IS) that is provided for USG-authorized use only.

By using this IS (which includes any device attached to this IS), you consent to the following conditions:

-The USG routinely intercepts and monitors communications on this IS for purposes including, but not limited to, penetration testing, COMSEC monitoring, network operations and defense, personnel misconduct (PM), law enforcement (LE), and counterintelligence (CI) investigations.

-At any time, the USG may inspect and seize data stored on this IS.

-Communications using, or data stored on, this IS are not private, are subject to routine monitoring, interception, and search, and may be disclosed or used for any USG-authorized purpose.

-This IS includes security measures (e.g., authentication and access controls) to protect USG interests--not for your personal benefit or privacy.

-Notwithstanding the above, using this IS does not constitute consent to PM, LE or CI investigative searching or monitoring of the content of privileged communications, or work product, related to personal representation or services by attorneys, psychotherapists, or clergy, and their assistants. Such communications and work product are private and confidential. See User Agreement for details.

Note: For MDM/Intune implementation, when configuring this policy via a Policy Configuration Service Provider (CSP), both the "Message text" and the "Interactive logon: Message title for users attempting to log on" must be configured to enable the legal notice to be displayed. It is recommended to set the "Message title" to a non-blank value, such as "U.S. Government Warning" or a period (".").
~~~~~


<a id="wn11-so-000085"></a>

## WN11-SO-000085 — Caching of logon credentials must be limited.

- Group: `V-253447`; rule revision: `SV-253447r1268251_rule`; source severity: **low**.

### Source check text

~~~~~text
This is the default configuration for this setting (10 logons to cache).

If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\

Value Name: CachedLogonsCount

Value Type: REG_SZ
Value: 10 (or less)

This setting only applies to domain-joined systems, however, it is configured by default on all systems.
~~~~~

### Source fix text

~~~~~text
This is the default configuration for this setting (10 logons to cache).

Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Interactive logon: Number of previous logons to cache (in case domain controller is not available)" to "10" logons or less.

This setting only applies to domain-joined systems, however, it is configured by default on all systems.
~~~~~


<a id="wn11-so-000095"></a>

## WN11-SO-000095 — The Smart Card removal option must be configured to Force Logoff or Lock Workstation.

- Group: `V-253448`; rule revision: `SV-253448r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\

Value Name: SCRemoveOption

Value Type: REG_SZ
Value: 1 (Lock Workstation) or 2 (Force Logoff)

This can be left not configured or set to "No action" on workstations with the following conditions. This must be documented with the ISSO.
-The setting cannot be configured due to mission needs, or because it interferes with applications.
-Policy must be in place that users manually lock workstations when leaving them unattended.
-The screen saver is properly configured to lock as required.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Interactive logon: Smart card removal behavior" to "Lock Workstation" or "Force Logoff".
~~~~~


<a id="wn11-so-000100"></a>

## WN11-SO-000100 — The Windows SMB client must be configured to always perform SMB packet signing.

- Group: `V-253449`; rule revision: `SV-253449r958908_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters\

Value Name: RequireSecuritySignature

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Microsoft network client: Digitally sign communications (always)" to "Enabled".
~~~~~


<a id="wn11-so-000110"></a>

## WN11-SO-000110 — Unencrypted passwords must not be sent to third-party SMB Servers.

- Group: `V-253450`; rule revision: `SV-253450r987796_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters\

Value Name: EnablePlainTextPassword

Value Type: REG_DWORD
Value: 0
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Microsoft network client: Send unencrypted password to third-party SMB servers" to "Disabled".
~~~~~


<a id="wn11-so-000120"></a>

## WN11-SO-000120 — The Windows SMB server must be configured to always perform SMB packet signing.

- Group: `V-253451`; rule revision: `SV-253451r958908_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Services\LanManServer\Parameters\

Value Name: RequireSecuritySignature

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Microsoft network server: Digitally sign communications (always)" to "Enabled".
~~~~~


<a id="wn11-so-000140"></a>

## WN11-SO-000140 — Anonymous SID/Name translation must not be allowed.

- Group: `V-253452`; rule revision: `SV-253452r1268251_rule`; source severity: **high**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options.

If the value for "Network access: Allow anonymous SID/Name translation" is not set to "Disabled", this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Network access: Allow anonymous SID/Name translation" to "Disabled".
~~~~~


<a id="wn11-so-000145"></a>

## WN11-SO-000145 — Anonymous enumeration of SAM accounts must not be allowed.

- Group: `V-253453`; rule revision: `SV-253453r1268251_rule`; source severity: **high**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Control\Lsa\

Value Name: RestrictAnonymousSAM

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Network access: Do not allow anonymous enumeration of SAM accounts" to "Enabled".
~~~~~


<a id="wn11-so-000150"></a>

## WN11-SO-000150 — Anonymous enumeration of shares must be restricted.

- Group: `V-253454`; rule revision: `SV-253454r1268233_rule`; source severity: **high**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Control\Lsa\

Value Name: RestrictAnonymous

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Network access: Do not allow anonymous enumeration of SAM accounts and shares" to "Enabled".
~~~~~


<a id="wn11-so-000160"></a>

## WN11-SO-000160 — The system must be configured to prevent anonymous users from having the same rights as the Everyone group.

- Group: `V-253455`; rule revision: `SV-253455r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Control\Lsa\

Value Name: EveryoneIncludesAnonymous

Value Type: REG_DWORD
Value: 0
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Network access: Let Everyone permissions apply to anonymous users" to "Disabled".
~~~~~


<a id="wn11-so-000165"></a>

## WN11-SO-000165 — Anonymous access to Named Pipes and Shares must be restricted.

- Group: `V-253456`; rule revision: `SV-253456r1268233_rule`; source severity: **high**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Services\LanManServer\Parameters\

Value Name: RestrictNullSessAccess

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Network access: Restrict anonymous access to Named Pipes and Shares" to "Enabled".
~~~~~


<a id="wn11-so-000167"></a>

## WN11-SO-000167 — Remote calls to the Security Account Manager (SAM) must be restricted to Administrators.

- Group: `V-253457`; rule revision: `SV-253457r1081060_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Control\Lsa\

Value Name: RestrictRemoteSAM

Value Type: REG_SZ
Value: O:BAG:BAD:(A;;RC;;;BA)

If a domain application account such as for a management tool requires this user right, this would not be a finding.
Vendor documentation must support the requirement for having the user right.
The requirement must be documented with the ISSO.
~~~~~

### Source fix text

~~~~~text
Navigate to the policy Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Network access: Restrict clients allowed to make remote calls to SAM".

Select "Edit Security" to configure the "Security descriptor:".

Add "Administrators" in "Group or user names:" if it is not already listed (this is the default).

Select "Administrators" in "Group or user names:".

Select "Allow" for "Remote Access" in "Permissions for "Administrators".

Click "OK".

The "Security descriptor:" must be populated with "O:BAG:BAD:(A;;RC;;;BA) for the policy to be enforced.
~~~~~


<a id="wn11-so-000180"></a>

## WN11-SO-000180 — NTLM must be prevented from falling back to a Null session.

- Group: `V-253458`; rule revision: `SV-253458r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Control\LSA\MSV1_0\

Value Name: allownullsessionfallback

Value Type: REG_DWORD
Value: 0
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Network security: Allow LocalSystem NULL session fallback" to "Disabled".
~~~~~


<a id="wn11-so-000185"></a>

## WN11-SO-000185 — PKU2U authentication using online identities must be prevented.

- Group: `V-253459`; rule revision: `SV-253459r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Control\LSA\pku2u\

Value Name: AllowOnlineID

Value Type: REG_DWORD
Value: 0
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Network security: Allow PKU2U authentication requests to this computer to use online identities" to "Disabled".
~~~~~


<a id="wn11-so-000190"></a>

## WN11-SO-000190 — Kerberos encryption types must be configured to prevent the use of DES and RC4 encryption suites.

- Group: `V-253460`; rule revision: `SV-253460r1268232_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\Kerberos\Parameters\

Value Name: SupportedEncryptionTypes

Value Type: REG_DWORD
Value: 0x7ffffff8 (2147483640)
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Network security: Configure encryption types allowed for Kerberos" to "Enabled" with only the following selected:

AES128_HMAC_SHA1
AES256_HMAC_SHA1
Future encryption types
~~~~~


<a id="wn11-so-000195"></a>

## WN11-SO-000195 — The system must be configured to prevent the storage of the LAN Manager hash of passwords.

- Group: `V-253461`; rule revision: `SV-253461r1051056_rule`; source severity: **high**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Control\Lsa\

Value Name: NoLMHash

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Network security: Do not store LAN Manager hash value on next password change" to "Enabled".
~~~~~


<a id="wn11-so-000205"></a>

## WN11-SO-000205 — The LanMan authentication level must be set to send NTLMv2 response only, and to refuse LM and NTLM.

- Group: `V-253462`; rule revision: `SV-253462r1268251_rule`; source severity: **high**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Control\Lsa\

Value Name: LmCompatibilityLevel

Value Type: REG_DWORD
Value: 5
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Network security: LAN Manager authentication level" to "Send NTLMv2 response only. Refuse LM & NTLM".
~~~~~


<a id="wn11-so-000210"></a>

## WN11-SO-000210 — The system must be configured to the required LDAP client signing level.

- Group: `V-253463`; rule revision: `SV-253463r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Services\LDAP\

Value Name: LDAPClientIntegrity

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Network security: LDAP client signing requirements" to "Negotiate signing" at a minimum.
~~~~~


<a id="wn11-so-000215"></a>

## WN11-SO-000215 — The system must be configured to meet the minimum session security requirement for NTLM SSP based clients.

- Group: `V-253464`; rule revision: `SV-253464r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Control\Lsa\MSV1_0\

Value Name: NTLMMinClientSec

Value Type: REG_DWORD
Value: 0x20080000 (537395200)
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Network security: Minimum session security for NTLM SSP based (including secure RPC) clients" to "Require NTLMv2 session security" and "Require 128-bit encryption" (all options selected).
~~~~~


<a id="wn11-so-000220"></a>

## WN11-SO-000220 — The system must be configured to meet the minimum session security requirement for NTLM SSP based servers.

- Group: `V-253465`; rule revision: `SV-253465r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Control\Lsa\MSV1_0\

Value Name: NTLMMinServerSec

Value Type: REG_DWORD
Value: 0x20080000 (537395200)
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "Network security: Minimum session security for NTLM SSP based (including secure RPC) servers" to "Require NTLMv2 session security" and "Require 128-bit encryption" (all options selected).
~~~~~


<a id="wn11-so-000230"></a>

## WN11-SO-000230 — The system must be configured to use FIPS-compliant algorithms for encryption, hashing, and signing.

- Group: `V-253466`; rule revision: `SV-253466r1210303_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Control\Lsa\FIPSAlgorithmPolicy\  (For GPO-managed systems)
Or
Registry Path: \SOFTWARE\Microsoft\PolicyManager\current\device\Cryptography!AllowFipsAlgorithmPolicy_ProviderSet  (For Intune-managed systems)

Value Name: Enabled

Value Type: REG_DWORD
Value: 1

Warning: Clients with this setting enabled will not be able to communicate via digitally encrypted or signed protocols with servers that do not support these algorithms.
~~~~~

### Source fix text

~~~~~text
For GPO-managed systems:

Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "System cryptography: Use FIPS compliant algorithms for encryption, hashing, and signing" to "Enabled".

For Intune-managed systems:

Set the Intune System Cryptography Policy to use FIPS-compliant algorithms for encryption, hashing, and signing.
~~~~~


<a id="wn11-so-000240"></a>

## WN11-SO-000240 — The default permissions of global system objects must be increased.

- Group: `V-253467`; rule revision: `SV-253467r1268251_rule`; source severity: **low**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SYSTEM\CurrentControlSet\Control\Session Manager\

Value Name: ProtectionMode

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "System objects: Strengthen default permissions of internal system objects (e.g. Symbolic links)" to "Enabled".
~~~~~


<a id="wn11-so-000245"></a>

## WN11-SO-000245 — User Account Control approval mode for the built-in Administrator must be enabled.

- Group: `V-253468`; rule revision: `SV-253468r1051057_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\

Value Name: FilterAdministratorToken

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "User Account Control: Admin Approval Mode for the Built-in Administrator account" to "Enabled".
~~~~~


<a id="wn11-so-000250"></a>

## WN11-SO-000250 — User Account Control must prompt administrators for consent on the secure desktop.

- Group: `V-253469`; rule revision: `SV-253469r958518_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\

Value Name: ConsentPromptBehaviorAdmin

Value Type: REG_DWORD
Value: 2 (Prompt for consent on the secure desktop)
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "User Account Control: Behavior of the elevation prompt for administrators in Admin Approval Mode" to "Prompt for consent on the secure desktop".
~~~~~


<a id="wn11-so-000251"></a>

## WN11-SO-000251 — Windows 11 must use multifactor authentication for local and network access to privileged and nonprivileged accounts.

- Group: `V-253470`; rule revision: `SV-253470r1268228_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the system is not a member of a domain, this is Not Applicable.

If all of the following settings exist and are populated, this is not a finding.

\HKLM\SOFTWARE\Microsoft\Cryptography\Calais\Readers
\HKLM\SOFTWARE\Microsoft\Cryptography\Calais\SmartCards
~~~~~

### Source fix text

~~~~~text
For nondomain joined systems, configuring Windows Hello for sign-on options would be suggested based on the organization's needs and capabilities.
~~~~~


<a id="wn11-so-000255"></a>

## WN11-SO-000255 — User Account Control must automatically deny elevation requests for standard users.

- Group: `V-253471`; rule revision: `SV-253471r1051058_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\

Value Name: ConsentPromptBehaviorUser

Value Type: REG_DWORD
Value: 0
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "User Account Control: Behavior of the elevation prompt for standard users" to "Automatically deny elevation requests".
~~~~~


<a id="wn11-so-000260"></a>

## WN11-SO-000260 — User Account Control must be configured to detect application installations and prompt for elevation.

- Group: `V-253472`; rule revision: `SV-253472r958518_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\

Value Name: EnableInstallerDetection

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "User Account Control: Detect application installations and prompt for elevation" to "Enabled".
~~~~~


<a id="wn11-so-000265"></a>

## WN11-SO-000265 — User Account Control must only elevate UIAccess applications that are installed in secure locations.

- Group: `V-253473`; rule revision: `SV-253473r958518_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\

Value Name: EnableSecureUIAPaths

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "User Account Control: Only elevate UIAccess applications that are installed in secure locations" to "Enabled".
~~~~~


<a id="wn11-so-000270"></a>

## WN11-SO-000270 — User Account Control must run all administrators in Admin Approval Mode, enabling UAC.

- Group: `V-253474`; rule revision: `SV-253474r1051059_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\

Value Name: EnableLUA

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "User Account Control: Run all administrators in Admin Approval Mode" to "Enabled".
~~~~~


<a id="wn11-so-000275"></a>

## WN11-SO-000275 — User Account Control must virtualize file and registry write failures to per-user locations.

- Group: `V-253475`; rule revision: `SV-253475r958518_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\

Value Name: EnableVirtualization

Value Type: REG_DWORD
Value: 1
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> Security Options >> "User Account Control: Virtualize file and registry write failures to per-user locations" to "Enabled".
~~~~~


<a id="wn11-so-000280"></a>

## WN11-SO-000280 — Passwords for enabled local Administrator accounts must be changed at least every 180 days.

- Group: `V-253476`; rule revision: `SV-253476r1268211_rule`; source severity: **medium**.

### Source check text

~~~~~text
If there are no enabled local Administrator accounts, this is Not Applicable.

Use of an enabled built-in account without management by LAPS must be documented and supplied to the information system security manager (ISSM)/information system security officer (ISSO) for their risk acceptance.

An alternative process to LAPS is acceptable if it is documented and produces evidence that passwords for Administrator accounts are changed at least every 180 days.

Review the password last set date for the enabled local Administrator account.

On the standalone or domain-joined workstation:

Open "PowerShell".

Enter "Get-LocalUser -Name * | Select-Object *".

If the "PasswordLastSet" date is greater than "180" days old for the local Administrator account for administering the computer/domain, this is a finding.

Verify LAPS is configured and operational.

Navigate to Local Computer Policy >> Computer Configuration >> Administrative Templates >> System >> LAPS >> Password Settings >> Set to enabled. Password Complexity, large letters + small letters + numbers + special, Password Length 14, Password Age 180. If not configured as shown, this is a finding.

Verify LAPS Operational logs >> Event Viewer >> Applications and Services Logs >> Microsoft >> Windows >> LAPS >> Operational. Verify LAPS policy process is completing. If it is not, this is a finding.
~~~~~

### Source fix text

~~~~~text
Change the enabled local Administrator account password at least every 180 days.

Windows LAPS must be used to change the built-in Administrator account password. Domain-joined and nondomain-joined systems can configure this to occur more frequently. LAPS will change the password every 30 days by default.

Operational limitations preventing the use of LAPS must be approved by the AO.

More information is available at:
https://techcommunity.microsoft.com/t5/windows-it-pro-blog/by-popular-demand-windows-laps-available-now/ba-p/3788747
https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-overview#windows-laps-supported-platforms-and-azure-ad-laps-preview-status
~~~~~
