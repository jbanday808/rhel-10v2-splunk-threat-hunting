# Worked hunt: Was an unusual Microsoft Entra sign-in expected?

**Status:** synthetic planning example. The repository's Azure sign-in example for GitHub Actions does not collect Microsoft Entra sign-in logs into Splunk. Confirm actual tenant access, retention, and record availability with its owner before using this guide.

## The question and the records

**Question:** “Does this sign-in need the account owner's review?” A new location, device, or application can be ordinary travel, a VPN, or a new work assignment. Location inferred from an IP address is approximate and cannot prove where a person was.

Agree on the tenant, user or small group, UTC window, permitted reviewer, and normal comparison period. In the Microsoft Entra admin center, use **Monitoring & health → Sign-in logs** with an approved read-only role. The portal displays times in the signed-in reviewer's time zone, so convert the agreed UTC window before filtering and record both zones. Check whether the relevant interactive or noninteractive records exist and whether licensing or retention limits hide needed details. No current Splunk index in this lab is designated for cloud sign-in data.

## Read-only hunt steps

1. Filter to the approved user and time window. Compare **Status**, **Application**, **Resource**, **IP address**, and available device and authentication details. The aim is to explain a specific lead, not to label every unfamiliar IP address suspicious.
2. Open the event and record its request ID, correlation ID, time, user, application, status, failure reason if any, and available authentication details. Check whether a successful request followed failures and whether the same session generated multiple records.
3. Compare with the user's known work pattern and ask the identity owner about travel, VPN egress, approved applications, password resets, and authorized testing. Check Conditional Access details where available; a status of “Success” there does not always mean every policy applied.
4. If the account owner cannot explain a successful event, request a separately approved review of other sign-ins and device or account activity. Do not reset credentials or revoke sessions without response authority.

**Illustrative training records only:**

| Observation | Interpretation to test | Ordinary explanation to check |
| --- | --- | --- |
| Several failures followed by a success for `learner@example.invalid` | Possible account misuse or a recovered login | User corrected a forgotten password |
| Successful sign-in from a new IP address | New network context needs review | Corporate VPN or mobile carrier exit point |
| Failed sign-in with no later success in the searched period | Attempt observed; access not established by that record | Outdated saved password in an approved app |

## What to record and explain

In approved private case storage, record the tenant and time coverage, request/correlation IDs, account-owner explanation, normal comparison, and missing data. A plain-language result could be: “The account had an unfamiliar successful sign-in after failures. We are checking with the owner and have not yet established whether it was expected.” A missing log or limited retention is a coverage gap, not evidence of safety.

Use the [hunt report template](templates/threat-hunt-report.md) for the decision and evidence register. Keep real user records and IP addresses out of GitHub. Sources: [Microsoft Entra sign-in log details](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-sign-in-log-activity-details) and [log filtering](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/howto-customize-filter-logs).

