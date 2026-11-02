/* Verify the browser engine against the Python engine, value by value. */
const fs = require('fs');
const vm = require('vm');
const path = require('path');

const jsDir = path.join(__dirname, '..', 'site', 'assets', 'js');
const ctx = { console, Date, Math, JSON, Object, Array, String, Number, isNaN };
ctx.window = ctx;
ctx.self = ctx;
vm.createContext(ctx);
for (const f of ['astronomy.js', 'data.js', 'core.js', 'ephemeris.js', 'dasha.js',
                 'panchanga.js', 'yogas.js', 'chart.js', 'transits.js', 'interpret.js']) {
  vm.runInContext(fs.readFileSync(path.join(jsDir, f), 'utf8'), ctx, { filename: f });
}
const JY = ctx.JY;

const birth = {
  date: '1935-11-02', time: '05:20:00', latitude: 13.0, longitude: 77.5833333,
  tz_offset: 5.1722222, place: 'Madras', ayanamsa: 'raman_397', house_system: 'whole_sign',
};
const chart = JY.buildChart(birth);
const transit = JY.transits.analyse(chart, Date.UTC(2026, 10, 2, 0, 0, 0));
const reading = JY.interpret.interpret(chart, transit);

const out = {
  ayanamsa: chart.ayanamsa.value,
  ascendant_tropical: chart.lagna.longitude + chart.ayanamsa.value,
  lagna_sign: chart.lagna.sign,
  lagna_deg: chart.lagna.degree_in_sign,
  planets: {},
  houses: chart.houses.map(h => ({ house: h.house, sign: h.sign, lord: h.lord,
                                   lord_house: h.lord_house, occupants: h.occupants })),
  dasha_balance: chart.vimshottari.balance_at_birth,
  janma_nakshatra: chart.vimshottari.janma_nakshatra,
  panchanga: { vara: chart.panchanga.vara.name, tithi: chart.panchanga.tithi.name,
               paksha: chart.panchanga.tithi.paksha, yoga: chart.panchanga.yoga.name,
               karana: chart.panchanga.karana.name },
  yogas_present: chart.yogas.filter(y => y.present).map(y => y.name).sort(),
  interpretation_sections: reading.sections.length,
  interpretation_statements: reading.sections.reduce((n, s) => n + s.statements.length, 0),
  aspects: chart.aspects.length,
  sade_sati: transit.sade_sati.active,
  gochara: transit.gochara.map(r => [r.planet, r.house_from_moon, r.result]),
};
for (const p of chart.planets) {
  out.planets[p.planet] = {
    longitude: Math.round(p.longitude * 1e4) / 1e4,
    sign: p.sign, house: p.house, dignity: p.dignity,
    nakshatra: p.nakshatra, pada: p.pada, navamsa: p.navamsa_sign,
    retrograde: p.retrograde, score: p.strength.score,
  };
}
fs.writeFileSync(path.join(__dirname, 'js_out.json'), JSON.stringify(out, null, 1));
console.log('JS engine OK. lagna', out.lagna_sign, 'ayanamsa', out.ayanamsa.toFixed(4),
            'statements', out.interpretation_statements);
