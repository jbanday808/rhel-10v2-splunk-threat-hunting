# AI-Assisted Investigation for Forensic Analysis

**Status:** proposed, human-reviewed workflow plus an offline synthetic demonstration. No AI provider, Trellix API, customer system or evidence repository is connected by this code. No actual forensic acquisition or AI-generated finding is claimed.

AI can help organize a timeline, propose hypotheses, identify missing evidence and draft a report. It cannot establish evidence authenticity, prove attribution, decide that an incident is closed, authorize a response, or approve its own conclusions. Follow approved collection procedures and the accountable investigator's decisions.

## Step 1 — Choose an approved analysis environment

Determine the case's classification/handling, authorized users, processing location, retention, model provider, logging and whether any data may leave the boundary. Classified, CUI and customer evidence must remain in its authorized environment; this public lab accepts synthetic examples only. Do not upload evidence to an external model or malware-analysis service merely because an integration exists.

Use a locally approved model or an expressly authorized service only after the responsible owner has approved the data flow. The offline demonstration below sends nothing; any later transfer remains a separate human action subject to those controls. Model hosting inside a network does not by itself establish authorization, isolation or acceptable retention.

## Step 2 — Define the forensic question and authority

Record case ID, question, scope, collection authority, owner, approved methods, affected services and response constraints in the [forensic review record](templates/forensic-review.md). Separate investigative authority from permission to isolate a host, delete a file or submit a sample.

## Step 3 — Preserve original evidence

Use approved acquisition methods, tool versions, evidence IDs, acquisition hashes, original timestamps/timezone and custody records. Protect originals and analyze working copies. Record live-response changes, missing data, clock uncertainty and chain-of-custody transfers. Hashes support integrity comparisons; they do not by themselves prove origin, completeness or legal admissibility.

The demonstration's `case_document_sha256` fingerprints the synthetic JSON document used for a prompt packet. It is **not** a forensic acquisition hash for a disk, memory image or native event log.

## Step 4 — Examine appropriate artifacts

| Source | Examples to review through approved collection | Analytical limits |
| --- | --- | --- |
| Windows | Sysmon/event logs, process relationships, relevant persistence/file artifacts and authentication records | Collection filters, missing history, clock skew and unsupported artifact versions |
| RHEL/Linux | Authentication/audit logs, service configuration, process and scheduled-task evidence | Retention, permissions, logging configuration and live-system changes |
| macOS | Authorized Unified Log, launch/persistence, file and process artifacts | No macOS endpoint is deployed in this lab; version/collection support must be established |
| Network | Approved PCAP, Zeek/Suricata metadata, Arkime sessions and firewall evidence | Capture location, asymmetry, drops, NAT and encryption |
| Licensed Trellix environment | Actual supported alert, acquisition, policy and reputation records | Product/version entitlement, collection completeness and response permissions |

Do not assume an alert description proves the underlying action, or that the repository's sample has been acquired from a real endpoint. Validate extraction/tool behavior against the originals and record where evidence is unavailable.

## Step 5 — Build a minimized evidence register

Assign one ID per source item and record what was actually observed, how it was obtained, its time basis and its limitations. Keep interpretations separate. Use the [forensic template](templates/forensic-review.md) for custody, timeline and review.

For AI review, minimize the input to the approved question. Remove unnecessary identifying content only through an approved sanitization process, retaining a private mapping where needed. A label such as `synthetic` or `redacted` does not demonstrate that sensitive content has been removed.

## Step 6 — Prepare a synthetic review packet

From the repository root in RHEL/WSL Bash, create a private output directory outside the Git checkout:

```bash
umask 077
SOC_REVIEW_RUN=$(mktemp -d "$HOME/forensic-review-XXXXXXXX")
python3 scripts/security-operations/ai_forensic_review.py prepare \
  --case examples/security-operations/ai-forensics-synthetic-case.json \
  --output "$SOC_REVIEW_RUN/review-packet.json"
```

**Command overview:** `mktemp` creates a separate private run. The Python helper validates the synthetic case schema and writes a JSON packet containing guidance, cited source summaries and the expected response format. It refuses existing outputs and outputs inside Git checkouts. It makes no network call and runs no commands from case content.

