# Can the optional sensor see the traffic it is meant to hunt?

**Status:** proposed acceptance exercise for the owned VMware Workstation Pro lab. No live mirror, packet capture, or sensor coverage is claimed here. The core VMs remain RHEL-SPLUNK01 (`172.25.250.10`), WINHUNT01 (`.20`), and RHEL-IDM01 (`.30`) on VMnet8. The optional RHEL-SENSOR01 (`.40`, only after an address check) or Kali VM is an analysis machine, not automatically a mirror.

## The question

Before using Zeek, Suricata, Wireshark, or Arkime to hunt between the VMs, ask: **“Did the proposed capture point actually see this approved conversation, in both directions?”** VMnet8 supplies NAT and ordinary switching. A promiscuous interface alone may miss unicast between other virtual machines. The [network architecture](ARCHITECTURE.md) explains the proposed mirror or TAP boundary.

## Choose one harmless, known conversation

1. Ask the VM owners to approve one existing, low-volume connection between two named lab VMs and a short UTC test window. Use a service they already expect; this guide does not enable a port or create a new listener.
2. Record the expected source, destination, transport, port, and approximate time in **private** test notes. Capture a small reference from an endpoint or its approved service log. Record the selected interface and direction. Do not copy packets or log content to GitHub.
3. During the same window, capture only on the approved optional sensor or Kali interface. A separate mirror/TAP design needs its own owner approval and configuration review; do not change VMnet8 to make a test pass.
4. In Wireshark, filter the private capture to the two test addresses, for example `ip.addr == 172.25.250.10 && ip.addr == 172.25.250.20`. Narrow further to the agreed protocol and port. Compare packet timestamps, addresses, ports, direction, and unique transaction context with the endpoint reference. A matching IP pair alone is insufficient.
5. Check packet drops, capture duration, clock agreement, and whether request **and** response were visible. Repeat with a second approved peer pair before describing coverage beyond the first conversation.

**Command overview:** the Wireshark filter shows packets involving both example VM addresses; it does not generate traffic. **Expected testable result:** a documented mirror shows the selected conversation in both directions, with matching context and no unexplained gap. If a sensor sees only its own traffic, or only one side of the conversation, report partial visibility. A zero-packet result cannot establish that the peers were quiet.

| Control | What it checks | Correct interpretation |
| --- | --- | --- |
| Approved peer conversation | Positive case for a verified capture path | Match the endpoint reference and both directions before accepting that path. |
| Sensor's own management traffic | Benign control | Its presence proves the interface works, **not** that peer traffic is mirrored. |
| A different peer, port, or earlier session | Nonmatching control | Do not count it as the selected test merely because the IP or time is similar. |

## Record a narrow result

Use the [network validation worksheet](../../evidence/sanitized/network-defense-validation.md) to record the approved scope, interface/mirror path, UTC window, reference and sensor capture hashes, matching packet/flow references, packet-loss checks, and owner decision. Keep the PCAPs in approved private storage. A successful test for one pair does not prove network-wide visibility, TLS content access, or threat detection. A failed test is a capture-placement question to resolve before promoting a Zeek, Suricata, or Arkime hunt.

**Plain-language update:** “We checked whether the monitoring point could see a known lab connection. Until we verify the right traffic reaches it, an empty alert list does not tell us the network is safe.”
