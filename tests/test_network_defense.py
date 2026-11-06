"""Offline network-defense unit tests; no PCAP sniffing, package installation or cloud access."""
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest

import dpkt

ROOT = Path(__file__).resolve().parents[1]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


pcap = load("synthetic_pcap", "scripts/network-defense/generate_synthetic_pcap.py")
summary = load("aggregate_network", "scripts/network-defense/summarize_network_logs.py")
http_fixtures = load("http_fixtures", "scripts/network-defense/generate_http_fixtures.py")


class NetworkDefenseTests(unittest.TestCase):
    def test_http_fixtures_are_reproducible_with_expected_packets_and_markers(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            captures = []
            for name in ("first", "second"):
                output = root / name
                result = subprocess.run(
                    [sys.executable, str(ROOT / "scripts/network-defense/generate_http_fixtures.py"),
                     str(output), "--start-epoch", "1760000000"],
                    capture_output=True, text=True, check=True,
                )
                self.assertIn("Wrote two synthetic captures", result.stdout)
                captures.append(output)

            for filename, expected_count in (("baseline.pcap", 33), ("investigation.pcap", 22)):
                first = (captures[0] / filename).read_bytes()
                second = (captures[1] / filename).read_bytes()
                self.assertEqual(first, second)
                with (captures[0] / filename).open("rb") as capture:
                    packets = list(dpkt.pcap.Reader(capture))
                self.assertEqual(len(packets), expected_count)

            with (captures[0] / "investigation.pcap").open("rb") as capture:
                investigation = list(dpkt.pcap.Reader(capture))
            self.assertEqual(investigation[0][0], 1760000300)
            candidate_frame = 17
            candidate_request = dpkt.ethernet.Ethernet(investigation[candidate_frame - 1][1])
            self.assertEqual(candidate_request.data.data.sport, 51005)
            self.assertIn(b"GET /downloads/review.txt HTTP/1.1", candidate_request.data.data.data)
            self.assertIn(b"Host: review.example.test", candidate_request.data.data.data)
            candidate_response = dpkt.ethernet.Ethernet(investigation[candidate_frame][1])
            self.assertIn(b"LAB_REVIEW_MARKER", candidate_response.data.data.data)
            self.assertIn(b"LAB_SYNTHETIC_HTTP_ARTIFACT", candidate_response.data.data.data)
            routine_response = dpkt.ethernet.Ethernet(investigation[6][1])
            self.assertIn(b"LAB_REVIEW_MARKER", routine_response.data.data.data)
            self.assertIn(b"Routine lab status.", routine_response.data.data.data)

    def test_http_fixture_timestamp_and_output_path_guards(self):
        script = ROOT / "scripts/network-defense/generate_http_fixtures.py"
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            last_supported_epoch = (2**32 - 1) - http_fixtures.INVESTIGATION_OFFSET - 20
            valid_output = root / "last-supported"
            valid = subprocess.run(
                [sys.executable, str(script), str(valid_output), "--start-epoch",
                 str(last_supported_epoch)],
                capture_output=True, text=True,
            )
            self.assertEqual(valid.returncode, 0, valid.stderr)
            self.assertTrue((valid_output / "investigation.pcap").is_file())

            for invalid_epoch in ("0", str(last_supported_epoch + 1)):
                output = root / f"invalid-{invalid_epoch}"
                result = subprocess.run(
                    [sys.executable, str(script), str(output), "--start-epoch", invalid_epoch],
                    capture_output=True, text=True,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("--start-epoch is outside the supported PCAP range", result.stderr)
                self.assertFalse(output.exists())

            output_in_repo = ROOT / "http-fixture-test-output"
            result = subprocess.run(
                [sys.executable, str(script), str(output_in_repo), "--start-epoch", "1760000000"],
                capture_output=True, text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Keep capture files outside the repository", result.stderr)
            self.assertFalse(output_in_repo.exists())

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
            "START_HERE_NETWORK_DEFENSE.md",
            "docs/network-defense/IMPLEMENTATION_GUIDE.md",
            "docs/network-defense/CMMC_LEVEL2.md",
            "docs/steps/README.md",
            "apps/LAB_SIEM/local/inputs.conf",
            "START_HERE_ZERO_TRUST.md",
            "START_HERE_RHEL10v2_STIG.md",
        ):
            self.assertTrue((ROOT / path).is_file(), path)


if __name__ == "__main__":
    unittest.main()
