# Step 52 — Publish the complete project to your existing GitHub repository

**Repository:** https://github.com/jbanday808/rhel-10v2-splunk-threat-hunting

**Location:** VS Code integrated WSL terminal, at the root of the **cloned** repository.

Follow [the full upload walkthrough](../WSL_VSCODE_GITHUB_UPLOAD_GUIDE.md) to copy the updated ZIP into a clean clone without overwriting `.git` or `LICENSE`. The default branch is `main`.

```bash
git status --short
python3 scripts/validate_project.py
python3 scripts/validate_project.py --verify-manifest
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
python3 tools/publication_preflight.py

git add -A
git diff --cached --check
git diff --cached --stat
git diff --cached
```

**Command overview:** `git status` shows changes; the Python commands validate source files, hashes, and unit tests; `git diff --cached` shows everything that would be published. Inspect every new screenshot and document for private information before committing.

After review:

```bash
git commit -m 'Complete RHEL 10.2 Splunk threat hunting lab documentation'
git push -u origin main
gh repo view jbanday808/rhel-10v2-splunk-threat-hunting --web
```

**Summary:** These commands publish the reviewed contents to your existing GitHub repository while preserving its current history and MIT license.

**Safety:** `.gitignore` does not erase secrets that were already committed. Keep installers, VM images, credentials, private certificate material, backups, and raw logs outside the repository. Actual Splunk, LDAP, and Azure validation remains pending until independently tested.
