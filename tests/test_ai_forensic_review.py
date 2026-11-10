"""Synthetic-only AI review boundary tests; no model, network or evidence acquisition."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('ai_forensic_review', ROOT / 'scripts/security-operations/ai_forensic_review.py')
review = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(review)
CASE = json.loads((ROOT / 'examples/security-operations/ai-forensics-synthetic-case.json').read_text())
RESPONSE = json.loads((ROOT / 'examples/security-operations/ai-review-response.example.json').read_text())


class AiForensicReviewTests(unittest.TestCase):
    def test_example_is_structurally_valid_and_still_pending(self):
        review.validate_case(CASE)
        review.validate_response(CASE, RESPONSE)
        self.assertEqual(RESPONSE['human_review_status'], 'pending')

    def test_prepare_preserves_case_and_fingerprints_case_document_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'case.json'
            source.write_text(json.dumps(CASE) + '\n', encoding='utf-8')
            original = source.read_bytes()
            output = Path(tmp) / 'packet.json'
            review.prepare(source, output)
            packet = json.loads(output.read_text())
            self.assertEqual(packet['source_case'], CASE)
            self.assertEqual(packet['case_document_sha256'], hashlib.sha256(original).hexdigest())
            self.assertEqual(packet['response_contract']['human_review_status'], 'pending')
            self.assertIn('not a forensic acquisition', packet['hash_scope'])
            self.assertEqual(source.read_bytes(), original)
            if os.name == 'posix':
                self.assertEqual(output.stat().st_mode & 0o777, 0o600)

    def test_prepare_contract_cites_first_record_when_ids_do_not_include_e001(self):
        case = copy.deepcopy(CASE)
        for index, record in enumerate(case['evidence'], start=101):
            record['id'] = f'E{index:03}'
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'case.json'
            source.write_text(json.dumps(case), encoding='utf-8')
            output = Path(tmp) / 'packet.json'
            review.prepare(source, output)
            contract = json.loads(output.read_text())['response_contract']
            self.assertEqual(contract['findings'][0]['evidence_ids'], ['E101'])
            contract['findings'][0]['type'] = 'observation'
            contract['findings'][0]['confidence'] = 'low'
            review.validate_response(case, contract)

    def test_date_only_timestamp_is_refused(self):
        case = copy.deepcopy(CASE)
        case['evidence'][0]['observed_at_utc'] = '2026-01-01Z'
        with self.assertRaisesRegex(ValueError, 'UTC time and zero UTC offset'):
            review.validate_case(case)

    def test_non_synthetic_handling_is_refused(self):
        case = copy.deepcopy(CASE)
        case['handling'] = 'PRIVATE_CASE'
        with self.assertRaisesRegex(ValueError, 'synthetic public lab'):
            review.validate_case(case)

    def test_schema_true_is_not_accepted_as_version_one(self):
        case = copy.deepcopy(CASE)
        case['schema_version'] = True
        with self.assertRaisesRegex(ValueError, 'schema version'):
            review.validate_case(case)

    def test_duplicate_evidence_identifiers_are_refused(self):
        case = copy.deepcopy(CASE)
        case['evidence'].append(copy.deepcopy(case['evidence'][0]))
        with self.assertRaisesRegex(ValueError, 'unique'):
            review.validate_case(case)

    def test_unknown_or_missing_citations_are_refused(self):
        for refs in (['E999'], []):
            response = copy.deepcopy(RESPONSE)
            response['findings'][0]['evidence_ids'] = refs
            with self.subTest(refs=refs), self.assertRaises(ValueError):
                review.validate_response(CASE, response)

    def test_model_cannot_approve_its_own_response(self):
        response = copy.deepcopy(RESPONSE)
        response['human_review_status'] = 'approved'
        with self.assertRaisesRegex(ValueError, 'human approval'):
            review.validate_response(CASE, response)

    def test_wrong_case_and_unsupported_action_fields_are_refused(self):
        response = copy.deepcopy(RESPONSE)
        response['case_id'] = 'OTHER-CASE'
        with self.assertRaisesRegex(ValueError, 'does not match'):
            review.validate_response(CASE, response)
        response = copy.deepcopy(RESPONSE)
        response['execute_actions'] = []
        with self.assertRaisesRegex(ValueError, 'unsupported fields'):
            review.validate_response(CASE, response)

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'packet.json'
            output.write_text('original')
            with self.assertRaisesRegex(ValueError, 'already exists'):
                review.write_exclusive_json(output, {'sample': True})
            self.assertEqual(output.read_text(), 'original')

    def test_output_in_git_worktree_is_refused(self):
        for marker_type in ('file', 'directory'):
            with self.subTest(marker_type=marker_type), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                marker = root / '.git'
                if marker_type == 'file':
                    marker.write_text('gitdir: example')
                else:
                    marker.mkdir()
                nested = root / 'nested'
                nested.mkdir()
                with self.assertRaisesRegex(ValueError, 'outside Git'):
                    review.write_exclusive_json(nested / 'packet.json', {})
                self.assertFalse((nested / 'packet.json').exists())

    def test_dangling_output_symlink_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / 'packet.json'
            try:
                output.symlink_to(root / 'absent.json')
            except (OSError, NotImplementedError):
                self.skipTest('Symlink creation not permitted')
            with self.assertRaisesRegex(ValueError, 'symbolic link'):
                review.write_exclusive_json(output, {})
            self.assertFalse((root / 'absent.json').exists())

    def test_duplicate_json_keys_are_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'response.json'
            path.write_text('{"case_id":"A","case_id":"B"}')
            with self.assertRaisesRegex(ValueError, 'Duplicate JSON key'):
                review.read_json(path)

    def test_oversized_input_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'large.json'
            path.write_bytes(b' ' * (review.MAX_BYTES + 1))
            with self.assertRaisesRegex(ValueError, 'size limit'):
                review.read_json(path)

    def test_structure_check_does_not_claim_semantic_validation(self):
        response = copy.deepcopy(RESPONSE)
        response['findings'][0]['text'] = 'Unsupported attribution to a real threat actor.'
        # Known IDs cannot establish that the statement is true; a human must reject it.
        review.validate_response(CASE, response)
        self.assertEqual(response['human_review_status'], 'pending')


if __name__ == '__main__':
    unittest.main()
