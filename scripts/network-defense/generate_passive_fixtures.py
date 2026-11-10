#!/usr/bin/env python3
"""Write synthetic passive-rule controls to private PCAPs; never transmit packets."""
from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
from pathlib import Path
import struct
import sys

from generate_synthetic_pcap import checksum

ROOT = Path(__file__).resolve().parents[2]
CLIENT = "192.0.2.20"
SERVER = "192.0.2.10"
RESOLVER = "192.0.2.30"
EXTERNAL = "198.51.100.10"
DEFAULT_TIMESTAMP = 1794268800


def frame(src: str, dst: str, protocol: int, payload: bytes) -> bytes:
    source, destination = ipaddress.IPv4Address(src).packed, ipaddress.IPv4Address(dst).packed
    pseudo = source + destination + struct.pack("!BBH", 0, protocol, len(payload))
    offset = 16 if protocol == 6 else 6
    check = checksum(pseudo + payload) or 0xFFFF
    payload = payload[:offset] + struct.pack("!H", check) + payload[offset + 2:]
    header = struct.pack("!BBHHHBBH4s4s", 0x45, 0, 20 + len(payload), 1, 0,
                         64, protocol, 0, source, destination)
    header = header[:10] + struct.pack("!H", checksum(header)) + header[12:]
    return bytes.fromhex("0200000000100200000000200800") + header + payload


def tcp_session(request: bytes, response: bytes, port: int, server: str = SERVER,
                split_response: int = 0) -> list[tuple[float, bytes]]:
    packets = []

    def add(to_server, flags, seq, ack=0, data=b""):
        src, dst = (CLIENT, server) if to_server else (server, CLIENT)
        sport, dport = (51000, port) if to_server else (port, 51000)
        segment = struct.pack("!HHIIBBHHH", sport, dport, seq, ack, 0x50, flags, 8192, 0, 0)
        packets.append((len(packets) / 100, frame(src, dst, 6, segment + data)))

    client, peer = 1001, 5001
    add(True, 0x02, client - 1)
    add(False, 0x12, peer - 1, client)
    add(True, 0x10, client, peer)
    add(True, 0x18, client, peer, request)
    client += len(request)
    chunks = [response[:split_response], response[split_response:]] if split_response else [response]
    for chunk in chunks:
        add(False, 0x18, peer, client, chunk)
        peer += len(chunk)
    add(True, 0x10, client, peer)
    add(True, 0x11, client, peer)
    add(False, 0x11, peer, client + 1)
    add(True, 0x10, client + 1, peer + 1)
    return packets


def dns_message(label: str, identifier: int = 1) -> bytes:
    name = ".".join((label, "example", "test")).encode("ascii")
    wire = b"".join(bytes([len(part)]) + part for part in name.split(b".")) + b"\x00"
    return struct.pack("!HHHHHH", identifier, 0x0100, 1, 0, 0, 0) + wire + struct.pack("!HH", 1, 1)


def dns_queries(label: str = "status", count: int = 1, resolver: str = RESOLVER,
                interval: int = 1, sources: tuple[str, ...] = (CLIENT,)) -> list[tuple[float, bytes]]:
    packets = []
    for index in range(count):
        message = dns_message(label, index + 1)
        udp = struct.pack("!HHHH", 53000 + index, 53, 8 + len(message), 0) + message
        packets.append((index * interval, frame(sources[index % len(sources)], resolver, 17, udp)))
    return packets


