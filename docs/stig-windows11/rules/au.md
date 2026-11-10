# Windows 11 STIG V2R11 — rule reference AU

This reference reproduces the **check and fix** text from the user-supplied, unclassified manual XCCDF (Release: 11 Benchmark Date: 30 Sep 2026). It contains 49 rules. Line-end whitespace is normalized for readability. The source is a version-specific reference: confirm the required release and use the official benchmark and your assessor’s applicability decision. All targets, evidence and assessment statuses remain unverified.

Read the implementation guide, back up the system, and obtain approval before making changes. The source fix text can contain commands or settings that change the system; do not run them blindly. In a managed system use the approved policy owner and source.

| Rule | Severity | Title |
| --- | --- | --- |
| [WN11-AU-000005](#wn11-au-000005) | medium | The system must be configured to audit Account Logon - Credential Validation failures. |
| [WN11-AU-000010](#wn11-au-000010) | medium | The system must be configured to audit Account Logon - Credential Validation successes. |
| [WN11-AU-000030](#wn11-au-000030) | medium | The system must be configured to audit Account Management - Security Group Management successes. |
| [WN11-AU-000035](#wn11-au-000035) | medium | The system must be configured to audit Account Management - User Account Management failures. |
| [WN11-AU-000040](#wn11-au-000040) | medium | The system must be configured to audit Account Management - User Account Management successes. |
| [WN11-AU-000045](#wn11-au-000045) | medium | The system must be configured to audit Detailed Tracking - PNP Activity successes. |
| [WN11-AU-000050](#wn11-au-000050) | medium | The system must be configured to audit Detailed Tracking - Process Creation successes. |
| [WN11-AU-000054](#wn11-au-000054) | medium | The system must be configured to audit Logon/Logoff - Account Lockout failures. |
| [WN11-AU-000060](#wn11-au-000060) | medium | The system must be configured to audit Logon/Logoff - Group Membership successes. |
| [WN11-AU-000065](#wn11-au-000065) | medium | The system must be configured to audit Logon/Logoff - Logoff successes. |
| [WN11-AU-000070](#wn11-au-000070) | medium | The system must be configured to audit Logon/Logoff - Logon failures. |
| [WN11-AU-000075](#wn11-au-000075) | medium | The system must be configured to audit Logon/Logoff - Logon successes. |
| [WN11-AU-000080](#wn11-au-000080) | medium | The system must be configured to audit Logon/Logoff - Special Logon successes. |
| [WN11-AU-000081](#wn11-au-000081) | medium | Windows 11 must be configured to audit Object Access - File Share failures. |
| [WN11-AU-000082](#wn11-au-000082) | medium | Windows 11 must be configured to audit Object Access - File Share successes. |
| [WN11-AU-000083](#wn11-au-000083) | medium | Windows 11 must be configured to audit Object Access - Other Object Access Events successes. |
| [WN11-AU-000084](#wn11-au-000084) | medium | Windows 11 must be configured to audit Object Access - Other Object Access Events failures. |
| [WN11-AU-000085](#wn11-au-000085) | medium | The system must be configured to audit Object Access - Removable Storage failures. |
| [WN11-AU-000090](#wn11-au-000090) | medium | The system must be configured to audit Object Access - Removable Storage successes. |
| [WN11-AU-000100](#wn11-au-000100) | medium | The system must be configured to audit Policy Change - Audit Policy Change successes. |
| [WN11-AU-000105](#wn11-au-000105) | medium | The system must be configured to audit Policy Change - Authentication Policy Change successes. |
| [WN11-AU-000107](#wn11-au-000107) | medium | The system must be configured to audit Policy Change - Authorization Policy Change successes. |
| [WN11-AU-000110](#wn11-au-000110) | medium | The system must be configured to audit Privilege Use - Sensitive Privilege Use failures. |
| [WN11-AU-000115](#wn11-au-000115) | medium | The system must be configured to audit Privilege Use - Sensitive Privilege Use successes. |
| [WN11-AU-000120](#wn11-au-000120) | medium | The system must be configured to audit System - IPsec Driver failures. |
| [WN11-AU-000130](#wn11-au-000130) | medium | The system must be configured to audit System - Other System Events successes. |
| [WN11-AU-000135](#wn11-au-000135) | medium | The system must be configured to audit System - Other System Events failures. |
| [WN11-AU-000140](#wn11-au-000140) | medium | The system must be configured to audit System - Security State Change successes. |
| [WN11-AU-000150](#wn11-au-000150) | medium | The system must be configured to audit System - Security System Extension successes. |
| [WN11-AU-000155](#wn11-au-000155) | medium | The system must be configured to audit System - System Integrity failures. |
| [WN11-AU-000160](#wn11-au-000160) | medium | The system must be configured to audit System - System Integrity successes. |
| [WN11-AU-000500](#wn11-au-000500) | medium | The Application event log size must be configured to 32768 KB or greater. |
| [WN11-AU-000505](#wn11-au-000505) | medium | The security event log size must be configured to a value that holds at least one week's worth of audit records. |
| [WN11-AU-000510](#wn11-au-000510) | medium | The System event log size must be configured to 32768 KB or greater. |
| [WN11-AU-000515](#wn11-au-000515) | medium | Windows 11 permissions for the Application event log must prevent access by non-privileged accounts. |
| [WN11-AU-000520](#wn11-au-000520) | medium | Windows 11 permissions for the Security event log must prevent access by non-privileged accounts. |
| [WN11-AU-000525](#wn11-au-000525) | medium | Windows 11 permissions for the System event log must prevent access by non-privileged accounts. |
| [WN11-AU-000555](#wn11-au-000555) | medium | Windows 11 must be configured to audit Other Policy Change Events Failures. |
| [WN11-AU-000560](#wn11-au-000560) | medium | Windows 11 must be configured to audit other Logon/Logoff Events Successes. |
| [WN11-AU-000565](#wn11-au-000565) | medium | Windows 11 must be configured to audit other Logon/Logoff Events Failures. |
| [WN11-AU-000570](#wn11-au-000570) | medium | Windows 11 must be configured to audit Detailed File Share Failures. |
| [WN11-AU-000575](#wn11-au-000575) | medium | Windows 11 must be configured to audit MPSSVC Rule-Level Policy Change Successes. |
| [WN11-AU-000580](#wn11-au-000580) | medium | Windows 11 must be configured to audit MPSSVC Rule-Level Policy Change Failures. |
| [WN11-AU-000585](#wn11-au-000585) | medium | Windows 11 must have command line process auditing events enabled for failures. |
| [WN11-AU-000583](#wn11-au-000583) | medium | Windows 11 must be configured to audit handle manipulation failures. |
| [WN11-AU-000589](#wn11-au-000589) | medium | Windows 11 must be configured to audit registry failures. |
| [WN11-AU-000586](#wn11-au-000586) | medium | Windows 11 must be configured to audit registry successes. |
| [WN11-AU-000587](#wn11-au-000587) | medium | Windows 11 must be configured to audit sensitive privilege use successes. |
| [WN11-AU-000588](#wn11-au-000588) | medium | Windows 11 must be configured to audit sensitive privilege use failures. |

<a id="wn11-au-000005"></a>

## WN11-AU-000005 — The system must be configured to audit Account Logon - Credential Validation failures.

- Group: `V-253306`; rule revision: `SV-253306r991570_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*".

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

Account Logon >> Credential Validation - Failure
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Account Logon >> "Audit Credential Validation" with "Failure" selected.
~~~~~


<a id="wn11-au-000010"></a>

## WN11-AU-000010 — The system must be configured to audit Account Logon - Credential Validation successes.

- Group: `V-253307`; rule revision: `SV-253307r991570_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*".

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

Account Logon >> Credential Validation - Success
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Account Logon >> "Audit Credential Validation" with "Success" selected.
~~~~~


<a id="wn11-au-000030"></a>

## WN11-AU-000030 — The system must be configured to audit Account Management - Security Group Management successes.

- Group: `V-253308`; rule revision: `SV-253308r971541_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*".

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

Account Management >> Security Group Management - Success
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Account Management >> "Audit Security Group Management" with "Success" selected.
~~~~~


<a id="wn11-au-000035"></a>

## WN11-AU-000035 — The system must be configured to audit Account Management - User Account Management failures.

- Group: `V-253309`; rule revision: `SV-253309r958566_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*".

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

Account Management >> User Account Management - Failure
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Account Management >> "Audit User Account Management" with "Failure" selected.
~~~~~


<a id="wn11-au-000040"></a>

## WN11-AU-000040 — The system must be configured to audit Account Management - User Account Management successes.

- Group: `V-253310`; rule revision: `SV-253310r991551_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*".

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

Account Management >> User Account Management - Success
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Account Management >> "Audit User Account Management" with "Success" selected.
~~~~~


<a id="wn11-au-000045"></a>

## WN11-AU-000045 — The system must be configured to audit Detailed Tracking - PNP Activity successes.

- Group: `V-253311`; rule revision: `SV-253311r1051047_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*"

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

Detailed Tracking >> Plug and Play Events - Success
~~~~~

### Source fix text

~~~~~text
Computer Configuration >> Windows Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Detailed Tracking >> "Audit PNP Activity" with "Success" selected.
~~~~~


<a id="wn11-au-000050"></a>

## WN11-AU-000050 — The system must be configured to audit Detailed Tracking - Process Creation successes.

- Group: `V-253312`; rule revision: `SV-253312r1051048_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*".

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

Detailed Tracking >> Process Creation - Success
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Detailed Tracking >> "Audit Process Creation" with "Success" selected.
~~~~~


<a id="wn11-au-000054"></a>

## WN11-AU-000054 — The system must be configured to audit Logon/Logoff - Account Lockout failures.

- Group: `V-253313`; rule revision: `SV-253313r991578_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:

Open a Command Prompt with elevated privileges ("Run as Administrator").

Enter "AuditPol /get /category:*"

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

Logon/Logoff >> Account Lockout - Failure
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Logon/Logoff >> "Audit Account Lockout" with "Failure" selected.
~~~~~


<a id="wn11-au-000060"></a>

## WN11-AU-000060 — The system must be configured to audit Logon/Logoff - Group Membership successes.

- Group: `V-253314`; rule revision: `SV-253314r991570_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings (Windows Vista or later) to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*"

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

Logon/Logoff >> Group Membership - Success
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Logon/Logoff >> "Audit Group Membership" with "Success" selected.
~~~~~


<a id="wn11-au-000065"></a>

## WN11-AU-000065 — The system must be configured to audit Logon/Logoff - Logoff successes.

- Group: `V-253315`; rule revision: `SV-253315r1268219_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*".

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

Logon/Logoff >> Logoff - Success
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Logon/Logoff >> "Audit Logoff" with "Success" selected.
~~~~~


<a id="wn11-au-000070"></a>

## WN11-AU-000070 — The system must be configured to audit Logon/Logoff - Logon failures.

- Group: `V-253316`; rule revision: `SV-253316r991581_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*".

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

Logon/Logoff >> Logon - Failure
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Logon/Logoff >> "Audit Logon" with "Failure" selected.
~~~~~


<a id="wn11-au-000075"></a>

## WN11-AU-000075 — The system must be configured to audit Logon/Logoff - Logon successes.

- Group: `V-253317`; rule revision: `SV-253317r991581_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings (Windows Vista or later) to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*".

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

Logon/Logoff >> Logon - Success
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Logon/Logoff >> "Audit Logon" with "Success" selected.
~~~~~


<a id="wn11-au-000080"></a>

## WN11-AU-000080 — The system must be configured to audit Logon/Logoff - Special Logon successes.

- Group: `V-253318`; rule revision: `SV-253318r991578_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings (Windows Vista or later) to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*".

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

Logon/Logoff >> Special Logon - Success
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Logon/Logoff >> "Audit Special Logon" with "Success" selected.
~~~~~


<a id="wn11-au-000081"></a>

## WN11-AU-000081 — Windows 11 must be configured to audit Object Access - File Share failures.

- Group: `V-253319`; rule revision: `SV-253319r991572_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings (Windows Vista or later) to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:

Open PowerShell or a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*"
Compare the AuditPol settings with the following:
Object Access >> File Share - Failure

If the system does not audit the above, this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Object Access >> "Audit File Share" with "Failure" selected.
~~~~~


<a id="wn11-au-000082"></a>

## WN11-AU-000082 — Windows 11 must be configured to audit Object Access - File Share successes.

- Group: `V-253320`; rule revision: `SV-253320r991572_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings (Windows Vista or later) to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:

Open PowerShell or a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*"

Compare the AuditPol settings with the following:

Object Access >> File Share - Success

If the system does not audit the above, this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Object Access >> "Audit File Share" with "Success" selected.
~~~~~


<a id="wn11-au-000083"></a>

## WN11-AU-000083 — Windows 11 must be configured to audit Object Access - Other Object Access Events successes.

- Group: `V-253321`; rule revision: `SV-253321r991572_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.
Use the AuditPol tool to review the current Audit Policy configuration:

Open PowerShell or a Command Prompt with elevated privileges ("Run as Administrator").

Enter "AuditPol /get /category:*"

Compare the AuditPol settings with the following:

Object Access >> Other Object Access Events - Success

If the system does not audit the above, this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Object Access >> "Audit Other Object Access Events" with "Success" selected.
~~~~~


<a id="wn11-au-000084"></a>

## WN11-AU-000084 — Windows 11 must be configured to audit Object Access - Other Object Access Events failures.

- Group: `V-253322`; rule revision: `SV-253322r991572_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:

Open PowerShell or a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*"
Compare the AuditPol settings with the following:
Object Access >> Other Object Access Events - Failure

If the system does not audit the above, this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Object Access >> "Audit Other Object Access Events" with "Failure" selected.
~~~~~


<a id="wn11-au-000085"></a>

## WN11-AU-000085 — The system must be configured to audit Object Access - Removable Storage failures.

- Group: `V-253323`; rule revision: `SV-253323r991583_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*"

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

Object Access >> Removable Storage - Failure

Some virtual machines may generate excessive audit events for access to the virtual hard disk itself when this setting is enabled. This may be set to Not Configured in such cases and would not be a finding. This must be documented with the ISSO to include mitigations such as monitoring or restricting any actual removable storage connected to the VM.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Object Access >> "Audit Removable Storage" with "Failure" selected.
~~~~~


<a id="wn11-au-000090"></a>

## WN11-AU-000090 — The system must be configured to audit Object Access - Removable Storage successes.

- Group: `V-253324`; rule revision: `SV-253324r991583_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings (Windows Vista or later) to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*"

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

Object Access >> Removable Storage - Success

Some virtual machines may generate excessive audit events for access to the virtual hard disk itself when this setting is enabled. This may be set to Not Configured in such cases and would not be a finding. This must be documented with the ISSO to include mitigations such as monitoring or restricting any actual removable storage connected to the VM.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Object Access >> "Audit Removable Storage" with "Success" selected.
~~~~~


<a id="wn11-au-000100"></a>

## WN11-AU-000100 — The system must be configured to audit Policy Change - Audit Policy Change successes.

- Group: `V-253325`; rule revision: `SV-253325r991572_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*".

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

Policy Change >> Audit Policy Change - Success
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Policy Change >> "Audit Policy Change" with "Success" selected.
~~~~~


<a id="wn11-au-000105"></a>

## WN11-AU-000105 — The system must be configured to audit Policy Change - Authentication Policy Change successes.

- Group: `V-253326`; rule revision: `SV-253326r991572_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.
Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*".

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

Policy Change >> Authentication Policy Change - Success
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Policy Change >> "Audit Authentication Policy Change" with "Success" selected.
~~~~~


<a id="wn11-au-000107"></a>

## WN11-AU-000107 — The system must be configured to audit Policy Change - Authorization Policy Change successes.

- Group: `V-253327`; rule revision: `SV-253327r991572_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:
-Open a Command Prompt with elevated privileges ("Run as Administrator").
-Enter "AuditPol /get /category:*".

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding.

Policy Change >> Authorization Policy Change - Success
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Policy Change >> "Audit Authorization Policy Change" with "Success" selected.
~~~~~


<a id="wn11-au-000110"></a>

## WN11-AU-000110 — The system must be configured to audit Privilege Use - Sensitive Privilege Use failures.

- Group: `V-253328`; rule revision: `SV-253328r958732_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*".

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

Privilege Use >> Sensitive Privilege Use - Failure
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Privilege Use >> "Audit Sensitive Privilege Use" with "Failure" selected.
~~~~~


<a id="wn11-au-000115"></a>

## WN11-AU-000115 — The system must be configured to audit Privilege Use - Sensitive Privilege Use successes.

- Group: `V-253329`; rule revision: `SV-253329r991575_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*".

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

Privilege Use >> Sensitive Privilege Use - Success
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Privilege Use >> "Audit Sensitive Privilege Use" with "Success" selected.
~~~~~


<a id="wn11-au-000120"></a>

## WN11-AU-000120 — The system must be configured to audit System - IPsec Driver failures.

- Group: `V-253330`; rule revision: `SV-253330r991586_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*".

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

System >> IPsec Driver - Failure
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> System >> "Audit IPsec Driver" with "Failure" selected.
~~~~~


<a id="wn11-au-000130"></a>

## WN11-AU-000130 — The system must be configured to audit System - Other System Events successes.

- Group: `V-253331`; rule revision: `SV-253331r991579_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*"

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

System >> Other System Events - Success
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> System >> "Audit Other System Events" with "Success" selected.
~~~~~


<a id="wn11-au-000135"></a>

## WN11-AU-000135 — The system must be configured to audit System - Other System Events failures.

- Group: `V-253332`; rule revision: `SV-253332r991579_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*"

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

System >> Other System Events - Failure
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> System >> "Audit Other System Events" with "Failure" selected.
~~~~~


<a id="wn11-au-000140"></a>

## WN11-AU-000140 — The system must be configured to audit System - Security State Change successes.

- Group: `V-253333`; rule revision: `SV-253333r991575_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*".

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

System >> Security State Change - Success
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> System >> "Audit Security State Change" with "Success" selected.
~~~~~


<a id="wn11-au-000150"></a>

## WN11-AU-000150 — The system must be configured to audit System - Security System Extension successes.

- Group: `V-253334`; rule revision: `SV-253334r991575_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*".

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

System >> Security System Extension - Success
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> System >> "Audit Security System Extension" with "Success" selected.
~~~~~


<a id="wn11-au-000155"></a>

## WN11-AU-000155 — The system must be configured to audit System - System Integrity failures.

- Group: `V-253335`; rule revision: `SV-253335r991573_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*".

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

System >> System Integrity - Failure
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> System >> "Audit System Integrity" with "Failure" selected.
~~~~~


<a id="wn11-au-000160"></a>

## WN11-AU-000160 — The system must be configured to audit System - System Integrity successes.

- Group: `V-253336`; rule revision: `SV-253336r991573_rule`; source severity: **medium**.

### Source check text

~~~~~text
Security Option "Audit: Force audit policy subcategory settings to override audit policy category settings" must be set to "Enabled" (WN11-SO-000030) for the detailed auditing subcategories to be effective.

Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*".

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

System >> System Integrity - Success
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> System >> "Audit System Integrity" with "Success" selected.
~~~~~


<a id="wn11-au-000500"></a>

## WN11-AU-000500 — The Application event log size must be configured to 32768 KB or greater.

- Group: `V-253337`; rule revision: `SV-253337r958752_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the system is configured to send audit records directly to an audit server, this is NA. This must be documented with the ISSO.

If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\EventLog\Application\

Value Name: MaxSize

Value Type: REG_DWORD
Value: 0x00008000 (32768) (or greater)
~~~~~

### Source fix text

~~~~~text
If the system is configured to send audit records directly to an audit server, this is NA. This must be documented with the ISSO.

Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Event Log Service >> Application >> "Specify the maximum log file size (KB)" to "Enabled" with a "Maximum Log Size (KB)" of "32768" or greater.
~~~~~


<a id="wn11-au-000505"></a>

## WN11-AU-000505 — The security event log size must be configured to a value that holds at least one week's worth of audit records.

- Group: `V-253338`; rule revision: `SV-253338r1186375_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the system is configured to send audit records directly to an audit server, this requirement is not applicable. This must be documented with the information system security officer (ISSO).

The registry configuration setting below must be set (at least) to a value equal to the size needed to contain one week's worth of audit records in the security event log. The value used below is an example that assumes a typical week’s log size of 5GB.

If the following registry value does not exist or is not configured as specified, this is a finding:

NOTE: The following registry entry is an example; the value must equal at least one week's worth of records.

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\EventLog\Security\

Value Name: MaxSize

Value Type: REG_DWORD
Value:0x49960800 (5120000) (or greater)
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Event Log Service >> Security >> "Specify the maximum log file size (KB)" to "Enabled" with a "Maximum Log Size (KB)" of a value that will contain one week of audit records or greater.

If the system is configured to send audit records directly to an audit server, this must be documented with the ISSO.
~~~~~


<a id="wn11-au-000510"></a>

## WN11-AU-000510 — The System event log size must be configured to 32768 KB or greater.

- Group: `V-253339`; rule revision: `SV-253339r958752_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the system is configured to send audit records directly to an audit server, this is NA. This must be documented with the ISSO.

If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\EventLog\System\

Value Name: MaxSize

Value Type: REG_DWORD
Value: 0x00008000 (32768) (or greater)
~~~~~

### Source fix text

~~~~~text
If the system is configured to send audit records directly to an audit server, this is NA. This must be documented with the ISSO.

Configure the policy value for Computer Configuration >> Administrative Templates >> Windows Components >> Event Log Service >> System >> "Specify the maximum log file size (KB)" to "Enabled" with a "Maximum Log Size (KB)" of "32768" or greater.
~~~~~


<a id="wn11-au-000515"></a>

## WN11-AU-000515 — Windows 11 permissions for the Application event log must prevent access by non-privileged accounts.

- Group: `V-253340`; rule revision: `SV-253340r958434_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the permissions on the Application event log (Application.evtx). Standard user accounts or groups must not have access. The default permissions listed below satisfy this requirement.

Eventlog - Full Control
SYSTEM - Full Control
Administrators - Full Control

The default location is the "%SystemRoot%\SYSTEM32\WINEVT\LOGS" directory. They may have been moved to another folder.

If the permissions for these files are not as restrictive as the ACLs listed, this is a finding.

Note: If "APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES" has Special Permissions, this would not be a finding.
~~~~~

### Source fix text

~~~~~text
Ensure the permissions on the Application event log (Application.evtx) are configured to prevent standard user accounts or groups from having access. The default permissions listed below satisfy this requirement.

Eventlog - Full Control
SYSTEM - Full Control
Administrators - Full Control

The default location is the "%SystemRoot%\SYSTEM32\WINEVT\LOGS" directory.

If the location of the logs has been changed, when adding Eventlog to the permissions, it must be entered as "NT Service\Eventlog".
~~~~~


<a id="wn11-au-000520"></a>

## WN11-AU-000520 — Windows 11 permissions for the Security event log must prevent access by non-privileged accounts.

- Group: `V-253341`; rule revision: `SV-253341r958434_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the permissions on the Security event log (Security.evtx). Standard user accounts or groups must not have access. The default permissions listed below satisfy this requirement.

Eventlog - Full Control
SYSTEM - Full Control
Administrators - Full Control

The default location is the "%SystemRoot%\SYSTEM32\WINEVT\LOGS" directory. They may have been moved to another folder.

If the permissions for these files are not as restrictive as the ACLs listed, this is a finding.

Note: If "APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES" has Special Permissions, this would not be a finding.
~~~~~

### Source fix text

~~~~~text
Ensure the permissions on the Security event log (Security.evtx) are configured to prevent standard user accounts or groups from having access. The default permissions listed below satisfy this requirement.

Eventlog - Full Control
SYSTEM - Full Control
Administrators - Full Control

The default location is the "%SystemRoot%\SYSTEM32\WINEVT\LOGS" directory.

If the location of the logs has been changed, when adding Eventlog to the permissions, it must be entered as "NT Service\Eventlog".
~~~~~


<a id="wn11-au-000525"></a>

## WN11-AU-000525 — Windows 11 permissions for the System event log must prevent access by non-privileged accounts.

- Group: `V-253342`; rule revision: `SV-253342r958434_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the permissions on the System event log (System.evtx). Standard user accounts or groups must not have access. The default permissions listed below satisfy this requirement.

Eventlog - Full Control
SYSTEM - Full Control
Administrators - Full Control

The default location is the "%SystemRoot%\SYSTEM32\WINEVT\LOGS" directory. They may have been moved to another folder.

If the permissions for these files are not as restrictive as the ACLs listed, this is a finding.

Note: If "APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES" has Special Permissions, this would not be a finding.
~~~~~

### Source fix text

~~~~~text
Ensure the permissions on the System event log (System.evtx) are configured to prevent standard user accounts or groups from having access. The default permissions listed below satisfy this requirement.

Eventlog - Full Control
SYSTEM - Full Control
Administrators - Full Control

The default location is the "%SystemRoot%\SYSTEM32\WINEVT\LOGS" directory.

If the location of the logs has been changed, when adding Eventlog to the permissions, it must be entered as "NT Service\Eventlog".
~~~~~


<a id="wn11-au-000555"></a>

## WN11-AU-000555 — Windows 11 must be configured to audit Other Policy Change Events Failures.

- Group: `V-253344`; rule revision: `SV-253344r958412_rule`; source severity: **medium**.

### Source check text

~~~~~text
Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*".

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

Policy Change >> Other Policy Change Events - Failure
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Policy Change>> "Audit Other Policy Change Events" with "Failure" selected.
~~~~~


<a id="wn11-au-000560"></a>

## WN11-AU-000560 — Windows 11 must be configured to audit other Logon/Logoff Events Successes.

- Group: `V-253345`; rule revision: `SV-253345r958412_rule`; source severity: **medium**.

### Source check text

~~~~~text
Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*".

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

Logon/Logoff >> Other Logon/Logoff Events - Success
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Logon/Logoff >> "Audit Other Logon/Logoff Events" with "Success" selected.
~~~~~


<a id="wn11-au-000565"></a>

## WN11-AU-000565 — Windows 11 must be configured to audit other Logon/Logoff Events Failures.

- Group: `V-253346`; rule revision: `SV-253346r958412_rule`; source severity: **medium**.

### Source check text

~~~~~text
Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*".

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

Logon/Logoff >> Other Logon/Logoff Events - Failure
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Logon/Logoff >> "Audit Other Logon/Logoff Events" with "Failure" selected.
~~~~~


<a id="wn11-au-000570"></a>

## WN11-AU-000570 — Windows 11 must be configured to audit Detailed File Share Failures.

- Group: `V-253347`; rule revision: `SV-253347r958412_rule`; source severity: **medium**.

### Source check text

~~~~~text
Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*".

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

Object Access >> Detailed File Share - Failure
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Object Access >> Audit Detailed File Share" with "Failure" selected.
~~~~~


<a id="wn11-au-000575"></a>

## WN11-AU-000575 — Windows 11 must be configured to audit MPSSVC Rule-Level Policy Change Successes.

- Group: `V-253348`; rule revision: `SV-253348r958412_rule`; source severity: **medium**.

### Source check text

~~~~~text
Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*".

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

Policy Change >> MPSSVC Rule-Level Policy Change - Success
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Policy Change >> Audit MPSSVC Rule-Level Policy Change" with "Success" selected.
~~~~~


<a id="wn11-au-000580"></a>

## WN11-AU-000580 — Windows 11 must be configured to audit MPSSVC Rule-Level Policy Change Failures.

- Group: `V-253349`; rule revision: `SV-253349r958412_rule`; source severity: **medium**.

### Source check text

~~~~~text
Use the AuditPol tool to review the current Audit Policy configuration:
Open a Command Prompt with elevated privileges ("Run as Administrator").
Enter "AuditPol /get /category:*".

Compare the AuditPol settings with the following. If the system does not audit the following, this is a finding:

Policy Change >> MPSSVC Rule-Level Policy Change - Failure
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Policy Change >> Audit MPSSVC Rule-Level Policy Change" with "Failure" selected.
~~~~~


<a id="wn11-au-000585"></a>

## WN11-AU-000585 — Windows 11 must have command line process auditing events enabled for failures.

- Group: `V-257770`; rule revision: `SV-257770r958412_rule`; source severity: **medium**.

### Source check text

~~~~~text
Ensure Audit Process Creation auditing has been enabled:

Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policy >> Detailed Tracking >> Audit Process Creation.

If "Audit Process Creation" is not set to "Failure", this is a finding.
~~~~~

### Source fix text

~~~~~text
Go to Computer Configuration >> Windows Settings >>Security Settings>> Advanced Audit Policy Configuration >> System Audit Policies >> Detailed Tracking >> Set "Audit Process Creation" to "Failure".
~~~~~


<a id="wn11-au-000583"></a>

## WN11-AU-000583 — Windows 11 must be configured to audit handle manipulation failures.

- Group: `V-278928`; rule revision: `SV-278928r1268225_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify that Audit Handle Manipulation auditing has been enabled:

Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Object Access >> Audit Handle Manipulation.

If "Audit Handle Manipulation" is not set to "Failure", this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Object Access >> "Audit Handle Manipulation" with "Failure" selected.
~~~~~


<a id="wn11-au-000589"></a>

## WN11-AU-000589 — Windows 11 must be configured to audit registry failures.

- Group: `V-278930`; rule revision: `SV-278930r1268225_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify that Audit Registry auditing has been enabled:

Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Object Access >> Audit Registry.

If "Audit Registry" is not set to "Failure", this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Object Access >> "Audit Registry" with "Failure" selected.
~~~~~


<a id="wn11-au-000586"></a>

## WN11-AU-000586 — Windows 11 must be configured to audit registry successes.

- Group: `V-278931`; rule revision: `SV-278931r1268225_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify that Audit Registry auditing has been enabled:

Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Object Access >> Audit Registry.

If "Audit Registry" is not set to "Success", this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Object Access >> "Audit Registry" with "Success" selected.
~~~~~


<a id="wn11-au-000587"></a>

## WN11-AU-000587 — Windows 11 must be configured to audit sensitive privilege use successes.

- Group: `V-278932`; rule revision: `SV-278932r1268225_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify that Audit Sensitive Privilege Use auditing has been enabled:

Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Privilege Use >> Audit Sensitive Privilege Use.

If "Audit Sensitive Privilege Use" is not set to "Success", this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Privilege Use >> Audit Sensitive Privilege Use with "Success" selected.
~~~~~


<a id="wn11-au-000588"></a>

## WN11-AU-000588 — Windows 11 must be configured to audit sensitive privilege use failures.

- Group: `V-278933`; rule revision: `SV-278933r1268225_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify that Audit Sensitive Privilege Use auditing has been enabled:

Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Privilege Use >> Audit Sensitive Privilege Use.

If "Audit Sensitive Privilege Use" is not set to "Failure", this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Advanced Audit Policy Configuration >> System Audit Policies >> Privilege Use >> Audit Sensitive Privilege Use with "Failure" selected.
~~~~~
