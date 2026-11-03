#!/usr/bin/env bash
# Read-only checks for a cloned WSL repository.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../.."
git rev-parse --is-inside-work-tree >/dev/null
python3 scripts/validate_project.py
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
python3 tools/publication_preflight.py
printf '\nFile inventory:\n'
printf 'SOP steps: '; find docs/steps -maxdepth 1 -type f -name '[0-9][0-9]-*.md' | wc -l
printf 'Appendices: '; find docs/appendices -maxdepth 1 -type f -name '[0-9][0-9]-*.md' | wc -l
printf 'Hunts: '; find hunts -maxdepth 1 -type f -name '*.spl' | wc -l
printf 'Screenshots: '; find screenshots -maxdepth 1 -type f -name '*.png' | wc -l
