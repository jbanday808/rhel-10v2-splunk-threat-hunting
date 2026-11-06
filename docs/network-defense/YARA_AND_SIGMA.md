# YARA and Sigma — File Classification and Portable Detection Engineering

**Different purposes:** YARA matches byte/text patterns in approved *files*; Sigma describes SIEM detection rules. Neither automatically sniffs network packets.

## YARA: install and test only with benign synthetic data

Check approved RHEL 10 repositories:

~~~bash
sudo dnf info yara || true
command -v yara || true
~~~

If \`yara\` exists from an approved repository, run:

~~~bash
mkdir -p "$HOME/network-lab/yara-test"
printf 'LAB_NETWORK_DEFENSE_FIXTURE\n' > "$HOME/network-lab/yara-test/harmless.txt"
yara rules/yara/lab_marker.yar "$HOME/network-lab/yara-test/harmless.txt"
~~~

**Expected:** The harmless marker rule matches the synthetic text file. Create a separate clean text file lacking the marker and verify no match.

If unavailable in approved RHEL packages, use an isolated Python \`yara-python\` environment on WSL for a scripted equivalent; do not assume the Python package provides a standalone \`yara\` binary.

**Data protection:** Never publish malware samples or extracted documents. YARA matching is a classification aid; a match against a generic byte string is not proof of malicious intent. Do not scan the whole OS or an arbitrary live process.

## Sigma: install a current supported backend in a private venv (WSL)

~~~bash
python3 -m venv "$HOME/.venvs/sigma-lab"
"$HOME/.venvs/sigma-lab/bin/python" -m pip install --upgrade pip
"$HOME/.venvs/sigma-lab/bin/python" -m pip install sigma-cli
"$HOME/.venvs/sigma-lab/bin/sigma" plugin list
"$HOME/.venvs/sigma-lab/bin/sigma" plugin install splunk
"$HOME/.venvs/sigma-lab/bin/sigma" list
~~~

**Command overview:** Installs isolated Sigma CLI and the Splunk backend and lists conversion capabilities. For reproducibility, review/pin versions after confirming compatibility; avoid pasting third-party rule packages directly into production.

Convert the [sample Sigma DNS test rule](../../rules/sigma/lab_network_dns_marker.yml):

~~~bash
"$HOME/.venvs/sigma-lab/bin/sigma" convert -t splunk \
  rules/sigma/lab_network_dns_marker.yml
~~~

**Important:** The conversion backend may require a matching processing pipeline and actual field mapping for your local \`net_zeek\` JSON sourcetype. The example rule's \`dns.query\` field is a **design field**, not guaranteed to be extracted exactly as named in Splunk. Test conversion, adjust the search fields to actual data and document the resulting SPL and test outcome. For Windows Sysmon, inspect the supported \`-p sysmon\` pipeline.

## Quality gates

- Rule syntax parses.
- Synthetic true-positive and negative fixtures are measured.
- SPL is visually reviewed for source index, sourcetype, field naming and timeframe.
- False positives, missing data and unstable field mappings are recorded.
- Any scheduled alert or escalation must be approved by the analyst/system owner.
- Neither YARA nor Sigma test passing constitutes an approved detection control or CMMC assessment.

**References:** [YARA command-line docs](https://yara.readthedocs.io/en/latest/commandline.html) · [Sigma CLI](https://github.com/SigmaHQ/sigma-cli) · [Sigma Getting Started](https://sigmahq.io/docs/guide/getting-started.html).
