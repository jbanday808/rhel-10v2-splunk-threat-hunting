# Complete step-by-step guide — ESS ePO 5.x STIG V3R8

Use this guide to prepare, assess, remediate, and revalidate an authorized Trellix ePolicy Orchestrator (ePO) environment. It covers the supplied DISA ESS ePO 5.x manual STIG, Version 3 Release 8, dated September 30, 2026. The actual rule checks, required values, and fixes remain in the controlled manual XCCDF file and the authorized STIG Viewer checklist.

The existing project uses RHEL-SPLUNK01, WINHUNT01, and RHEL-IDM01. An ePO server has not been documented as deployed. The steps below require a separately authorized ePO environment, an appropriately authorized assessment workstation, and the version-specific Trellix installation and license.

## Scope and important version decision

The supplied unclassified V3R8 overview states that the ePO server scope extends through version 5.9x. Identify the actual installed version and ask the system owner or security control assessor to confirm applicability. For ePO 5.10 or a different product generation, obtain the applicable current benchmark or a documented applicability decision before using this STIG as an assessment baseline. Trellix 5.10 public documentation cited below illustrates product functions and menu terminology. Confirm the equivalent screen in the version actually being assessed.

The supplied XML is a manual XCCDF and includes CUI markings. A checklist generated from it and detailed assessment results may also require controlled handling. Follow the source markings and the organization's CUI program. The public repository contains no controlled rule text, completed checklists, server exports, credentials, or assessment evidence.

## Phase 1 — Prepare the ePO environment

### Step 01 — Identify the goal and assessment owner

Record the system owner, assessor, ePO administrator, network and database contacts, approved maintenance window, and reporting channel in an approved private record. Define whether the work is an initial assessment, remediation, retest, or periodic review.

**Expected result:** Named owners and a documented assessment boundary.

### Step 02 — Record the installed product and update level

On the authorized ePO console, inspect its About or product-information screen and vendor-supported inventory. Record the full product version, build, update level, installed extensions, and evidence date. Obtain vendor support and product ownership confirmation if the version is unclear.

Compare the installed version to the scope in the supplied overview. Stop for the applicability decision when it falls outside the stated range.

### Step 03 — Separate the application from its dependencies

Inventory the ePO application server, Windows host, SQL Server instance, agent handlers, managed endpoints, identity service, and network boundaries. Record which components are local or remote and who owns each.

The ePO application STIG does not automatically assess the host operating system, database, endpoint products, network devices, or Splunk. Identify the applicable guidance and separate checklist for each component.

### Step 04 — Confirm the lab and licensing

Use an authorized isolated or otherwise approved test environment with a properly licensed and supported ePO installation. Check the vendor's version-specific OS, SQL, browser, and patch compatibility information. Use the vendor's installer and documentation when a new server is required.

WINHUNT01 is an existing Windows 11 endpoint in this project. Do not assume it is a supported ePO server host. Document any separate Windows Server and database requirements before building an optional ePO environment.

### Step 05 — Establish private handling locations

Use an assessment workstation, storage, and transfer method approved for the source's markings. Keep the XCCDF, viewer library, checklist, screenshots, reports, workbook, database exports, and private credentials in their approved locations.

Use a separate public Git checkout for documentation and source. Do not place controlled material in the checkout, public GitHub, unapproved cloud synchronization, or Splunk inputs.

### Step 06 — Confirm recovery

Before changes, review the vendor's disaster-recovery process for the exact ePO build. Protect a consistent SQL backup and the ePO disaster-recovery snapshot, required security keys, recovery passphrase, and configuration dependencies. Verify who can restore them and perform an authorized recovery test.

A VM snapshot can supplement an approved recovery plan. Validate application and database consistency rather than relying on an untested snapshot alone.

### Step 07 — Record service and policy health

Document the pre-change state of the ePO console, application services, database connectivity, agent communication, update repositories, recent tasks, and sample endpoint policy status. Record known failures separately.

**Expected result:** A baseline that allows you to distinguish existing problems from changes made during the assessment.

### Step 08 — Plan the change window and communications

Choose a small test group and at least one recoverable, authorized test endpoint. Agree on the change order, approval owner, monitoring contact, stop conditions, and rollback decision. Preserve an approved emergency access method.

Changes to account access, certificates, repository settings, server tasks, and policies can affect management or endpoint protection. Test each approved change within the planned scope.

## Phase 2 — Open the controlled STIG and build the checklist

### Step 09 — Verify the supplied package

On the approved assessment workstation, confirm the XML came from an authorized source and that the overview identifies ESS ePO 5.x, Version 3 Release 8, dated September 30, 2026. Compare a local file hash with the value obtained through your organization's trusted source. A hash by itself proves byte equality, not the publisher's identity.

