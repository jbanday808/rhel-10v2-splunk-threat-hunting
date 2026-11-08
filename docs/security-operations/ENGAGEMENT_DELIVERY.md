# Consultant Engagement, Training and Knowledge Transfer

**Status:** reusable planning process, not a record of a Trellix customer engagement or a promise about product features. Keep customer and commercial information in approved private systems.

1. **Initiate:** Name the sponsor, technical owner, mission outcome, environment boundary, handling requirements and decision authority. Agree on work products, measurable acceptance criteria, dependencies and out-of-scope activities.
2. **Discover:** Review architecture, asset/product versions, licenses, lifecycle, identity, agent health, logging, retention, network visibility and existing incident/vulnerability processes. Use the [product questions](TRELLIX_PRODUCT_OVERVIEW.md). Record assumptions and unverified information.
3. **Plan effort and schedule:** Break work into tasks, owners, estimated hours, dependencies, approved rates if relevant, milestones and review points. Identify travel/access/clearance constraints without publishing sensitive details. Track actual effort against the authorized scope; do not invent estimates or financial results.
4. **Design:** Document data flows, roles, approved integrations, least privilege, evidence handling, operational impact, acceptance tests and rollback. Review architecture/control gaps with the owner and security engineer.
5. **Implement only authorized changes:** Use change control, a controlled pilot, private backups and documented failure/recovery conditions. Coordinate with system, network, endpoint, SIEM and governance teams. Repository documentation alone deploys nothing.
6. **Validate:** Test collection, effective policies, query behavior, response boundaries, recovery and service health separately. Use matching/nonmatching controls and report coverage gaps. Confirm the customer's accepted version/platform combination rather than assuming the home lab proves compatibility.
7. **Communicate:** Provide concise progress, findings, blockers, decisions and next milestones. Escalate schedule/cost/scope changes through the agreed owner; record approved changes before delivering extra work.
8. **Train and mentor:** Use a sanitized or synthetic case. Demonstrate the procedure, have the recipient repeat it, review their interpretation and record unresolved questions. Explain safe rollback and when to escalate. Keep a versioned lesson, practice steps and answer key.
9. **Close and hand over:** Complete the [engagement report](templates/engagement-closeout.md), operational runbooks, product/configuration inventory, evidence references, open risks, ownership, support path and acceptance record. Transfer secrets only through approved channels.
10. **Reconcile and improve:** Compare approved deliverables and time/expense records with contract acceptance and billing rules. Route invoicing through the authorized commercial process. Capture reusable sanitized lessons, peer-review detection improvements and propose follow-on work through the established account owner without making unsupported product promises.

## Suggested training session

| Segment | Demonstration | Acceptance check |
| --- | --- | --- |
| Product roles | ENS versus HX, TIE versus DXL, DLP versus encryption | Recipient explains each in plain language |
| Case intake | Open the synthetic tabletop record | Owner, priority basis and next action are recorded |
| Hunt execution | Review the pipe or HTTP hypothesis and controls | Recipient distinguishes collected data, search match and interpretation |
| Forensic review | Build the synthetic AI packet and check citations | Recipient identifies at least one unsupported conclusion/collection gap |
| Handover | Brief findings, limitations and decisions | Receiving owner acknowledges open actions and support route |

Training completion is not proof of product certification or validated production operation. Record actual attendance, exercises and feedback only after delivery.
