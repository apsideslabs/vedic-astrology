/* yogas.js -- port of src/jyotish/yogas.py.
 *
 * SOURCE: ch. III, "Yogas" and "Important Yogas", plus Gurumangala from
 * ch. VI.  Sign-based, as the book works.
 */
(function () {
  const JY = window.JY;
  const D = JY.D;

  const rel = (a, b) => JY.houseFrom(a, b);
  const yoga = (name, present, planets, description, source) =>
    ({ name, present, planets, description, source });

  function detect(chart) {
    const signs = chart._signs;
    const lagna = chart.lagna.sign;
    const moon = signs.Moon;
    const out = [];

    const malefics = ["Sun", "Mars", "Saturn"];

    /* -- Papakarthari / Subhakarthari ------------------------------- */
    const second = D.SIGNS[(D.SIGNS.indexOf(lagna) + 1) % 12];
    const twelfth = D.SIGNS[(D.SIGNS.indexOf(lagna) + 11) % 12];
    const occ2 = D.PLANETS.filter((p) => signs[p] === second);
    const occ12 = D.PLANETS.filter((p) => signs[p] === twelfth);
    const mal2 = occ2.filter((p) => malefics.includes(p));
    const mal12 = occ12.filter((p) => malefics.includes(p));
    const ben2 = occ2.filter((p) => D.NATURAL_BENEFICS.includes(p));
    const ben12 = occ12.filter((p) => D.NATURAL_BENEFICS.includes(p));

    out.push(yoga("Papakarthari", mal2.length > 0 && mal12.length > 0, mal2.concat(mal12),
      "The Ascendant is hemmed in between two malefics. The source says this subjects the native to a chequered career.",
      "ch. III"));
    out.push(yoga("Subhakarthari", ben2.length > 0 && ben12.length > 0, ben2.concat(ben12),
      "Benefics on either side of the Ascendant, which augments the good.", "ch. III"));

    /* -- Moon yogas ------------------------------------------------- */
    const moonSecond = D.SIGNS[(D.SIGNS.indexOf(moon) + 1) % 12];
    const moonTwelfth = D.SIGNS[(D.SIGNS.indexOf(moon) + 11) % 12];
    const inSecond = D.PLANETS.filter((p) => signs[p] === moonSecond && p !== "Sun");
    const inTwelfth = D.PLANETS.filter((p) => signs[p] === moonTwelfth && p !== "Sun");

    out.push(yoga("Sunapha", inSecond.length >= 2, inSecond,
      "Two or more planets (except the Sun) in the 2nd from the Moon: intelligent and reputed, occupies a high position, earns well by his own exertions.",
      "ch. III"));
    out.push(yoga("Anapha", inTwelfth.length >= 2, inTwelfth,
      "Two or more planets (except the Sun) in the 12th from the Moon: enjoys worldly pleasure of every kind and possesses an unruffled temper.",
      "ch. III"));
    out.push(yoga("Durdhura", inSecond.length > 0 && inTwelfth.length > 0, inSecond.concat(inTwelfth),
      "Planets on either side of the Moon: self-sacrifice, good servants, wealth and conveyances.",
      "ch. III"));

    const kendraFromMoon = D.PLANETS.filter((p) =>
      p !== "Moon" && D.KENDRAS.includes(rel(moon, signs[p])));
    const kemadruma = inSecond.length === 0 && inTwelfth.length === 0;
    out.push(yoga("Kemadruma", kemadruma && kendraFromMoon.length === 0, [],
      "No planets on either side of the Moon: dirty habits, subservient and sorrowful. Cancelled if a planet occupies a quadrant from the Moon.",
      "ch. III"));
    if (kemadruma && kendraFromMoon.length > 0) {
      out.push(yoga("Kemadruma-bhanga", true, kendraFromMoon,
        "Kemadruma is formed but cancelled by planets in a quadrant from the Moon.",
        "ch. III"));
    }

    /* -- Adhiyoga --------------------------------------------------- */
    const adhiSigns = [6, 7, 8].map((d) => D.SIGNS[(D.SIGNS.indexOf(moon) + d - 1) % 12]);
    const adhi = [];
    for (const s of adhiSigns) {
      for (const p of D.NATURAL_BENEFICS) if (signs[p] === s) adhi.push(p);
    }
    const adhiUnique = [...new Set(adhi)];
    out.push(yoga("Adhiyoga",
      new Set(adhi.map((p) => signs[p])).size === 3, adhiUnique.sort(),
      "Benefics in the 6th, 7th and 8th from the Moon: happy, fearless, high position, influential and long-lived.",
      "ch. III"));

    /* -- Gurumangala (named in ch. VI) ------------------------------ */
    out.push(yoga("Gurumangala", signs.Jupiter === signs.Mars, ["Jupiter", "Mars"],
      "Jupiter and Mars together; the source cites it as a wealth-producing combination when it falls in the 2nd from the Moon.",
      "ch. VI"));

    /* -- Rajayoga --------------------------------------------------- */
    const lagnaLord = JY.lordOfSign(lagna);
    const pairs = [];
    for (const t of D.TRIKONAS) {
      const tSign = D.SIGNS[(D.SIGNS.indexOf(lagna) + t - 1) % 12];
      const tLord = JY.lordOfSign(tSign);
      for (const k of D.KENDRAS) {
        const kSign = D.SIGNS[(D.SIGNS.indexOf(lagna) + k - 1) % 12];
        const kLord = JY.lordOfSign(kSign);
        if (tLord === kLord) continue;
        if (signs[tLord] === signs[kLord]) {
          if ([tLord, kLord].includes(lagnaLord) || signs[lagnaLord] === signs[tLord]) {
            pairs.push([tLord, kLord]);
          }
        }
      }
    }
    out.push(yoga("Rajayoga", pairs.length > 0, pairs.flat(),
      "A lord of a trine combines with a lord of a quadrant, with a connection to the lord of the 1st: high power and authority.",
      "ch. III"));

    /* -- Yogakaraka ------------------------------------------------- */
    const yogakarakas = [];
    for (const planet of D.SEVEN_GRAHAS) {
      const owned = D.SIGNS.filter((s) => JY.lordOfSign(s) === planet);
      const ownedHouses = owned.map((s) => JY.houseFrom(lagna, s));
      const hasKendra = ownedHouses.some((h) => D.KENDRAS.includes(h));
      const hasTrine = ownedHouses.some((h) => D.TRIKONAS.includes(h));
      if (hasKendra && hasTrine) yogakarakas.push(planet);
    }
    out.push(yoga("Yogakaraka", yogakarakas.length > 0, yogakarakas,
      "A planet owning both a quadrant and a trine from the Ascendant. The source calls such a planet a Rajayoga karaka.",
      "ch. III"));

    return out;
  }

  JY.yogas = { detect };
})();
