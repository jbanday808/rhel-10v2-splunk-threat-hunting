# Windows 11 STIG V2R11 — rule reference UR

This reference reproduces the **check and fix** text from the user-supplied, unclassified manual XCCDF (Release: 11 Benchmark Date: 30 Sep 2026). It contains 28 rules. Line-end whitespace is normalized for readability. The source is a version-specific reference: confirm the required release and use the official benchmark and your assessor’s applicability decision. All targets, evidence and assessment statuses remain unverified.

Read the implementation guide, back up the system, and obtain approval before making changes. The source fix text can contain commands or settings that change the system; do not run them blindly. In a managed system use the approved policy owner and source.

| Rule | Severity | Title |
| --- | --- | --- |
| [WN11-UR-000005](#wn11-ur-000005) | medium | The "Access Credential Manager as a trusted caller" user right must not be assigned to any groups or accounts. |
| [WN11-UR-000010](#wn11-ur-000010) | medium | The "Access this computer from the network" user right must only be assigned to the Administrators and Remote Desktop Users groups. |
| [WN11-UR-000015](#wn11-ur-000015) | high | The "Act as part of the operating system" user right must not be assigned to any groups or accounts. |
| [WN11-UR-000025](#wn11-ur-000025) | medium | The "Allow log on locally" user right must only be assigned to the Administrators and Users groups. |
| [WN11-UR-000030](#wn11-ur-000030) | medium | The "Back up files and directories" user right must only be assigned to the Administrators group. |
| [WN11-UR-000035](#wn11-ur-000035) | medium | The "Change the system time" user right must only be assigned to Administrators and Local Service. |
| [WN11-UR-000040](#wn11-ur-000040) | medium | The "Create a pagefile" user right must only be assigned to the Administrators group. |
| [WN11-UR-000045](#wn11-ur-000045) | high | The "Create a token object" user right must not be assigned to any groups or accounts. |
| [WN11-UR-000050](#wn11-ur-000050) | medium | The "Create global objects" user right must only be assigned to Administrators, Service, Local Service, and Network Service. |
| [WN11-UR-000055](#wn11-ur-000055) | medium | The "Create permanent shared objects" user right must not be assigned to any groups or accounts. |
| [WN11-UR-000060](#wn11-ur-000060) | medium | The "Create symbolic links" user right must only be assigned to the Administrators group. |
| [WN11-UR-000065](#wn11-ur-000065) | high | The "Debug programs" user right must only be assigned to the Administrators group. |
| [WN11-UR-000070](#wn11-ur-000070) | medium | The "Deny access to this computer from the network" user right on workstations must be configured to prevent access from highly privileged domain accounts and local accounts on domain systems and unauthenticated access on all systems. |
| [WN11-UR-000075](#wn11-ur-000075) | medium | The "Deny log on as a batch job" user right on domain-joined workstations must be configured to prevent access from highly privileged domain accounts. |
| [WN11-UR-000080](#wn11-ur-000080) | medium | The "Deny log on as a service" user right on Windows 11 domain-joined workstations must be configured to prevent access from highly privileged domain accounts. |
| [WN11-UR-000085](#wn11-ur-000085) | medium | The "Deny log on locally" user right on workstations must be configured to prevent access from highly privileged domain accounts on domain systems and unauthenticated access on all systems. |
| [WN11-UR-000090](#wn11-ur-000090) | medium | The "Deny log on through Remote Desktop Services" user right on Windows 11 workstations must be configured to prevent access from highly privileged domain accounts and local accounts on domain systems and unauthenticated access on all systems. |
| [WN11-UR-000095](#wn11-ur-000095) | medium | The "Enable computer and user accounts to be trusted for delegation" user right must not be assigned to any groups or accounts. |
| [WN11-UR-000100](#wn11-ur-000100) | medium | The "Force shutdown from a remote system" user right must only be assigned to the Administrators group. |
| [WN11-UR-000110](#wn11-ur-000110) | medium | The "Impersonate a client after authentication" user right must only be assigned to Administrators, Service, Local Service, and Network Service. |
| [WN11-UR-000120](#wn11-ur-000120) | medium | The "Load and unload device drivers" user right must only be assigned to the Administrators group. |
| [WN11-UR-000125](#wn11-ur-000125) | medium | The "Lock pages in memory" user right must not be assigned to any groups or accounts. |
| [WN11-UR-000130](#wn11-ur-000130) | medium | The "Manage auditing and security log" user right must only be assigned to the Administrators group. |
| [WN11-UR-000140](#wn11-ur-000140) | medium | The "Modify firmware environment values" user right must only be assigned to the Administrators group. |
| [WN11-UR-000145](#wn11-ur-000145) | medium | The "Perform volume maintenance tasks" user right must only be assigned to the Administrators group. |
| [WN11-UR-000150](#wn11-ur-000150) | medium | The "Profile single process" user right must only be assigned to the Administrators group. |
| [WN11-UR-000160](#wn11-ur-000160) | medium | The "Restore files and directories" user right must only be assigned to the Administrators group. |
| [WN11-UR-000165](#wn11-ur-000165) | medium | The "Take ownership of files or other objects" user right must only be assigned to the Administrators group. |

<a id="wn11-ur-000005"></a>

## WN11-UR-000005 — The "Access Credential Manager as a trusted caller" user right must not be assigned to any groups or accounts.

- Group: `V-253479`; rule revision: `SV-253479r958726_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If any groups or accounts are granted the "Access Credential Manager as a trusted caller" user right, this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Access Credential Manager as a trusted caller" to be defined but containing no entries (blank).
~~~~~


<a id="wn11-ur-000010"></a>

## WN11-UR-000010 — The "Access this computer from the network" user right must only be assigned to the Administrators and Remote Desktop Users groups.

- Group: `V-253480`; rule revision: `SV-253480r1268226_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If any groups or accounts other than the following are granted the "Access this computer from the network" user right, this is a finding:

Administrators
Remote Desktop Users

If a domain application account such as for a management tool requires this user right, this would not be a finding.

Vendor documentation must support the requirement for having the user right.

The requirement must be documented with the ISSO.

The application account, managed at the domain level, must meet requirements for application account passwords, such as length and frequency of changes as defined in the Windows Server STIGs.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Access this computer from the network" to only include the following groups or accounts:

Administrators
Remote Desktop Users
~~~~~


<a id="wn11-ur-000015"></a>

## WN11-UR-000015 — The "Act as part of the operating system" user right must not be assigned to any groups or accounts.

- Group: `V-253481`; rule revision: `SV-253481r958726_rule`; source severity: **high**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If any groups or accounts (to include administrators), are granted the "Act as part of the operating system" user right, this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Act as part of the operating system" to be defined but containing no entries (blank).
~~~~~


<a id="wn11-ur-000025"></a>

## WN11-UR-000025 — The "Allow log on locally" user right must only be assigned to the Administrators and Users groups.

- Group: `V-253482`; rule revision: `SV-253482r1268226_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.

Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If any groups or accounts other than the following are granted the "Allow log on locally" user right, this is a finding:

Administrators
Users
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Allow log on locally" to only include the following groups or accounts:

Administrators
Users
~~~~~


<a id="wn11-ur-000030"></a>

## WN11-UR-000030 — The "Back up files and directories" user right must only be assigned to the Administrators group.

- Group: `V-253483`; rule revision: `SV-253483r958726_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If any groups or accounts other than the following are granted the "Back up files and directories" user right, this is a finding:

Administrators
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Back up files and directories" to only include the following groups or accounts:

Administrators
~~~~~


<a id="wn11-ur-000035"></a>

## WN11-UR-000035 — The "Change the system time" user right must only be assigned to Administrators and Local Service.

- Group: `V-253484`; rule revision: `SV-253484r958726_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If any groups or accounts other than the following are granted the "Change the system time" user right, this is a finding:

Administrators
LOCAL SERVICE
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Change the system time" to only include the following groups or accounts:

Administrators
LOCAL SERVICE
~~~~~


<a id="wn11-ur-000040"></a>

## WN11-UR-000040 — The "Create a pagefile" user right must only be assigned to the Administrators group.

- Group: `V-253485`; rule revision: `SV-253485r958726_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If any groups or accounts other than the following are granted the "Create a pagefile" user right, this is a finding:

Administrators
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Create a pagefile" to only include the following groups or accounts:

Administrators
~~~~~


<a id="wn11-ur-000045"></a>

## WN11-UR-000045 — The "Create a token object" user right must not be assigned to any groups or accounts.

- Group: `V-253486`; rule revision: `SV-253486r958726_rule`; source severity: **high**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If any groups or accounts are granted the "Create a token object" user right, this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Create a token object" to be defined but containing no entries (blank).
~~~~~


<a id="wn11-ur-000050"></a>

## WN11-UR-000050 — The "Create global objects" user right must only be assigned to Administrators, Service, Local Service, and Network Service.

- Group: `V-253487`; rule revision: `SV-253487r958726_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If any groups or accounts other than the following are granted the "Create global objects" user right, this is a finding:

Administrators
LOCAL SERVICE
NETWORK SERVICE
SERVICE
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Create global objects" to only include the following groups or accounts:

Administrators
LOCAL SERVICE
NETWORK SERVICE
SERVICE
~~~~~


<a id="wn11-ur-000055"></a>

## WN11-UR-000055 — The "Create permanent shared objects" user right must not be assigned to any groups or accounts.

- Group: `V-253488`; rule revision: `SV-253488r958726_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If any groups or accounts are granted the "Create permanent shared objects" user right, this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Create permanent shared objects" to be defined but containing no entries (blank).
~~~~~


<a id="wn11-ur-000060"></a>

## WN11-UR-000060 — The "Create symbolic links" user right must only be assigned to the Administrators group.

- Group: `V-253489`; rule revision: `SV-253489r958726_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If any groups or accounts other than the following are granted the "Create symbolic links" user right, this is a finding:

Administrators

If the workstation has an approved use of Hyper-V, such as being used as a dedicated admin workstation using Hyper-V to separate administration and standard user functions, "NT VIRTUAL MACHINES\VIRTUAL MACHINE" may be assigned this user right and is not a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Create symbolic links" to only include the following groups or accounts:

Administrators
~~~~~


<a id="wn11-ur-000065"></a>

## WN11-UR-000065 — The "Debug programs" user right must only be assigned to the Administrators group.

- Group: `V-253490`; rule revision: `SV-253490r958726_rule`; source severity: **high**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If any groups or accounts other than the following are granted the "Debug Programs" user right, this is a finding:

Administrators
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Debug programs" to only include the following groups or accounts:

Administrators
~~~~~


<a id="wn11-ur-000070"></a>

## WN11-UR-000070 — The "Deny access to this computer from the network" user right on workstations must be configured to prevent access from highly privileged domain accounts and local accounts on domain systems and unauthenticated access on all systems.

- Group: `V-253491`; rule revision: `SV-253491r1268226_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.

Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If the following groups or accounts are not defined for the "Deny access to this computer from the network" right, this is a finding:

Domain Systems Only:
Enterprise Admins group
Domain Admins group
Local account (see Note below)

All Systems:
Guests group

Privileged Access Workstations (PAWs) dedicated to the management of Active Directory are exempt from denying the Enterprise Admins and Domain Admins groups. (See the Windows Privileged Access Workstation STIG for PAW requirements.)

Note: "Local account" is a built-in security group used to assign user rights and permissions to all local accounts.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Deny access to this computer from the network" to include the following:

Domain Systems Only:
Enterprise Admins group
Domain Admins group
Local account (see Note below)

All Systems:
Guests group

Privileged Access Workstations (PAWs) dedicated to the management of Active Directory are exempt from denying the Enterprise Admins and Domain Admins groups. (See the Windows Privileged Access Workstation STIG for PAW requirements.)

Note: "Local account" is a built-in security group used to assign user rights and permissions to all local accounts.
~~~~~


<a id="wn11-ur-000075"></a>

## WN11-UR-000075 — The "Deny log on as a batch job" user right on domain-joined workstations must be configured to prevent access from highly privileged domain accounts.

- Group: `V-253492`; rule revision: `SV-253492r1268226_rule`; source severity: **medium**.

### Source check text

~~~~~text
This requirement is applicable to domain-joined systems, for standalone systems this is NA.

Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If the following groups or accounts are not defined for the "Deny log on as a batch job" right, this is a finding:

Domain Systems Only:
Enterprise Admin Group
Domain Admin Group
~~~~~

### Source fix text

~~~~~text
This requirement is applicable to domain-joined systems, for standalone systems this is NA.

Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Deny log on as a batch job" to include the following:

Domain Systems Only:
Enterprise Admin Group
Domain Admin Group
~~~~~


<a id="wn11-ur-000080"></a>

## WN11-UR-000080 — The "Deny log on as a service" user right on Windows 11 domain-joined workstations must be configured to prevent access from highly privileged domain accounts.

- Group: `V-253493`; rule revision: `SV-253493r1268226_rule`; source severity: **medium**.

### Source check text

~~~~~text
This requirement is applicable to domain-joined systems, for standalone systems this is NA.

Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If the following groups or accounts are not defined for the "Deny log on as a service" right , this is a finding:

Domain Systems Only:
Enterprise Admins Group
Domain Admins Group
~~~~~

### Source fix text

~~~~~text
This requirement is applicable to domain-joined systems, for standalone systems this is NA.

Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Deny log on as a service" to include the following:

Domain Systems Only:
Enterprise Admins Group
Domain Admins Group
~~~~~


<a id="wn11-ur-000085"></a>

## WN11-UR-000085 — The "Deny log on locally" user right on workstations must be configured to prevent access from highly privileged domain accounts on domain systems and unauthenticated access on all systems.

- Group: `V-253494`; rule revision: `SV-253494r1268226_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.

Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If the following groups or accounts are not defined for the "Deny log on locally" right, this is a finding.

Domain Systems Only:
Enterprise Admins Group
Domain Admins Group

Privileged Access Workstations (PAWs) dedicated to the management of Active Directory are exempt from denying the Enterprise Admins and Domain Admins groups. (See the Windows Privileged Access Workstation STIG for PAW requirements.)

All Systems:
Guests Group
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Deny log on locally" to include the following:

Domain Systems Only:
Enterprise Admins Group
Domain Admins Group

Privileged Access Workstations (PAWs) dedicated to the management of Active Directory are exempt from denying the Enterprise Admins and Domain Admins groups. (See the Windows Privileged Access Workstation STIG for PAW requirements.)

All Systems:
Guests Group
~~~~~


<a id="wn11-ur-000090"></a>

## WN11-UR-000090 — The "Deny log on through Remote Desktop Services" user right on Windows 11 workstations must be configured to prevent access from highly privileged domain accounts and local accounts on domain systems and unauthenticated access on all systems.

- Group: `V-253495`; rule revision: `SV-253495r1268226_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.

Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If the following groups or accounts are not defined for the "Deny log on through Remote Desktop Services" right, this is a finding:

If Remote Desktop Services is not used by the organization, the "Everyone" group can replace all of the groups listed below.

Domain Systems Only:
Enterprise Admins group
Domain Admins group
Local account (see Note below)

All Systems:
Guests group

Privileged Access Workstations (PAWs) dedicated to the management of Active Directory are exempt from denying the Enterprise Admins and Domain Admins groups. (See the Windows Privileged Access Workstation STIG for PAW requirements.)

Note: "Local account" is a built-in security group used to assign user rights and permissions to all local accounts.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Deny log on through Remote Desktop Services" to include the following:

If Remote Desktop Services is not used by the organization, assign the Everyone group this right to prevent all access.

Domain Systems Only:
Enterprise Admins group
Domain Admins group
Local account (see Note below)

All Systems:
Guests group

Privileged Access Workstations (PAWs) dedicated to the management of Active Directory are exempt from denying the Enterprise Admins and Domain Admins groups. (See the Windows Privileged Access Workstation STIG for PAW requirements.)

Note: "Local account" is a built-in security group used to assign user rights and permissions to all local accounts.
~~~~~


<a id="wn11-ur-000095"></a>

## WN11-UR-000095 — The "Enable computer and user accounts to be trusted for delegation" user right must not be assigned to any groups or accounts.

- Group: `V-253496`; rule revision: `SV-253496r958726_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If any groups or accounts are granted the "Enable computer and user accounts to be trusted for delegation" user right, this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Enable computer and user accounts to be trusted for delegation" to be defined but containing no entries (blank).
~~~~~


<a id="wn11-ur-000100"></a>

## WN11-UR-000100 — The "Force shutdown from a remote system" user right must only be assigned to the Administrators group.

- Group: `V-253497`; rule revision: `SV-253497r958726_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If any groups or accounts other than the following are granted the "Force shutdown from a remote system" user right, this is a finding:

Administrators
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Force shutdown from a remote system" to only include the following groups or accounts:

Administrators
~~~~~


<a id="wn11-ur-000110"></a>

## WN11-UR-000110 — The "Impersonate a client after authentication" user right must only be assigned to Administrators, Service, Local Service, and Network Service.

- Group: `V-253498`; rule revision: `SV-253498r1138526_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.

Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If any groups or accounts other than the following are granted the "Impersonate a client after authentication" user right, this is a finding:

Administrators
LOCAL SERVICE
NETWORK SERVICE
RESTRICTED SERVICES\PrintSpoolerService
SERVICE
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Impersonate a client after authentication" to only include the following groups or accounts:

Administrators
LOCAL SERVICE
NETWORK SERVICE
RESTRICTED SERVICES\PrintSpoolerService
SERVICE
~~~~~


<a id="wn11-ur-000120"></a>

## WN11-UR-000120 — The "Load and unload device drivers" user right must only be assigned to the Administrators group.

- Group: `V-253499`; rule revision: `SV-253499r958726_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If any groups or accounts other than the following are granted the "Load and unload device drivers" user right, this is a finding:

Administrators
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Load and unload device drivers" to only include the following groups or accounts:

Administrators
~~~~~


<a id="wn11-ur-000125"></a>

## WN11-UR-000125 — The "Lock pages in memory" user right must not be assigned to any groups or accounts.

- Group: `V-253500`; rule revision: `SV-253500r958726_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If any groups or accounts are granted the "Lock pages in memory" user right, this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Lock pages in memory" to be defined but containing no entries (blank).
~~~~~


<a id="wn11-ur-000130"></a>

## WN11-UR-000130 — The "Manage auditing and security log" user right must only be assigned to the Administrators group.

- Group: `V-253501`; rule revision: `SV-253501r958434_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If any groups or accounts other than the following are granted the "Manage auditing and security log" user right, this is a finding:

Administrators

If the organization has an "Auditors" group the assignment of this group to the user right would not be a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Manage auditing and security log" to only include the following groups or accounts:

Administrators
~~~~~


<a id="wn11-ur-000140"></a>

## WN11-UR-000140 — The "Modify firmware environment values" user right must only be assigned to the Administrators group.

- Group: `V-253502`; rule revision: `SV-253502r958726_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If any groups or accounts other than the following are granted the "Modify firmware environment values" user right, this is a finding:

Administrators
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Modify firmware environment values" to only include the following groups or accounts:

Administrators
~~~~~


<a id="wn11-ur-000145"></a>

## WN11-UR-000145 — The "Perform volume maintenance tasks" user right must only be assigned to the Administrators group.

- Group: `V-253503`; rule revision: `SV-253503r958726_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If any groups or accounts other than the following are granted the "Perform volume maintenance tasks" user right, this is a finding:

Administrators
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Perform volume maintenance tasks" to only include the following groups or accounts:

Administrators
~~~~~


<a id="wn11-ur-000150"></a>

## WN11-UR-000150 — The "Profile single process" user right must only be assigned to the Administrators group.

- Group: `V-253504`; rule revision: `SV-253504r958726_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If any groups or accounts other than the following are granted the "Profile single process" user right, this is a finding:

Administrators
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Profile single process" to only include the following groups or accounts:

Administrators
~~~~~


<a id="wn11-ur-000160"></a>

## WN11-UR-000160 — The "Restore files and directories" user right must only be assigned to the Administrators group.

- Group: `V-253505`; rule revision: `SV-253505r958726_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If any groups or accounts other than the following are granted the "Restore files and directories" user right, this is a finding:

Administrators
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Restore files and directories" to only include the following groups or accounts:

Administrators
~~~~~


<a id="wn11-ur-000165"></a>

## WN11-UR-000165 — The "Take ownership of files or other objects" user right must only be assigned to the Administrators group.

- Group: `V-253506`; rule revision: `SV-253506r958726_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment.

If any groups or accounts other than the following are granted the "Take ownership of files or other objects" user right, this is a finding:

Administrators
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Local Policies >> User Rights Assignment >> "Take ownership of files or other objects" to only include the following groups or accounts:

Administrators
~~~~~
