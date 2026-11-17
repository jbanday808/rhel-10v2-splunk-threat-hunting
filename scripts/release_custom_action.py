#!/usr/bin/env python3
"""Publish a tested action release and its compatible major tag with GitHub CLI."""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys


REPOSITORY = 'jbanday808/rhel-10v2-splunk-threat-hunting'


def gh(*args: str, allow_missing: bool = False) -> str | None:
    result = subprocess.run(['gh', *args], capture_output=True, text=True, check=False)
    if result.returncode:
        if allow_missing and 'HTTP 404' in result.stderr:
            return None
        raise RuntimeError(f'GitHub CLI operation failed: {result.stderr.strip()}')
    return result.stdout


def api(endpoint: str, *, allow_missing: bool = False) -> dict | None:
    body = gh('api', endpoint, allow_missing=allow_missing)
    return None if body is None else json.loads(body)


def resolve_tag(repository: str, tag: str) -> str | None:
    ref = api(f'repos/{repository}/git/ref/tags/{tag}', allow_missing=True)
    if ref is None:
        return None
    obj = ref['object']
    while obj['type'] == 'tag':
        obj = api(f'repos/{repository}/git/tags/{obj["sha"]}')['object']
    if obj['type'] != 'commit':
        raise RuntimeError('Release tag must resolve to a commit.')
    return obj['sha']


def main() -> int:
    repository = os.environ.get('GITHUB_REPOSITORY', '')
    commit = os.environ.get('GITHUB_SHA', '')
    if repository != REPOSITORY or os.environ.get('GITHUB_REF') != 'refs/heads/main':
        raise ValueError('Releases are restricted to the authoritative main branch.')
    if not re.fullmatch(r'[0-9a-f]{40}', commit):
        raise ValueError('GITHUB_SHA must identify the tested commit.')
    root = Path(__file__).resolve().parents[1]
    version = (root / 'ACTION_VERSION').read_text(encoding='utf-8').strip()
    if not re.fullmatch(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)', version):
        raise ValueError('ACTION_VERSION must contain a stable semantic version such as 1.0.0.')
    tag = f'v{version}'
    major = f'v{version.split(".")[0]}'
    existing_commit = resolve_tag(repository, tag)
    if existing_commit is not None and existing_commit != commit:
        raise RuntimeError('This version tag already identifies a different commit; bump ACTION_VERSION.')
    release = api(f'repos/{repository}/releases/tags/{tag}', allow_missing=True)
    if release is None:
        notes = root / '.github/action-release-notes.md'
        if not notes.is_file():
            raise ValueError('Release notes are required.')
        gh('release', 'create', tag, '--repo', repository, '--target', commit,
           '--title', f'RHEL Splunk source check {tag}', '--notes-file', str(notes))
        release = api(f'repos/{repository}/releases/tags/{tag}')
    elif release.get('draft') or release.get('prerelease'):
        raise RuntimeError('An existing draft or prerelease needs owner review before stable publication.')

    if resolve_tag(repository, tag) != commit:
        raise RuntimeError('Published release does not resolve to the tested commit.')
    major_commit = resolve_tag(repository, major)
    if major_commit is None:
        gh('api', '--method', 'POST', f'repos/{repository}/git/refs',
           '-f', f'ref=refs/tags/{major}', '-f', f'sha={commit}')
    elif major_commit != commit:
        comparison = api(f'repos/{repository}/compare/{major_commit}...{commit}')
        if comparison.get('status') not in {'ahead', 'identical'}:
            raise RuntimeError('The major tag is newer or diverged; refusing to move it backwards.')
        gh('api', '--method', 'PATCH', f'repos/{repository}/git/refs/tags/{major}',
           '-f', f'sha={commit}', '-F', 'force=true')
    if resolve_tag(repository, major) != commit:
        raise RuntimeError('Major version tag verification failed.')
    url = release['html_url']
    print(f'Published {tag} and {major}: {url}')
    summary = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary:
        with open(summary, 'a', encoding='utf-8') as stream:
            stream.write(f'## Custom action release\n\nPublished [{tag}]({url}) at `{commit}`. '
                         f'The `{major}` tag identifies the same tested commit.\n\n'
                         'Marketplace listing is a separate step in the GitHub release editor.\n')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, RuntimeError) as error:
        print(f'Release failed: {error}', file=sys.stderr)
        raise SystemExit(1)
