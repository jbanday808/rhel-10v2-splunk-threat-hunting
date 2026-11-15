# Worked hunt: Was a new AWS IAM user expected?

**Status:** synthetic planning example. AWS events are not being sent to the six Splunk indexes in this repository. Use this guide only with the cloud owner's permission and actual records; it does not show a completed hunt.

## The question and the records

**Question:** “Did someone create a new IAM user outside the approved account setup process?” A new user can be a normal onboarding step. The event alone does not show misuse.

Agree on the AWS account, UTC time window, authorized reviewer, and expected change record. In the AWS CloudTrail console, **Event history** shows recent management events for one account and Region. Ask the owner which Regions and longer-term trails or event data stores must be checked. Event history is limited to the past 90 days and does not include data events. No cloud-to-Splunk connection is configured by this repository.

## Read-only hunt steps

1. Open the approved account's CloudTrail **Event history** for the agreed time window. Filter **Event name** to `CreateUser` and review the result in each relevant Region. Keep a private note of the account and Region searched, including any gaps.
2. Open each candidate's event details. Check `eventTime`, `eventID`, `eventSource` (`iam.amazonaws.com`), `eventName`, `userIdentity`, `requestParameters.userName`, `sourceIPAddress`, and any `errorCode`. Field presence and nesting depend on the actual event; confirm them in the original record.
3. Separate successful creation from denied or failed attempts. Compare the actor, created username, time, and change request with the account owner's authorized onboarding list.
4. If the creation is unexplained, ask the owner to review related IAM changes and later use of the new identity using records that are actually available. Do not disable the identity or change permissions without response authority.

**Illustrative training records only:**

| Record | What it might mean | Next check |
| --- | --- | --- |
| `CreateUser`, success, actor `onboarding-example`, user `trainee-example`, approved change | Expected setup is plausible | Confirm the change record and owner |
| `CreateUser`, success, actor `unknown-example`, user `review-example`, no matched change | Needs review, not proof of an attack | Confirm the actor with the account owner and inspect available follow-on events |
| `CreateUser`, `AccessDenied` | Attempted change, not a created user | Check whether the attempt was a permitted test or misconfiguration |

## What to record and explain

In approved private case storage, keep the search scope, CloudTrail event IDs, UTC times, change approvals, any missing Regions or older records, and the owner's interpretation. A concise briefing is: “We found a user-creation event without a matched change record. We have asked the account owner to confirm it; the event alone does not establish unauthorized use.” If no events appear, report the coverage and retention checked rather than saying no account was created.

For a full case record, use the [hunt report template](templates/threat-hunt-report.md). Keep real identifiers and exported events out of GitHub. [AWS CloudTrail Event history limits](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html) and [AWS's `CreateUser` event example](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-examples.html) explain the source fields and coverage.