Example on an approved Windows workstation after replacing the placeholder directory:

~~~powershell
$EpoPrivateFolder = 'C:\REPLACE_WITH_APPROVED_PRIVATE_FOLDER'
$EpoStigFile = Join-Path $EpoPrivateFolder 'CUI_ESS_ePO_5-x_STIG_V3R8_Manual-xccdf.xml'
Test-Path -LiteralPath $EpoStigFile -PathType Leaf
Get-FileHash -LiteralPath $EpoStigFile -Algorithm SHA256 |
    Select-Object Algorithm, Hash
~~~

**Command overview:** The variables identify the authorized private folder and XML file. Test-Path checks that the file exists. Get-FileHash calculates a SHA-256 fingerprint. Record and compare the value only in the approved assessment record.

**Expected result:** Test-Path returns True and the fingerprint matches the trusted copy.

### Step 10 — Install or open the approved STIG Viewer

Obtain STIG Viewer through the authorized DISA Cyber Exchange channel, verify the package according to local software policy, and install or launch it on the approved workstation. Confirm the workstation's application data, temporary files, and autosave locations are approved for the STIG's markings.

Viewer menu wording can vary by version. The following sequence is documented for STIG Viewer 3.x.

### Step 11 — Load the manual benchmark

1. Open STIG Viewer and choose STIG Explorer or the magnifying-glass icon.
2. Select Add STIG to Library.
3. Browse to the private manual XCCDF XML and select Load.
4. Confirm the displayed STIG title, Version 3, Release 8, and benchmark date.
5. Open the STIG and confirm the rule list is present.

The XML is a manual checklist source. Loading it into Viewer does not scan the ePO server or establish compliance. The supplied XSL stylesheet and logo support browser presentation and are not required for the Viewer import.

### Step 12 — Create and save the checklist

1. Open Checklists from the home page.
2. Select Create Checklist, enter an approved private checklist name, and create it.
3. Select the plus sign beside the ePO STIG to include its full rule set.
4. Select Fill Checklist and enter only approved target information.
5. Save the resulting Viewer checklist in the approved private location.

Choose and apply the appropriate classification and CUI markings for target data, comments, and finding details under local policy. Protect Viewer autosaves and exports as well as the saved checklist.

### Step 13 — Understand assessment statuses

| Status | Use |
| --- | --- |
| Not Reviewed | The assessor has not completed the check or lacks sufficient evidence |
| Open | Applicable evidence shows the required condition is not met |
| Not a Finding | Applicable evidence supports the required condition |
| Not Applicable | The rule does not apply, with documented justification accepted by the assessment authority |

Do not mark an unknown condition as Not a Finding or Not Applicable. Record the evidence and reviewer for each decision.

### Step 14 — Review each source rule

For each rule in Viewer, record its ID, revision, severity, applicability, check instructions, expected condition, observed evidence, status, and assessor. Read the check and fix text in the supplied benchmark. Use its exact thresholds, exceptions, and instructions for the in-scope version.

Classify CAT I, II, and III findings according to the source and local risk process. Prioritize urgent findings with the system owner while considering operational impact.

### Step 15 — Optionally create a private rule-by-rule workbook

The repository includes a helper that reads the local V3R8 XML and writes a private text workbook containing each rule's source check and fix text. It performs no ePO connection or configuration changes. Use the helper only on a workstation and in storage approved for the source markings.

1. Place an approved copy of the public repository outside the controlled source folder.
2. Place the XML in an existing approved private folder outside every Git working tree.
3. In PowerShell, replace both example paths with the actual approved paths.

~~~powershell
Set-Location -LiteralPath 'C:\REPLACE_WITH_APPROVED_REPOSITORY'
$EpoPrivateFolder = 'C:\REPLACE_WITH_APPROVED_PRIVATE_FOLDER'
$EpoStigFile = Join-Path $EpoPrivateFolder 'CUI_ESS_ePO_5-x_STIG_V3R8_Manual-xccdf.xml'
$EpoWorkbook = Join-Path $EpoPrivateFolder 'epo-v3r8-private-workbook.txt'
py -3 --version
py -3 scripts\stig-epo\build_private_workbook.py --source $EpoStigFile --output $EpoWorkbook
if ($LASTEXITCODE -ne 0) { throw 'Workbook generation failed. Review the message before continuing.' }
~~~

**Command overview:** Set-Location opens the reviewed repository checkout. The variables point to the private input and a new output file. The Python command reads the manual XCCDF and writes one section per rule. The final command stops on an error.

