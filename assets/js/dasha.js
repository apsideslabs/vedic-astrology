/* dasha.js -- Vimshottari, ported from src/jyotish/dasha.py.
 *
 * SOURCE: ch. X.  Years of 365.25 days, the convention of Indian ephemerides.
 */
(function () {
  const JY = window.JY;
  const D = JY.D;

  const YEAR_DAYS = 365.25;
  const MS_PER_YEAR = YEAR_DAYS * 86400000;

  const addYears = (ms, years) => new Date(ms + years * MS_PER_YEAR);
  const isoDate = (d) => d.toISOString().slice(0, 10);
  const isoTime = (d) => d.toISOString().slice(0, 19);

  function period(lord, startMs, years) {
    const end = addYears(startMs, years);
    return {
      lord,
      years,
      start: isoTime(new Date(startMs)),
      end: isoTime(end),
      start_date: isoDate(new Date(startMs)),
      end_date: isoDate(end),
    };
  }

  function antardashas(mahaLord, startMs, mahaYears) {
    const order = D.VIMSHOTTARI_ORDER;
    const i = order.indexOf(mahaLord);
    const out = [];
    let cursor = startMs;
    for (let k = 0; k < 9; k++) {
      const sub = order[(i + k) % 9];
      const years = (mahaYears * D.VIMSHOTTARI_YEARS[sub]) / 120;
      out.push(period(sub, cursor, years));
      cursor += years * MS_PER_YEAR;
    }
    return out;
  }

  function vimshottari(moonLongitude, birthUtcMs, atMs) {
    const at = atMs === undefined ? Date.now() : atMs;

    const nakIndex = JY.nakIndex(moonLongitude);
    const lord = D.NAKSHATRA_LORDS[nakIndex];
    const span = JY.NAK_SPAN;
    const elapsed = (JY.mod360(moonLongitude) % span) / span;
    const lordYears = D.VIMSHOTTARI_YEARS[lord];
    const balanceYears = lordYears * (1.0 - elapsed);

    let cursor = birthUtcMs - elapsed * lordYears * MS_PER_YEAR;
    const order = D.VIMSHOTTARI_ORDER;
    const i = order.indexOf(lord);
    const mahadashas = [];
    for (let k = 0; k < 9; k++) {
      const maha = order[(i + k) % 9];
      const years = D.VIMSHOTTARI_YEARS[maha];
      const entry = period(maha, cursor, years);
      entry.antardashas = antardashas(maha, cursor, years);
      mahadashas.push(entry);
      cursor += years * MS_PER_YEAR;
    }

    let current = { mahadasha: null, antardasha: null };
    for (const maha of mahadashas) {
      const s = Date.parse(maha.start + "Z");
      const e = Date.parse(maha.end + "Z");
      if (at >= s && at < e) {
        current = { mahadasha: maha, antardasha: null };
        for (const sub of maha.antardashas) {
          const ss = Date.parse(sub.start + "Z");
          const se = Date.parse(sub.end + "Z");
          if (at >= ss && at < se) { current.antardasha = sub; break; }
        }
        break;
      }
    }

    return {
      system: "Vimshottari",
      year_days: YEAR_DAYS,
      janma_nakshatra: D.NAKSHATRAS[nakIndex],
      janma_nakshatra_index: nakIndex + 1,
      janma_nakshatra_lord: lord,
      elapsed_fraction: Math.round(elapsed * 1e6) / 1e6,
      balance_at_birth: {
        lord,
        years: Math.floor(balanceYears),
        months: Math.floor((balanceYears % 1) * 12),
        days: Math.floor(((balanceYears * 12) % 1) * 30),
        decimal_years: Math.round(balanceYears * 1e6) / 1e6,
        ends_on: isoDate(addYears(birthUtcMs, balanceYears)),
      },
      mahadashas,
      current,
      as_of: isoTime(new Date(at)),
    };
  }

  JY.dasha = { vimshottari, antardashas, YEAR_DAYS };
})();
