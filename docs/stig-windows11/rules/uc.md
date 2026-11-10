# Windows 11 STIG V2R11 — rule reference UC

This reference reproduces the **check and fix** text from the user-supplied, unclassified manual XCCDF (Release: 11 Benchmark Date: 30 Sep 2026). It contains 2 rules. Line-end whitespace is normalized for readability. The source is a version-specific reference: confirm the required release and use the official benchmark and your assessor’s applicability decision. All targets, evidence and assessment statuses remain unverified.

Read the implementation guide, back up the system, and obtain approval before making changes. The source fix text can contain commands or settings that change the system; do not run them blindly. In a managed system use the approved policy owner and source.

| Rule | Severity | Title |
| --- | --- | --- |
| [WN11-UC-000015](#wn11-uc-000015) | low | Toast notifications to the lock screen must be turned off. |
| [WN11-UC-000020](#wn11-uc-000020) | medium | Zone information must be preserved when saving attachments. |

<a id="wn11-uc-000015"></a>

## WN11-UC-000015 — Toast notifications to the lock screen must be turned off.

- Group: `V-253477`; rule revision: `SV-253477r1260004_rule`; source severity: **low**.

### Source check text

~~~~~text
Note: This Check must be performed for each interactive user profile on the system.
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_CURRENT_USER
Registry Path: \SOFTWARE\Policies\Microsoft\Windows\CurrentVersion\PushNotifications\

Value Name: NoToastApplicationNotificationOnLockScreen

Value Type: REG_DWORD
Value: 1

Note: This requirement is applicable to profiles for interactive logins. It is not applicable for Service accounts.

To determine the system's enabled user profiles:
Run "PowerShell" as an administrator.

Execute the following command:
Get-LocalUser | Where-Object {$_.Enabled -eq $true}
~~~~~

### Source fix text

~~~~~text
For each user profile on the system, configure the policy value for User Configuration >> Administrative Templates >> Start Menu and Taskbar >> Notifications >> "Turn off toast notifications on the lock screen" to "Enabled".
~~~~~


<a id="wn11-uc-000020"></a>

## WN11-UC-000020 — Zone information must be preserved when saving attachments.

- Group: `V-253478`; rule revision: `SV-253478r1268251_rule`; source severity: **medium**.

### Source check text

~~~~~text
Note: This Check must be performed for each interactive user profile on the system.

The default behavior is for Windows to mark file attachments with their zone information.

If it exists and is configured with a value of "1", this is a finding.

Registry Hive: HKEY_CURRENT_USER
Registry Path: \SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Attachments\

Value Name: SaveZoneInformation

Value Type: REG_DWORD
Value: 0x00000002 (2) (or if the Value Name does not exist)

Note: This requirement is applicable to profiles for interactive logins. It is not applicable for Service accounts.

To determine the system's enabled user profiles:
Run "PowerShell" as an administrator.

Execute the following command:
Get-LocalUser | Where-Object {$_.Enabled -eq $true}
~~~~~

### Source fix text

~~~~~text
The default behavior is for Windows to mark file attachments with their zone information.

To correct this, (for each user profile on the system) configure the policy value for User Configuration >> Administrative Templates >> Windows Components >> Attachment Manager >> "Do not preserve zone information in file attachments" to "Not Configured" or "Disabled".
~~~~~
