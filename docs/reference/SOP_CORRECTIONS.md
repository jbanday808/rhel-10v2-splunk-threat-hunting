# Repository-specific corrections to the original lab SOP

The original full guide is retained as an educational reference. Apply these corrections when publishing from WSL:

1. **Repository name:** the existing GitHub repository is `jbanday808/rhel-10v2-splunk-threat-hunting`; the older name `rhel-splunk-threat-hunting` is a local project folder name only.
2. **Upload process:** do not run `git init` or `gh repo create` for this existing repository. Clone it, stage and review the ZIP, and push to `main`.
3. **Existing MIT license:** preserve the `LICENSE` already in GitHub. The ZIP intentionally has no second copy.
4. **Azure OIDC:** the OIDC workflows and their GitHub repository guards must use the actual owner/name; any previously configured Azure federated credential using the old repository must be reviewed and updated before enabling Azure login.
5. **Secrets:** never publish real credentials, LDAP bind passwords, root CA private keys, HEC tokens, installers, backups, or unredacted event records. Rotate any real credentials copied from an earlier version of the lab SOP.
6. **Verification:** local syntax and unit tests are not evidence of live Splunk, LDAPS, Sysmon, or Azure success.
7. **Role separation:** WSL is for authoring and publishing; installation happens on the designated RHEL and Windows VMware guests.

The Markdown copies of the relevant numbered steps have been updated to reflect the existing GitHub repository. The original Word guide is retained as reference material; this errata applies where its older Git commands or repository names differ.
