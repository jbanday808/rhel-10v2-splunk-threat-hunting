# Start here — ESS ePO 5.x STIG Version 3 Release 8

This optional workstream explains how to assess and harden an authorized Trellix ePolicy Orchestrator (ePO) server with the supplied DISA ESS ePO 5.x manual STIG. Start with the complete guide and keep the assessment checklist and evidence in an approved private environment.

- [Complete step-by-step implementation guide](docs/stig-epo/IMPLEMENTATION_GUIDE.md)
- [Official and supporting references](docs/stig-epo/REFERENCES.md)
- [Private rule workbook generator](scripts/stig-epo/build_private_workbook.py)
- [Sanitized validation worksheet](evidence/sanitized/epo-stig-validation.md)

## Decide where the work runs

| System | Purpose |
| --- | --- |
| CUI-approved Windows or Linux assessment workstation | Review the supplied benchmark, use STIG Viewer, and keep checklists and evidence private |
| Authorized ePO server and managed test endpoint | Review applicable ePO settings and validate approved changes |
| RHEL-SPLUNK01 | Optional review of approved, sanitized ePO audit telemetry using the existing lab index |
| WINHUNT01 and RHEL-IDM01 | Existing lab roles; use only when explicitly included in a separate test plan |

The supplied unclassified overview states that this STIG covers ePO server versions through 5.9x. If your installed product is 5.10 or another version outside that stated scope, obtain the applicable benchmark or an authorized applicability decision before assessing it under V3R8.

The supplied XCCDF contains CUI markings. The source file, generated workbook, completed checklists, screenshots and detailed findings belong only on systems approved for their handling. The public repository contains the workflow and software for producing a private rule-by-rule workbook from an authorized local copy.

The private workbook preserves the source check and fix text for every rule and starts each as Not Reviewed. The official checklist remains the assessment record. No ePO deployment, STIG assessment, remediation, or compliance result has been verified in this lab.
