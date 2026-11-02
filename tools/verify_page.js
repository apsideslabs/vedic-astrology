/* Load chart.html in a DOM and check the page actually renders a chart. */
const { JSDOM } = require('/scratch/node_modules/jsdom');
const fs = require('fs');
const path = require('path');

const file = path.join(__dirname, '..', 'site', 'chart.html');
const dom = new JSDOM(fs.readFileSync(file, 'utf8'), {
  runScripts: 'dangerously',
  resources: undefined,
  url: 'https://example.org/chart.html',
  pretendToBeVisual: true,
  beforeParse(window) {
    window.scrollTo = () => {};
    // jsdom does not fetch external scripts without a resource loader; inject manually.
    const jsDir = path.join(__dirname, '..', 'site', 'assets', 'js');
    window.__inject = (names) => {
      for (const n of names) {
        const code = fs.readFileSync(path.join(jsDir, n), 'utf8');
        window.eval(code);
      }
    };
  },
});

const w = dom.window;
const errors = [];
w.addEventListener('error', (e) => errors.push(String(e.message)));

const scripts = [...w.document.querySelectorAll('script[src]')].map((s) => s.getAttribute('src'));
w.__inject(scripts.map((s) => s.split('/').pop()));
w.document.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true }));

const out = w.document.getElementById('out');
const err = w.document.getElementById('err');
setTimeout(() => {
  const html = out ? out.innerHTML : '';
  console.log('scripts:', scripts.length);
  console.log('out hidden:', out.classList.contains('hidden'));
  console.log('error box:', err.classList.contains('hidden') ? 'hidden' : err.textContent);
  console.log('rendered length:', html.length);
  const checks = {
    'Lagna card': html.includes('Ascendant'),
    'Rasi grid': html.includes('Rasi chakra'),
    'Navamsa grid': html.includes('Navamsa (D9)'),
    'graha table': html.includes('Nakshatra'),
    'dasha table': html.includes('Vimshottari'),
    'reading': html.includes('Ascendant, appearance and character'),
    'transits': html.includes('Gochara'),
    'book lagna Libra': html.includes('Libra'),
  };
  for (const [k, v] of Object.entries(checks)) console.log((v ? 'ok   ' : 'FAIL ') + k);
  if (errors.length) console.log('JS errors:', errors);
  const bad = Object.values(checks).filter((v) => !v).length;
  process.exit(bad || errors.length ? 1 : 0);
}, 1500);
