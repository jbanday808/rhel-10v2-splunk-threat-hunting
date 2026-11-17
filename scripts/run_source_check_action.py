#!/usr/bin/env python3
"""Run the action's bundled validator against a checked-out lab source tree."""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sys
from typing import Callable, Mapping


def target_directory(workspace_value: str, path_value: str) -> Path:
    """Resolve the input within the runner workspace, including symbolic links."""
    if not workspace_value:
        raise ValueError('GITHUB_WORKSPACE must identify the checked-out workspace.')
    workspace = Path(workspace_value).resolve(strict=True)
    if not workspace.is_dir():
        raise ValueError('GITHUB_WORKSPACE must be a directory.')
    if not path_value or '\x00' in path_value or '\n' in path_value or '\r' in path_value:
        raise ValueError('The path input must be a nonempty single-line directory path.')
    target = (workspace / path_value).resolve(strict=True)
    if not target.is_relative_to(workspace) or not target.is_dir():
        raise ValueError('The path input must identify a directory inside GITHUB_WORKSPACE.')
    # The bundled validator reads files. Do not let source-tree links redirect it
    # to other runner files, even if the requested root itself is in the workspace.
    for parent, directories, files in os.walk(target, followlinks=False):
        directories[:] = [name for name in directories if name != '.git']
        for name in directories + files:
            child = Path(parent) / name
            if child.is_symlink() and not child.resolve().is_relative_to(target):
                raise ValueError('Source-tree symbolic links must stay inside the selected project.')
    return target


def parse_manifest(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized not in ('true', 'false'):
        raise ValueError('The verify-manifest input must be true or false.')
    return normalized == 'true'


def bundled_validator() -> Callable[[Path, bool], list[str]]:
    """Load code next to this trusted action, never from the selected checkout."""
    path = Path(__file__).resolve().with_name('validate_project.py')
    spec = importlib.util.spec_from_file_location('_source_check_validator', path)
    if spec is None or spec.loader is None:
        raise RuntimeError('The bundled source validator could not be loaded.')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.validate


def write_results(environment: Mapping[str, str], count: int) -> None:
    result = 'failed' if count else 'passed'
    output = environment.get('GITHUB_OUTPUT')
    if output:
        with Path(output).open('a', encoding='utf-8', newline='\n') as stream:
            stream.write(f'result={result}\nerror-count={count}\n')
    summary = environment.get('GITHUB_STEP_SUMMARY')
    if summary:
        with Path(summary).open('a', encoding='utf-8', newline='\n') as stream:
            stream.write(
                '### RHEL Splunk source check\n\n'
                f'Result: **{result}**. Errors: **{count}**.\n\n'
                'Offline source checks only; live lab behavior remains unverified.\n'
            )


def main(environment: Mapping[str, str] | None = None,
         validator: Callable[[Path, bool], list[str]] | None = None) -> int:
    environment = os.environ if environment is None else environment
    if sys.version_info < (3, 10):
        print('Python 3.10 or newer is required.', file=sys.stderr)
        return 1
    try:
        verify_manifest = parse_manifest(environment.get('SOURCE_CHECK_VERIFY_MANIFEST', 'false'))
        target = target_directory(environment.get('GITHUB_WORKSPACE', ''),
                                  environment.get('SOURCE_CHECK_PATH', '.'))
        check = bundled_validator() if validator is None else validator
        errors = check(target, verify_manifest)
        count = len(errors)
        # Filenames and parser diagnostics may contain workflow commands or
        # credentials. Keep untrusted diagnostics out of shared runner logs.
        if count:
            print(f'Source validation failed with {count} error(s).', file=sys.stderr)
            print('Run scripts/validate_project.py locally to inspect source diagnostics.', file=sys.stderr)
        else:
            print('Source validation passed. Live lab behavior remains unverified.')
    except Exception:
        # This is the runner boundary: malformed source must fail with outputs,
        # including unexpected parser errors, without logging source contents.
        count = 1
        print('Source check could not run. Check the path, boolean input, and lab source layout.',
              file=sys.stderr)
    try:
        write_results(environment, count)
    except OSError:
        print('Could not write GitHub action outputs or summary.', file=sys.stderr)
        return 1
    return 1 if count else 0


if __name__ == '__main__':
    raise SystemExit(main())
