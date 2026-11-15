# TraceVector · Threat Hunting Lab

[Open the current Site](https://tracevector.jamesbanday.chatgpt.site/) · [Try a guided hunt](https://tracevector.jamesbanday.chatgpt.site/#scenarios) · [Read the simple guide](../../docs/network-defense/INTERACTIVE_LAB.md)

This folder holds the public source for the current TraceVector Site. It is a browser-based **threat-hunting practice workspace**. The Site offers ten guided hunts with made-up records, example Splunk searches, and explanations of what each clue means. It also helps organize evidence, draft searches, and prepare a short report. The exercises do not connect to a live Splunk system or change a lab machine.

| File | Purpose |
| --- | --- |
| `index.html` | Page shell |
| `styles.css` | Layout and readable text |
| `context.js` | Links to hunting guides, tools, and existing lab images |
| `scenarios.js` | Ten synthetic investigations and their example searches |
| `app.js` | Guided workflow, notes, evidence, drafts, and browser-local backup |

## Use the workspace

1. Open **Scenario lab** and choose a hunt.
2. Read the sample records and answer the three questions.
3. Review the explanation and example Splunk search.
4. Write down what you would check next in a real investigation.

The other sections are **Lab overview**, **Lab objectives**, **Evidence & screenshots**, **Hunt follow-up**, **Detection studio**, **Project documentation**, **Progress tracking**, and **Lab proposals**. These sections support the hunting workflow. The [full guide](../../docs/network-defense/INTERACTIVE_LAB.md) explains them in plain language.

The example searches use `index=tracevector_lab`, a training placeholder. The real lab has six documented indexes: `win_security`, `win_system`, `powershell`, `sysmon`, `linux`, and `lab`. Map each search to the logs you actually collect before testing it in Splunk. Finishing a practice hunt does not prove live detection coverage.

## Save and protect your work

Your progress, notes, proposals, and evidence attachments stay in the browser you use. **Export lab backup** saves a copy; **Import backup** replaces the current browser workspace after a confirmation step. Keep backups private because they may contain your notes or evidence. The repository does not contain personal browser data, hosting credentials, or live customer records.

The Site source includes no direct GitHub write or live Splunk connection. Proposals and review decisions are local drafts for a person to inspect and apply separately. Existing version 1 workspace backups remain importable.

## Preview the source

From the repository root, run a local static server:

```bash
python3 -m http.server 8000 --bind 127.0.0.1 --directory website/tracevector-lab
```

Open `http://127.0.0.1:8000/` on the same computer. No build or package installation is needed. You can check JavaScript syntax with:

```bash
node --check website/tracevector-lab/context.js
node --check website/tracevector-lab/scenarios.js
node --check website/tracevector-lab/app.js
```

The [repository checks](../../README.md#validate-and-publish) cover the wider project. Interface captures and sample results do not establish live lab validation.
