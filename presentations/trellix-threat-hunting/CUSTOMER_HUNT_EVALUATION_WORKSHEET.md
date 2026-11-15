# Customer threat-hunt evaluation worksheet

Use this conversation guide with the [Trellix role and PowerPoint guide](README.md), especially slides 42–44 and 50–52. Copy it into an approved **private** customer workspace before entering names, account details, logs, or other real information. This public file is an empty example, not a record of a customer engagement or a Trellix deployment.

## 1. Agree on the question

| Prompt | Working answer |
| --- | --- |
| What is the customer's concern, in everyday language? | To be agreed privately |
| What single question will this evaluation try to answer? | To be agreed privately |
| Who owns the decision after the findings are explained? | To be agreed privately |
| What would make the evaluation useful to that decision-maker? | To be agreed privately |

**Example question:** “Can we tell whether an unusual sign-in was expected?” This is a question to investigate, not a conclusion that an account was compromised.

## 2. Confirm permission and boundaries

| Check | Record privately |
| --- | --- |
| Approving person and date | Approval pending |
| Computers, accounts, services, and time period in scope | Scope pending |
| Systems or information excluded from review | Exclusions pending |
| Allowed read-only review or agreed harmless test | Method pending |
| Where evidence may be stored and when it must be removed | Handling pending |

Do not begin a test or expand the scope until the customer's authorized owner approves it. Response actions, configuration changes, and access changes need separate approval.

## 3. Check whether the clues are available

| Possible clue | Available and healthy? | Owner / gap to resolve |
| --- | --- | --- |
| Account sign-in records | Unknown | Confirm source, time coverage, and owner |
| Device activity records | Unknown | Confirm source, time coverage, and owner |
| Network activity records, if relevant | Unknown | Confirm whether collection exists and is permitted |
| A normal comparison period | Unknown | Confirm what expected activity looks like |

Ask whether records have the needed time, account, and device context. A missing record may mean collection was unavailable; it does not prove that nothing happened.

## 4. Define a small, reviewable evaluation

- **Question and expected clue:** What pattern will the team look for?
- **Ordinary explanation:** What legitimate behavior could produce the same pattern?
- **Comparison:** What known-good activity or harmless agreed test will help distinguish the two?
- **Success measure:** What evidence would show that the team can answer the question reliably?
- **Limit:** What conclusion would still be unsupported, even if the tool finds a clue?
- **Product check:** If a Trellix capability is proposed, who will confirm its current name, availability, licensing, configuration, and supported systems?

An alert count alone is not a success measure. The team should be able to explain what was observed, what remains uncertain, and who can act on it.

## 5. Explain the result and next decision

| Plain-language result | Private notes |
| --- | --- |
| What was actually observed? Include evidence references. | Pending review |
| What other explanations were checked? | Pending review |
| What information was missing? | Pending review |
| Is the question answered, unanswered, or inconclusive? Why? | Pending review |
| What action is recommended, who owns it, and what approval is needed? | Pending review |
| When will the customer receive an update or final report? | Pending review |

**Example briefing:** “We reviewed the approved sign-in records. We found activity that needs the account owner's confirmation. The records alone do not establish misuse. The customer can decide whether to authorize a wider review.”

Keep the completed worksheet and evidence in the customer's approved private location. For a detailed investigation, use the repository's [hunt plan](../../docs/security-operations/templates/threat-hunt-plan.md) and [briefing outline](../../docs/security-operations/templates/hunt-briefing.md). Do not publish a filled worksheet or raw customer evidence to GitHub.
