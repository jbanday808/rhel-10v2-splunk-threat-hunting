"""Offline network-defense unit tests; no PCAP sniffing, package installation or cloud access."""
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


pcap = load("synthetic_pcap", "scripts/network-defense/generate_synthetic_pcap.py")
summary = load("aggregate_network", "scripts/network-defense/summarize_network_logs.py")


class NetworkDefenseTests(unittest.TestCase):
    def test_packet_is_deterministic_and_ethernet_ipv4_udp_dns(self):
        data = pcap.generate_pcap()
        self.assertEqual(data, pcap.generate_pcap())
        self.assertEqual(struct.unpack_from("<I", data, 0)[0], 0xA1B2C3D4)
        self.assertEqual(struct.unpack_from("<I", data, 20)[0], 1)  # Ethernet link type
        frame_len = struct.unpack_from("<I", data, 32)[0]
        self.assertEqual(len(data), 40 + frame_len)
        frame = data[40:]
        self.assertEqual(frame[12:14], b"\x08\x00")
        self.assertEqual(frame[14] >> 4, 4)
        self.assertEqual(frame[23], 17)  # UDP
        self.assertEqual(struct.unpack_from("!H", frame, 14 + 20 + 2)[0], 53)
        self.assertIn(b"lab-marker", frame)
        self.assertIn(b"example", frame)

    def test_ipv4_header_checksum(self):
        header = pcap.create_packet()[14:34]
        self.assertEqual(pcap.checksum(header), 0)

    def test_replay_timestamp_changes_only_packet_time(self):
        original = pcap.generate_pcap()
        replay = pcap.generate_pcap(1760000000)
        self.assertEqual(struct.unpack_from("<I", replay, 24)[0], 1760000000)
        self.assertEqual(replay[:24] + replay[28:], original[:24] + original[28:])
        for invalid in (-1, 2**32):
            with self.assertRaises(ValueError):
                pcap.generate_pcap(invalid)

    def test_aggregate_suricata_events_without_raw_data(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "eve.json"
            path.write_text('{"event_type":"dns","src_ip":"192.0.2.10"}\n'
                            '{"event_type":"alert","signature":"private-test"}\n'
                            'invalid-json\n', encoding="utf-8")
            out = summary.summarize(path, "suricata")
            self.assertEqual(out["events"], 2)
            self.assertEqual(out["invalid"], 1)
            self.assertEqual(out["types"], {"dns": 1, "alert": 1})
            self.assertNotIn("private-test", json.dumps(out))

    def test_aggregate_zeek_events(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "dns.log"
            path.write_text('{"query":"lab-marker.example.test"}\n', encoding="utf-8")
            out = summary.summarize(path, "zeek")
            self.assertEqual(out["events"], 1)
            self.assertEqual(out["types"], {"zeek-json": 1})

    def test_synthetic_suricata_rule(self):
        rule = (ROOT / "configs/network-defense/suricata/local.rules").read_text()
        self.assertIn('dns.query; content:"lab-marker.example.test"', rule)
        self.assertIn("sid:1000001", rule)
        self.assertNotIn("drop dns", rule.lower())

    def test_yara_and_sigma_are_fixture_only(self):
        yara = (ROOT / "rules/yara/lab_marker.yar").read_text()
        sigma = (ROOT / "rules/sigma/lab_network_dns_marker.yml").read_text()
        self.assertIn("LAB_NETWORK_DEFENSE_FIXTURE", yara)
        self.assertIn("lab-marker.example.test", sigma)
        self.assertIn("experimental", sigma)

    def test_documents_and_original_source_are_present(self):
        for path in (
            "start-here/START_HERE_NETWORK_DEFENSE.md",
            "docs/network-defense/IMPLEMENTATION_GUIDE.md",
            "docs/network-defense/CMMC_LEVEL2.md",
            "docs/steps/README.md",
            "apps/LAB_SIEM/local/inputs.conf",
            "start-here/START_HERE_ZERO_TRUST.md",
            "start-here/START_HERE_RHEL10v2_STIG.md",
        ):
            self.assertTrue((ROOT / path).is_file(), path)


if __name__ == "__main__":
    unittest.main()
