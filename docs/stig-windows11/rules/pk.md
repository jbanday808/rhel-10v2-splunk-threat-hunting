# Windows 11 STIG V2R11 — rule reference PK

This reference reproduces the **check and fix** text from the user-supplied, unclassified manual XCCDF (Release: 11 Benchmark Date: 30 Sep 2026). It contains 4 rules. Line-end whitespace is normalized for readability. The source is a version-specific reference: confirm the required release and use the official benchmark and your assessor’s applicability decision. All targets, evidence and assessment statuses remain unverified.

Read the implementation guide, back up the system, and obtain approval before making changes. The source fix text can contain commands or settings that change the system; do not run them blindly. In a managed system use the approved policy owner and source.

| Rule | Severity | Title |
| --- | --- | --- |
| [WN11-PK-000005](#wn11-pk-000005) | medium | The DoW Root CA certificates must be installed in the Trusted Root Store. |
| [WN11-PK-000010](#wn11-pk-000010) | medium | The External Root CA certificates must be installed in the Trusted Root Store on unclassified systems. |
| [WN11-PK-000015](#wn11-pk-000015) | medium | The DoW Interoperability Root CA cross-certificates must be installed in the Untrusted Certificates Store on unclassified systems. |
| [WN11-PK-000020](#wn11-pk-000020) | medium | The US DoW CCEB Interoperability Root CA cross-certificates must be installed in the Untrusted Certificates Store on unclassified systems. |

<a id="wn11-pk-000005"></a>

## WN11-PK-000005 — The DoW Root CA certificates must be installed in the Trusted Root Store.

- Group: `V-253427`; rule revision: `SV-253427r1256656_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the DoW Root CA certificates are installed as Trusted Root Certification Authorities.

The certificates referenced below apply to unclassified systems; refer to PKE documentation for other networks.

Run "PowerShell" as an administrator.

Execute the following command:

Get-ChildItem -Path Cert:Localmachine\root | Where Subject -Like "*DoD*" | FL Subject, NotAfter

If valid DoW Root CA certificates (such as those below) are not displayed, this is a finding.

Note: The Common Names (CN) below are examples. Verify the "CN" displayed is a DoW Root CA and is not expired.

Subject: CN=DoD Root CA 3, OU=PKI, OU=DoD, O=U.S. Government, C=US
NotAfter: 12/30/2029

Subject: CN=DoD Root CA 5, OU=PKI, OU=DoD, O=U.S. Government, C=US
NotAfter: 6/14/2041

Subject: CN=DoD Root CA 6 OU=PKI, OU=DoD, O=U.S. Government, C=US
NotAfter: 1/24/2053

Alternately, use the Certificates MMC snap-in:

Run "MMC".

Select "File" and "Add/Remove Snap-in".

Select "Certificates" and click "Add".

Select "Computer account" and click "Next".

Select "Local computer: (the computer this console is running on)" and click "Finish".

Click "OK".

Expand "Certificates" and navigate to Trusted Root Certification Authorities >> Certificates.

For each of the DoW Root CA certificates listed:

Right-click on the certificate and select "Open".

Select the "Details" tab.

Verify the Expiration Date is a future date.

Scroll to the bottom and select "Subject".

If valid (unexpired) DoW Root CA certificates (such as those below) are not listed, this is a finding.

DoD Root CA 3
DoD Root CA 5
DoD Root CA 6
~~~~~

### Source fix text

~~~~~text
Install valid (unexpired) DoW Root CA certificates.

The list below is not to be treated as exhaustive. The STIG should not be used as a definitive resource for the organizationally approved certificates for the systems.

DoD Root CA 3
DoD Root CA 5
DoD Root CA 6

The InstallRoot tool is available on Cyber Exchange at https://cyber.mil/pki-pke/tools-configuration-files. Certificate bundles published by the PKI can be found at https://crl.gds.disa.mil/.
~~~~~


<a id="wn11-pk-000010"></a>

## WN11-PK-000010 — The External Root CA certificates must be installed in the Trusted Root Store on unclassified systems.

- Group: `V-253428`; rule revision: `SV-253428r1256659_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the ECA Root CA certificates are installed on unclassified systems as Trusted Root Certification Authorities.

Run "PowerShell" as an administrator.

Execute the following command:

Get-ChildItem -Path Cert:Localmachine\root | Where Subject -Like "*ECA*" | FL Subject, NotAfter

If valid ECA Root CA certificates (such as those below) are not displayed, this is a finding.

Note: The Common Names (CN) below are examples. Verify the "CN" displayed (ECA Root CA) is not expired. As of this writing, ECA Root CA 4 and ECA Root 5 are valid (among others).

Subject: CN=ECA Root CA 4, OU=ECA, O=U.S. Government, C=US
Subject: CN=ECA Root CA 5, OU=ECA, O=U.S. Government, C=US

Alternately, use the Certificates MMC snap-in:

Run "MMC".

Select "File" and "Add/Remove Snap-in".

Select "Certificates" and click "Add".

Select "Computer account" and click "Next".

Select "Local computer: (the computer this console is running on)" and click "Finish".

Click "OK".

Expand "Certificates" and navigate to Trusted Root Certification Authorities >> Certificates.

For each ECA Root CA certificate displayed:

Right-click on the certificate and select "Open".

Select the "Details" tab.

Verify the Expiration Date is a future date.

Scroll to the bottom and select "Subject".

If any of the certificates listed do not include "ECA Root CA" in the name or are expired, this is a finding.

Note: This should not be relied upon as a complete list of possible ECA Root CA certificates.

ECA Root CA 4
ECA Root CA 5
~~~~~

### Source fix text

~~~~~text
Install valid (unexpired) ECA Root CA certificates on unclassified systems.

The list below is not to be treated as exhaustive. The STIG should not be used as a definitive resource for the organizationally approved certificates for the systems.

ECA Root CA 4
ECA Root CA 5

The InstallRoot tool is available on Cyber Exchange at https://cyber.mil/pki-pke/tools-configuration-files. Certificate bundles published by the PKI can be found at https://crl.gds.disa.mil/.
~~~~~


<a id="wn11-pk-000015"></a>

## WN11-PK-000015 — The DoW Interoperability Root CA cross-certificates must be installed in the Untrusted Certificates Store on unclassified systems.

- Group: `V-253429`; rule revision: `SV-253429r1256662_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the DoW Interoperability cross-certificates are installed on unclassified systems as Untrusted Certificates.

Run "PowerShell" as an administrator.

Execute the following command:

Get-ChildItem -Path Cert:Localmachine\disallowed | Where {$_.Issuer -Like "*DoD Interoperability*" -and $_.Subject -Like "*DoD*"} | FL Subject, NotAfter

If valid DoW Interoperability cross-certificates (such as those below) are not displayed, this is a finding.

Subject: CN=DoD Interoperability Root CA 2, OU=PKI, OU=DoD, O=U.S. Government, C=US
NotAfter: 11/24/2030

Alternately, use the Certificates MMC snap-in:

Run "MMC".

Select "File", "Add/Remove Snap-in".

Select "Certificates", click "Add".

Select "Computer account", click "Next".

Select "Local computer: (the computer this console is running on)", click "Finish".

Click "OK".

Expand "Certificates" and navigate to Untrusted Certificates >> Certificates.

For each DoW Interoperability Root CA certificate displayed:

Right-click on the certificate and select "Open".

Select the "Details" tab.

Verify the Expiration Date is a future date.

Scroll to the bottom and select "Subject".

If any of the certificates listed do not include "DoD Interoperability Root CA" in the name or are expired, this is a finding.

Note: This should not be relied upon as a complete list of possible DoW Interoperability Root CA certificates.

DoD Interoperability Root CA 2

Note: Interoperability cross certificates will have a different value (such as "...Root CA 6") in the 'Issued To'  field than in the 'Subject' and 'Issuer' fields.
~~~~~

### Source fix text

~~~~~text
Install valid (unexpired) DoW Interoperability Root CA cross-certificates on unclassified systems.

The list below is not to be treated as exhaustive. The STIG should not be used as a definitive resource for the organizationally approved certificates for the systems.

DoD Interoperability Root CA 2

The certificates can be installed using the InstallRoot tool. The tool and user guide are available on Cyber Exchange at https://cyber.mil/pki-pke/tools-configuration-files. Certificate bundles published by the PKI can be found at https://crl.gds.disa.mil/.
~~~~~


<a id="wn11-pk-000020"></a>

## WN11-PK-000020 — The US DoW CCEB Interoperability Root CA cross-certificates must be installed in the Untrusted Certificates Store on unclassified systems.

- Group: `V-253430`; rule revision: `SV-253430r1268247_rule`; source severity: **medium**.

### Source check text

~~~~~text
Verify the US DoW CCEB Interoperability Root CA cross-certificate is installed on unclassified systems as an Untrusted Certificate.

Run "PowerShell" as an administrator.

Execute the following command:

Get-ChildItem -Path Cert:Localmachine\disallowed | Where Issuer -Like "*CCEB Interoperability*" | FL Subject, NotAfter

If valid US DoW CCEB Interoperability Root CA certificates (such as those below) are not displayed, this is a finding.

Note: The Common Names (CN) below are examples. Verify the "CN" displayed is a DoW CCEB Interoperability Root CA and is not expired.

Subject: CN= US DoD CCEB Interoperability Root CA 2, OU=PKI, OU=DoD, O=U.S. Government, C=US
NotAfter: 12/30/2030

Alternately, use the Certificates MMC snap-in:

Run "MMC".

Select "File", then click "Add/Remove Snap-in".

Select "Certificates", then click "Add".

Select "Computer account", then click "Next".

Select "Local computer: (the computer this console is running on)", then click "Finish".

Click "OK".

Expand "Certificates" and navigate to Untrusted Certificates >> Certificates.

For each US DoW CCEB Interoperability Root CA certificate displayed:

Right-click on the certificate and select "Open".

Select the "Details" tab.

Scroll to the bottom and select "Subject".

If any of the certificates listed do not include "DoD Interoperability Root CA" in the name or are expired, this is a finding.

US DoD CCEB Interoperability Root CA 2

Note: Interoperability cross certificates will have a different value (such as "...Root CA 6") in the 'Issued To'  field than in the 'Subject' and 'Issuer' fields.
~~~~~

### Source fix text

~~~~~text
Install the US DoW CCEB Interoperability Root CA cross-certificate on unclassified systems.

The list below is not to be treated as exhaustive. The STIG should not be used as a definitive resource for the organizationally approved certificates for the systems.

US DOD CCEB Interoperability Root CA 2

The certificates can be installed using the InstallRoot tool. The tool and user guide are available on Cyber Exchange at https://cyber.mil/pki-pke/tools-configuration-files. Certificate bundles published by the PKI can be found at https://crl.gds.disa.mil/.
~~~~~
