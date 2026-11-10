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

If no approved RHEL package is available, use the [Ubuntu WSL YARA CLI setup](OFFLINE_HTTP_WALKTHROUGH.md#1-set-up-an-analysis-workspace). The [worked artifact exercise](OFFLINE_HTTP_WALKTHROUGH.md#6-pivot-and-validate-the-exported-file-with-yara) includes a matching file and a near-match control.

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
"$HOME/.venvs/sigma-lab/bin/sigma" convert -t splunk --without-pipeline \
  rules/sigma/lab_network_dns_marker.yml
~~~

**Command overview:** `--without-pipeline` keeps the custom rule's field as `query`, the field in the native Zeek DNS JSON. Expect `query="lab-marker.example.test"`. If using the optional forwarded source, scope it to `index=net_zeek sourcetype="zeek:json"` and the known capture window. Confirm the field and match in Splunk before enabling any alert. For Windows process creation use the [separate Sysmon example](OFFLINE_HTTP_WALKTHROUGH.md#7-convert-a-separate-sysmon-sigma-control-to-spl) and the Windows pipeline.

## Quality gates

- Rule syntax parses.
- Synthetic true-positive and negative fixtures are measured.
- SPL is visually reviewed for source index, sourcetype, field naming and timeframe.
- False positives, missing data and unstable field mappings are recorded.
- Any scheduled alert or escalation must be approved by the analyst/system owner.
- Neither YARA nor Sigma test passing constitutes an approved detection control or CMMC assessment.

**References:** [YARA command-line docs](https://yara.readthedocs.io/en/latest/commandline.html) · [Sigma CLI](https://github.com/SigmaHQ/sigma-cli) · [Sigma Getting Started](https://sigmahq.io/docs/guide/getting-started.html).