**Expected result:** A new private workbook and a rule count are reported. The workbook contains the source check and fix text and initializes each entry as Not Reviewed. Confirm its count against Viewer. It is a working aid, not a completed assessment.

The output folder must already exist. Source and output must be outside Git working trees. An existing output file is never replaced. On Windows, the directory and file must have organization-approved access controls. On POSIX systems, the helper creates a new file with owner-only permissions, subject to the filesystem and organizational policy.

### Step 16 — Protect the workbook and checklist

Apply the source's required markings and handling instructions to the generated workbook and Viewer checklist. Restrict access and follow the approved retention and disposal process. Keep both out of public repositories, screenshots, issue comments, and unapproved transfer tools.

## Phase 3 — Review the ePO environment

Steps 17–27 organize the review by operational area. They support the rule-by-rule checklist in Step 14. Use the actual source check and fix text to decide which observations are required and whether a condition is a finding.

### Step 17 — Review server inventory and extensions

Verify the ePO server identity, version and update level, installed extensions, connected agent handlers, and managed test endpoint. Compare each item with the approved inventory and vendor support matrix. Record any unknown component for the owner.

### Step 18 — Review administrative accounts

In the version-specific ePO console, open the user-management area. Trellix's current on-premises guide documents Menu → User Management → Users. Review enabled, disabled, shared, service, and emergency accounts against the approved access list.

For an applicable source rule, compare its check criteria to observed account configuration. Record only the minimum necessary evidence. Do not remove or disable an account before the owner confirms its purpose and recovery access.

### Step 19 — Review permission sets and least privilege

Open the permission-set area, documented in current Trellix guidance as Menu → User Management → Permission Sets. Compare each test administrator's permissions and group assignments with approved duties.

Plan a controlled positive test for an allowed action and a negative test for a denied action. Capture the result and the associated audit entry in the private record.

### Step 20 — Review authentication and identity integration

Inspect the supported authentication method, directory integration, account lifecycle, session handling, and recovery procedure against applicable source checks and the organization's policy. Verify the identity source and owner before changing sign-in settings.

The supplied unclassified V3R8 revision history notes a password-age change to 180 days for one control. Review the rule's exact scope and check text in the controlled source, as well as the applicable identity policy, before deciding whether that value applies to a particular account.

### Step 21 — Review communication paths and certificates

Inventory administrative access, agent-to-server communication, database connections, approved network paths, and certificates. Confirm names, trust chains, expiration dates, and access restrictions with the owners.

Use the applicable rule and version-specific vendor documentation to determine exact settings. Validate certificates and connectivity after any approved change.

### Step 22 — Review the system tree and agent health

In current Trellix on-premises documentation, Menu → Systems → System Tree lists managed systems. Verify the approved pilot endpoint, group membership, agent communication time, and effective policy using the installed version's screens.

Record the existing agent and policy state before changing assignments.

### Step 23 — Review policies and assignment scope

Open the Policy Catalog and identify the existing policy, owner, inheritance, assigned systems, and change history. Compare applicable settings with the controlled rule text.

When a policy change is approved, use a reviewed copy or other vendor-supported change method and a limited test group. Preserve the prior assignment and rollback information.

### Step 24 — Review repositories, content, and tasks

Inventory configured update sources, content versions, update schedules, server tasks, and relevant access controls. Compare them with approved sources and the source checklist. Capture the latest successful and failed task information privately.

Avoid changing the master repository or enterprise-wide schedules as an unreviewed first step.

### Step 25 — Review audit events and reporting

Find the ePO audit log in the installed version's console. Current Trellix documentation identifies Menu → Reporting → Audit Log. Verify whether the events required by the applicable rules are present, protected, retained, and reviewed.

Record a known benign administrative test action and its audit entry only after authorization. Check timestamps, actor, action, and outcome.

### Step 26 — Review optional Splunk integration

For approved lab telemetry, first identify the supported ePO log export or integration method, event format, field mapping, transport, access controls, and retention. The existing Splunk lab index is named lab. Confirm the actual Splunk version and effective input configuration before making a change.

CUI benchmark content and assessment evidence must stay in approved systems. Configure collection only after the owner approves the actual data classification and destination.

To practice the search workflow without an ePO connection, use this synthetic Splunk search:

~~~spl
| makeresults
| eval source_system="synthetic:epo", action="policy_change", result="success", actor="training-user", target="test-policy"
| table _time source_system action result actor target
~~~

**Command overview:** makeresults creates one temporary search result. eval adds fictional training fields. table displays them. The result is generated by the search and does not verify ePO logging or ingestion.

### Step 27 — Review dependent host and database controls separately

