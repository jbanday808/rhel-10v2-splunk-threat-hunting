const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const app = fs.readFileSync(path.join(__dirname, '..', 'website', 'tracevector-lab', 'app.js'), 'utf8');
const start = app.indexOf('function isMobile(){');
const end = app.indexOf('\nconst objectives=', start);
const gotoStart = app.indexOf('function goto(id){');
const gotoEnd = app.indexOf('\nfunction fixturePreview()', gotoStart);
assert.ok(start >= 0 && end > start && gotoStart >= 0 && gotoEnd > gotoStart, 'mobile navigation handlers must be present');

function setup() {
  let small = true;
  const classes = new Set();
  const document = { activeElement: null };
  const focusable = ['close', 'brand', 'last'].map(name => ({
    name, focus() { document.activeElement = this; },
  }));
  const [close, brand, last] = focusable;
  const sidebar = {
    inert: true,
    classList: {
      add(name) { classes.add(name); },
      remove(name) { classes.delete(name); },
      contains(name) { return classes.has(name); },
    },
    querySelectorAll() { return focusable; },
    contains(node) { return focusable.includes(node); },
  };
  const main = { inert: false };
  const toggle = {
    attrs: {},
    setAttribute(name, value) { this.attrs[name] = value; },
    focus() { document.activeElement = this; },
  };
  document.querySelector = selector => ({ '.sidebar': sidebar, '.main': main, '.mobile-toggle': toggle, '.mobile-close': close })[selector];
  const heading = { focus() { document.activeElement = this; } };
  document.getElementById = id => id === 'page-title' ? heading : null;
  const window = { matchMedia: () => ({ matches: small }), scrollTo() {} };
  const location = { hash: '' };
  const api = vm.runInNewContext(`${app.slice(start, end)}\n${app.slice(gotoStart, gotoEnd)}\n({openMobileNavigation,closeMobileNavigation,handleMobileNavigationKey,synchronizeNavigation,goto});`, {
    document, window, location, titles: { overview: true, scenarios: true }, render() {}, page: 'overview', currentScenario: null,
  });
  return { api, document, sidebar, main, toggle, close, brand, last, heading, location, setSmall(value) { small = value; } };
}

test('opening the mobile menu moves focus inside and blocks the page', () => {
  const ui = setup();
  ui.api.openMobileNavigation();
  assert.equal(ui.sidebar.classList.contains('open'), true);
  assert.equal(ui.sidebar.inert, false);
  assert.equal(ui.main.inert, true);
  assert.equal(ui.toggle.attrs['aria-expanded'], 'true');
  assert.equal(ui.document.activeElement, ui.close);
});

test('Escape closes the menu and returns focus to its opener', () => {
  const ui = setup();
  ui.api.openMobileNavigation();
  let prevented = false;
  assert.equal(ui.api.handleMobileNavigationKey({ key: 'Escape', preventDefault() { prevented = true; } }), true);
  assert.equal(prevented, true);
  assert.equal(ui.sidebar.classList.contains('open'), false);
  assert.equal(ui.sidebar.inert, true);
  assert.equal(ui.main.inert, false);
  assert.equal(ui.toggle.attrs['aria-expanded'], 'false');
  assert.equal(ui.document.activeElement, ui.toggle);
});

test('Tab and Shift+Tab wrap within the open menu', () => {
  const ui = setup();
  ui.api.openMobileNavigation();
  ui.document.activeElement = ui.last;
  let prevented = false;
  ui.api.handleMobileNavigationKey({ key: 'Tab', shiftKey: false, preventDefault() { prevented = true; } });
  assert.equal(prevented, true);
  assert.equal(ui.document.activeElement, ui.close);
  prevented = false;
  ui.api.handleMobileNavigationKey({ key: 'Tab', shiftKey: true, preventDefault() { prevented = true; } });
  assert.equal(prevented, true);
  assert.equal(ui.document.activeElement, ui.last);
});

test('desktop navigation stays available and does not trap focus', () => {
  const ui = setup();
  ui.setSmall(false);
  ui.api.synchronizeNavigation();
  assert.equal(ui.sidebar.inert, false);
  assert.equal(ui.main.inert, false);
  assert.equal(ui.api.handleMobileNavigationKey({ key: 'Tab' }), false);
});

test('choosing a section from the menu focuses the new heading', () => {
  const ui = setup();
  ui.api.openMobileNavigation();
  ui.api.goto('scenarios');
  assert.equal(ui.location.hash, 'scenarios');
  assert.equal(ui.document.activeElement, ui.heading);
});

test('rendered menu has a labeled close control and a linked opener', () => {
  assert.match(app, /id="mobile-nav"[^>]*><button class="mobile-close"[^>]*aria-label="Close navigation"/);
  assert.match(app, /class="mobile-toggle"[^>]*aria-controls="mobile-nav"[^>]*aria-expanded="false"/);
  assert.match(app, /id="page-title" tabindex="-1"/);
  assert.match(app, /const brand=e\.target\.closest\('\.sidebar \.brand'\);if\(brand&&isMobile\(\)\)\{e\.preventDefault\(\);goto\('overview'\)/);
});
