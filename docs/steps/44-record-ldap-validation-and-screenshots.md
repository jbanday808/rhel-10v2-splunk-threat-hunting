**Step 44 — Record LDAP validation and screenshots**

The repository already contains [`evidence/sanitized/ldap-validation.md`](../../evidence/sanitized/ldap-validation.md) and LDAP protection rules in `.gitignore`. Edit the existing record; do not run the earlier `cat >` command, which would overwrite it, or append duplicate ignore rules.

### 1. Record what was tested

On **RHEL-SPLUNK01** or in your repository checkout in WSL:

```bash
cd "$HOME/rhel-splunk-threat-hunting"
ls -l evidence/sanitized/ldap-validation.md
date -u '+%Y-%m-%dT%H:%M:%SZ'
```

Open the existing validation file in your editor. The lab owner reports completing the checks. Record the actual outcome, the evidence you reviewed, and the UTC time for **each** check. The `date` command gives the current UTC time for a new review; it does not establish when an earlier test ran. If a historical time is unavailable, write `UTC not recorded` instead of inventing one.

Some observations have already been shared: the `openssl s_client` output showed certificate verification and a matching `idm01.lab.test` peer name; `ldapwhoami` showed that the bind account could authenticate; Splunk Web showed the LDAP strategy enabled; and `ipa-backup` reported success followed by running IdM services. A successful bind alone does not show that the account can read both intended groups. The filename of a screenshot does not establish its outcome. Review the relevant results before marking the remaining checks verified.

The [validation record](../../evidence/sanitized/ldap-validation.md) now distinguishes these supplied observations from checks reported complete by the owner whose detailed evidence and UTC time have not yet been recorded. Keep error and recovery results distinct: a screenshot titled `Role_Mapping_Errors` documents troubleshooting, while a successful backup does not prove an isolated restore was tested.

### 2. Match screenshots to the checks

Replace the seven earlier `LDAP_01`–`LDAP_07` suggested names with the filenames in the owner's current listing. These are filenames, not proof that each image shows the required result:

| Evidence requested | Current filename to review |
| --- | --- |
| Directory VM network | `03_RHEL_IDM01_VM_Overview.png` — check whether the network details are actually visible. |
| Directory application groups | `30_Splunk_LDAP_Groups.png` — check whether it shows IdM group membership or only Splunk mapping; capture the IdM view if needed. |
| Verified LDAPS connection | `40_Splunk_to_IdM_LDAPS_Connection_Verification.png` |
| Splunk LDAP strategy without password fields | `28_Splunk_LDAP_Authentication_Selected.png`, `29_Splunk_LDAP_Strategy_Enabled.png` |
| Directory groups mapped to Splunk roles | `30_Splunk_LDAP_Groups.png`, `31_Splunk_Lab_Hunter_Role_Inheritance.png` |
| Hunter's permitted searches | `33_Splunk_Linux_Index_Event_Count.png` — confirm the search ran in the hunter session. |
| Recent authentication activity | `38_Splunk_Login_Audit_Results.png` — record what the result actually shows. |

The same local listing includes supporting LDAP and recovery images:

| Area | Current filename |
| --- | --- |
| Hunter authentication | `32_Hunter01_LDAPS_Authentication_Verification.png` |
| Hunter membership removed | `34_Hunter01_Removed_From_Splunk_Hunters_Group.png` |
| Hunter membership restored | `35_Hunter01_Added_To_Splunk_Hunters_Group.png` |
| Unmapped account disabled | `36_Unmapped01_User_Account_Disabled.png` |
| Role mapping troubleshooting | `37_Splunk_LDAP_Role_Mapping_Errors.png` |
| IdM services and LDAPS listener | `39_IdM_Services_and_LDAPS_Port_Status.png` |
| IdM backup and service restart | `41_IdM_Backup_and_Service_Status.png` |
| IdM backup archive check | `42_IdM_Backup_Archive_and_Directory_Check.png` |

At this revision, GitHub tracks screenshots `01`–`22`; the directory-listing image does not upload the newer image files. The local list also has two filenames beginning with `28`: one for the lab pipeline and one for LDAP. Use the **full filename** when matching evidence, and review any renaming before updating links.

Inspect each image for passwords, bind credentials, private paths, tokens, and identifying data. After sanitizing and reviewing an image, copy that image into `screenshots/`, update `screenshots/README.md`, and link it from the matching validation row. Keep raw screenshots and the IdM backup private. Do not label an error screenshot as a successful validation without the later resolution evidence.

### 3. Review the repository changes

From the repository root, check which evidence files are actually tracked or changed:

```bash
git ls-files screenshots/
git status --short evidence/sanitized/ldap-validation.md screenshots/
```

Review the final diff before publishing. `.gitignore` already protects live `authentication.conf`, `splunk.secret`, `*.keytab`, and `ldap-private/`; do not append those rules again. An ignore rule does not remove a sensitive file that was previously committed.

**Command overview:** `cd` enters the repository; `ls` confirms the checklist exists; `date -u` prints the current UTC time; `git ls-files` shows committed screenshots; `git status --short` shows changed evidence files.

**Summary:** Record the reported work with the observed result, supporting evidence, and an honest UTC timestamp. Publish only screenshots whose contents have been reviewed and sanitized.

---
