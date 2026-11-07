# Windows 11 STIG V2R11 — rule reference EP

This reference reproduces the **check and fix** text from the user-supplied, unclassified manual XCCDF (Release: 11 Benchmark Date: 30 Sep 2026). It contains 1 rules. Line-end whitespace is normalized for readability. The source is a version-specific reference: confirm the required release and use the official benchmark and your assessor’s applicability decision. All targets, evidence and assessment statuses remain unverified.

Read the implementation guide, back up the system, and obtain approval before making changes. The source fix text can contain commands or settings that change the system; do not run them blindly. In a managed system use the approved policy owner and source.

| Rule | Severity | Title |
| --- | --- | --- |
| [WN11-EP-000310](#wn11-ep-000310) | medium | Windows 11 Kernel (Direct Memory Access) DMA Protection must be enabled. |

<a id="wn11-ep-000310"></a>

## WN11-EP-000310 — Windows 11 Kernel (Direct Memory Access) DMA Protection must be enabled.

- Group: `V-253426`; rule revision: `SV-253426r991580_rule`; source severity: **medium**.

### Source check text

~~~~~text
If the following registry value does not exist or is not configured as specified, this is a finding:

Registry Hive: HKEY_LOCAL_MACHINE
Registry Path: \Software\Policies\Microsoft\Windows\Kernel DMA Protection

Value Name: DeviceEnumerationPolicy
Value Type: REG_DWORD
Value: 0
~~~~~

### Source fix text

~~~~~text
Configure the policy value for Computer Configuration >> Administrative Templates >> System >> Kernel DMA Protection >> "Enumeration policy for external devices incompatible with Kernel DMA Protection" to "Enabled" with "Enumeration Policy" set to "Block All".
~~~~~