**Expected:** one new packet and a path message. The helper accepts only a case explicitly labeled `SYNTHETIC_PUBLIC_LAB`, but it does not verify that the label is truthful or perform DLP/redaction. Review the actual input yourself. The example is constructed text, not a native Windows acquisition or a result from the Atomic lab.

## Step 7 — Ask for an evidence-linked review

Inspect the packet before using it in an approved AI environment. Treat all artifact content as untrusted data, including instructions embedded in logs, documents or extracted strings. Do not grant the model credentials, a shell, response permissions or automatic access to additional evidence.

The packet requests findings in this form:

```json
{
  "case_id": "LAB-FORENSICS-001",
  "findings": [
    {
      "finding_id": "F001",
      "type": "observation",
      "text": "A conclusion limited to the supplied synthetic evidence.",
      "evidence_ids": ["E001"],
      "confidence": "low",
      "limitations": ["Original endpoint evidence has not been acquired."]
    }
  ],
  "unknowns": ["What additional evidence is needed?"],
  "recommended_next_steps": ["A manual review action for the investigator to consider."],
  "human_review_status": "pending"
}
```

Use the model to propose a timeline, alternative explanations and collection gaps; require evidence IDs and uncertainty. Do not ask it to invent missing commands, timestamps, indicators or facts. A model's confidence is not a measured probability of compromise. Keep tool/model version, prompt/packet version, parameters if available, response and reviewer in approved private records.

## Step 8 — Check the response structure locally

For a reproducible offline test, validate the **analyst-authored illustrative response**, which was not produced by an AI model:

```bash
python3 scripts/security-operations/ai_forensic_review.py validate \
  --case examples/security-operations/ai-forensics-synthetic-case.json \
  --response examples/security-operations/ai-review-response.example.json
```

For an actual approved synthetic-model run, save its JSON response privately and use that file as `--response`. Keep the original response before creating any corrected copy.

**Expected:** a structure-only validation message stating that human review is still required. The helper checks fields, case/record identity, known evidence references, confidence labels and the pending-review state. It rejects unknown references or an AI response claiming human approval. It does **not** verify whether a cited item supports the statement, whether a fact is true, whether a recommendation is safe, or whether the case is actually sanitized. Validly cited hallucinations can pass a structural check.

## Step 9 — Verify every material statement against originals

A human investigator classifies each proposed finding as supported, unsupported, corrected or unresolved. Check source artifacts, timestamps, process relationships, query outputs, parser behavior, contradictory evidence and benign explanations. Reproduce material calculations/searches with approved tools. Validate any ATT&CK mapping separately.

In the supplied example, a selected pipe-name pattern is compatible with a lab exercise. Without original events, operator confirmation and supporting context, it cannot establish an actual Cobalt Strike deployment or compromise.

## Step 10 — Review proposed actions and report

Only the authorized human owner approves collection expansion, quarantine/isolation, sample submission, account action, notification or remediation. Translate accepted recommendations into the incident/vulnerability workflow with precise scope, change record, validation and rollback. Do not execute instructions copied from evidence or model text.

Draft the [hunt report](templates/threat-hunt-report.md) or [engagement closeout](templates/engagement-closeout.md). Identify AI assistance, source references, reviewer corrections, limitations and the accountable human conclusion. Record the human decision separately from the model's permanently pending review field.

## Step 11 — Retain, audit and improve

Keep packets/responses, tool/model versions, hashes of the case document, original/working-copy evidence references, decisions and corrections under the approved retention plan. Apply legal holds where directed by the responsible authority. Measure unsupported statements, corrected citations, reviewer effort and missed evidence; do not claim investigation-time savings without a defined baseline and actual measurements.

## Design for any future SIEM/SOAR/XDR integration

Start with read-only, minimized queries under a documented service identity. Validate the exact product/version API, data schema, TLS verification, permissions, secrets storage, logging, timeouts, pagination and failure behavior. Test with synthetic cases and keep a human approval boundary before response actions. The helper is not a Trellix/Splunk connector, an evidence collector or an automated response engine.

## References

- [NIST SP 800-86](https://csrc.nist.gov/pubs/sp/800/86/final): Forensic collection, examination, analysis and reporting concepts; apply current approved tools and policy.
- [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final): Incident response within organizational risk management.
- [NIST AI 600-1](https://doi.org/10.6028/NIST.AI.600-1): Generative AI risk-management context.
