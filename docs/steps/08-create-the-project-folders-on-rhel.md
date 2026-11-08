**Step 8 — Create the project folders on RHEL**

```
mkdir -p "$HOME/rhel-splunk-threat-hunting"

cd "$HOME/rhel-splunk-threat-hunting"

mkdir -p \
  apps/LAB_SIEM/local \
  apps/LAB_SIEM/metadata \
  apps/LAB_SIEM/default/data/ui/views \
  apps/LAB_UF_WINDOWS/local \
  configs/rsyslog \
  configs/logrotate \
  scripts/rhel \
  scripts/windows \
  sysmon \
  hunts \
  docs/reference \
  docs/images \
  evidence/sanitized \
  evidence/raw

mkdir -p "$HOME/siem-downloads"

touch README.md docs/reference/versions.md
```

**Command overview:**

- `mkdir -p` creates folders and missing parents.
- `cd` selects the working folder.
- `touch` creates empty files.

Create `.gitignore`:

```
cat > .gitignore <<'EOF'
downloads/
private/
backups/
evidence/raw/
.env
*.key
*.pem
*.pfx
*.p12
*.csr
*.srl
*.iso
*.vmdk
*.vmem
*.vmss
*.nvram
*.msi
*.exe
*.evtx
*.log
*.tgz
*.tar.gz
*.zip
__pycache__/
Thumbs.db
.DS_Store
EOF
```

Create `.gitattributes`:

```
cat > .gitattributes <<'EOF'
* text=auto
*.sh text eol=lf
*.conf text eol=lf
*.meta text eol=lf
*.xml text eol=lf
*.spl text eol=lf
*.md text eol=lf
*.ps1 text eol=crlf
EOF
```

**Command overview:**

- `cat > filename` creates or replaces a file.
- `<<'EOF'` preserves the enclosed text exactly.
- `.gitignore` excludes private and unnecessary files.
- `.gitattributes` keeps line endings consistent.

At the start of another RHEL terminal session, return to the project:

```
cd "$HOME/rhel-splunk-threat-hunting"
```

---
