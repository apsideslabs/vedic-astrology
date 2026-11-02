/* ephemeris.js -- positions, sidereal time, obliquity, ascendant, cusps.
 *
 * A browser port of src/jyotish/{ephemeris,houses}.py, using the vendored
 * astronomy-engine build.  Same bodies, same frame, same conventions:
 * apparent geocentric tropical longitude of date, mean lunar node for
 * Rahu/Ketu.
 */
(function () {
  const JY = window.JY;
  const A = window.Astronomy;
  const D = JY.D;

  const MS_PER_DAY = 86400000;
  const J2000_MS = Date.UTC(2000, 0, 1, 12, 0, 0);

  const BODIES = {
    Sun: A.Body.Sun,
    Moon: A.Body.Moon,
    Mars: A.Body.Mars,
    Mercury: A.Body.Mercury,
    Jupiter: A.Body.Jupiter,
    Venus: A.Body.Venus,
    Saturn: A.Body.Saturn,
  };

  const jdToDate = (jd) => new Date(J2000_MS + (jd - JY.J2000) * MS_PER_DAY);
  const dateToJd = (date) => JY.J2000 + (date.getTime() - J2000_MS) / MS_PER_DAY;

  JY.jdToDate = jdToDate;
  JY.dateToJd = dateToJd;

  function eclipticLongitude(body, time) {
    if (body === "Moon") {
      const sph = A.EclipticGeoMoon(time);
      return [JY.mod360(sph.lon), sph.lat];
    }
    const vec = A.GeoVector(BODIES[body], time, true);
    const ecl = A.Ecliptic(vec);
    return [JY.mod360(ecl.elon), ecl.elat];
  }

  function signedDelta(later, earlier) {
    let d = JY.mod360(later - earlier);
    return d > 180.0 ? d - 360.0 : d;
  }

  /* Mean longitude of the Moon's ascending node (Rahu) -- Meeus ch. 47. */
  function meanNode(jd) {
    const t = (jd - JY.J2000) / 36525.0;
    const omega =
      125.0445479 -
      1934.1362891 * t +
      0.0020754 * t * t +
      Math.pow(t, 3) / 467441.0 -
      Math.pow(t, 4) / 60616000.0;
    return JY.mod360(omega);
  }

  function tropicalLongitudes(jd, withSpeed = true) {
    const date = jdToDate(jd);
    const time = A.MakeTime(date);
    const out = {};
    for (const planet of D.SEVEN_GRAHAS) {
      const [lon, lat] = eclipticLongitude(planet, time);
      let speed = 0.0;
      if (withSpeed) {
        const before = eclipticLongitude(planet, A.MakeTime(new Date(date.getTime() - MS_PER_DAY / 2)))[0];
        const after = eclipticLongitude(planet, A.MakeTime(new Date(date.getTime() + MS_PER_DAY / 2)))[0];
        speed = signedDelta(after, before);
      }
      out[planet] = { longitude: lon, latitude: lat, speed };
    }
    const rahu = meanNode(jd);
    out.Rahu = { longitude: rahu, latitude: 0.0, speed: -0.0529539 };
    out.Ketu = { longitude: JY.mod360(rahu + 180.0), latitude: 0.0, speed: -0.0529539 };
    return out;
  }

  /* Mean obliquity of the ecliptic (IAU 1980, Meeus 22.2). */
  function obliquity(jd) {
    const t = (jd - JY.J2000) / 36525.0;
    const arcsec = 84381.448 - 46.815 * t - 0.00059 * t * t + 0.001813 * Math.pow(t, 3);
    return arcsec / 3600.0;
  }

  function siderealTimeHours(jd) {
    return JY.mod360(A.SiderealTime(A.MakeTime(jdToDate(jd))) * 15.0) / 15.0;
  }

  function localSiderealDegrees(jd, longitudeEast) {
    return JY.mod360(siderealTimeHours(jd) * 15.0 + longitudeEast);
  }

  function ascendant(lstDeg, latitude, epsDeg) {
    const ramc = (lstDeg * Math.PI) / 180;
    const eps = (epsDeg * Math.PI) / 180;
    const phi = (latitude * Math.PI) / 180;
    const y = Math.cos(ramc);
    const x = -(Math.sin(ramc) * Math.cos(eps) + Math.tan(phi) * Math.sin(eps));
    return JY.mod360((Math.atan2(y, x) * 180) / Math.PI);
  }

  function midheaven(lstDeg, epsDeg) {
    const ramc = (lstDeg * Math.PI) / 180;
    const eps = (epsDeg * Math.PI) / 180;
    return JY.mod360(
      (Math.atan2(Math.sin(ramc), Math.cos(ramc) * Math.cos(eps)) * 180) / Math.PI
    );
  }

  /* ---------------------------------------------------------------- *
   * House systems -- port of houses.py
   * ---------------------------------------------------------------- */
  function cusps(system, lstDeg, latitude, epsDeg) {
    const asc = ascendant(lstDeg, latitude, epsDeg);
    const mc = midheaven(lstDeg, epsDeg);
    const ic = JY.mod360(mc + 180.0);
    const desc = JY.mod360(asc + 180.0);
    const out = {};

    if (system === "whole_sign") {
      const start = Math.floor(asc / 30.0) * 30.0;
      for (let h = 1; h <= 12; h++) out[h] = JY.mod360(start + 30.0 * (h - 1));
      return out;
    }
    if (system === "equal") {
      for (let h = 1; h <= 12; h++) out[h] = JY.mod360(asc + 30.0 * (h - 1));
      return out;
    }
    if (system !== "sripati") throw new Error(`unknown house system '${system}'`);

    const arc = (a, b) => JY.mod360(b - a);
    const q1 = arc(mc, asc);
    const q2 = arc(asc, ic);
    out[10] = mc;
    out[1] = asc;
    out[4] = ic;
    out[7] = desc;
    out[11] = JY.mod360(mc + q1 / 3.0);
    out[12] = JY.mod360(mc + (2.0 * q1) / 3.0);
    out[2] = JY.mod360(asc + q2 / 3.0);
    out[3] = JY.mod360(asc + (2.0 * q2) / 3.0);
    out[5] = JY.mod360(out[4] + arc(ic, desc) / 3.0);
    out[6] = JY.mod360(out[4] + (2.0 * arc(ic, desc)) / 3.0);
    out[8] = JY.mod360(desc + arc(desc, mc) / 3.0);
    out[9] = JY.mod360(desc + (2.0 * arc(desc, mc)) / 3.0);
    return out;
  }

  /* A single body's apparent tropical longitude -- cheaper than the full set,
   * for scanning forward to the next sign ingress. */
  function longitudeOf(planet, jd) {
    if (planet === "Rahu") return meanNode(jd);
    if (planet === "Ketu") return JY.mod360(meanNode(jd) + 180.0);
    return eclipticLongitude(planet, A.MakeTime(jdToDate(jd)))[0];
  }

  JY.ephemeris = {
    tropicalLongitudes,
    longitudeOf,
    meanNode,
    obliquity,
    siderealTimeHours,
    localSiderealDegrees,
    ascendant,
    midheaven,
    cusps,
  };
})();
