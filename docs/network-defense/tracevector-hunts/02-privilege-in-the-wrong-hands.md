# Privilege in the wrong hands: review sudo use

TraceVector's made-up trail shows an approved service-status check, an unexpected `sudo` shell, and a denied request. The concern is the **allowed** root shell by an account that the exercise says has no administrative role. [Open the exercise](https://tracevector.jamesbanday.chatgpt.site/#scenarios).

## Where the lab might see it

Look in the existing `linux` index for local authentication-facility `sudo` messages from the RHEL Splunk VM. The [syslog review search](../../../hunts/linux/01-syslog-review.spl) and [syslog guide](../../security-operations/SYSLOG_HUNTING_GUIDE.md) show the configured source. The Site's `process=sudo`, `action=allowed`, `user`, `run_as`, and `command` are training fields; check the original message before assuming Splunk extracts them.

For each candidate, identify the requesting account, target account (`root` in the example), command, host, timestamp, terminal/session if present, and whether the request succeeded or was denied. A denied request does not prove privileged execution. A `sudo` message may show the command request but not every action inside an interactive shell; separately approved audit or process records would be needed for that detail. The repository does not claim those records are collected.

## A controlled review

1. Confirm that both a known allowed and a known denied `sudo` record reach the configured file and `linux` index. Use a prearranged, harmless service-status command in the isolated lab only if the owner authorizes it.
2. Treat that approved status check as the benign control: the actor, command, and time should match the change plan. Compare it with any shell invocation, keeping requesting and target identities separate.
3. Ask the host owner to review the account's current sudo policy and the approval trail. Preserve the raw event and any available session evidence privately before proposing a policy change.

Routine administration, emergency maintenance, and stale documentation can explain a surprising command. Conversely, missing `sudo` logs or shell-level activity limits what this source can establish. The [ATT&CK mapping](../../mitre-attack/coverage.md) treats T1548.003 as a hypothesis, not a verdict.

**Plain-language next step:** “This account received elevated access. Please confirm who approved it and whether the command was part of planned work.” Document a narrowly scoped policy review; do not change the host from this guide.
