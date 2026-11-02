/* transits.js -- Gochara from the Janma Rasi (port of transits.py).
 *
 * SOURCE: ch. XII.  Cells that are null are places where the scanned book is
 * damaged; they are reported as gaps, never filled in from another book.
 */
(function () {
  const JY = window.JY;
  const D = JY.D;

  function currentPositions(jd, ayanamsa) {
    const ay = JY.ayanamsa.value(ayanamsa, jd);
    const trop = JY.ephemeris.tropicalLongitudes(jd);
    const out = {};
    for (const planet of D.PLANETS) {
      const data = trop[planet];
      const sid = JY.mod360(data.longitude - ay);
      out[planet] = {
        longitude: Math.round(sid * 1e4) / 1e4,
        dms: JY.dms(sid),
        sign: JY.signOf(sid),
        degree_in_sign: Math.round(JY.degreeInSign(sid) * 1e4) / 1e4,
        nakshatra: JY.nakName(sid),
        retrograde: data.speed < 0,
      };
    }
    return out;
  }

  function gochara(janmaRasi, positions) {
    return D.PLANETS.map((planet) => {
      const pos = positions[planet];
      const house = JY.houseFrom(janmaRasi, pos.sign);
      const table = D.GOCHARA[planet] || {};
      const result = table[String(house)] === undefined ? null : table[String(house)];
      return {
        planet,
        sign: pos.sign,
        house_from_moon: house,
        result,
        gap_in_source: result === null,
        sade_sati: planet === "Saturn" && D.SADE_SATI_HOUSES.includes(house),
      };
    });
  }

  function analyse(chart, atMs) {
    const at = atMs === undefined ? Date.now() : atMs;
    const jd = JY.J2000 + (at - Date.UTC(2000, 0, 1, 12, 0, 0)) / 86400000;
    const positions = currentPositions(jd, chart.ayanamsa.model);
    const janma = chart.lagna.moon_sign;
    const rows = gochara(janma, positions);
    const saturn = rows.find((r) => r.planet === "Saturn");
    return {
      as_of: new Date(at).toISOString().slice(0, 19),
      janma_rasi: janma,
      positions,
      gochara: rows,
      sade_sati: {
        active: saturn.sade_sati,
        saturn_house_from_moon: saturn.house_from_moon,
        note: "Saturn in the 12th, 1st or 2nd from the radical Moon is Sade Sati, the '7 1/2 years' Saturn of the source.",
      },
      weighting:
        "The source insists transits must never be read without the prevailing dasha and bhukti (ch. XII).",
    };
  }

  JY.transits = { currentPositions, gochara, analyse };
})();
