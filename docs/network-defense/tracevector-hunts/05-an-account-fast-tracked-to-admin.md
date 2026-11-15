# An account fast-tracked to admin: follow the account SID

The synthetic exercise creates a Windows account at 18:10 and adds it to an Administrators group eight minutes later. It also includes an unrelated member and a later group addition that the one-hour training rule excludes. Correlation depends on the **account SID**, not a matching actor name. [Open the exercise](https://tracevector.jamesbanday.chatgpt.site/#scenarios).

## Evidence to look for

Use the existing `win_security` index and the [account-to-group hunt](../../../hunts/mitre-attack/03-account-to-group.spl). Windows Security Event 4720 identifies the newly created account in `TargetSid`; Event 4732 identifies the added account in `MemberSid` while its `TargetSid` is the **group**. Confirm those fields, `SubjectUserName`, group name/SID, host, `_time`, and the original event text before joining records. Check that auditing and forwarding deliver both event types.

The Site's `target_sid`, `member_sid`, and parsed `time` are fixture fields. The documented lab is not domain-joined, so identify whether the real account and group are local before using the T1136.001/T1098.007 mapping. Group names can be renamed or localized; confirm the group's SID and actual privileges rather than trusting its display name.

## Validate the relationship

1. Scope one authorized Windows lab host and a short change window. Review raw 4720 and 4732 records before using the one-hour search.
2. A documented, approved addition to a standard-user group is the benign control. It should demonstrate that a group change alone is not an admin grant.
3. If the owner has an approved local-account onboarding event, verify the 4720 `TargetSid` equals the later 4732 `MemberSid`, then confirm the destination group and approval. Preserve both records privately. Do not create a privileged account solely to produce a match.

An administrator can legitimately onboard an account; missing 4720 events, delayed forwarding, equal timestamps, or a lookback boundary can break a real correlation. The search does not prove the new account logged in or that the change was hostile.

**Plain-language next step:** “A new account was added to a group. Confirm the group’s privileges and the approved request before treating it as unauthorized access.”
