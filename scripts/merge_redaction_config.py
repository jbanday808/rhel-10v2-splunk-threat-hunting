#!/usr/bin/env python3
"""Preview or append the dedicated identity lab stanzas without replacing an app."""
from __future__ import annotations

import argparse
import configparser
from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import tempfile


def parse(text: str) -> configparser.RawConfigParser:
    result = configparser.RawConfigParser(interpolation=None, strict=True)
    result.optionxform = str
    result.read_string(text)
    return result


def prepare(target_dir: Path, snippets_dir: Path) -> list[tuple[Path, str]]:
    """Preflight every file before proposing any write; preserve existing text."""
    changes = []
    for name in ('inputs.conf', 'props.conf'):
        target = target_dir / name
        if not target.is_file() or target.is_symlink():
            raise ValueError(f'Expected an existing regular app file: {target}')
        original = target.read_text(encoding='utf-8')
        snippet = (snippets_dir / (name + '.example')).read_text(encoding='utf-8')
        current, expected = parse(original), parse(snippet)
        if len(expected.sections()) != 1:
            raise ValueError(f'Expected exactly one snippet stanza: {name}')
        section = expected.sections()[0]
        if current.has_section(section):
            if any(not current.has_option(section, key) or current.get(section, key) != value
                   for key, value in expected.items(section)):
                raise ValueError(f'{target}: [{section}] already exists with different settings. Merge manually.')
        else:
            changes.append((target, original.rstrip() + '\n\n' + snippet.strip() + '\n'))
    return changes


def apply(changes: list[tuple[Path, str]], backup_root: Path) -> Path | None:
    if not changes:
        return None
    backup_root.mkdir(parents=True, exist_ok=True, mode=0o700)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup = Path(tempfile.mkdtemp(prefix=f'redaction-{stamp}-', dir=backup_root))
    backup.chmod(0o700)
    for target, _ in changes:
        shutil.copy2(target, backup / target.name)
    for target, updated in changes:
        metadata = target.stat()
        fd, temp = tempfile.mkstemp(prefix='.' + target.name + '-', dir=target.parent)
        try:
            with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as stream:
                stream.write(updated)
                stream.flush()
                os.fsync(stream.fileno())
            if os.name == 'posix':
                os.chown(temp, metadata.st_uid, metadata.st_gid)
            os.chmod(temp, metadata.st_mode & 0o777)
            os.replace(temp, target)
        finally:
            if os.path.exists(temp):
                os.unlink(temp)
    return backup


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target-dir', type=Path, required=True)
    parser.add_argument('--snippets-dir', type=Path,
                        default=Path(__file__).resolve().parents[1] / 'configs/redaction')
    parser.add_argument('--backup-root', type=Path, default=Path('/var/backups/siem-lab'))
    parser.add_argument('--apply', action='store_true', help='Write after all files pass preflight.')
    args = parser.parse_args()
    try:
        changes = prepare(args.target_dir, args.snippets_dir)
        for target, _ in changes:
            print(f'Append the missing lab stanza: {target}')
        if args.apply:
            backup = apply(changes, args.backup_root)
            print(f'Backup: {backup}' if backup else 'No changes; expected settings already exist.')
        elif changes:
            print('Preview only. Review the snippets, then use --apply or the RHEL installer.')
        else:
            print('No changes; expected settings already exist.')
    except (OSError, ValueError, configparser.Error) as exc:
        parser.exit(1, f'ERROR: {exc}\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
