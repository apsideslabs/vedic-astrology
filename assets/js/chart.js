/* chart.js -- strength, dignity and the chart builder.
 *
 * A browser port of src/jyotish/{strength,chart}.py.
 */
(function () {
  const JY = window.JY;
  const D = JY.D;
  const E = JY.ephemeris;

  /* ---------------------------------------------------------------- *
   * Strength and dignity
   * ---------------------------------------------------------------- */
  function naturalRelation(planet, other) {
    if (planet === other) return "own";
    const t = D.NATURAL_FRIENDS[planet];
    if (!t) return "neutral";
    if (t.friends.includes(other)) return "friend";
    if (t.enemies.includes(other)) return "enemy";
    return "neutral";
  }

  /* SOURCE: ch. I, "Temporary Friendship" -- 2,3,4,10,11,12 are friends. */
  function temporaryRelation(planetSign, otherSign) {
    if (planetSign === otherSign) return "own";
    const distance = JY.houseFrom(planetSign, otherSign);
    return [2, 3, 4, 10, 11, 12].includes(distance) ? "friend" : "enemy";
  }

  /* SOURCE: ch. I, "Mixed Relations". */
  function compoundRelation(planet, other, signs) {
    if (planet === other) return "own";
    const nat = naturalRelation(planet, other);
    if (!signs || !signs[planet] || !signs[other]) return nat;
    const temp = temporaryRelation(signs[planet], signs[other]);
    if (nat === "friend") return temp === "friend" ? "intimate friend" : "friend";
    if (nat === "enemy") return temp === "enemy" ? "bitter enemy" : "neutral";
    return temp === "friend" ? "friend" : "enemy";
  }

  function dignity(planet, longitude, signs) {
    const sign = JY.signOf(longitude);
    const deg = JY.degreeInSign(longitude);

    const exalt = D.EXALTATION[planet];
    if (exalt && exalt[0] === sign) return "exalted";
    const deb = D.DEBILITATION[planet];
    if (deb && deb[0] === sign) return "debilitated";

    const mool = D.MOOLATRIKONA[planet];
    if (mool && mool[0] === sign && deg >= mool[1] && deg <= mool[2]) return "moolatrikona";

    if (JY.lordOfSign(sign) === planet) return "own";
    return compoundRelation(planet, JY.lordOfSign(sign), signs);
  }

  function isCombust(planet, longitude, sunLongitude, retrograde) {
    if (["Sun", "Rahu", "Ketu"].includes(planet)) return false;
    let orb = D.COMBUSTION_ORB[planet];
    if (orb === undefined) return false;
    if (retrograde && D.COMBUSTION_ORB_RETRO[planet] !== undefined) {
      orb = D.COMBUSTION_ORB_RETRO[planet];
    }
    const diff = Math.abs((JY.mod360(longitude - sunLongitude + 180) - 180));
    return diff <= orb;
  }

  function positionalStrength(planet, longitude, house, opts) {
    const o = opts || {};
    const dig = dignity(planet, longitude, o.signs);
    const components = { dignity: D.DIGNITY_POINTS[dig] };

    const kind = D.HOUSE_KIND[String(house)] || "apoklima";
    components.house = D.HOUSE_POINTS[kind];
    if (D.TRIKONAS.includes(house)) components.trine = D.TRINE_BONUS;
    components.digbala = D.DIGBALA_HOUSE[planet] === house ? 0.5 : 0.0;
    components.chestabala = o.retrograde ? 0.25 : 0.0;
    components.combustion = o.combust ? -0.75 : 0.0;

    let vargottama = false;
    if (o.navamsaSign) {
      vargottama = o.navamsaSign === JY.signOf(longitude);
      components.vargottama = vargottama ? 0.5 : 0.0;
    }

    const raw = Object.values(components).reduce((a, b) => a + b, 0);
    const score = Math.max(0, Math.min(100, ((raw + 3.25) / 7.75) * 100));
    return {
      dignity: dig,
      dignity_points: D.DIGNITY_POINTS[dig],
      house_kind: kind,
      vargottama,
      components,
      raw: Math.round(raw * 100) / 100,
      score: Math.round(score * 10) / 10,
    };
  }

  JY.strength = {
    naturalRelation,
    temporaryRelation,
    compoundRelation,
    dignity,
    isCombust,
    positionalStrength,
  };

  /* ---------------------------------------------------------------- *
   * Aspects -- SOURCE: ch. I, "Drishti or Aspect"
   * ---------------------------------------------------------------- */
  function computeAspects(signs) {
    const out = [];
    for (const a of D.PLANETS) {
      if (!signs[a]) continue;
      const allowed = D.SPECIAL_ASPECTS[a] || D.DEFAULT_ASPECTS;
      for (const b of D.PLANETS) {
        if (a === b || !signs[b]) continue;
        const distance = JY.houseFrom(signs[a], signs[b]);
        if (!allowed.includes(distance)) continue;
        const special = (D.SPECIAL_ASPECTS[a] || []).includes(distance);
        out.push({
          from: a,
          to: b,
          house_distance: distance,
          kind: distance !== 7 && special ? "special" : "full",
          sight: D.PARTIAL_SIGHT[String(distance)] !== undefined
            ? D.PARTIAL_SIGHT[String(distance)] : 1.0,
          benefic: D.NATURAL_BENEFICS.includes(a),
        });
      }
    }
    return out;
  }

  function aspectedHouses(planet, sign) {
    const out = [];
    for (const distance of D.SPECIAL_ASPECTS[planet] || D.DEFAULT_ASPECTS) {
      const target = D.SIGNS[(D.SIGNS.indexOf(sign) + distance - 1) % 12];
      out.push({
        house: distance,
        sign: target,
        sight: distance === 7 ? 1.0
          : (D.PARTIAL_SIGHT[String(distance)] !== undefined ? D.PARTIAL_SIGHT[String(distance)] : 1.0),
        special: (D.SPECIAL_ASPECTS[planet] || []).includes(distance),
      });
    }
    return out;
  }

  /* ---------------------------------------------------------------- *
   * Birth data
   * ---------------------------------------------------------------- */
  function parseLocal(dateStr, timeStr) {
    const [y, m, d] = dateStr.split("-").map(Number);
    const parts = timeStr.split(":").map(Number);
    while (parts.length < 3) parts.push(0);
    return new Date(Date.UTC(y, m - 1, d, parts[0], parts[1], parts[2]));
  }

  /* ---------------------------------------------------------------- *
   * buildChart
   * ---------------------------------------------------------------- */
  function buildChart(birth) {
    const localMs = parseLocal(birth.date, birth.time).getTime();
    const tz = birth.tz_offset === undefined ? 5.5 : birth.tz_offset;
    const utcMs = localMs - tz * 3600000;
    const jd = JY.J2000 + (utcMs - Date.UTC(2000, 0, 1, 12, 0, 0)) / 86400000;

    const ayanamsaModel = birth.ayanamsa || "lahiri";
    const houseSystem = birth.house_system || "whole_sign";
    const ay = JY.ayanamsa.value(ayanamsaModel, jd);

    const tropical = E.tropicalLongitudes(jd);
    const eps = E.obliquity(jd);
    const lst = E.localSiderealDegrees(jd, birth.longitude);
    const ascTrop = E.ascendant(lst, birth.latitude, eps);
    const mcTrop = E.midheaven(lst, eps);
    const cuspMap = E.cusps(houseSystem, lst, birth.latitude, eps);

    const asc = JY.mod360(ascTrop - ay);
    const lagnaSign = JY.signOf(asc);
    const cuspsSidereal = {};
    for (const h of Object.keys(cuspMap)) cuspsSidereal[h] = JY.mod360(cuspMap[h] - ay);

    const signs = {};
    for (const p of D.PLANETS) signs[p] = JY.signOf(JY.mod360(tropical[p].longitude - ay));
    const sunLon = JY.mod360(tropical.Sun.longitude - ay);

    const planets = {};
    for (const planet of D.PLANETS) {
      const data = tropical[planet];
      const sid = JY.mod360(data.longitude - ay);
      const retro = data.speed < 0;
      const house = JY.houseFrom(lagnaSign, JY.signOf(sid));
      const nav = JY.navamsaSign(sid);
      const combust = isCombust(planet, sid, sunLon, retro);
      const st = positionalStrength(planet, sid, house, {
        signs, retrograde: retro, combust, navamsaSign: nav,
      });
      planets[planet] = {
        planet,
        longitude: sid,
        tropical_longitude: data.longitude,
        latitude: data.latitude,
        speed: Math.round(data.speed * 1e5) / 1e5,
        retrograde: retro,
        sign: JY.signOf(sid),
        sign_index: JY.signIndex(sid),
        degree_in_sign: JY.degreeInSign(sid),
        nakshatra: JY.nakName(sid),
        nakshatra_index: JY.nakIndex(sid),
        pada: JY.pada(sid),
        nakshatra_lord: JY.nakLord(sid),
        navamsa_sign: nav,
        house,
        dignity: st.dignity,
        combust,
        strength: st,
        sign_glyph: D.SIGN_GLYPHS[JY.signIndex(sid)],
        planet_glyph: D.PLANET_GLYPHS[planet],
        longitude_dms: JY.dms(sid),
        degree_in_sign_dms: JY.dms(JY.degreeInSign(sid)),
      };
    }

    const houses = [];
    for (let h = 1; h <= 12; h++) {
      const sign = houseSystem !== "whole_sign"
        ? JY.signOf(cuspsSidereal[String(h)])
        : D.SIGNS[(D.SIGNS.indexOf(lagnaSign) + h - 1) % 12];
      const lord = JY.lordOfSign(sign);
      houses.push({
        house: h,
        sign,
        sign_index: D.SIGNS.indexOf(sign),
        lord,
        lord_house: planets[lord].house,
        cusp_tropical: Math.round(cuspMap[h] * 1e4) / 1e4,
        cusp_sidereal: Math.round(cuspsSidereal[String(h)] * 1e4) / 1e4,
        occupants: D.PLANETS.filter((p) => planets[p].house === h),
        kind: D.HOUSE_KIND[String(h)],
        significations: D.HOUSE_SIGNIFICATIONS[String(h)],
      });
    }

    const chart = {
      birth: {
        name: birth.name || "",
        place: birth.place || "",
        local: new Date(localMs).toISOString().slice(0, 19),
        tz_offset: tz,
        utc: new Date(utcMs).toISOString().slice(0, 19) + "Z",
        jd_ut: Math.round(jd * 1e6) / 1e6,
        latitude: birth.latitude,
        longitude: birth.longitude,
      },
      ayanamsa: { model: ayanamsaModel, value: Math.round(ay * 1e6) / 1e6, dms: JY.dms(ay) },
      house_system: houseSystem,
      lagna: {
        longitude: Math.round(asc * 1e6) / 1e6,
        dms: JY.dms(asc),
        sign: lagnaSign,
        sign_index: D.SIGNS.indexOf(lagnaSign),
        degree_in_sign: Math.round((asc % 30) * 1e6) / 1e6,
        nakshatra: JY.nakName(asc),
        pada: JY.pada(asc),
        lord: JY.lordOfSign(lagnaSign),
        navamsa_sign: JY.navamsaSign(asc),
        moon_sign: planets.Moon.sign,
      },
      planets: D.PLANETS.map((p) => planets[p]),
      houses,
      aspects: computeAspects(signs),
      aspects_by_house: {},
      meta: {
        engine: "jyotish (browser)",
        ephemeris: "astronomy-engine",
        node: "mean",
        note: "Strength figures are a simplified positional score, not Shadbala.",
      },
      _signs: signs,
      _planets: planets,
      _asc: asc,
    };
    for (const p of D.PLANETS) chart.aspects_by_house[p] = aspectedHouses(p, signs[p]);

    /* helpers the reading needs */
    chart.planetsInHouse = (h) => D.PLANETS.filter((p) => planets[p].house === h);
    chart.planetsInSign = (s) => D.PLANETS.filter((p) => planets[p].sign === s);
    chart.lordOfSign = JY.lordOfSign;
    chart.moonSign = () => planets.Moon.sign;

    chart.panchanga = JY.panchanga.compute(localMs, planets.Sun.longitude, planets.Moon.longitude);
    chart.vimshottari = JY.dasha.vimshottari(planets.Moon.longitude, utcMs);
    chart.yogas = JY.yogas.detect(chart);
    return chart;
  }

  JY.buildChart = buildChart;
})();
