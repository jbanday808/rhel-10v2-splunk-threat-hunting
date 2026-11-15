# Worked hunt: Was a Microsoft Entra directory role assigned as expected?

**Status:** synthetic planning example. This is a review of Microsoft Entra **directory roles**, not Azure resource RBAC assignments. The repository does not configure or validate Entra audit-log collection into Splunk.

## The question and the records

**Question:** “Who gave this identity a directory role, and was the change approved?” A role assignment may be ordinary administration, temporary Privileged Identity Management activity, or a change that needs follow-up. The audit entry alone does not show misuse of the granted access.

Agree on the tenant, role or affected identity, UTC window, audit-log reader, expected change approval, and role owner. In the Microsoft Entra admin center, use **Monitoring & health → Audit logs**. Confirm that the records cover the period and that the reviewer can view the actor, target, result, and modified properties. Current lab indexes do not contain a validated Entra audit feed.

## Read-only hunt steps

1. Filter audit logs to **Category: RoleManagement** and the approved time window. Examine relevant activity names such as `Add member to role`; include the tenant's actual Privileged Identity Management assignment or activation names if that service is used. Do not assume one activity label covers every role path.
2. Open a candidate entry. Note its time, activity name, result, correlation ID, **Initiated by** actor, target resource, role name or identifier, and changed properties where present. A failed attempt must be described differently from a successful assignment.
3. Ask the role owner to compare the actor, target, scope, duration, and approval against the change request. Check whether the actor was a permitted administrator, automation, or approved PIM workflow. If the role is assigned through a group, review the relevant group membership change as a separate evidence path.
4. If the grant is unexplained, request a separately authorized review of the new role holder's sign-ins and administrative actions. Do not remove a role, change a policy, or contact the user as a response action without the customer's authority.

**Illustrative training records only:**

| Observation | Interpretation to test | Benign control |
| --- | --- | --- |
| `Add member to role`, success, approved admin and matched ticket | Expected grant is plausible | Confirm the assigned role, scope, and expiry with the owner |
| Role assignment success with no matched approval | Change needs owner review | Check emergency-change and PIM approval records |
| Role assignment failure | Attempt seen; grant not established by that entry | Check whether an approved workflow was retried successfully later |

## What to record and explain

Store the correlation ID, UTC time, role and actor details, approval, available retention, and owner decision only in approved private case storage. A plain-language result could be: “We found a successful directory-role assignment, but its approval is not yet confirmed. The role owner needs to verify the reason, scope, and duration.” If the audit period is missing, report an inconclusive result.

Use the [hunt report template](templates/threat-hunt-report.md) for evidence and next actions. Keep real tenant, identity, and role records out of GitHub. Sources: [Microsoft Entra audit-log details](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-audit-logs), [activity names](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/reference-audit-activities), and [role-change investigation guidance](https://learn.microsoft.com/en-us/entra/architecture/security-operations-privileged-accounts).

