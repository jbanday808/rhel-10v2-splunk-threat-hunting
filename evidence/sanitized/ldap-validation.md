# LDAP integration validation

The lab owner reported on **2026-11-09** that the Step 44 checks were completed. That report is not a UTC timestamp for each test. The rows below distinguish outcomes visible in owner-supplied terminal or Splunk output from checks whose detailed result has not been entered in this public record. The repository has not independently tested the VMs or inspected the newer local screenshots. See [Step 44](../../docs/steps/44-record-ldap-validation-and-screenshots.md) for the screenshot inventory and review process.

For each row, add the observed outcome, the sanitized evidence reference, and the actual test or review time in UTC after checking the source. `UTC not recorded` must not be replaced with a guessed time or a file sync timestamp. Do not publish bind passwords, private certificates, backup archives, or raw authentication logs.

| Check | Current result | Evidence / next record | Observed at (UTC) |
| --- | --- | --- | --- |
| Exact RHEL and IdM builds recorded | Owner reports check completed | Record sanitized version output for both VMs. | UTC not recorded |
| Authentication-capable Splunk license confirmed | Owner reports check completed | Review the local license screenshot and record its actual state. | UTC not recorded |
| Directory DNS resolves to `172.25.250.30` | Observed in owner-supplied TLS command output | `idm01.lab.test` resolved to `172.25.250.30` during the connection test. | UTC not recorded |
| Directory CA fingerprint verified | Owner reports check completed | Record the compared fingerprints without publishing private key material. | UTC not recorded |
| LDAPS chain and hostname verification succeed | Observed in owner-supplied TLS command output | TLSv1.3; `Verification: OK`; verified peer name `idm01.lab.test`. | UTC not recorded |
| Lookup account reads intended users and both groups | Owner reports check completed | A shared `ldapwhoami` result confirms the bind only; add sanitized user and group lookup outcomes. | UTC not recorded |
| Splunk LDAP client requires certificate verification | Owner reports check completed | Record the effective Splunk LDAP strategy setting separately from the OpenSSL test. | UTC not recorded |
| Hunter signs in with `lab_hunter` only | Owner reports check completed | Review the hunter login and effective-role evidence; the local screenshot filename alone does not establish the role. | UTC not recorded |
| Hunter can search populated lab indexes | Owner reports check completed | Record a hunter-session search and the index counts, with sensitive event fields removed. | UTC not recorded |
| Hunter cannot retrieve protected `_internal` records | Owner reports check completed | Record the restricted hunter search and a separate positive administrator control. | UTC not recorded |
| Hunter cannot change authentication or users | Owner reports check completed | Record the denied administration attempt without credentials. | UTC not recorded |
| Directory Splunk administrator signs in | Owner reports check completed | Record the mapped admin role and successful login. | UTC not recorded |
| Unmapped user and incorrect password are denied | Owner reports check completed | Record both negative login outcomes; disabling the unmapped user is a separate check. | UTC not recorded |
| Removing hunter membership blocks a new login after refresh | Owner reports check completed | Record group removal, authentication refresh, and denial of a new session. | UTC not recorded |
| Hunter membership restored and retested | Owner reports check completed | Record restored group membership and a new successful login. | UTC not recorded |
| Unmapped test account disabled | Owner reports check completed | Review the local IdM account screenshot or a sanitized `ipa user-show` result. | UTC not recorded |
| Local Splunk admin remains usable | Owner reports check completed | Record a local account login after the LDAP tests. | UTC not recorded |
| Login audit activity reviewed | Owner reports check completed | Review the local audit screenshot and record actual `login attempt` outcomes, including an empty result if that is what it shows. | UTC not recorded |
| Splunk configuration backup completed | Owner reports check completed | Record the private backup location and successful command outcome in private notes; publish only a sanitized summary. | UTC not recorded |
| IdM full backup created and services returned | Observed in owner-supplied terminal output | `ipa-backup` reported success; `ipactl status` reported the configured services running. | UTC not recorded |
| IdM backup contains `header` and a nonempty archive | Owner reports check completed | Review the exact-path Step 43 check; a screenshot filename alone does not confirm file contents. | UTC not recorded |
| Recovery validated in an isolated copy | Owner reports check completed | Record the isolated restore procedure, outcome, and recovery time without publishing backup data. | UTC not recorded |

The status `Owner reports check completed` records the owner's statement; it is not an independently verified pass. Replace it with a precise observed result after reviewing the corresponding evidence. Keep troubleshooting screenshots, such as role-mapping errors, alongside their later resolution rather than presenting the error as a successful check.
