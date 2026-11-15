# Example customer briefing: unusual lab sign-ins

**Training example only.** Every event, address, person, and decision below is fictional. This is a filled example of the [six-part briefing outline](templates/hunt-briefing.md), not a real customer report, observed lab result, or Trellix product finding. Copy the outline into approved private storage for actual work; never place customer logs here.

## 1. Purpose and decision

**Question:** “Were several failed sign-ins followed by access that the system owner cannot explain?”

**Decision requested:** The authorized system owner should confirm whether the later sign-in was expected. No account restriction or incident declaration is proposed from this example alone.

## 2. Scope and coverage

The fictional review is limited to SSH messages on one RHEL Splunk lab VM during an agreed short UTC window. The [syslog guide](SYSLOG_HUNTING_GUIDE.md) describes a possible local route into `index=linux` from `/var/log/siem-lab/linux.log`. This example assumes those records exist solely to show how to brief a result; it does **not** establish that the pipeline was tested. IdM authentication, other hosts, and network packets are outside this example's available evidence.

## 3. What the example evidence shows

| Synthetic reference | Fictional clue | What it supports |
| --- | --- | --- |
| SYN-01 | Five failed SSH attempts for `trainee-example` from documentation address `192.0.2.44`. | A short failure cluster is worth reviewing. It does not show access. |
| SYN-02 | A later accepted SSH sign-in for the same example account from `192.0.2.77`. | Access was logged from a **different** source. It does not prove the first source succeeded. |
| SYN-03 | No verified change or owner explanation has yet been attached. | The authorization question remains open; missing context is not proof of misuse. |

The [worked SSH guide](syslog-hunts/SSH_FAILURE_TO_SUCCESS.md) explains how to check the original message wording, account, source, time order, and pipeline health in an authorized lab. A forgotten password, an approved test, a shared jump host, or routine access are possible ordinary explanations. They are questions for the owner, not explanations established by these fictional records.

## 4. Impact and present action

No misuse, lateral movement, data loss, or service impact is established. No response action has been taken. The example outcome is **needs owner review** because the records alone cannot identify the person behind an account or connect the two addresses into one session.

## 5. Recommendation and tradeoff

Ask the owner to check the approved access or maintenance record for the successful sign-in. If it remains unexplained, request permission to review a wider, clearly bounded period and any separately available device or identity evidence. The benefit is a better supported answer; the tradeoff is access to more sensitive records, so the owner must approve the scope and handling location first.

## 6. Handover and next update

| Open decision | Owner in a real engagement | Evidence needed | Status in this example |
| --- | --- | --- | --- |
| Was the accepted sign-in expected? | Authorized system owner | Private event references and approved change record | Pending; synthetic exercise only |
| Is a wider review needed? | Customer incident or hunt lead | Owner's answer and available source coverage | Pending separate approval |

**Plain-language spoken update:** “The example records show repeated failed sign-ins and a later successful sign-in to the same account from another address. We cannot tell from these records whether the access was authorized or whether the failures are related. The system owner should confirm the successful access before we recommend a wider investigation.”

For a real case, capture the actual UTC window, source-health check, evidence IDs, owner acknowledgment, next update time, and private storage location in the [detailed hunt report](templates/threat-hunt-report.md). Share only a reviewed, sanitized summary outside the case team.
