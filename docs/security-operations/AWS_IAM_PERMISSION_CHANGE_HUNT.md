# Worked hunt: Who changed AWS IAM permissions?

**Status:** synthetic planning example. This repository has no validated AWS log feed into Splunk. Review real records only in an account and time period approved by its owner.

## The question and the records

**Question:** “Was this IAM permission change approved, and what access could it give?” A policy attachment may be routine maintenance. The API event documents a request; it does not by itself show what the identity subsequently did.

Confirm the account, UTC window, relevant Regions, expected change request, and IAM owner. CloudTrail **Event history** can show recent management events; it is limited to one account and Region at a time and the past 90 days. Ask whether a trail or event data store covers earlier or organization-wide activity. Check actual event fields and permissions with the owner before broadening the hunt.

## Read-only hunt steps

1. In the approved CloudTrail Event history, search a narrow time window for one change type at a time: `AttachRolePolicy`, `AttachUserPolicy`, `PutRolePolicy`, or `PutUserPolicy`. These cover different ways permissions may be attached or written; this list is illustrative, not complete.
2. Open each candidate record. Record `eventTime`, `eventID`, `eventSource`, `eventName`, actor in `userIdentity`, target role or user and policy in `requestParameters`, `sourceIPAddress`, and `errorCode` if present. Confirm whether the call succeeded. Preserve the original field names in private notes because a console summary can omit context.
3. Ask the IAM owner to compare the target, policy contents, approval, and effective permission change. A policy name alone does not prove privilege level. Check whether the actor was a human, an approved automation role, or a service process.
4. If the change lacks an explanation, request a separately authorized review of nearby IAM events and the target identity's subsequent activity. Do not remove a policy as part of the hunt without response authority.

**Illustrative training records only:**

| Record | Interpretation to test | Benign control |
| --- | --- | --- |
| `AttachRolePolicy` by `deploy-example` for `build-role-example`, matched deployment ticket | Possibly expected automation | Ask the deployment owner to confirm the ticket and policy effect |
| `PutUserPolicy` by `review-example` for `service-user-example`, no matched change | Permission change needs review | Check whether emergency maintenance was approved but recorded elsewhere |
| `AttachUserPolicy` with `AccessDenied` | Attempt, not a completed attachment | Compare with authorized testing or a misconfigured script |

## What to record and explain

Store event IDs, UTC times, account/Region coverage, policy review, change approvals, and unanswered questions in approved private case storage. A plain-language result could be: “A permission change occurred, but we have not found its approval. The account owner needs to confirm its purpose and access impact.” If the records do not cover the period, call the outcome **inconclusive**.

Use the [hunt report template](templates/threat-hunt-report.md) for evidence and owner decisions. Keep real policy text and account identifiers out of GitHub. Sources: [CloudTrail Event history coverage](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html) and [AWS's IAM policy-change event examples](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudwatch-alarms-for-cloudtrail.html).

