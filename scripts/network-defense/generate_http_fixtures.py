#!/usr/bin/env python3
"""Write two synthetic Ethernet captures without transmitting packets."""

import argparse
from ipaddress import IPv4Address
from pathlib import Path
import time

import dpkt


REPO_ROOT = Path(__file__).resolve().parents[2]
CLIENT = "192.0.2.20"
SERVER = "192.0.2.10"
RESOLVER = "192.0.2.30"
MAC = {
    CLIENT: bytes.fromhex("020000000020"),
    SERVER: bytes.fromhex("020000000010"),
    RESOLVER: bytes.fromhex("020000000030"),
}
ROUTINE = b"LAB_REVIEW_MARKER\nRoutine lab status.\n"
CANDIDATE = b"LAB_REVIEW_MARKER\nLAB_SYNTHETIC_HTTP_ARTIFACT\n"
INVESTIGATION_OFFSET = 300


def ethernet(src, dst, protocol, payload):
    ip = dpkt.ip.IP(src=IPv4Address(src).packed, dst=IPv4Address(dst).packed,
                    p=protocol, data=payload)
    return dpkt.ethernet.Ethernet(src=MAC[src], dst=MAC[dst], data=ip)


def exchange(client_port, name, path, body):
    dns = dpkt.dns
    question = dns.DNS.Q(name=name)
    query = dns.DNS(id=client_port, op=dns.DNS_RD, qd=[question])
    answer = dns.DNS(
        id=client_port, op=dns.DNS_QR | dns.DNS_RD | dns.DNS_RA, qd=[question],
        an=[dns.DNS.RR(name=name, ttl=60, ip=IPv4Address(SERVER).packed)],
    )

    def datagram(src, dst, sport, dport, message):
        payload = bytes(message)
        udp = dpkt.udp.UDP(sport=sport, dport=dport, data=payload)
        udp.ulen = len(udp)
        return ethernet(src, dst, dpkt.ip.IP_PROTO_UDP, udp)

    yield datagram(CLIENT, RESOLVER, client_port, 53, query)
    yield datagram(RESOLVER, CLIENT, 53, client_port, answer)

    request = f"GET {path} HTTP/1.1\r\nHost: {name}\r\nConnection: close\r\n\r\n".encode("ascii")
    response = (
        b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n"
        + f"Content-Length: {len(body)}\r\nConnection: close\r\n\r\n".encode("ascii")
        + body
    )
    client_seq, server_seq = 1000, 5000
    client_open, server_open = client_seq + 1, server_seq + 1
    client_end = client_open + len(request)
    server_end = server_open + len(response)

    def client(flags, seq, ack=0, data=b""):
        tcp = dpkt.tcp.TCP(
            sport=client_port, dport=80, flags=flags, seq=seq, ack=ack, data=data
        )
        return ethernet(CLIENT, SERVER, dpkt.ip.IP_PROTO_TCP, tcp)

    def server(flags, seq, ack, data=b""):
        tcp = dpkt.tcp.TCP(
            sport=80, dport=client_port, flags=flags, seq=seq, ack=ack, data=data
        )
        return ethernet(SERVER, CLIENT, dpkt.ip.IP_PROTO_TCP, tcp)

    tcp = dpkt.tcp
    yield client(tcp.TH_SYN, client_seq)
    yield server(tcp.TH_SYN | tcp.TH_ACK, server_seq, client_open)
    yield client(tcp.TH_ACK, client_open, server_open)
    yield client(tcp.TH_PUSH | tcp.TH_ACK, client_open, server_open, request)
    yield server(tcp.TH_PUSH | tcp.TH_ACK, server_open, client_end, response)
    yield client(tcp.TH_ACK, client_end, server_end)
    yield client(tcp.TH_FIN | tcp.TH_ACK, client_end, server_end)
    yield server(tcp.TH_FIN | tcp.TH_ACK, server_end, client_end + 1)
    yield client(tcp.TH_ACK, client_end + 1, server_end + 1)


def write_capture(path, start_epoch, sessions):
    with path.open("xb") as capture:
        writer = dpkt.pcap.Writer(capture)
        packet_id = 1
        for session_index, session in enumerate(sessions):
            for packet_index, packet in enumerate(exchange(*session)):
                timestamp = start_epoch + session_index * 10 + packet_index / 100
                packet.data.id = packet_id
                writer.writepkt(packet, timestamp)
                packet_id += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", type=Path, help="New private directory with an existing parent")
    parser.add_argument("--start-epoch", type=int, default=int(time.time()) - 600,
                        help="Baseline start in UTC epoch seconds")
    args = parser.parse_args()
    # Leave space for all transaction timestamps in the classic PCAP seconds field.
    last_start_epoch = (2**32 - 1) - INVESTIGATION_OFFSET - 20
    if not 1 <= args.start_epoch <= last_start_epoch:
        parser.error("--start-epoch is outside the supported PCAP range")
    try:
        output_dir = args.output_dir.expanduser().resolve()
        if output_dir.is_relative_to(REPO_ROOT):
            parser.error("Keep capture files outside the repository")
        output_dir.mkdir(mode=0o700)
    except OSError as exc:
        parser.error(str(exc))
    write_capture(output_dir / "baseline.pcap", args.start_epoch, [
        (51001, "updates.example.test", "/status", ROUTINE),
        (51002, "updates.example.test", "/downloads/review.txt", ROUTINE),
        (51003, "updates.example.test", "/status", ROUTINE),
    ])
    write_capture(output_dir / "investigation.pcap", args.start_epoch + INVESTIGATION_OFFSET, [
        (51004, "updates.example.test", "/downloads/review.txt", ROUTINE),
        (51005, "review.example.test", "/downloads/review.txt", CANDIDATE),
    ])
    print(f"Wrote two synthetic captures to {output_dir}")


if __name__ == "__main__":
    main()