Coordinate Windows Server, SQL Server, identity, network, endpoint-product, and Splunk configuration reviews with the responsible owners. Use their applicable benchmarks and vendor support guidance. Track dependencies separately from the ePO application checklist.

## Phase 4 — Remediate and validate

### Step 28 — Review open findings with the owner

For each applicable open rule, document the affected component, observed condition, source rule revision, impact, available fix, owner, and approved maintenance window. Rank work using source severity and mission impact.

### Step 29 — Prepare one change record

For each proposed change, capture the exact prior state, approved target value from the controlled rule, test plan, expected operational effect, rollback action, and verification method. Protect the change record according to its content.

Do not invent default values or copy a setting from another ePO version. If the check or fix is unclear, ask the designated STIG authority or vendor support.

### Step 30 — Test a narrowly scoped change

Apply one approved change to the authorized test environment or pilot policy. Use the exact fix and exceptions in the controlled source. If changing a policy, confirm the intended test group and assignment before saving.

### Step 31 — Verify the change on the server and endpoint

Recheck the ePO setting using the original source check. Confirm the ePO console, database connection, policy assignment, agent communication, and relevant product function remain healthy. Compare the results to the baseline from Step 07.

For a separately approved test endpoint, a manual agent wake-up call can be used when needed. In current Trellix documentation, select the single endpoint in Menu → Systems → System Tree, choose Actions → Agent → Wake Up Agents, verify the Target Systems list, and confirm the action. Review Menu → Automation → Server Task Log and the endpoint's effective policy. Menu wording varies by product version.

### Step 32 — Recheck allowed and denied actions

For access-control changes, use authorized test accounts to confirm the intended action is permitted and an unauthorized action is denied. Review the audit trail and retain private evidence. Stop and restore access through the approved recovery procedure if an administrative lockout occurs.

### Step 33 — Update the checklist from observed evidence

Return to the same rule revision in Viewer, repeat the complete check, and record the observed condition, date, reviewer, and private evidence location. Update the status only when supported by the evidence. Save the checklist.

### Step 34 — Document exceptions and remediation work

For a finding that cannot be corrected immediately, document the risk, affected component, owner, proposed corrective action, milestone, and approval in the organization's authorized process. Handle any plan of action and milestones according to the applicable assessment authority's rules.

### Step 35 — Complete all applicable rules

Repeat Steps 14 and 28–34 for the entire approved checklist. Reconcile the total rule count and status counts with Viewer. Investigate any Not Reviewed entries or missing evidence. Validate each Not Applicable decision independently.

## Phase 5 — Report, sustain, and hand off

### Step 36 — Prepare the assessment report

In the approved private reporting system, summarize the scope, product and benchmark versions, assessment dates, status totals, open findings, accepted exceptions, remediation owners, retest results, limitations, and evidence locations. Have the assessor and system owner review it.

A completed checklist, assessment report, and authorization decision are separate records governed by the responsible organization.

### Step 37 — Review existing lab services

If an approved ePO/Splunk integration was implemented, verify the existing Windows and Linux event sources, Splunk searches, storage, TLS, and directory services according to their own runbooks. Compare with the original health baseline. Investigate any regression through the appropriate owner.

### Step 38 — Publish only a sanitized progress summary

Use the [sanitized validation worksheet](../../evidence/sanitized/epo-stig-validation.md) for public project progress. Leave statuses Pending until observed and approved for publication. Remove controlled source text, actual system details, screenshots, checklists, credentials, and private findings from any public update.

### Step 39 — Maintain the assessment

Monitor authorized DISA releases and vendor advisories, compare new benchmark revisions in STIG Viewer, review changed rules, retest affected settings, and refresh the private checklist. Record changes in version scope, responsible owners, evidence, and approved exceptions.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| STIG does not appear in Viewer | Confirm the correct XML, approved Viewer version, library import, and Version 3 Release 8 |
| Workbook generation fails | Check Python version, source title/release, XML integrity, private output directory, existing output, and whether either path is inside a Git working tree |
| Product is ePO 5.10 | Obtain the applicable benchmark or an authorized applicability decision before using V3R8 |
| Console or agent stops working after a change | Stop the change, follow the reviewed rollback, and compare services and policies with the baseline |
| A rule cannot be evaluated | Keep it Not Reviewed, record the missing evidence, and request assessor or vendor guidance |
| No Splunk events appear | Verify that a source and approved transport were actually configured, then inspect source health and field mapping |

## References

See [official and supporting references](REFERENCES.md) for DISA STIG Viewer, the ePO overview and revision history supplied with the benchmark, and version-specific Trellix documentation.
