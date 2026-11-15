# One source, several accounts: test a spray hypothesis

TraceVector's made-up Windows failures target three distinct domain/account pairs in the same 15-minute bucket. One account repeats, a loopback event is excluded, and a later event falls in the next bucket. The exercise's threshold is **three**; the repository's candidate hunt uses **five** and needs tuning for the real environment. [Open the exercise](https://tracevector.jamesbanday.chatgpt.site/#scenarios).

## Read the identity records first

Use the existing `win_security` index for Event 4625 and the [multiple-account-failures hunt](../../../hunts/mitre-attack/07-multiple-account-failures.spl). Confirm `EventCode`/`EventID`, `IpAddress` or equivalent, `TargetUserName`, `TargetDomainName`, host, `_time`, status/substatus, and the original event. Combine domain **and** account when counting distinct identities; the same username can mean different identities in different namespaces. The lab is not domain-joined, so the Site's `LAB` and `DEV` labels are training examples, not lab directory telemetry.

Check which failures carry a usable remote address. Loopback, blank, or placeholder source values cannot support a reliable one-source count. Fixed 15-minute buckets can split activity at a boundary. Security 4625 does not reveal the password attempted, so even a strong multi-account pattern cannot prove that one password was sprayed.

## Validate the query and its control

1. Confirm recent 4625 events arrive for the Windows lab host and that their account/domain and source fields are extracted correctly.
2. Use the Site fixture to check the intended grouping, then review a short authorized lab window. A documented service with a stale password repeatedly failing for **one** account is the benign control: it may create many failures but should not satisfy a distinct-account rule.
3. If several identities do appear from one source, check approved testing, device ownership, status codes, and any later 4624 successes without assuming a shared password or compromise. Preserve the raw records privately.

Small labs, NAT/shared addresses, a missing domain, and collection delay can distort the count. Neither a match nor an empty result is a verdict. The [coverage map](../../mitre-attack/coverage.md) treats T1110.003 as a candidate.

**Plain-language next step:** “One source tried several accounts. Confirm whether it belongs to an approved device or test, then check whether any access succeeded.”
