/* interpret.js -- the rule engine, ported from src/jyotish/interpret.py.
 *
 * Every statement carries a rule id and the chapter of the source it comes
 * from, so a reading can be audited rather than taken on trust.
 */
(function () {
  const JY = window.JY;
  const D = JY.D;

  const stmt = (rule, text, source, extra) =>
    Object.assign({ rule, text, source }, extra || {});

  const houseOf = (chart, p) => chart._planets[p].house;
  const P = (chart, p) => chart._planets[p];

  const maleficAspecting = (chart, planet) =>
    chart.aspects.some((a) => a.to === planet &&
      ["Saturn", "Mars", "Sun", "Rahu", "Ketu"].includes(a.from));
  const beneficAspecting = (chart, planet) =>
    chart.aspects.some((a) => a.to === planet && ["Jupiter", "Venus", "Mercury"].includes(a.from));

  function interpret(chart, transit) {
    const sections = [];
    const lagna = chart.lagna.sign;
    const lagnaLord = JY.lordOfSign(lagna);
    const signs = chart._signs;

    /* ---------------- Lagna and appearance ---------------- */
    let stmts = [
      stmt("R-LAGNA-SIGN", `${lagna} rises: ${D.LAGNA_APPEARANCE[lagna]}.`, "ch. V"),
    ];
    for (const planet of D.PLANETS) {
      if (houseOf(chart, planet) === 1) {
        stmts.push(stmt(`R-LAGNA-${planet.toUpperCase()}`, D.PLANET_ON_LAGNA[planet], "ch. V"));
      }
    }
    if (beneficAspecting(chart, "Moon") && !maleficAspecting(chart, "Moon")) {
      stmts.push(stmt("R-LAGNA-MOON-CLEAR",
        "The Moon is free of malefic aspect, which the source treats as a mark of a settled mind.",
        "ch. V"));
    }
    const lordPos = P(chart, lagnaLord);
    stmts.push(stmt("R-LAGNA-LORD",
      `The lord of the Ascendant, ${lagnaLord}, is in ${lordPos.sign} (${lordPos.dignity}) in the ${lordPos.house}th house` +
      (lordPos.combust ? " and is combust" : "") +
      (lordPos.retrograde ? " and retrograde" : "") + ".",
      "ch. III, ch. V"));
    sections.push({ title: "Ascendant, appearance and character", statements: stmts });

    /* ---------------- Mind ---------------- */
    const moon = P(chart, "Moon");
    stmts = [stmt("R-MIND-MOON",
      `The Moon, which the source makes the seat of the mind, is in ${moon.sign} in the ${moon.house}th house, in ${moon.nakshatra} pada ${moon.pada}.`,
      "ch. V")];
    if (maleficAspecting(chart, "Moon") || moon.combust) {
      stmts.push(stmt("R-MIND-AFFLICTED",
        "The Moon is afflicted by malefic aspect or conjunction. The source says this inclines the subject to pessimism and constant worry, and that affliction of the Moon and Mercury together makes a quick, restless and imaginative temperament most liable to mental disturbance.",
        "ch. V"));
    }
    if (beneficAspecting(chart, "Moon")) {
      stmts.push(stmt("R-MIND-SUPPORTED",
        "The Moon receives benefic aspect, which steadies it.", "ch. V"));
    }
    sections.push({ title: "Mind and temperament", statements: stmts });

    /* ---------------- Health ---------------- */
    stmts = [];
    const sixth = chart.houses[5];
    if (sixth.occupants.length) {
      stmts.push(stmt("R-HEALTH-6OCC",
        `The 6th house holds ${sixth.occupants.join(", ")}. The source: malefics in the 6th always indicate illness.`,
        "ch. V"));
    }
    if ([6, 8, 12].includes(P(chart, lagnaLord).house) || signs[lagnaLord] === sixth.sign) {
      stmts.push(stmt("R-HEALTH-LORD",
        "The lord of the Ascendant has to do with the 6th house, which the source reads as a sickly constitution.",
        "ch. V"));
    }
    if (P(chart, "Sun").house === 6) {
      stmts.push(stmt("R-HEALTH-SUN6",
        "The Sun is in the 6th, which brings enteric and bowel disorders when malefics also afflict it.",
        "ch. V"));
    }
    if (!stmts.length) {
      stmts.push(stmt("R-HEALTH-CLEAR",
        "The Ascendant and its lord are clear of the 6th house and its lord, which the source requires for sound health.",
        "ch. V"));
    }
    sections.push({ title: "Health", statements: stmts });

    /* ---------------- Longevity ---------------- */
    const beneficsInKendra = ["Jupiter", "Venus", "Mercury"]
      .filter((q) => D.KENDRAS.includes(P(chart, q).house));
    let longevity, text;
    if (beneficsInKendra.length >= 2) {
      longevity = "long";
      text = `${beneficsInKendra.join(", ")} occupy angles. The source: according as benefics and the lord of the Lagna are in kendras, panaparas or apoklimas, life is long, medium or short.`;
    } else if (D.KENDRAS.includes(P(chart, lagnaLord).house)) {
      longevity = "long";
      text = "The lord of the Ascendant occupies an angle, which supports a long life.";
    } else if (D.PANAPARAS.includes(P(chart, lagnaLord).house)) {
      longevity = "medium";
      text = "The lord of the Ascendant occupies a panapara, which the source reads as medium life.";
    } else {
      longevity = "short";
      text = "The lord of the Ascendant occupies an apoklima, which the source reads as short life.";
    }
    stmts = [stmt("R-LONGEVITY", text, "ch. IV", { longevity })];
    stmts.push(stmt("R-LONGEVITY-CAVEAT",
      "The source's longevity rules are stated for a beginner and are the most contested part of the book; treat this as an indicator, not a prediction.",
      "ch. IV"));
    sections.push({ title: "Longevity indicators", statements: stmts });

    /* ---------------- Education ---------------- */
    const fourthLord = chart.houses[3].lord;
    stmts = [];
    if (chart.houses[3].occupants.some((q) => ["Mars", "Saturn", "Sun", "Rahu", "Ketu"].includes(q))) {
      stmts.push(stmt("R-EDU-4MALEFIC",
        "A malefic occupies the 4th house, which the source reads as broken education.", "ch. VI"));
    }
    if ([4, 10].includes(P(chart, "Jupiter").house)) {
      stmts.push(stmt("R-EDU-JUPITER",
        "Jupiter is in the 4th or the 10th, which the source says gives high legal education.", "ch. VI"));
    }
    if (D.KENDRAS.includes(P(chart, "Mercury").house)) {
      stmts.push(stmt("R-EDU-MERCURY",
        "Mercury is in an angle, which gives good knowledge of men and matters.", "ch. VI"));
    }
    if ([3, 6, 11].includes(P(chart, fourthLord).house)) {
      stmts.push(stmt("R-EDU-4LORD",
        `The lord of the 4th, ${fourthLord}, sits in the ${P(chart, fourthLord).house}th house, which the source says obstructs a sound educational career.`,
        "ch. VI"));
    }
    if (!stmts.length) {
      stmts.push(stmt("R-EDU-OPEN",
        "The 4th house, its lord and Jupiter are free of the afflictions the source names for education.",
        "ch. VI"));
    }
    sections.push({ title: "Education", statements: stmts });

    /* ---------------- Wealth ---------------- */
    const second = chart.houses[1];
    stmts = [];
    if (second.occupants.includes("Jupiter")) {
      stmts.push(stmt("R-WEALTH-JUP2",
        "Jupiter occupies the 2nd, which the source singles out as giving considerable wealth.", "ch. VI"));
    }
    if (P(chart, "Venus").house === 11) {
      stmts.push(stmt("R-WEALTH-VEN11",
        "Venus occupies the 11th, which is a strong mark for gains.", "ch. VI"));
    }
    if (["Saturn", "Rahu", "Ketu"].includes(second.lord) ||
        second.occupants.some((q) => ["Saturn", "Rahu", "Ketu"].includes(q))) {
      stmts.push(stmt("R-WEALTH-SATURN",
        "Saturn, Rahu or Ketu touches the 2nd house. The source: this shows complications in finance, loss by fraud, and many ups and downs of fortune.",
        "ch. VI"));
    }
    if (D.TRIKONAS.includes(P(chart, second.lord).house) || D.KENDRAS.includes(P(chart, second.lord).house)) {
      stmts.push(stmt("R-WEALTH-2LORD",
        `The lord of the 2nd, ${second.lord}, is in a trine or quadrant, which the source reads as a sign of good fortune.`,
        "ch. VI"));
    }
    if (!stmts.length) {
      stmts.push(stmt("R-WEALTH-NEUTRAL",
        "The 2nd and 11th houses carry none of the strong markers or afflictions the source names for wealth.",
        "ch. VI"));
    }
    sections.push({ title: "Financial prospects", statements: stmts });

    /* ---------------- Livelihood ---------------- */
    const tenth = chart.houses[9];
    const tenthLord = tenth.lord;
    const element = D.SIGN_NATURE[tenth.sign].element;
    stmts = [
      stmt("R-CAREER-SIGN",
        `The 10th house is ${tenth.sign}, a ${element} sign: ${D.TENTH_SIGN_CAREER[element]}.`,
        "ch. VII"),
      stmt("R-CAREER-LORD",
        `The lord of the 10th is ${tenthLord}, which points to ${D.TENTH_LORD_CAREER[tenthLord]}.`,
        "ch. VII"),
    ];
    if (tenth.occupants.length) {
      stmts.push(stmt("R-CAREER-OCC",
        `The 10th holds ${tenth.occupants.join(", ")}, whose own significations colour the profession.`,
        "ch. VII"));
    }
    const navLord = JY.lordOfSign(P(chart, tenthLord).navamsa_sign);
    stmts.push(stmt("R-CAREER-NAVAMSA",
      `The navamsa occupied by the lord of the 10th is ${P(chart, tenthLord).navamsa_sign}, whose lord is ${navLord}; the source reads that lord as a further indication of the calling (${D.TENTH_LORD_CAREER[navLord]}).`,
      "ch. VII"));
    sections.push({ title: "Means of livelihood", statements: stmts });

    /* ---------------- Parents and siblings ---------------- */
    const fourth = chart.houses[3];
    const ninth = chart.houses[8];
    stmts = [];
    if (ninth.occupants.includes("Sun") && ninth.occupants.includes("Saturn")) {
      stmts.push(stmt("R-FATHER-EARLY",
        "The Sun and Saturn together in the 9th indicate early death of the father.", "ch. VIII"));
    }
    if (fourth.occupants.includes("Saturn") && fourth.occupants.includes("Moon")) {
      stmts.push(stmt("R-MOTHER-EARLY",
        "Saturn with the Moon in the 4th denotes early death to the mother.", "ch. VIII"));
    }
    if (maleficAspecting(chart, "Sun")) {
      stmts.push(stmt("R-FATHER-AFFLICTED",
        "The Sun is afflicted, which the source reads as trouble to the father.", "ch. VIII"));
    }
    if (maleficAspecting(chart, "Moon")) {
      stmts.push(stmt("R-MOTHER-AFFLICTED",
        "The Moon is afflicted, which touches the mother's condition.", "ch. VIII"));
    }
    if (chart.houses[2].occupants.includes("Mars")) {
      stmts.push(stmt("R-BROTHERS-MARS3",
        "Mars in the 3rd does not indicate many brothers.", "ch. VIII"));
    }
    if (!stmts.length) {
      stmts.push(stmt("R-PARENTS-OPEN",
        "Neither luminary is afflicted and neither the 4th nor the 9th carries the combinations the source names for the parents.",
        "ch. VIII"));
    }
    sections.push({ title: "Parents, brothers and debts", statements: stmts });

    /* ---------------- Marriage ---------------- */
    const seventh = chart.houses[6];
    stmts = [];
    for (const occupant of seventh.occupants) {
      stmts.push(stmt(`R-MARRIAGE-${occupant.toUpperCase()}`,
        `${occupant} is in the 7th: the partner is ${D.SEVENTH_HOUSE_PARTNER[occupant]}.`,
        "ch. IX"));
    }
    if (seventh.occupants.includes("Venus") && maleficAspecting(chart, "Venus")) {
      stmts.push(stmt("R-MARRIAGE-VENUS-AFFLICTED",
        "Venus is in the 7th but afflicted, which the source reads as an unsatisfactory marriage.",
        "ch. IX"));
    }
    if (P(chart, seventh.lord).house === 6) {
      stmts.push(stmt("R-MARRIAGE-7LORD6",
        "The lord of the 7th occupies the 6th, which the source warns against for marital happiness.",
        "ch. IX"));
    }
    if (maleficAspecting(chart, "Venus")) {
      stmts.push(stmt("R-MARRIAGE-VENUS",
        "Venus is afflicted by a malefic; the source reads this as little emotional calm and prolonged separation when Mars is the afflictor.",
        "ch. IX"));
    }
    if (!stmts.length) {
      stmts.push(stmt("R-MARRIAGE-OPEN",
        "The 7th house and its lord carry none of the afflictions the source names for marriage.",
        "ch. IX"));
    }
    sections.push({ title: "Marriage", statements: stmts });

    /* ---------------- Children ---------------- */
    const fifth = chart.houses[4];
    stmts = [];
    if (fifth.occupants.includes("Saturn")) {
      stmts.push(stmt("R-CHILDREN-SATURN5",
        "Saturn in the 5th is among the afflictions the source names for children.", "ch. IX"));
    }
    if (fifth.occupants.some((q) => ["Mars", "Saturn", "Rahu", "Ketu"].includes(q))) {
      stmts.push(stmt("R-CHILDREN-MALEFIC",
        "A malefic occupies the 5th, which the source says produces results opposite to those of a well-aspected 5th.",
        "ch. IX"));
    }
    if (beneficAspecting(chart, "Jupiter") || [5, 9].includes(P(chart, "Jupiter").house)) {
      stmts.push(stmt("R-CHILDREN-JUPITER",
        "Jupiter, the Putrakaraka, is well placed, which supports progeny.", "ch. IX"));
    }
    if (!stmts.length) {
      stmts.push(stmt("R-CHILDREN-OPEN",
        "The 5th house, its lord and Jupiter carry none of the afflictions the source names for children.",
        "ch. IX"));
    }
    sections.push({ title: "Children", statements: stmts });

    /* ---------------- Yogas ---------------- */
    const present = chart.yogas.filter((y) => y.present);
    stmts = present.map((y) =>
      stmt(`R-YOGA-${y.name.toUpperCase()}`, `${y.name}: ${y.description}`, y.source));
    if (!stmts.length) {
      stmts.push(stmt("R-YOGA-NONE",
        "None of the yogas this engine detects are present in the chart.", "ch. III"));
    }
    sections.push({ title: "Yogas present", statements: stmts });

    /* ---------------- Dasha ---------------- */
    const current = chart.vimshottari.current;
    stmts = [];
    if (current.mahadasha) {
      const lord = current.mahadasha.lord;
      const house = P(chart, lord).house;
      const base = D.DASHA_HOUSE_RESULT[String(house)] || "";
      stmts.push(stmt("R-DASHA-MAHA",
        `The mahadasha of ${lord} runs from ${current.mahadasha.start_date} to ${current.mahadasha.end_date}. ${lord} rules the ${house}th house and is ${P(chart, lord).dignity}. The source expects: ${base}.`,
        "ch. X"));
      if (["debilitated", "enemy", "bitter enemy"].includes(P(chart, lord).dignity)) {
        stmts.push(stmt("R-DASHA-WEAK",
          `${lord} is weak by dignity, so the source would temper the above and expect ailment, unhappiness or obstruction instead.`,
          "ch. X"));
      }
      if (current.antardasha) {
        const sub = current.antardasha;
        stmts.push(stmt("R-DASHA-ANTAR",
          `The bhukti of ${sub.lord} runs from ${sub.start_date} to ${sub.end_date}. The source says the relations between the major lord and the sub-lord decide the result, and that a temporary friendship does not overcome a radical enmity.`,
          "ch. X"));
      }
    }
    sections.push({ title: "Current period (Vimshottari)", statements: stmts });

    /* ---------------- Transits ---------------- */
    if (transit) {
      stmts = [];
      for (const row of transit.gochara) {
        if (!["Jupiter", "Saturn", "Rahu"].includes(row.planet)) continue;
        if (!row.result) continue;
        stmts.push(stmt(`R-TRANSIT-${row.planet.toUpperCase()}`,
          `${row.planet} transits ${row.sign}, the ${row.house_from_moon}th from the Janma Rasi ${transit.janma_rasi}: ${row.result}.`,
          "ch. XII"));
      }
      if (transit.sade_sati.active) {
        stmts.push(stmt("R-TRANSIT-SADESATI",
          "Sade Sati is running: Saturn transits the 12th, 1st or 2nd from the radical Moon. The source warns of quarrels, litigation, failure of business, restlessness, change of place, sickness in the family and mental worry -- unless the ruling period is powerful.",
          "ch. XII"));
      }
      stmts.push(stmt("R-TRANSIT-CAVEAT", transit.weighting, "ch. XII"));
      sections.push({ title: "Transits (gochara) as of today", statements: stmts });
    }

    return {
      sections,
      disclaimer:
        "This is a rule-based reading of a single classical primer, produced by software. It is presented for study and self-reflection, not as medical, financial or legal advice, and not as a factual prediction about any person.",
    };
  }

  JY.interpret = { interpret };
})();