def http_request(header: bytes = b"", method: bytes = b"GET") -> list[tuple[float, bytes]]:
    request = method + b" /status HTTP/1.1\r\nHost: updates.example.test\r\n" + header + b"\r\n"
    return tcp_session(request, b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n", 80)


def tls_hello(version: int, server: bool = False, record_version: int = 0x0301) -> bytes:
    body = struct.pack("!H", min(version, 0x0303)) + b"\x11" * 32 + b"\x00"
    if server:
        body += struct.pack("!H", 0x1301 if version == 0x0304 else 0x002F) + b"\x00"
        extensions = struct.pack("!HHH", 43, 2, version) if version == 0x0304 else b""
    else:
        body += b"\x00\x04\x00\x2f\x13\x01\x01\x00"
        extensions = (b"\x00\x2b\x00\x09\x08\x03\x04\x03\x03\x03\x02\x03\x01"
                      if version >= 0x0303 else b"")
    body += struct.pack("!H", len(extensions)) + extensions
    handshake = bytes([2 if server else 1]) + len(body).to_bytes(3, "big") + body
    return struct.pack("!BHH", 22, record_version, len(handshake)) + handshake


def smb1(command: int = 0x2B, response: bool = False) -> bytes:
    header = (b"\xffSMB" + bytes([command]) + bytes(4) + bytes([0x98 if response else 0x18])
              + struct.pack("<H", 1) + bytes(12) + struct.pack("<HHHH", 0, 1, 0, 1))
    if command == 0x72:
        dialects = b"\x02NT LM 0.12\x00\x02SMB 2.002\x00"
        body = b"\x00" + struct.pack("<H", len(dialects)) + dialects
    else:
        body = b"\x01\x01\x00\x03\x00LAB"
    message = header + body
    return b"\x00" + len(message).to_bytes(3, "big") + message


def smb2(response: bool = False) -> bytes:
    header = b"\xfeSMB" + struct.pack("<HHIHHIIQIIQ16s", 64, 0, 0, 0, 1,
                                     int(response), 0, 1, 1, 0, 0, bytes(16))
    if response:
        body = struct.pack("<HHHH16sIIIIQQHHI", 65, 1, 0x0202, 0, bytes(16),
                           0, 65536, 65536, 65536, 0, 0, 0, 0, 0)
    else:
        body = struct.pack("<HHHHI16sIHHH", 36, 1, 1, 0, 0, bytes(16), 0, 0, 0, 0x0202)
    message = header + body
    return b"\x00" + len(message).to_bytes(3, "big") + message


def rdp(selected: int, response: bool = True, failure: bool = False) -> bytes:
    header = b"\x03\x00\x00\x13\x0e" + bytes([0xD0 if response else 0xE0]) + bytes(5)
    return header + struct.pack("<BBHI", 3 if failure else (2 if response else 1), 0, 8, selected)


def cases() -> dict[str, tuple[dict[int, int], list[tuple[float, bytes]]]]:
    question = dns_message("status")
    answer = question[:2] + b"\x81\x80" + question[4:]
    tcp_query = struct.pack("!H", len(question)) + question
    tcp_answer = struct.pack("!H", len(answer)) + answer
    result = {
        "dns-unapproved": ({1002001: 1}, dns_queries(resolver=EXTERNAL)),
        "dns-approved": ({}, dns_queries()),
        "dns-tcp-unapproved": ({1002001: 1}, tcp_session(tcp_query, tcp_answer, 53, EXTERNAL)),
        "dns-tcp-approved": ({}, tcp_session(tcp_query, tcp_answer, 53, RESOLVER)),
        "dns-long-five": ({1002002: 1}, dns_queries("a" * 50, 5)),
        "dns-long-four": ({}, dns_queries("a" * 50, 4)),
        "dns-label-49": ({}, dns_queries("a" * 49, 5)),
        "dns-label-63": ({1002002: 1}, dns_queries("a" * 63, 5)),
        "dns-long-spaced": ({}, dns_queries("a" * 50, 5, interval=61)),
        "dns-separate-sources": ({}, dns_queries("a" * 50, 8, sources=(CLIENT, "192.0.2.21"))),
        "http-basic": ({1002003: 1}, http_request(b"Authorization: Basic REPLACE_SYNTHETIC_VALUE\r\n")),
        "http-basic-whitespace": ({1002003: 1}, http_request(b"aUtHoRiZaTiOn:\tBasic\tREPLACE_SYNTHETIC_VALUE\r\n")),
        "http-proxy-basic": ({1002004: 1}, http_request(b"Proxy-Authorization: Basic REPLACE_SYNTHETIC_VALUE\r\n")),
        "http-bearer": ({}, http_request(b"Authorization: Bearer REPLACE_SYNTHETIC_VALUE\r\n")),
        "http-empty-basic": ({}, http_request(b"Authorization: Basic \r\n")),
        "http-unrelated-header": ({}, http_request(b"X-Note: Authorization: Basic REPLACE_SYNTHETIC_VALUE\r\n")),
        "http-trace": ({1002005: 1}, http_request(method=b"TRACE")),
        "http-get": ({}, http_request()),
        "smb1-command": ({1002008: 1}, tcp_session(smb1(), smb1(response=True), 445)),
        "smb1-negotiate-smb2": ({}, tcp_session(smb1(0x72), smb2(response=True), 445)),
        "smb2-internal": ({}, tcp_session(smb2(), smb2(response=True), 445)),
        "smb2-external": ({1002009: 1}, tcp_session(smb2(), smb2(response=True), 445, EXTERNAL)),
        "rdp-standard": ({1002010: 1}, tcp_session(rdp(11, response=False), rdp(0), 3389)),
        "rdp-tls-only": ({1002011: 1}, tcp_session(rdp(11, response=False), rdp(1), 3389)),
        "rdp-credssp": ({}, tcp_session(rdp(11, response=False), rdp(2), 3389)),
        "rdp-credssp-ex": ({}, tcp_session(rdp(11, response=False), rdp(8), 3389)),
        "rdp-failure": ({}, tcp_session(rdp(11, response=False), rdp(1, failure=True), 3389)),
        "rdp-client-offer": ({}, tcp_session(rdp(0, response=False), rdp(2), 3389)),
        "rdp-segmented": ({1002010: 1}, tcp_session(rdp(11, response=False), rdp(0), 3389, split_response=2)),
        "rdp-external": ({1002012: 1}, tcp_session(rdp(11, response=False), rdp(2), 3389, EXTERNAL)),
    }
    for minor, sid in ((1, 1002006), (2, 1002007), (3, None), (4, None)):
        alerts = {sid: 1} if sid is not None else {}
        result[f"tls-1-{minor - 1}"] = (
            alerts, tcp_session(tls_hello(0x0303), tls_hello(0x0300 + minor, server=True), 443)
        )
    result["tls-client-legacy-rejected"] = (
        {}, tcp_session(tls_hello(0x0301), b"\x15\x03\x01\x00\x02\x02\x46", 443)
    )
    return result


def capture_bytes(packets: list[tuple[float, bytes]], start_epoch: int) -> bytes:
    if not 1 <= start_epoch <= 0xFFFFFFFF - 600:
        raise ValueError("Start time is outside the supported PCAP range")
    data = bytearray(struct.pack("<IHHIIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1))
    for offset, packet in packets:
        micros = round(offset * 1_000_000)
        seconds, fraction = divmod(micros, 1_000_000)
        data.extend(struct.pack("<IIII", start_epoch + seconds, fraction, len(packet), len(packet)))
        data.extend(packet)
    return bytes(data)


def write_fixtures(output_dir: Path, start_epoch: int = DEFAULT_TIMESTAMP) -> dict:
    output_dir = output_dir.expanduser().resolve()
    if output_dir.is_relative_to(ROOT):
        raise ValueError("Keep capture files outside the repository")
    fixtures = {name: (alerts, packets, capture_bytes(packets, start_epoch))
                for name, (alerts, packets) in cases().items()}
    output_dir.mkdir(mode=0o700)
    manifest = {}
    for name, (alerts, packets, data) in fixtures.items():
        path = output_dir / f"{name}.pcap"
        with path.open("xb") as capture:
            path.chmod(0o600)
            capture.write(data)
        manifest[name] = {"alerts": alerts, "packets": len(packets),
                          "sha256": hashlib.sha256(data).hexdigest()}
    manifest_path = output_dir / "expected-alerts.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    manifest_path.chmod(0o600)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", type=Path, help="New private directory with an existing parent")
    parser.add_argument("--start-epoch", type=int, default=DEFAULT_TIMESTAMP,
                        help="Fixed UTC epoch seconds for reproducible regression captures")
    args = parser.parse_args()
    try:
        manifest = write_fixtures(args.output_dir, args.start_epoch)
    except (OSError, ValueError) as exc:
        print(f"Fixture generation error: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote {len(manifest)} synthetic captures and expected-alerts.json to {args.output_dir}")
    print("No network calls or live captures occurred.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
