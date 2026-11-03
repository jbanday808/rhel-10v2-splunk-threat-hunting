**Step 44 — Record LDAP validation and screenshots**

On **RHEL-SPLUNK01**, add a separate validation record to the project:

```bash
cd "$HOME/rhel-splunk-threat-hunting"
cat > evidence/sanitized/ldap-validation.md <<'EOF'
# LDAP integration validation

Record observations and UTC timestamps. Replace Pending only after testing.

| Check | Actual result | Observed at (UTC) |
| --- | --- | --- |
| Exact RHEL and IdM builds recorded | Pending | Pending |
| Authentication-capable Splunk license confirmed | Pending | Pending |
| Directory DNS resolves to 172.25.250.30 | Pending | Pending |
| Directory CA fingerprint verified | Pending | Pending |
| LDAPS chain and hostname verification succeed | Pending | Pending |
| Lookup account reads intended users and both groups | Pending | Pending |
| Splunk LDAP client requires certificate verification | Pending | Pending |
| Hunter signs in with lab_hunter only | Pending | Pending |
| Hunter can search populated lab indexes | Pending | Pending |
| Hunter cannot retrieve protected _internal records | Pending | Pending |
| Hunter cannot change authentication or users | Pending | Pending |
| Directory Splunk administrator signs in | Pending | Pending |
| Unmapped user and incorrect password are denied | Pending | Pending |
| Removing hunter membership blocks a new login after refresh | Pending | Pending |
| Hunter membership restored and retested | Pending | Pending |
| Unmapped test account disabled | Pending | Pending |
| Local Splunk admin remains usable | Pending | Pending |
| Login audit activity reviewed | Pending | Pending |
| Splunk configuration and separate IdM backup completed | Pending | Pending |
| Recovery validated in an isolated copy | Pending | Pending |
EOF

cat >> .gitignore <<'EOF'

# LDAP secrets and live runtime settings
authentication.conf
splunk.secret
*.keytab
ldap-private/
EOF
```

If a sensitive file was already tracked, `.gitignore` alone does not remove it from Git history. Review staged content before committing; keep only the `.example` files and sanitized evidence.

Suggested screenshot filenames:

| Screenshot | Filename |
| --- | --- |
| Directory VM network | `LDAP_01_IdM_Network.png` |
| Directory application groups | `LDAP_02_Splunk_Groups.png` |
| Verified LDAPS connection | `LDAP_03_TLS_Validation.png` |
| Splunk LDAP strategy without password fields | `LDAP_04_Splunk_Strategy.png` |
| Directory groups mapped to Splunk roles | `LDAP_05_Role_Mapping.png` |
| Hunter's permitted searches | `LDAP_06_Hunter_Search.png` |
| Recent authentication activity | `LDAP_07_Login_Audit.png` |

**Command overview:** `cat >` creates the validation record; `cat >>` adds ignore rules; quoted `EOF` markers preserve the file text.

**Summary:** The project includes reusable examples and a validation checklist without claiming unperformed tests have passed.

---
