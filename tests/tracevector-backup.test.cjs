const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const app = fs.readFileSync(path.join(__dirname, '..', 'website', 'tracevector-lab', 'app.js'), 'utf8');
const helperStart = app.indexOf('function validateBackupAttachments(b){');
const helperEnd = app.indexOf('\nconst defaults=', helperStart);
const start = app.indexOf('function validateBackup(b){');
const end = app.indexOf('\nasync function applyImport()', start);
assert.ok(helperStart >= 0 && helperEnd > helperStart && start >= 0 && end > start, 'the Site backup validator must be present');
const validateBackup = vm.runInNewContext(`${app.slice(helperStart, helperEnd)}\n${app.slice(start, end)}\nvalidateBackup;`);

function backup() {
  return {
    app: 'TraceVector', version: 1,
    state: {
      version: 1, objectives: {}, scenarioProgress: {}, evidenceUpdates: {}, docUpdates: {}, stig: {},
      evidence: [{ title: 'Synthetic note', created: '2026-01-01T00:00:00Z', fileId: 'file-1' }],
      proposals: [], detections: [], activity: [], notes: '',
    },
    files: [{ id: 'file-1', name: 'note.txt', mime: 'text/plain', data: 'data:text/plain;base64,SGVsbG8=' }],
  };
}

test('accepts a normal version 1 backup with an attachment', () => {
  assert.doesNotThrow(() => validateBackup(backup()));
});

test('keeps version 1 backups without attachments importable', () => {
  const b = backup();
  delete b.state.evidence[0].fileId;
  b.files = [];
  assert.doesNotThrow(() => validateBackup(b));
});

test('rejects a duplicate attachment ID before import', () => {
  const b = backup();
  b.files.push({ ...b.files[0], name: 'different.txt' });
  assert.throws(() => validateBackup(b), /Duplicate evidence attachment ID/);
});

test('rejects an attachment above the Site file limit', () => {
  const b = backup();
  b.files[0].data = 'data:text/plain;base64,' + 'A'.repeat(12 * 1024 * 1024);
  assert.throws(() => validateBackup(b), /Attachment exceeds 8 MB/);
});

test('checks decoded bytes as well as text length', () => {
  const b = backup();
  const justOverEightMb = 4 * Math.ceil((8 * 1024 * 1024 + 1) / 3);
  b.files[0].data = 'data:text/plain;base64,' + 'A'.repeat(justOverEightMb);
  assert.throws(() => validateBackup(b), /Attachment exceeds 8 MB/);
});

test('rejects malformed base64', () => {
  const b = backup();
  b.files[0].data = 'data:text/plain;base64,A===';
  assert.throws(() => validateBackup(b), /Invalid evidence attachment/);
});

test('rejects a missing referenced attachment', () => {
  const b = backup();
  b.files = [];
  assert.throws(() => validateBackup(b), /attachment is missing/);
});
