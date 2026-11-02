/* Render one page in a DOM and check it actually works.
 * Usage: node tools/verify_pages.js chart.html
 */
const { JSDOM } = require('/scratch/node_modules/jsdom');
const fs = require('fs');
const path = require('path');

const SITE = path.join(__dirname, '..', 'site');
const JS = path.join(SITE, 'assets', 'js');

const PAGES = {
  'index.html': ['Cast a chart', 'Checked against the book', 'What it will not do'],
  'chart.html': ['Rasi wheel', 'Grahas', 'Vimshottari dasha', 'Gochara', 'Libra'],
  'panchanga.html': ['Sunrise', 'The five limbs', 'Nakshatra', 'Karana'],
  'transits.html': ['Gochara', 'Sade Sati', 'Next sign ingress'],
  'knowledge.html': ['Knowledge base', 'Interpretation', 'Source notes'],
  'docs/07-calculation.html': ['Casting a horoscope', 'Ayanamsa'],
  'api.html': ['POST /api/chart', 'FastAPI'],
  'about.html': ['Provenance', 'What the scan damaged'],
};

const rel = process.argv[2];
if (!rel) { console.error('usage: node tools/verify_pages.js <page>'); process.exit(2); }
const probes = PAGES[rel];

const dom = new JSDOM(fs.readFileSync(path.join(SITE, rel), 'utf8'), {
  runScripts: 'dangerously', url: 'https://example.org/' + rel, pretendToBeVisual: true,
  beforeParse(w) {
    w.scrollTo = () => {};
    w.IntersectionObserver = class { observe() {} disconnect() {} };
    w.__inject = (names) => {
      for (const n of names) w.eval(fs.readFileSync(path.join(JS, n), 'utf8'));
    };
  },
});
const w = dom.window;
const errors = [];
w.addEventListener('error', (e) => errors.push(e.message));
const srcs = [...w.document.querySelectorAll('script[src]')]
  .map((s) => s.getAttribute('src').split('/').pop());
try { w.__inject(srcs); } catch (e) { errors.push('inject: ' + e.message); }
w.document.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true }));

setTimeout(() => {
  const body = w.document.body;
  const text = body.textContent;
  const chrome = !!body.querySelector('.appbar') && !!body.querySelector('.drawer')
    && !!body.querySelector('.burger');
  const missing = probes.filter((p) => !text.includes(p));
  let extra = '';
  if (rel === 'chart.html') {
    const planets = w.document.querySelectorAll('#wheel .planet').length;
    const spokes = w.document.querySelectorAll('#wheel .spoke').length;
    const rows = w.document.querySelectorAll('#grahas tbody tr').length;
    extra = ` wheel planets=${planets} spokes=${spokes} graha-rows=${rows}`;
    if (planets !== 9 || spokes !== 12 || rows !== 9) missing.push('wheel/table structure');
  }
  const ok = chrome && !missing.length && !errors.length;
  console.log(`${ok ? 'ok  ' : 'FAIL'} ${rel.padEnd(26)} scripts=${srcs.length} chrome=${chrome}${extra}`);
  if (missing.length) console.log('     missing:', missing);
  if (errors.length) console.log('     errors:', errors.slice(0, 3));
  process.exit(ok ? 0 : 1);
}, 1200);
