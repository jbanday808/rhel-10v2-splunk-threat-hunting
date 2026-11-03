"""Run the sender with a fake curl; do not contact a HEC listener."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
DUMMY_TOKEN = '00000000-0000-0000-0000-000000000000'


@unittest.skipUnless(shutil.which('bash'), 'Bash is required for sender tests')
class HecSender(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        (self.work / 'ca.pem').write_text('Dummy CA fixture; fake curl performs no TLS handshake.\n')
        fake = self.work / 'curl'
        fake.write_text('''#!/usr/bin/env python3
import json, os, pathlib, stat, sys
args = sys.argv[1:]
assert '--cacert' in args and '--fail-with-body' in args
assert '--insecure' not in args and '-k' not in args
assert args[-1] == 'https://172.25.250.10:8088/services/collector'
header = pathlib.Path(args[args.index('--header') + 1][1:])
payload = pathlib.Path(args[args.index('--data-binary') + 1][1:])
assert stat.S_IMODE(header.stat().st_mode) == 0o600
assert stat.S_IMODE(header.parent.stat().st_mode) == 0o700
assert header.read_text().startswith('Authorization: Splunk 00000000-0000-0000-0000-000000000000\\n')
data = json.loads(payload.read_text())
assert data['index'] == 'lab' and data['sourcetype'] == 'siem:hec'
assert 'SIEM-LAB-HEC-' in data['event']
pathlib.Path(os.environ['CAPTURE_PATH']).write_text(str(header.parent))
print(json.dumps({'text': 'Success', 'code': int(os.environ.get('MOCK_HEC_CODE', '0'))}))
''')
        fake.chmod(0o755)
        self.env = dict(os.environ, CA_FILE=str(self.work / 'ca.pem'),
                        HEC_URL='https://172.25.250.10:8088/services/collector',
                        PATH=str(self.work) + os.pathsep + os.environ['PATH'],
                        CAPTURE_PATH=str(self.work / 'capture.txt'))

    def send(self, token=DUMMY_TOKEN):
        return subprocess.run(['bash', str(ROOT / 'scripts/rhel/send-hec-event.sh')],
                              input=token + '\n', text=True, capture_output=True, env=self.env)

    def test_acceptance_and_private_file_cleanup(self):
        result = self.send()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('HEC returned code 0', result.stdout)
        self.assertNotIn(DUMMY_TOKEN, result.stdout + result.stderr)
        self.assertFalse(Path((self.work / 'capture.txt').read_text()).exists())

    def test_nonzero_hec_code_fails_and_cleans_up(self):
        self.env['MOCK_HEC_CODE'] = '7'
        self.assertNotEqual(self.send().returncode, 0)
        self.assertFalse(Path((self.work / 'capture.txt').read_text()).exists())

    def test_bad_token_is_not_sent(self):
        self.assertNotEqual(self.send('invalid-token').returncode, 0)
        self.assertFalse((self.work / 'capture.txt').exists())

    def test_http_is_refused(self):
        self.env['HEC_URL'] = 'http://172.25.250.10:8088/services/collector'
        self.assertNotEqual(self.send().returncode, 0)
        self.assertFalse((self.work / 'capture.txt').exists())


if __name__ == '__main__':
    unittest.main()
