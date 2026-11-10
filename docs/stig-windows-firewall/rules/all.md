# Windows Defender Firewall STIG V2R2 — rule reference all

This reference reproduces the **check and fix** text from the user-supplied, unclassified manual XCCDF (Release: 2 Benchmark Date: 09 Nov 2023). It contains 21 rules. Line-end whitespace is normalized for readability. The source is a version-specific reference: confirm the required release and use the official benchmark and your assessor’s applicability decision. All targets, evidence and assessment statuses remain unverified.

Read the implementation guide, back up the system, and obtain approval before making changes. The source fix text can contain commands or settings that change the system; do not run them blindly. In a managed system use the approved policy owner and source.

| Rule | Severity | Title |
| --- | --- | --- |
| [WNFWA-000001](#wnfwa-000001) | medium | Windows Defender Firewall with Advanced Security must be enabled when connected to a domain. |
| [WNFWA-000002](#wnfwa-000002) | medium | Windows Defender Firewall with Advanced Security must be enabled when connected to a private network. |
| [WNFWA-000003](#wnfwa-000003) | medium | Windows Defender Firewall with Advanced Security must be enabled when connected to a public network. |
| [WNFWA-000004](#wnfwa-000004) | high | Windows Defender Firewall with Advanced Security must block unsolicited inbound connections when connected to a domain. |
| [WNFWA-000005](#wnfwa-000005) | medium | Windows Defender Firewall with Advanced Security must allow outbound connections, unless a rule explicitly blocks the connection when connected to a domain. |
| [WNFWA-000009](#wnfwa-000009) | low | Windows Defender Firewall with Advanced Security log size must be configured for domain connections. |
| [WNFWA-000010](#wnfwa-000010) | low | Windows Defender Firewall with Advanced Security must log dropped packets when connected to a domain. |
| [WNFWA-000011](#wnfwa-000011) | low | Windows Defender Firewall with Advanced Security must log successful connections when connected to a domain. |
| [WNFWA-000012](#wnfwa-000012) | high | Windows Defender Firewall with Advanced Security must block unsolicited inbound connections when connected to a private network. |
| [WNFWA-000013](#wnfwa-000013) | medium | Windows Defender Firewall with Advanced Security must allow outbound connections, unless a rule explicitly blocks the connection when connected to a private network. |
| [WNFWA-000017](#wnfwa-000017) | low | Windows Defender Firewall with Advanced Security log size must be configured for private network connections. |
| [WNFWA-000018](#wnfwa-000018) | low | Windows Defender Firewall with Advanced Security must log dropped packets when connected to a private network. |
| [WNFWA-000019](#wnfwa-000019) | low | Windows Defender Firewall with Advanced Security must log successful connections when connected to a private network. |
| [WNFWA-000020](#wnfwa-000020) | high | Windows Defender Firewall with Advanced Security must block unsolicited inbound connections when connected to a public network. |
| [WNFWA-000021](#wnfwa-000021) | medium | Windows Defender Firewall with Advanced Security must allow outbound connections, unless a rule explicitly blocks the connection when connected to a public network. |
| [WNFWA-000024](#wnfwa-000024) | medium | Windows Defender Firewall with Advanced Security local firewall rules must not be merged with Group Policy settings when connected to a public network. |
| [WNFWA-000025](#wnfwa-000025) | medium | Windows Defender Firewall with Advanced Security local connection rules must not be merged with Group Policy settings when connected to a public network. |
| [WNFWA-000027](#wnfwa-000027) | low | Windows Defender Firewall with Advanced Security log size must be configured for public network connections. |
| [WNFWA-000028](#wnfwa-000028) | low | Windows Defender Firewall with Advanced Security must log dropped packets when connected to a public network. |
| [WNFWA-000029](#wnfwa-000029) | low | Windows Defender Firewall with Advanced Security must log successful connections when connected to a public network. |
| [WNFWA-000100](#wnfwa-000100) | medium | Inbound exceptions to the firewall on domain workstations must only allow authorized remote management hosts. |

<a id="wnfwa-000001"></a>

## WNFWA-000001 — Windows Defender Firewall with Advanced Security must be enabled when connected to a domain.

- Group: `V-241989`; rule revision: `SV-241989r922928_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the system is not a member of a domain, the Domain Profile requirements can be marked NA.

If the following policy-based registry value exists and is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SOFTWARE\Policies\Microsoft\WindowsFirewall\DomainProfile\

Value Name:  EnableFirewall

Type:  REG_DWORD
Value:  0x00000001 (1)

If the policy-based registry value does not exist, verify the following registry value. If it is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\DomainProfile\

Value Name:  EnableFirewall

Type:  REG_DWORD
Value:  0x00000001 (1)
~~~~~

### Source fix text

~~~~~text
The preferred method of configuring the firewall settings is with a policy, particularly in a domain environment.

Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall Properties (this link will be in the right pane) >> Domain Profile tab >> State, "Firewall state" to "On (recommended)".

In addition to using policies, systems may also be configured using the firewall GUI or Netsh commands. These methods may be more appropriate for standalone systems.

The configuration settings in the GUI are the same as those specified in the policy above. Microsoft Defender Firewall Properties will be a link in the center pane after opening Microsoft Defender Firewall with Advanced Security.

The following Netsh commands may also be used to configure this setting:

"Netsh advfirewall set domainprofile state on".
or
"Netsh advfirewall set allprofiles state on".
~~~~~


<a id="wnfwa-000002"></a>

## WNFWA-000002 — Windows Defender Firewall with Advanced Security must be enabled when connected to a private network.

- Group: `V-241990`; rule revision: `SV-241990r922930_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following policy-based registry value exists and is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SOFTWARE\Policies\Microsoft\WindowsFirewall\PrivateProfile\

Value Name:  EnableFirewall

Type:  REG_DWORD
Value:  0x00000001 (1)

If the policy-based registry value does not exist, verify the following registry value. If it is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\StandardProfile\

Value Name:  EnableFirewall

Type:  REG_DWORD
Value:  0x00000001 (1)
~~~~~

### Source fix text

~~~~~text
The preferred method of configuring the firewall settings is with a policy, particularly in a domain environment.

Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall Properties (this link will be in the right pane) >> Private Profile tab >> State, "Firewall state" to "On (recommended)".

In addition to using policies, systems may also be configured using the firewall GUI or Netsh commands. These methods may be more appropriate for standalone systems.

The configuration settings in the GUI are the same as those specified in the policy above. Microsoft Defender Firewall Properties will be a link in the center pane after opening Microsoft Defender Firewall with Advanced Security.

The following Netsh commands may also be used to configure this setting:

"Netsh advfirewall set privateprofile state on".
or
"Netsh advfirewall set allprofiles state on".
~~~~~


<a id="wnfwa-000003"></a>

## WNFWA-000003 — Windows Defender Firewall with Advanced Security must be enabled when connected to a public network.

- Group: `V-241991`; rule revision: `SV-241991r922932_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following policy-based registry value exists and is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SOFTWARE\Policies\Microsoft\WindowsFirewall\PublicProfile\

Value Name:  EnableFirewall

Type:  REG_DWORD
Value:  0x00000001 (1)

If the policy-based registry value does not exist, verify the following registry value. If it is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\PublicProfile\

Value Name:  EnableFirewall

Type:  REG_DWORD
Value:  0x00000001 (1)
~~~~~

### Source fix text

~~~~~text
The preferred method of configuring the firewall settings is with a policy, particularly in a domain environment.

Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall Properties (this link will be in the right pane) >> Public Profile tab >> State, "Firewall state" to "On (recommended)".

In addition to using policies, systems may also be configured using the firewall GUI or Netsh commands. These methods may be more appropriate for standalone systems.

The configuration settings in the GUI are the same as those specified in the policy above. Microsoft Defender Firewall Properties will be a link in the center pane after opening Microsoft Defender Firewall with Advanced Security.

The following Netsh commands may also be used to configure this setting:

"Netsh advfirewall set publicprofile state on".
or
"Netsh advfirewall set allprofiles state on".
~~~~~


<a id="wnfwa-000004"></a>

## WNFWA-000004 — Windows Defender Firewall with Advanced Security must block unsolicited inbound connections when connected to a domain.

- Group: `V-241992`; rule revision: `SV-241992r922934_rule`; source severity: **high**.

### Source check text

~~~~~text
If the system is not a member of a domain, the Domain Profile requirements can be marked NA.

If the system is a member of a domain and the firewall's Domain Profile is not enabled (see V-17415), this requirement is also a finding.

If the following policy-based registry value exists and is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SOFTWARE\Policies\Microsoft\WindowsFirewall\DomainProfile\

Value Name:  DefaultInboundAction

Type:  REG_DWORD
Value:  0x00000001 (1)

If the policy-based registry value does not exist, verify the following registry value. If it is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\DomainProfile\

Value Name:  DefaultInboundAction

Type:  REG_DWORD
Value:  0x00000001 (1)
~~~~~

### Source fix text

~~~~~text
The preferred method of configuring the firewall settings is with a policy, particularly in a domain environment.

Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall Properties (this link will be in the right pane) >> Domain Profile tab >> State, "Inbound connections" to "Block (default)".

In addition to using policies, systems may also be configured using the firewall GUI or Netsh commands. These methods may be more appropriate for standalone systems.

The configuration settings in the GUI are the same as those specified in the policy above. Microsoft Defender Firewall Properties will be a link in the center pane after opening Microsoft Defender Firewall with Advanced Security.

The following Netsh commands may also be used to configure this setting:

"Netsh advfirewall set domainprofile firewallpolicy blockinbound,allowoutbound".
or
"Netsh advfirewall set allprofiles firewallpolicy blockinbound,allowoutbound".

Both inbound and outbound parameters must be specified to execute this command.
~~~~~


<a id="wnfwa-000005"></a>

## WNFWA-000005 — Windows Defender Firewall with Advanced Security must allow outbound connections, unless a rule explicitly blocks the connection when connected to a domain.

- Group: `V-241993`; rule revision: `SV-241993r922936_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the system is not a member of a domain, the Domain Profile requirements can be marked NA.

If the system is a member of a domain and the firewall's Domain Profile is not enabled (see V-17415), this requirement is also a finding.

If the following policy-based registry value exists and is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SOFTWARE\Policies\Microsoft\WindowsFirewall\DomainProfile\

Value Name:  DefaultOutboundAction

Type:  REG_DWORD
Value:  0x00000000 (0)

If the policy-based registry value does not exist, verify the following registry value. If it is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\DomainProfile\

Value Name:  DefaultOutboundAction

Type:  REG_DWORD
Value:  0x00000000 (0)
~~~~~

### Source fix text

~~~~~text
The preferred method of configuring the firewall settings is with a policy, particularly in a domain environment.

Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall Properties (this link will be in the right pane) >> Domain Profile tab >> State, "Outbound connections" to "Allow (default)".

In addition to using policies, systems may also be configured using the firewall GUI or Netsh commands. These methods may be more appropriate for standalone systems.

The configuration settings in the GUI are the same as those specified in the policy above. Microsoft Defender Firewall Properties will be a link in the center pane after opening Microsoft Defender Firewall with Advanced Security.

The following Netsh commands may also be used to configure this setting:

"Netsh advfirewall set domainprofile firewallpolicy blockinbound,allowoutbound".
or
"Netsh advfirewall set allprofiles firewallpolicy blockinbound,allowoutbound".

Both inbound and outbound parameters must be specified to execute this command.
~~~~~


<a id="wnfwa-000009"></a>

## WNFWA-000009 — Windows Defender Firewall with Advanced Security log size must be configured for domain connections.

- Group: `V-241994`; rule revision: `SV-241994r922938_rule`; source severity: **low**.

### Source check text

~~~~~text
If the system is not a member of a domain, the Domain Profile requirements can be marked NA.

If the system is a member of a domain and the firewall's Domain Profile is not enabled (see V-17415), this requirement is also a finding.

If the following policy-based registry value exists and is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SOFTWARE\Policies\Microsoft\WindowsFirewall\DomainProfile\Logging\

Value Name:  LogFileSize

Type:  REG_DWORD
Value:  0x00004000 (16384) (or greater)

If the policy-based registry value does not exist, verify the following registry value. If it is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\DomainProfile\Logging\

Value Name:  LogFileSize

Type:  REG_DWORD
Value:  0x00004000 (16384) (or greater)
~~~~~

### Source fix text

~~~~~text
The preferred method of configuring the firewall settings is with a policy, particularly in a domain environment.

Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Microsoft Defender Firewall with Advanced Security >> Microsoft Defender Firewall with Advanced Security >> Microsoft Defender Firewall Properties (this link will be in the right pane) >> Domain Profile tab >> Logging (select Customize), "Size limit (KB):" to "16,384" or greater.

In addition to using policies, systems may also be configured using the firewall GUI or Netsh commands. These methods may be more appropriate for standalone systems.

The configuration settings in the GUI are the same as those specified in the policy above. Microsoft Defender Firewall Properties will be a link in the center pane after opening Microsoft Defender Firewall with Advanced Security.

The following Netsh command may also be used to configure this setting:

"Netsh advfirewall set domainprofile logging maxfilesize 16384" or greater.
~~~~~


<a id="wnfwa-000010"></a>

## WNFWA-000010 — Windows Defender Firewall with Advanced Security must log dropped packets when connected to a domain.

- Group: `V-241995`; rule revision: `SV-241995r922940_rule`; source severity: **low**.

### Source check text

~~~~~text
If the system is not a member of a domain, the Domain Profile requirements can be marked NA.

If the system is a member of a domain and the firewall's Domain Profile is not enabled (see V-17415), this requirement is also a finding.

If the following policy-based registry value exists and is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SOFTWARE\Policies\Microsoft\WindowsFirewall\DomainProfile\Logging\

Value Name:  LogDroppedPackets

Type:  REG_DWORD
Value:  0x00000001 (1)

If the policy-based registry value does not exist, verify the following registry value. If it is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\DomainProfile\Logging\

Value Name:  LogDroppedPackets

Type:  REG_DWORD
Value:  0x00000001 (1)
~~~~~

### Source fix text

~~~~~text
The preferred method of configuring the firewall settings is with a policy, particularly in a domain environment.

Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall Properties (this link will be in the right pane) >> Domain Profile tab >> Logging (select Customize), "Log dropped packets" to "Yes".

In addition to using policies, systems may also be configured using the firewall GUI or Netsh commands. These methods may be more appropriate for standalone systems.

The configuration settings in the GUI are the same as those specified in the policy above. Microsoft Defender Firewall Properties will be a link in the center pane after opening Microsoft Defender Firewall with Advanced Security.

The following Netsh commands may also be used to configure this setting:

"Netsh advfirewall set domainprofile logging droppedconnections enable".
or
"Netsh advfirewall set allprofiles logging droppedconnections enable".
~~~~~


<a id="wnfwa-000011"></a>

## WNFWA-000011 — Windows Defender Firewall with Advanced Security must log successful connections when connected to a domain.

- Group: `V-241996`; rule revision: `SV-241996r922942_rule`; source severity: **low**.

### Source check text

~~~~~text
If the system is not a member of a domain, the Domain Profile requirements can be marked NA.

If the system is a member of a domain and the firewall's Domain Profile is not enabled (see V-17415), this requirement is also a finding.

If the following policy-based registry value exists and is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SOFTWARE\Policies\Microsoft\WindowsFirewall\DomainProfile\Logging\

Value Name:  LogSuccessfulConnections

Type:  REG_DWORD
Value:  0x00000001 (1)

If the policy-based registry value does not exist, verify the following registry value. If it is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\DomainProfile\Logging\

Value Name:  LogSuccessfulConnections

Type:  REG_DWORD
Value:  0x00000001 (1)
~~~~~

### Source fix text

~~~~~text
The preferred method of configuring the firewall settings is with a policy, particularly in a domain environment.

Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall Properties (this link will be in the right pane) >> Domain Profile tab >> Logging (select Customize), "Log successful connections" to "Yes".

In addition to using policies, systems may also be configured using the firewall GUI or Netsh commands. These methods may be more appropriate for standalone systems.

The configuration settings in the GUI are the same as those specified in the policy above. Microsoft Defender Firewall Properties will be a link in the center pane after opening Microsoft Defender Firewall with Advanced Security.

The following Netsh commands may also be used to configure this setting:

"Netsh advfirewall set domainprofile logging allowedconnections enable".
or
"Netsh advfirewall set allprofiles logging allowedconnections enable".
~~~~~


<a id="wnfwa-000012"></a>

## WNFWA-000012 — Windows Defender Firewall with Advanced Security must block unsolicited inbound connections when connected to a private network.

- Group: `V-241997`; rule revision: `SV-241997r922944_rule`; source severity: **high**.

### Source check text

~~~~~text
If the firewall's Private Profile is not enabled (see V-17416), this requirement is also a finding.

If the following policy-based registry value exists and is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SOFTWARE\Policies\Microsoft\WindowsFirewall\PrivateProfile\

Value Name:  DefaultInboundAction

Type:  REG_DWORD
Value:  0x00000001 (1)

If the policy-based registry value does not exist, verify the following registry value. If it is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\StandardProfile\

Value Name:  DefaultInboundAction

Type:  REG_DWORD
Value:  0x00000001 (1)
~~~~~

### Source fix text

~~~~~text
The preferred method of configuring the firewall settings is with a policy, particularly in a domain environment.

Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall Properties (this link will be in the right pane) >> Private Profile tab >> State, "Inbound connections" to "Block (default)".

In addition to using policies, systems may also be configured using the firewall GUI or Netsh commands. These methods may be more appropriate for standalone systems.

The configuration settings in the GUI are the same as those specified in the policy above. Microsoft Defender Firewall Properties will be a link in the center pane after opening Microsoft Defender Firewall with Advanced Security.

The following Netsh commands may also be used to configure this setting:

"Netsh advfirewall set privateprofile firewallpolicy blockinbound,allowoutbound".
or
"Netsh advfirewall set allprofiles firewallpolicy blockinbound,allowoutbound".

Both inbound and outbound parameters must be specified to execute this command.
~~~~~


<a id="wnfwa-000013"></a>

## WNFWA-000013 — Windows Defender Firewall with Advanced Security must allow outbound connections, unless a rule explicitly blocks the connection when connected to a private network.

- Group: `V-241998`; rule revision: `SV-241998r922946_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the firewall's Private Profile is not enabled (see V-17416), this requirement is also a finding.

If the following policy-based registry value exists and is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SOFTWARE\Policies\Microsoft\WindowsFirewall\PrivateProfile\

Value Name:  DefaultOutboundAction

Type:  REG_DWORD
Value:  0x00000000 (0)

If the policy-based registry value does not exist, verify the following registry value. If it is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\StandardProfile\

Value Name:  DefaultOutboundAction

Type:  REG_DWORD
Value:  0x00000000 (0)
~~~~~

### Source fix text

~~~~~text
The preferred method of configuring the firewall settings is with a policy, particularly in a domain environment.

Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall Properties (this link will be in the right pane) >> Private Profile tab >> State, "Outbound connections" to "Allow (default)".

In addition to using policies, systems may also be configured using the firewall GUI or Netsh commands. These methods may be more appropriate for standalone systems.

The configuration settings in the GUI are the same as those specified in the policy above. Microsoft Defender Firewall Properties will be a link in the center pane after opening Microsoft Defender Firewall with Advanced Security.

The following Netsh commands may also be used to configure this setting:

"Netsh advfirewall set privateprofile firewallpolicy blockinbound,allowoutbound".
or
"Netsh advfirewall set allprofiles firewallpolicy blockinbound,allowoutbound".

Both inbound and outbound parameters must be specified to execute this command.
~~~~~


<a id="wnfwa-000017"></a>

## WNFWA-000017 — Windows Defender Firewall with Advanced Security log size must be configured for private network connections.

- Group: `V-241999`; rule revision: `SV-241999r922948_rule`; source severity: **low**.

### Source check text

~~~~~text
If the firewall's Private Profile is not enabled (see V-17416), this requirement is also a finding.

If the following policy-based registry value exists and is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SOFTWARE\Policies\Microsoft\WindowsFirewall\PrivateProfile\Logging\

Value Name:  LogFileSize

Type:  REG_DWORD
Value:  0x00004000 (16384) (or greater)

If the policy-based registry value does not exist, verify the following registry value. If it is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\StandardProfile\Logging\

Value Name:  LogFileSize

Type:  REG_DWORD
Value:  0x00004000 (16384) (or greater)
~~~~~

### Source fix text

~~~~~text
The preferred method of configuring the firewall settings is with a policy, particularly in a domain environment.

Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall Properties (this link will be in the right pane) >> Private Profile tab >> Logging (select Customize), "Size limit (KB)" to "16,384" or greater.

In addition to using policies, systems may also be configured using the firewall GUI or Netsh commands. These methods may be more appropriate for standalone systems.

The configuration settings in the GUI are the same as those specified in the policy above. Microsoft Defender Firewall Properties will be a link in the center pane after opening Microsoft Defender Firewall with Advanced Security.

The following Netsh command may also be used to configure this setting:

"Netsh advfirewall set privateprofile logging maxfilesize 16384" or greater.
~~~~~


<a id="wnfwa-000018"></a>

## WNFWA-000018 — Windows Defender Firewall with Advanced Security must log dropped packets when connected to a private network.

- Group: `V-242000`; rule revision: `SV-242000r922950_rule`; source severity: **low**.

### Source check text

~~~~~text
If the firewall's Private Profile is not enabled (see V-17416), this requirement is also a finding.

If the following policy-based registry value exists and is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SOFTWARE\Policies\Microsoft\WindowsFirewall\PrivateProfile\Logging\

Value Name:  LogDroppedPackets

Type:  REG_DWORD
Value:  0x00000001 (1)

If the policy-based registry value does not exist, verify the following registry value. If it is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\StandardProfile\Logging\

Value Name:  LogDroppedPackets

Type:  REG_DWORD
Value:  0x00000001 (1)
~~~~~

### Source fix text

~~~~~text
The preferred method of configuring the firewall settings is with a policy, particularly in a domain environment.

Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall Properties (this link will be in the right pane) >> Private Profile tab >> Logging (select Customize), "Log dropped packets" to "Yes".

In addition to using policies, systems may also be configured using the firewall GUI or Netsh commands. These methods may be more appropriate for standalone systems.

The configuration settings in the GUI are the same as those specified in the policy above. Microsoft Defender Firewall Properties will be a link in the center pane after opening Microsoft Defender Firewall with Advanced Security.

The following Netsh commands may also be used to configure this setting:

"Netsh advfirewall set privateprofile logging droppedconnections enable".
or
"Netsh advfirewall set allprofiles logging droppedconnections enable".
~~~~~


<a id="wnfwa-000019"></a>

## WNFWA-000019 — Windows Defender Firewall with Advanced Security must log successful connections when connected to a private network.

- Group: `V-242001`; rule revision: `SV-242001r922952_rule`; source severity: **low**.

### Source check text

~~~~~text
If the firewall's Private Profile is not enabled (see V-17416), this requirement is also a finding.

If the following policy-based registry value exists and is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SOFTWARE\Policies\Microsoft\WindowsFirewall\PrivateProfile\Logging\

Value Name:  LogSuccessfulConnections

Type:  REG_DWORD
Value:  0x00000001 (1)

If the policy-based registry value does not exist, verify the following registry value. If it is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\StandardProfile\Logging\

Value Name:  LogSuccessfulConnections

Type:  REG_DWORD
Value:  0x00000001 (1)
~~~~~

### Source fix text

~~~~~text
The preferred method of configuring the firewall settings is with a policy, particularly in a domain environment.

Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Microsoft Defender Firewall with Advanced Security >> Microsoft Defender Firewall with Advanced Security >> Microsoft Defender Firewall Properties (this link will be in the right pane) >> Private Profile tab >> Logging (select Customize), "Logged successful connections" to "Yes".

In addition to using policies, systems may also be configured using the firewall GUI or Netsh commands. These methods may be more appropriate for standalone systems.

The configuration settings in the GUI are the same as those specified in the policy above. Microsoft Defender Firewall Properties will be a link in the center pane after opening Microsoft Defender Firewall with Advanced Security.

The following Netsh commands may also be used to configure this setting:

"Netsh advfirewall set privateprofile logging allowedconnections enable".
or
"Netsh advfirewall set allprofiles logging allowedconnections enable".
~~~~~


<a id="wnfwa-000020"></a>

## WNFWA-000020 — Windows Defender Firewall with Advanced Security must block unsolicited inbound connections when connected to a public network.

- Group: `V-242002`; rule revision: `SV-242002r922954_rule`; source severity: **high**.

### Source check text

~~~~~text
If the firewall's Public Profile is not enabled (see V-17417), this requirement is also a finding.

If the following policy-based registry value exists and is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SOFTWARE\Policies\Microsoft\WindowsFirewall\PublicProfile\

Value Name:  DefaultInboundAction

Type:  REG_DWORD
Value:  0x00000001 (1)

If the policy-based registry value does not exist, verify the following registry value. If it is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\PublicProfile\

Value Name:  DefaultInboundAction

Type:  REG_DWORD
Value:  0x00000001 (1)
~~~~~

### Source fix text

~~~~~text
The preferred method of configuring the firewall settings is with a policy, particularly in a domain environment.

Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall Properties (this link will be in the right pane) >> Public Profile tab >> State, "Inbound connections" to "Block (default)".

In addition to using policies, systems may also be configured using the firewall GUI or Netsh commands. These methods may be more appropriate for standalone systems.

The configuration settings in the GUI are the same as those specified in the policy above. Microsoft Defender Firewall Properties will be a link in the center pane after opening Microsoft Defender Firewall with Advanced Security.

The following Netsh commands may also be used to configure this setting:

"Netsh advfirewall set publicprofile firewallpolicy blockinbound,allowoutbound".
or
"Netsh advfirewall set allprofiles firewallpolicy blockinbound,allowoutbound".

Both inbound and outbound parameters must be specified to execute this command.
~~~~~


<a id="wnfwa-000021"></a>

## WNFWA-000021 — Windows Defender Firewall with Advanced Security must allow outbound connections, unless a rule explicitly blocks the connection when connected to a public network.

- Group: `V-242003`; rule revision: `SV-242003r922956_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the firewall's Public Profile is not enabled (see V-17417), this requirement is also a finding.

If the following policy-based registry value exists and is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SOFTWARE\Policies\Microsoft\WindowsFirewall\PublicProfile\

Value Name:  DefaultOutboundAction

Type:  REG_DWORD
Value:  0x00000000 (0)

If the policy-based registry value does not exist, verify the following registry value. If it is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\PublicProfile\

Value Name:  DefaultOutboundAction

Type:  REG_DWORD
Value:  0x00000000 (0)
~~~~~

### Source fix text

~~~~~text
The preferred method of configuring the firewall settings is with a policy, particularly in a domain environment.

Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall Properties (this link will be in the right pane) >> Public Profile tab >> State, "Outbound connections" to "Allow (default)".

In addition to using policies, systems may also be configured using the firewall GUI or Netsh commands. These methods may be more appropriate for standalone systems.

The configuration settings in the GUI are the same as those specified in the policy above. Microsoft Defender Firewall Properties will be a link in the center pane after opening Microsoft Defender Firewall with Advanced Security.

The following Netsh commands may also be used to configure this setting:

"Netsh advfirewall set publicprofile firewallpolicy blockinbound,allowoutbound".
or
"Netsh advfirewall set allprofiles firewallpolicy blockinbound,allowoutbound".

Both inbound and outbound parameters must be specified to execute this command.
~~~~~


<a id="wnfwa-000024"></a>

## WNFWA-000024 — Windows Defender Firewall with Advanced Security local firewall rules must not be merged with Group Policy settings when connected to a public network.

- Group: `V-242004`; rule revision: `SV-242004r922958_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the system is not a member of a domain, this is NA.

If the firewall's Public Profile is not enabled (see V-17417), this requirement is also a finding.

Verify the registry value below.

If this registry value does not exist or is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SOFTWARE\Policies\Microsoft\WindowsFirewall\PublicProfile\

Value Name:  AllowLocalPolicyMerge

Type:  REG_DWORD
Value:  0x00000000 (0)
~~~~~

### Source fix text

~~~~~text
If the system is not a member of a domain, this is NA.

Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall Properties (this link will be in the right pane) >> Public Profile tab >> Settings (select Customize) >> Rule merging, "Apply local firewall rules:" to "No".
~~~~~


<a id="wnfwa-000025"></a>

## WNFWA-000025 — Windows Defender Firewall with Advanced Security local connection rules must not be merged with Group Policy settings when connected to a public network.

- Group: `V-242005`; rule revision: `SV-242005r922960_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the system is not a member of a domain, this is NA.

If the firewall's Public Profile is not enabled (see V-17417), this requirement is also a finding.

Verify the registry value below.

If this registry value does not exist or is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SOFTWARE\Policies\Microsoft\WindowsFirewall\PublicProfile\

Value Name:  AllowLocalIPsecPolicyMerge

Type:  REG_DWORD
Value:  0x00000000 (0)
~~~~~

### Source fix text

~~~~~text
If the system is not a member of a domain, this is NA.

Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall Properties (this link will be in the right pane) >> Public Profile tab >> Settings (select Customize) >> Rule merging, "Apply local connection security rules:" to "No".
~~~~~


<a id="wnfwa-000027"></a>

## WNFWA-000027 — Windows Defender Firewall with Advanced Security log size must be configured for public network connections.

- Group: `V-242006`; rule revision: `SV-242006r922962_rule`; source severity: **low**.

### Source check text

~~~~~text
If the firewall's Public Profile is not enabled (see V-17417), this requirement is also a finding.

If the following policy-based registry value exists and is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SOFTWARE\Policies\Microsoft\WindowsFirewall\PublicProfile\Logging\

Value Name:  LogFileSize

Type:  REG_DWORD
Value:  0x00004000 (16384) (or greater)

If the policy-based registry value does not exist, verify the following registry value. If it is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\PublicProfile\Logging\

Value Name:  LogFileSize

Type:  REG_DWORD
Value:  0x00004000 (16384) (or greater)
~~~~~

### Source fix text

~~~~~text
The preferred method of configuring the firewall settings is with a policy, particularly in a domain environment.

Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Microsoft Defender Firewall with Advanced Security >> Microsoft Defender Firewall with Advanced Security >> Microsoft Defender Firewall Properties (this link will be in the right pane) >> Public Profile tab >> Logging (select Customize), "Size limit (KB)" to "16,384" or greater.

In addition to using policies, systems may also be configured using the firewall GUI or Netsh commands. These methods may be more appropriate for standalone systems.

The configuration settings in the GUI are the same as those specified in the policy above. Microsoft Defender Firewall Properties will be a link in the center pane after opening Microsoft Defender Firewall with Advanced Security.

The following Netsh command may also be used to configure this setting:

"Netsh advfirewall set publicprofile logging maxfilesize 16384" or greater.
~~~~~


<a id="wnfwa-000028"></a>

## WNFWA-000028 — Windows Defender Firewall with Advanced Security must log dropped packets when connected to a public network.

- Group: `V-242007`; rule revision: `SV-242007r922964_rule`; source severity: **low**.

### Source check text

~~~~~text
If the firewall's Public Profile is not enabled (see V-17417), this requirement is also a finding.

If the following policy-based registry value exists and is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SOFTWARE\Policies\Microsoft\WindowsFirewall\PublicProfile\Logging\

Value Name:  LogDroppedPackets

Type:  REG_DWORD
Value:  0x00000001 (1)

If the policy-based registry value does not exist, verify the following registry value. If it is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\PublicProfile\Logging\

Value Name:  LogDroppedPackets

Type:  REG_DWORD
Value:  0x00000001 (1)
~~~~~

### Source fix text

~~~~~text
The preferred method of configuring the firewall settings is with a policy, particularly in a domain environment.

Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall Properties (this link will be in the right pane) >> Public Profile tab >> Logging (select Customize), "Log dropped packets" to "Yes".

In addition to using policies, systems may also be configured using the firewall GUI or Netsh commands. These methods may be more appropriate for standalone systems.

The configuration settings in the GUI are the same as those specified in the policy above. Microsoft Defender Firewall Properties will be a link in the center pane after opening Microsoft Defender Firewall with Advanced Security.

The following Netsh commands may also be used to configure this setting:

"Netsh advfirewall set publicprofile logging droppedconnections enable".
or
"Netsh advfirewall set allprofiles logging droppedconnections enable".
~~~~~


<a id="wnfwa-000029"></a>

## WNFWA-000029 — Windows Defender Firewall with Advanced Security must log successful connections when connected to a public network.

- Group: `V-242008`; rule revision: `SV-242008r922966_rule`; source severity: **low**.

### Source check text

~~~~~text
If the firewall's Public Profile is not enabled (see V-17417), this requirement is also a finding.

If the following policy-based registry value exists and is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SOFTWARE\Policies\Microsoft\WindowsFirewall\PublicProfile\Logging\

Value Name:  LogSuccessfulConnections

Type:  REG_DWORD
Value:  0x00000001 (1)

If the policy-based registry value does not exist, verify the following registry value. If it is not configured as specified, this is a finding.

Registry Hive:  HKEY_LOCAL_MACHINE
Registry Path:  \SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\PublicProfile\Logging\

Value Name:  LogSuccessfulConnections

Type:  REG_DWORD
Value:  0x00000001 (1)
~~~~~

### Source fix text

~~~~~text
The preferred method of configuring the firewall settings is with a policy, particularly in a domain environment.

Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall with Advanced Security >> Windows Defender Firewall Properties (this link will be in the right pane) >> Public Profile tab >> Logging (select Customize), "Logged successful connections" to "Yes".

In addition to using policies, systems may also be configured using the firewall GUI or Netsh commands. These methods may be more appropriate for standalone systems.

The configuration settings in the GUI are the same as those specified in the policy above. Microsoft Defender Firewall Properties will be a link in the center pane after opening Microsoft Defender Firewall with Advanced Security.

The following Netsh commands may also be used to configure this setting:

"Netsh advfirewall set publicprofile logging allowedconnections enable".
or
"Netsh advfirewall set allprofiles logging allowedconnections enable".
~~~~~


<a id="wnfwa-000100"></a>

## WNFWA-000100 — Inbound exceptions to the firewall on domain workstations must only allow authorized remote management hosts.

- Group: `V-242009`; rule revision: `SV-242009r922967_rule`; source severity: **medium**.

### Source check text

~~~~~text
This requirement is NA for servers and non domain workstations.

Verify firewall exceptions for inbound connections on domain workstations only allow authorized management systems and remote management hosts.

Review inbound firewall exception rules in Microsoft Defender Firewall with Advanced Security. Firewall rules can be complex and should be reviewed with the firewall administrator.

One method for restricting inbound connections is to only allow exceptions for a specific scope of remote IP addresses.

If allowed inbound exceptions are not limited to authorized management systems and remote management hosts, this is a finding.
~~~~~

### Source fix text

~~~~~text
Ensure firewall exceptions to inbound connections on domain workstations only allow authorized management systems and remote management hosts.

Firewall rules can be complex and should be thoroughly tested before applying in a production environment.

One method for restricting inbound connections is to only allow exceptions for a specific scope of remote IP addresses. For any inbound rules that allow connections from other systems, configure the Scope for Remote IP addresses to those of authorized management systems and remote management hosts. This may be defined as an IP address, subnet, or range. Apply the rule to all firewall profiles.
~~~~~
