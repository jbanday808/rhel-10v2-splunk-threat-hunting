**Step 39 — Map the directory groups to Splunk roles**

On the LDAP strategies page, choose **Map groups** beside `LAB_IDM_LDAPS`. Apply these mappings and save each one:

| Directory group | Splunk role | Intended access |
| --- | --- | --- |
| `splunk-hunters` | `lab_hunter` only | Search the six lab indexes and view the lab dashboard |
| `splunk-admins` | `admin` only | Administer this lab's Splunk instance |

Do not map the broad IdM `ipausers` group to a Splunk role. Keep `unmapped01` outside both mapped groups. Keep `hunter01` outside `splunk-admins`.

Confirm **Settings → Roles → lab_hunter** contains only the six lab indexes from Step 30 and has no inherited role granting wider access. Confirm the Threat Hunting Lab app and dashboard permit `lab_hunter` to read them. A user in both mapped groups receives the combined permissions, including administrator access.

**Summary:** Directory membership determines who can hunt and who can administer Splunk.

References:

- [Splunk LDAP Group Mapping Guide](https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.6/use-ldap-as-an-authentication-scheme/map-ldap-groups-to-splunk-roles-in-splunk-web): This guide explains assigning Splunk roles to directory groups.

---
