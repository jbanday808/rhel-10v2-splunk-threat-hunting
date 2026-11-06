#!/usr/bin/env python3
"""Build a deterministic DNS request PCAP from reserved documentation IPs, offline."""
from __future__ import annotations
import argparse
import hashlib
import ipaddress
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
QUERY = "lab-marker.example.test"
SRC = "192.0.2.10"
DST = "198.51.100.53"


def checksum(raw: bytes) -> int:
    if len(raw) % 2:
        raw += b"\x00"
    numbers = struct.unpack("!" + "H" * (len(raw) // 2), raw)
    total = sum(numbers)
    while total > 65535:
        total = (total & 65535) + (total >> 16)
    return (~total) & 65535


def create_packet() -> bytes:
    labels = QUERY.encode("ascii").split(b".")
    name = b"".join(bytes([len(label)]) + label for label in labels) + b"\x00"
    dns = struct.pack("!HHHHHH", 0x4242, 0x0100, 1, 0, 0, 0) + name + struct.pack("!HH", 1, 1)
    udp = struct.pack("!HHHH", 53000, 53, len(dns) + 8, 0) + dns
    ip = struct.pack("!BBHHHBBH4s4s", 0x45, 0, len(udp) + 20, 0x1234, 0, 64, 17, 0,
                     ipaddress.IPv4Address(SRC).packed, ipaddress.IPv4Address(DST).packed)
    ip = ip[:10] + struct.pack("!H", checksum(ip)) + ip[12:]
    ethernet = bytes.fromhex("0200000000530200000000100800")
    return ethernet + ip + udp


def generate_pcap() -> bytes:
    packet = create_packet()
    global_header = struct.pack("<IHHIIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1)
    packet_header = struct.pack("<IIII", 1700000000, 0, len(packet), len(packet))
    return global_header + packet_header + packet


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        dst = args.output.expanduser().resolve()
        if dst.is_relative_to(ROOT):
            raise ValueError("Keep PCAP files outside public Git repository")
        if dst.suffix.lower() != ".pcap":
            raise ValueError("Expected .pcap output file")
        dst.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        data = generate_pcap()
        dst.write_bytes(data)
        dst.chmod(0o600)
        print("PRIVATE synthetic PCAP:", dst)
        print("Query:", QUERY, "source:", SRC, "destination:", DST)
        print("SHA-256:", hashlib.sha256(data).hexdigest())
        print("Synthetic timestamp: 2023-11-14; use earliest=0 in Splunk replay searches.")
        print("No network calls or live captures occurred.")
        return 0
    except (OSError, ValueError) as exc:
        print("PCAP generation error:", exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
