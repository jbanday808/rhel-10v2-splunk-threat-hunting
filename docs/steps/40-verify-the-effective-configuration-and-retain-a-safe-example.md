**Step 40 — Verify Splunk and review the safe LDAP examples**

Run these checks on **RHEL-SPLUNK01**. Step 38 created the `LAB_IDM_LDAPS` strategy in Splunk Web. The example files below document its intended settings; they do not change the live strategy.

### 40.1 — Check Splunk's configuration and service

Run each command separately:

```bash
sudo -u splunk /opt/splunk/bin/splunk btool check && echo 'btool check completed'
sudo systemctl is-active Splunkd
sudo journalctl -u Splunkd -n 30 --no-pager
```

**Expected:** Review any `btool` warnings; the completion message appears only if the command exits successfully. `systemctl is-active` returns `active`. The journal should show Splunk starting without a service failure. If you changed a **live** Splunk configuration file since its last restart, restart once and check again:

```bash
sudo systemctl restart Splunkd
sudo systemctl is-active Splunkd
```

**Observed in the supplied lab output:** `btool check` showed no problem text, `systemctl is-active` returned `active`, and the journal showed Splunk stopping and starting successfully. Those lines do not indicate a Splunk startup error. The later `No such file or directory` messages came from trying to write documentation files into a missing local folder.

**Command overview:** `btool check` checks Splunk configuration syntax; `systemctl is-active` checks the service; `journalctl` shows recent service messages. Restart Splunk only after a relevant live configuration change.

### 40.2 — Check the local repository before editing documentation

The **current GitHub repository already contains** both sanitized examples under `docs/reference/`. The earlier `cat > docs/reference/...` commands failed because that folder was absent from the local checkout. A shell redirection cannot create a missing parent folder. Do not rerun those commands or overwrite the tracked examples.

In the local project directory, run each command separately:

```bash
cd "$HOME/rhel-splunk-threat-hunting"
git rev-parse --show-toplevel
git remote get-url origin
git branch --show-current
git status --short
test -d docs/reference && echo 'docs/reference exists' || echo 'docs/reference is missing'
```

**Expected:** The directory is the intended project checkout, `origin` is `jbanday808/rhel-10v2-splunk-threat-hunting`, the branch is `main`, and `git status --short` prints nothing before an update. A different remote, branch, or local changes require review before syncing; do not discard work.

If those conditions hold and `docs/reference` is missing, bring this **clean `main` checkout** up to date:

```bash
git pull --ff-only origin main
ls -l docs/reference/ldap-authentication.conf.example \
  docs/reference/ldap-client.conf.example
```

**Expected:** Both files are listed. If the fast-forward pull fails or the files remain missing, stop and check the remote and checkout rather than creating a second copy or overwriting local work.

**Command overview:** `git rev-parse` identifies the checkout; `git remote get-url` identifies its source; `git status` exposes local changes; `test -d` checks the folder; `git pull --ff-only` updates a clean `main` without creating a merge commit; `ls` confirms the two tracked examples are present.

### 40.3 — Review the existing sanitized examples

- [LDAP authentication example](../reference/ldap-authentication.conf.example): Shows `LAB_IDM_LDAPS`, LDAPS on port `636`, certificate verification and CA path, search bases, group filter, and role mappings. The bind password is a **placeholder**.
- [Splunk LDAP client example](../reference/ldap-client.conf.example): Shows `TLS_REQCERT demand` and the public IdM CA path.

These are **documentation examples**, not instructions to replace live `/opt/splunk/etc/system/local/authentication.conf` or `/opt/splunk/etc/openldap/ldap.conf`. Step 38 entered the real bind password through Splunk Web. Keep live credentials, encrypted password values, `splunk.secret`, and unredacted `btool authentication list --debug` output outside GitHub.

Confirm in Splunk Web that `LAB_IDM_LDAPS` is **Enabled**. Step 39 separately maps `splunk-hunters` to `lab_hunter` and `splunk-admins` to `admin`; a successful strategy save or service restart does not prove that an LDAP user can sign in with the intended role.

**Summary:** The supplied output confirms Splunk is running. Update the correct local checkout to obtain the already tracked examples; the missing `docs/reference` folder is a local repository layout issue, not a Splunk service failure.

---
