#!/usr/bin/env python3
"""Validate illustrative Zero Trust flow policy OFFLINE; never contacts hosts or changes firewalls."""
from __future__ import annotations
import argparse
import ipaddress
import json
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT_FILE = REPO_ROOT / "configs" / "zero-trust" / "allowed-flows.example.json"
EXPECTED_HOSTS = {
    "management_host": "172.25.250.1",
    "splunk": "172.25.250.10",
    "windows": "172.25.250.20",
    "idm": "172.25.250.30",
}
VALID_PROTOCOLS = {"tcp", "udp"}
VALID_STATUSES = {"proposed", "test_pending", "not_deployed"}


def validate(policy: dict) -> list[str]:
    errors = []
    if not isinstance(policy, dict):
        return ["Root policy must be a JSON object"]
    if policy.get("status") != "proposed_not_deployed":
        errors.append("Policy must not claim live deployment")
    try:
        net = ipaddress.ip_network(policy["subnet"], strict=True)
        if str(net) != "172.25.250.0/24":
            errors.append("Unexpected lab subnet; review before adapting")
    except (ValueError, KeyError, TypeError):
        errors.append("Missing or invalid lab subnet")
        net = ipaddress.ip_network("172.25.250.0/24")
    assets = policy.get("assets")
    if not isinstance(assets, dict):
        return errors + ["Assets must be an object"]
    if set(assets) != set(EXPECTED_HOSTS):
        errors.append("Asset names must match the known four documented lab nodes")
    for asset, expected_ip in EXPECTED_HOSTS.items():
        record = assets.get(asset)
        if not isinstance(record, dict) or record.get("address") != expected_ip:
            errors.append(f"Unexpected/missing IP for {asset}")
            continue
        try:
            if ipaddress.ip_address(record["address"]) not in net:
                errors.append(f"Asset {asset} falls outside lab subnet")
        except ValueError:
            errors.append(f"Invalid IP for {asset}")
    allowed = policy.get("allowed_flows")
    if not isinstance(allowed, list) or not allowed:
        return errors + ["allowed_flows must be a nonempty list"]
    ids, tuples = set(), set()
    for i, flow in enumerate(allowed, 1):
        if not isinstance(flow, dict):
            errors.append(f"Flow {i} is not an object")
            continue
        ident = flow.get("id")
        if not isinstance(ident, str) or not ident:
            errors.append(f"Flow {i} missing ID")
        elif ident in ids:
            errors.append(f"Duplicate flow ID: {ident}")
        ids.add(ident)
        src, dst = flow.get("source"), flow.get("destination")
        proto, port = flow.get("protocol"), flow.get("port")
        if src not in EXPECTED_HOSTS or dst not in EXPECTED_HOSTS or src == dst:
            errors.append(f"Flow {i} uses invalid source/destination")
        if proto not in VALID_PROTOCOLS:
            errors.append(f"Flow {i} has invalid protocol")
        if type(port) is not int or not (1 <= port <= 65535):
            errors.append(f"Flow {i} has invalid port")
            continue
        if port == 8089:
            errors.append(f"Flow {i} must not expose Splunk management 8089")
        key = (src, dst, proto, port)
        if key in tuples:
            errors.append(f"Duplicate flow: {key}")
        tuples.add(key)
        if flow.get("status") != "proposed":
            errors.append(f"Flow {i} must be proposed, not already deployed")
        if not str(flow.get("purpose", "")).strip():
            errors.append(f"Flow {i} needs a clear service purpose")
    denied = policy.get("denied_examples")
    if not isinstance(denied, list):
        errors.append("denied_examples must be a list")
    else:
        for i, flow in enumerate(denied, 1):
            if not isinstance(flow, dict):
                errors.append(f"Denied example {i} is not an object")
                continue
            src, dst, proto, port = (
                flow.get("source"), flow.get("destination"),
                flow.get("protocol"), flow.get("port"),
            )
            if src not in EXPECTED_HOSTS or dst not in EXPECTED_HOSTS:
                errors.append(f"Denied example {i} has unknown asset")
            if proto not in VALID_PROTOCOLS or type(port) is not int:
                errors.append(f"Denied example {i} has invalid protocol/port")
            if (src, dst, proto, port) in tuples:
                errors.append(f"Denied example {i} conflicts with allowed flows")
            if flow.get("status") not in VALID_STATUSES:
                errors.append(f"Denied example {i} must be non-deployed")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("policy", nargs="?", type=pathlib.Path, default=DEFAULT_FILE)
    args = parser.parse_args()
    try:
        document = json.loads(args.policy.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"POLICY INVALID: cannot read JSON: {exc}", file=sys.stderr)
        return 2
    errors = validate(document)
    if errors:
        for err in errors:
            print(f"POLICY INVALID: {err}", file=sys.stderr)
        return 1
    print(
        "POLICY SOURCE VALID (offline only): "
        f"{len(document['allowed_flows'])} proposed allowed flows and "
        f"{len(document['denied_examples'])} denial examples. "
        "No firewall changes or live tests performed."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
