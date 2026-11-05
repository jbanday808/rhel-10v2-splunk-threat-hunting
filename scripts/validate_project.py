#!/usr/bin/env python3
"""Check the portable source package without connecting to lab services."""
from __future__ import annotations

import argparse
import ast
import configparser
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

REQUIRED = (
    'README.md', 'START_HERE_WINDOWS.md', '.gitignore', '.gitattributes',
    'apps/LAB_SIEM/local/indexes.conf',
    'apps/LAB_SIEM/local/inputs.conf',
    'apps/LAB_SIEM/local/props.conf',
    'apps/LAB_SIEM/local/transforms.conf',
    'apps/LAB_SIEM/local/authorize.conf',
    'apps/LAB_SIEM/default/data/ui/views/overview.xml',
    'apps/LAB_UF_WINDOWS/local/inputs.conf',
    'apps/LAB_UF_WINDOWS/local/outputs.conf',
    'apps/Splunk_TA_nginx/local/inputs.conf',
    'configs/nginx/nginx.conf', 'sysmon/sysmon.xml',
    'docs/ldap-authentication.conf.example',
    'docs/ldap-client.conf.example',
    'scripts/windows/Test-Project.ps1',
    '.github/workflows/validate-project.yml',
    '.github/workflows/oidc-claims.yml',
    '.github/workflows/azure-oidc.yml',
    'configs/redaction/inputs.conf.example', 'configs/redaction/props.conf.example',
    'scripts/merge_redaction_config.py', 'scripts/rhel/install-redaction-lab.sh',
    'scripts/rhel/generate-redaction-marker.sh', 'tests/test_redaction.py',
    'examples/redaction/cases.json', 'hunts/11-password-redaction-check.spl',
    'configs/hec/inputs.conf.example', 'scripts/rhel/send-hec-event.sh',
    'examples/hec/event.json', 'hunts/12-hec-ingestion-check.spl',
    'tests/test_hec_sender.py',
)


def parse_conf(path: Path) -> configparser.RawConfigParser:
    parser = configparser.RawConfigParser(strict=True, interpolation=None)
    parser.optionxform = str
    parser.read_string(path.read_text(encoding='utf-8-sig'))
    return parser


def validate(root: Path, verify_manifest: bool = False) -> list[str]:
    errors: list[str] = []
    for name in REQUIRED:
        if not (root / name).is_file():
            errors.append(f'Missing required file: {name}')
    if errors:
        return errors
    paths = [p for p in root.rglob('*') if p.is_file()
             and '.git' not in p.relative_to(root).parts]
    for p in paths:
        rel = p.relative_to(root).as_posix()
        if p.suffix in ('.py', '.sh', '.ps1', '.conf', '.md', '.yml', '.json', '.xml', '.spl', '.kql'):
            try:
                text = p.read_text(encoding='utf-8-sig')
                if ('/workspace' + '/scratch/') in text:
                    errors.append(f'Nonportable workspace path: {rel}')
                if ('-----BEGIN ' + 'PRIVATE KEY-----') in text or ('-----BEGIN ' + 'RSA PRIVATE KEY-----') in text:
                    errors.append(f'Private key material: {rel}')
                if p.suffix == '.py':
                    ast.parse(text, filename=rel)
                elif p.suffix == '.xml':
                    ET.fromstring(text)
                elif p.suffix == '.json':
                    json.loads(text)
                elif p.suffix == '.sh':
                    if b'\r' in p.read_bytes():
                        errors.append(f'Shell script must use LF line endings: {rel}')
                    if shutil.which('bash'):
                        result = subprocess.run(['bash', '-n', str(p)], capture_output=True, text=True)
                        if result.returncode:
                            errors.append(f'Shell syntax: {rel}: {result.stderr.strip()}')
            except (OSError, UnicodeError, SyntaxError, ValueError, ET.ParseError) as exc:
                errors.append(f'{rel}: {exc}')
    try:
        indexes = parse_conf(root / 'apps/LAB_SIEM/local/indexes.conf')
        allowed = {'win_security', 'win_system', 'powershell', 'sysmon', 'linux', 'lab'}
        if not allowed.issubset(set(indexes.sections())):
            errors.append('One or more required lab indexes are absent.')
        nginx = parse_conf(root / 'apps/Splunk_TA_nginx/local/inputs.conf')
        stanza = 'monitor:///var/log/nginx/access.log'
        if nginx.get(stanza, 'index') != 'lab' or nginx.get(stanza, 'sourcetype') != 'nginx:plus:access':
            errors.append('NGINX access input must select lab and nginx:plus:access.')
        if nginx.get(stanza, 'disabled') not in ('0', 'false'):
            errors.append('NGINX access input is disabled.')
        outputs = parse_conf(root / 'apps/LAB_UF_WINDOWS/local/outputs.conf')
        if outputs.get('tcpout:lab_tls', 'sslVerifyServerCert').lower() != 'true':
            errors.append('Windows forwarding must verify the receiving certificate.')
        props = parse_conf(root / 'apps/LAB_SIEM/local/props.conf')
        transforms = parse_conf(root / 'apps/LAB_SIEM/local/transforms.conf')
        if props.get('siem:lab', 'REPORT-lab-fields') != 'lab_fields' or not transforms.has_section('lab_fields'):
            errors.append('Custom search field extraction reference is incomplete.')
        if props.get('identity', 'SEDCMD-redact_pw') != r's/\b(password=)[^,\s]+/\1REDACTED/g':
            errors.append('Identity password redaction rule is absent or differs from the tested lab rule.')
        inputs = parse_conf(root / 'apps/LAB_SIEM/local/inputs.conf')
        identity = 'monitor:///var/log/siem-lab/identity.log'
        if inputs.get(identity, 'sourcetype') != 'identity' or inputs.get(identity, 'index') != 'lab':
            errors.append('Identity input must use source type identity and index lab.')
        if inputs.get(identity, 'disabled') not in ('0', 'false'):
            errors.append('Identity input is disabled.')
        hec = parse_conf(root / 'configs/hec/inputs.conf.example')
        if hec.get('http', 'enableSSL') != '1' or hec.get('http', 'port') != '8088':
            errors.append('HEC example must enable TLS on port 8088.')
    except (configparser.Error, KeyError, ValueError) as exc:
        errors.append(f'Configuration structure: {exc}')
    if len(list((root / 'docs/steps').glob('[0-9][0-9]-*.md'))) != 52:
        errors.append('Expected all 52 numbered step files.')
    if verify_manifest:
        try:
            manifest = json.loads((root / 'FILE_MANIFEST.json').read_text(encoding='utf-8-sig'))
            for item in manifest['files']:
                p = (root / item['path']).resolve()
                if not p.is_relative_to(root.resolve()) or not p.is_file():
                    errors.append(f'Manifest path missing or outside project: {item["path"]}')
                elif hashlib.sha256(p.read_bytes()).hexdigest() != item['sha256']:
                    errors.append(f'Initial file hash changed: {item["path"]}')
        except (OSError, ValueError, KeyError) as exc:
            errors.append(f'Manifest: {exc}')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--verify-manifest', action='store_true', help='Verify the unmodified downloaded release.')
    args = parser.parse_args()
    errors = validate(args.root.resolve(), args.verify_manifest)
    if errors:
        for error in errors:
            print('FAIL:', error, file=sys.stderr)
        return 1
    print('Source validation passed. Live VM, Splunk, NGINX, and Azure tests remain separate.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
