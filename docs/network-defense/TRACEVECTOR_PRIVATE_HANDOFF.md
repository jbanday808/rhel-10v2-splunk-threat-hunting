# Move a TraceVector practice hunt into a private case record

TraceVector's [guided investigations](INTERACTIVE_LAB.md) use synthetic records. Its progress, notes, evidence attachments, search drafts, and proposals stay in the current browser. The Site does not submit a hunt report to GitHub or run Splunk. Use this handoff when a practice idea becomes a separately approved lab or customer investigation.

## Keep the practice record safe

1. In **Scenario lab**, record the question, the training answer, the example search, and an ordinary explanation to check. Mark these as **synthetic practice**.
2. In **Progress tracking**, export the workspace backup if you need to retain your browser notes or attachments. Store the download in an approved private location; a backup may contain sensitive attachments. Importing it later replaces that browser's TraceVector workspace after confirmation.
3. If you drafted a proposal, use the Site's proposal export for a Markdown copy. Review it before sharing. A proposal is a draft, not a validated detection or an approved GitHub change.

The backup is for restoring the workspace. It is **not** a customer report. Do not commit it, raw evidence, or a filled customer worksheet to this public repository.

## Open a separate investigation

Use a private copy of the [hunt plan](../security-operations/templates/threat-hunt-plan.md) and [detailed report](../security-operations/templates/threat-hunt-report.md). Enter:

| Case field | What to carry over, after review |
| --- | --- |
| Question and owner | Rewrite the practice question for the approved host, account, period, and decision maker. |
| Scope and permission | Record who approved the read-only review or harmless test and where evidence may be stored. |
| Data source | Replace the Site's `index=tracevector_lab` placeholder with a verified source from `win_security`, `win_system`, `powershell`, `sysmon`, `linux`, or `lab`. Do not assume any of them contain the needed events. |
| Search and fields | Copy the search as a **draft**; confirm real field names, timestamp, host and account context, and source health before interpreting output. |
| Comparison | Check a known-good or harmless control and at least one alternate explanation. |
| Evidence and limits | Record private references to actual results, missing records, collection gaps, and what the result cannot prove. |
| Decision and next step | State the supported finding in everyday language and name the person who can approve follow-up. |

The [ten scenario-to-lab guides](tracevector-hunts/README.md) describe candidate sources and controls for each exercise. A source that is not collected produces a **visibility gap**, not a clean result. A completed Site exercise never by itself proves a live detection.

## Share only a reviewed summary

Before a customer briefing or repository update, have the case owner review the wording and handling boundary. Use the [briefing outline](../security-operations/templates/hunt-briefing.md) to explain the question, observed evidence, uncertainty, and next owner decision. Follow the [public sanitization checklist](../reference/security-and-sanitization.md) before publishing any example. Keep the original backup and complete case record private.
