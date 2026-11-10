"""Offline network-defense unit tests; no PCAP sniffing, package installation or cloud access."""
from collections import Counter
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


pcap = load("synthetic_pcap", "scripts/network-defense/generate_synthetic_pcap.py")
summary = load("aggregate_network", "scripts/network-defense/summarize_network_logs.py")
with patch.object(sys, "path", [str(ROOT / "scripts/network-defense"), *sys.path]):
    passive = load("passive_fixtures", "scripts/network-defense/generate_passive_fixtures.py")

SURICATA = os.environ.get("SURICATA_BIN") or shutil.which("suricata")


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


class PassiveRuleTests(unittest.TestCase):
    def test_fixture_files_match_manifest_and_are_reproducible(self):
        with tempfile.TemporaryDirectory() as temp:
            first, second = Path(temp) / "first", Path(temp) / "second"
            manifest = passive.write_fixtures(first)
            self.assertEqual(manifest, passive.write_fixtures(second))
            stored = json.loads((first / "expected-alerts.json").read_text())
            for name, entry in manifest.items():
                with self.subTest(case=name):
                    data = (first / f"{name}.pcap").read_bytes()
                    self.assertEqual(data, (second / f"{name}.pcap").read_bytes())
                    self.assertEqual(hashlib.sha256(data).hexdigest(), stored[name]["sha256"])
                    position, frames = 24, 0
                    while position < len(data):
                        length = struct.unpack_from("<I", data, position + 8)[0]
                        position += 16 + length
                        frames += 1
                    self.assertEqual(position, len(data))
                    self.assertEqual(frames, entry["packets"])

    def test_fixture_writer_rejects_repo_paths_and_preserves_existing_directory(self):
        with self.assertRaisesRegex(ValueError, "outside the repository"):
            passive.write_fixtures(ROOT / "private-pcaps")
        with tempfile.TemporaryDirectory() as temp:
            existing = Path(temp) / "existing"
            existing.mkdir()
            marker = existing / "keep.txt"
            marker.write_text("keep")
            with self.assertRaises(FileExistsError):
                passive.write_fixtures(existing)
            self.assertEqual(marker.read_text(), "keep")
            self.assertEqual(list(existing.iterdir()), [marker])
            link = Path(temp) / "repository-link"
            link.symlink_to(ROOT, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "outside the repository"):
                passive.write_fixtures(link / "private-pcaps")

    def test_invalid_timestamp_does_not_create_output(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "captures"
            for timestamp in (-1, 0, 2**32):
                with self.subTest(timestamp=timestamp), self.assertRaises(ValueError):
                    passive.write_fixtures(output, timestamp)
                self.assertFalse(output.exists())

    @unittest.skipUnless(SURICATA, "Offline engine replay requires Suricata or SURICATA_BIN")
    def test_passive_rule_replay_matrix(self):
        assert SURICATA is not None
        config = ROOT / "configs/network-defense/suricata/passive-offline.yaml.example"
        rules = ROOT / "configs/network-defense/suricata/passive-review.rules"
        with tempfile.TemporaryDirectory() as temp:
            work = Path(temp)
            manifest = passive.write_fixtures(work / "captures")
            check = work / "check"
            check.mkdir()
            common = [SURICATA, "-c", str(config), "-S", str(rules)]
            result = subprocess.run(common + ["-T", "-l", str(check)],
                                    capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for name, expected in manifest.items():
                with self.subTest(case=name):
                    output = work / name
                    output.mkdir()
                    result = subprocess.run(
                        common + ["--runmode", "single", "-r", str(work / "captures" / f"{name}.pcap"),
                                  "-l", str(output)],
                        capture_output=True, text=True, timeout=30,
                    )
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    events = [json.loads(line) for line in (output / "eve.json").read_text().splitlines()]
                    actual = Counter(event["alert"]["signature_id"] for event in events
                                     if event["event_type"] == "alert")
                    self.assertEqual(dict(actual), expected["alerts"])
                    flows = [event for event in events if event["event_type"] == "flow"]
                    self.assertTrue(flows, "No flow evidence: a zero-alert replay is not a valid control")
                    protocol = "smb" if name.startswith("smb") else name.split("-", 1)[0]
                    self.assertEqual({flow.get("app_proto") for flow in flows}, {protocol})
                    processed = sum(flow["flow"]["pkts_toserver"] + flow["flow"]["pkts_toclient"]
                                    for flow in flows)
                    self.assertEqual(processed, expected["packets"])


if __name__ == "__main__":
    unittest.main()
