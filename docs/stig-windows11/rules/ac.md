# Windows 11 STIG V2R11 — rule reference AC

This reference reproduces the **check and fix** text from the user-supplied, unclassified manual XCCDF (Release: 11 Benchmark Date: 30 Sep 2026). It contains 9 rules. Line-end whitespace is normalized for readability. The source is a version-specific reference: confirm the required release and use the official benchmark and your assessor’s applicability decision. All targets, evidence and assessment statuses remain unverified.

Read the implementation guide, back up the system, and obtain approval before making changes. The source fix text can contain commands or settings that change the system; do not run them blindly. In a managed system use the approved policy owner and source.

| Rule | Severity | Title |
| --- | --- | --- |
| [WN11-AC-000005](#wn11-ac-000005) | medium | Windows 11 account lockout duration must be configured to 15 minutes or greater. |
| [WN11-AC-000010](#wn11-ac-000010) | medium | The number of allowed bad logon attempts must be configured to three or less. |
| [WN11-AC-000015](#wn11-ac-000015) | medium | The period of time before the bad logon counter is reset must be configured to 15 minutes. |
| [WN11-AC-000020](#wn11-ac-000020) | medium | The password history must be configured to 24 passwords remembered. |
| [WN11-AC-000025](#wn11-ac-000025) | medium | The maximum password age must be configured to 180 days or less. |
| [WN11-AC-000030](#wn11-ac-000030) | medium | The minimum password age must be configured to at least 1 day. |
| [WN11-AC-000035](#wn11-ac-000035) | medium | Passwords must, at a minimum, be 14 characters. |
| [WN11-AC-000040](#wn11-ac-000040) | medium | The built-in Microsoft password complexity filter must be enabled. |
| [WN11-AC-000045](#wn11-ac-000045) | high | Reversible password encryption must be disabled. |

<a id="wn11-ac-000005"></a>

## WN11-AC-000005 — Windows 11 account lockout duration must be configured to 15 minutes or greater.

- Group: `V-253297`; rule revision: `SV-253297r958736_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Account Policies >> Account Lockout Policy.

If the "Account lockout duration" is less than "15" minutes (excluding "0"), this is a finding.

Configuring this to "0", requiring an administrator to unlock the account, is more restrictive and is not a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Account Policies >> Account Lockout Policy >> "Account lockout duration" to "15" minutes or greater.

A value of "0" is also acceptable, requiring an administrator to unlock the account.
~~~~~


<a id="wn11-ac-000010"></a>

## WN11-AC-000010 — The number of allowed bad logon attempts must be configured to three or less.

- Group: `V-253298`; rule revision: `SV-253298r958388_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Account Policies >> Account Lockout Policy.

If the "Account lockout threshold" is "0" or more than "3" attempts, this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Account Policies >> Account Lockout Policy >> "Account lockout threshold" to "3" or less invalid logon attempts (excluding "0" which is unacceptable).
~~~~~


<a id="wn11-ac-000015"></a>

## WN11-AC-000015 — The period of time before the bad logon counter is reset must be configured to 15 minutes.

- Group: `V-253299`; rule revision: `SV-253299r958388_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Account Policies >> Account Lockout Policy.

If the "Reset account lockout counter after" value is less than "15" minutes, this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Account Policies >> Account Lockout Policy >> "Reset account lockout counter after" to "15" minutes.
~~~~~


<a id="wn11-ac-000020"></a>

## WN11-AC-000020 — The password history must be configured to 24 passwords remembered.

- Group: `V-253300`; rule revision: `SV-253300r1256653_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.

Run "gpedit.msc".

For GPO-managed systems, navigate to:

Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Account Policies >> Password Policy.

Or

For Intune-managed systems, navigate to:

HKLM:\SOFTWARE\Microsoft\PolicyManager\current\device\DeviceLock!DevicePasswordHistory

If the value for "Enforce password history" is less than "24" passwords remembered, this is a finding.
~~~~~

### Source fix text

~~~~~text
For GPO-managed systems:

Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Account Policies >> Password Policy >> "Enforce password history" to "24" passwords remembered.

For Intune-managed systems:

Revise the Intune policy to set password history policy to "24" passwords remembered.
~~~~~


<a id="wn11-ac-000025"></a>

## WN11-AC-000025 — The maximum password age must be configured to 180 days or less.

- Group: `V-253301`; rule revision: `SV-253301r1268211_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Account Policies >> Password Policy.

If the value for the "Maximum password age" is greater than "180" days, this is a finding. If the value is set to "0" (never expires), this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Account Policies >> Password Policy >> "Maximum Password Age" to "180" days or less (excluding "0" which is unacceptable).
~~~~~


<a id="wn11-ac-000030"></a>

## WN11-AC-000030 — The minimum password age must be configured to at least 1 day.

- Group: `V-253302`; rule revision: `SV-253302r1051043_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Account Policies >> Password Policy.

If the value for the "Minimum password age" is less than "1" day, this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Account Policies >> Password Policy >> "Minimum Password Age" to at least "1" day.
~~~~~


<a id="wn11-ac-000035"></a>

## WN11-AC-000035 — Passwords must, at a minimum, be 14 characters.

- Group: `V-253303`; rule revision: `SV-253303r1051044_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Account Policies >> Password Policy.

If the value for the "Minimum password length," is less than "14" characters, this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Account Policies >> Password Policy >> "Minimum password length" to "14" characters.
~~~~~


<a id="wn11-ac-000040"></a>

## WN11-AC-000040 — The built-in Microsoft password complexity filter must be enabled.

- Group: `V-253304`; rule revision: `SV-253304r1051045_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Account Policies >> Password Policy.

If the value for "Password must meet complexity requirements" is not set to "Enabled", this is a finding.

If the site is using a password filter that requires this setting be set to "Disabled" for the filter to be used, this would not be considered a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Account Policies >> Password Policy >> "Password must meet complexity requirements" to "Enabled".
~~~~~


<a id="wn11-ac-000045"></a>

## WN11-AC-000045 — Reversible password encryption must be disabled.

- Group: `V-253305`; rule revision: `SV-253305r1051046_rule`; source severity: **high**.

### Source check text

~~~~~text
Verify the effective setting in Local Group Policy Editor.
Run "gpedit.msc".

Navigate to Local Computer Policy >> Computer Configuration >> Windows Settings >> Security Settings >> Account Policies >> Password Policy.

If the value for "Store password using reversible encryption" is not set to "Disabled", this is a finding.
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Windows Settings >> Security Settings >> Account Policies >> Password Policy >> "Store passwords using reversible encryption" to "Disabled".
~~~~~
