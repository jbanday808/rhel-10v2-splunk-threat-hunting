#!/usr/bin/env python3
"""Build a deterministic DNS request PCAP from documentation or lab IPs, offline."""
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
LAB_SRC = "172.25.250.20"
LAB_DST = "172.25.250.30"
LAB_LONG_QUERY = "a" * 50 + ".lab.test"
DEFAULT_TIMESTAMP = 1700000000


def checksum(raw: bytes) -> int:
    if len(raw) % 2:
        raw += b"\x00"
    numbers = struct.unpack("!" + "H" * (len(raw) // 2), raw)
    total = sum(numbers)
    while total > 65535:
        total = (total & 65535) + (total >> 16)
    return (~total) & 65535


def create_packet(src: str = SRC, dst: str = DST, long_label: bool = False) -> bytes:
    query = LAB_LONG_QUERY if long_label else QUERY
    labels = query.encode("ascii").split(b".")
    name = b"".join(bytes([len(label)]) + label for label in labels) + b"\x00"
    dns = struct.pack("!HHHHHH", 0x4242, 0x0100, 1, 0, 0, 0) + name + struct.pack("!HH", 1, 1)
    udp = struct.pack("!HHHH", 53000, 53, len(dns) + 8, 0) + dns
    ip = struct.pack("!BBHHHBBH4s4s", 0x45, 0, len(udp) + 20, 0x1234, 0, 64, 17, 0,
                     ipaddress.IPv4Address(src).packed, ipaddress.IPv4Address(dst).packed)
    ip = ip[:10] + struct.pack("!H", checksum(ip)) + ip[12:]
    ethernet = bytes.fromhex("0200000000530200000000100800")
    return ethernet + ip + udp


def generate_pcap(timestamp: int = DEFAULT_TIMESTAMP, *, lab_addresses: bool = False,
                  long_label: bool = False) -> bytes:
    if not 0 <= timestamp <= 0xFFFFFFFF:
        raise ValueError("Timestamp must fit the PCAP seconds field")
    src, dst = (LAB_SRC, LAB_DST) if lab_addresses else (SRC, DST)
    packet = create_packet(src, dst, long_label)
    global_header = struct.pack("<IHHIIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1)
    packet_header = struct.pack("<IIII", timestamp, 0, len(packet), len(packet))
    return global_header + packet_header + packet


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--timestamp", type=int, default=DEFAULT_TIMESTAMP,
                        help="Capture time in UTC epoch seconds. Default is fixed for regression tests.")
    parser.add_argument("--lab-addresses", action="store_true",
                        help="Use synthetic WINHUNT01-to-IdM addresses within 172.25.250.0/24")
    parser.add_argument("--long-label", action="store_true",
                        help="Use a synthetic 50-character first DNS label (requires --lab-addresses)")
    args = parser.parse_args()
    if args.long_label and not args.lab_addresses:
        parser.error("--long-label requires --lab-addresses")
    try:
        dst = args.output.expanduser().resolve()
        if dst.is_relative_to(ROOT):
            raise ValueError("Keep PCAP files outside public Git repository")
        if dst.suffix.lower() != ".pcap":
            raise ValueError("Expected .pcap output file")
        dst.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        data = generate_pcap(args.timestamp, lab_addresses=args.lab_addresses,
                             long_label=args.long_label)
        dst.write_bytes(data)
        dst.chmod(0o600)
        src_ip, dst_ip = (LAB_SRC, LAB_DST) if args.lab_addresses else (SRC, DST)
        query = LAB_LONG_QUERY if args.long_label else QUERY
        print("PRIVATE synthetic PCAP:", dst)
        print("Query:", query, "source:", src_ip, "destination:", dst_ip)
        print("SHA-256:", hashlib.sha256(data).hexdigest())
        print("Synthetic timestamp (UTC epoch seconds):", args.timestamp)
        print("No network calls or live captures occurred.")
        return 0
    except (OSError, ValueError) as exc:
        print("PCAP generation error:", exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
