const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const root = path.join(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'website', 'tracevector-lab', 'context.js'), 'utf8');
const sandbox = { window: {} };
vm.runInNewContext(source, sandbox);
const context = sandbox.window.TV_CONTEXT;

test('TraceVector repository guides and screenshots point to files that exist', () => {
  assert.equal(context.repository, 'jbanday808/rhel-10v2-splunk-threat-hunting');
  const base = `https://github.com/${context.repository}`;
  assert.equal(context.repoUrl, base);
  assert.equal(context.readmeUrl, `${base}/blob/main/README.md`);

  const entries = [...context.docs, ...context.screenshots];
  assert.ok(entries.length > 0, 'the Site should expose repository references');
  const paths = new Set();
  for (const entry of entries) {
    assert.ok(entry.path, 'every reference has a repository path');
    assert.ok(!paths.has(entry.path), `duplicate repository path: ${entry.path}`);
    paths.add(entry.path);
    assert.ok(fs.existsSync(path.join(root, entry.path)), `missing repository file: ${entry.path}`);
    assert.equal(entry.url, `${base}/blob/main/${entry.path}`, `URL mismatch: ${entry.path}`);
  }
});

test('every synthetic scenario has a matching lab validation guide', () => {
  const scenarioSource = fs.readFileSync(path.join(root, 'website', 'tracevector-lab', 'scenarios.js'), 'utf8');
  vm.runInNewContext(scenarioSource, sandbox);
  const ids = Array.from(sandbox.window.TV_SCENARIOS, scenario => scenario.id).sort();
  const guideIds = Object.keys(context.huntGuides).sort();
  assert.deepEqual(guideIds, ids, 'each scenario must map to exactly one guide');

  for (const id of ids) {
    const guide = context.huntGuides[id];
    assert.ok(guide.startsWith('docs/network-defense/tracevector-hunts/'), `unexpected guide location: ${id}`);
    assert.ok(fs.existsSync(path.join(root, guide)), `missing lab guide: ${id}`);
  }
});
