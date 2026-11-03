#!/usr/bin/env python3
"""High-confidence preflight for files in a PUBLIC GitHub repo (not a full security audit)."""
from __future__ import annotations
import re
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
# Use Git's staged and untracked inventory, honoring the repository ignore rules.
cmd = ['git', '-C', str(root), 'ls-files', '--cached', '--others', '--exclude-standard', '-z']
res = subprocess.run(cmd, capture_output=True, check=False)
if res.returncode:
    print('Git repository required: run this check from the cloned checkout.', file=sys.stderr)
    raise SystemExit(2)
files = [Path(s.decode('utf-8', 'surrogateescape')) for s in res.stdout.split(b'\0') if s]
errors: list[str] = []
for rel in files:
    path = root / rel
    if not path.is_file():
        continue
    posix = rel.as_posix()
    forbidden_dirs = {'private', 'backups', 'downloads', 'secrets', 'local-private'}
    forbidden_suffixes = {'.key', '.pem', '.pfx', '.p12', '.keytab', '.iso', '.vmdk', '.evtx', '.pcap', '.pcapng', '.kdbx', '.zip', '.tgz'}
    if any(part in forbidden_dirs for part in rel.parts) or posix.startswith('evidence/raw/'):
        errors.append(f'Private directory included: {posix}')
    if path.suffix.lower() in forbidden_suffixes:
        errors.append(f'Forbidden file type included: {posix}')
    if path.suffix.lower() not in {'.md', '.txt', '.sh', '.ps1', '.json', '.conf', '.example', '.xml', '.py', '.yml', '.yaml', '.spl', '.meta'}:
        continue
    try:
        body=path.read_text(encoding='utf-8')
    except UnicodeError:
        continue
    if re.search(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', body):
        errors.append(f'Private key block included: {posix}')
    if re.search(r'(?i)github_pat_[a-zA-Z0-9_]{35,}|gh[pousr]_[a-zA-Z0-9]{36,}', body):
        errors.append(f'GitHub token-shaped value: {posix}')
    if re.search(r'(?im)^\s*(?:bindDNpassword|aws_secret_access_key)\s*[:=]\s*(?!REPLACE|EXAMPLE|DUMMY|PLACEHOLDER|<|\[)[^\s#]+',body):
        errors.append(f'Potential real credential assignment: {posix}')
if errors:
    print('Publication preflight found files to review:')
    for e in errors: print('FAIL:', e)
    raise SystemExit(1)
print(f'Publication preflight passed for {len(files)} Git-visible paths. Review screenshots and DOCX manually before publishing.')
