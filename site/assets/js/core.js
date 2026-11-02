/* core.js -- namespace, zodiac helpers, ayanamsa.
 *
 * A browser port of src/jyotish/{zodiac,ayanamsa}.py.  The data tables come
 * from data.js, which is generated from the Python source so that the two
 * implementations cannot drift apart.
 */
(function () {
  const D = window.JY_DATA;
  const JY = (window.JY = window.JY || {});
  JY.D = D;

  JY.SIGN_SPAN = 30.0;
  JY.NAK_SPAN = 360.0 / 27.0;          // 13 deg 20 min
  JY.PADA_SPAN = JY.NAK_SPAN / 4.0;    // 3 deg 20 min
  JY.J2000 = 2451545.0;

  const mod360 = (x) => ((x % 360) + 360) % 360;
  JY.mod360 = mod360;

  JY.signIndex = (lon) => Math.floor(mod360(lon) / 30.0);
  JY.signOf = (lon) => D.SIGNS[JY.signIndex(lon)];
  JY.degreeInSign = (lon) => mod360(lon) % 30.0;

  JY.nakIndex = (lon) => Math.floor(mod360(lon) / JY.NAK_SPAN);
  JY.nakName = (lon) => D.NAKSHATRAS[JY.nakIndex(lon)];
  JY.pada = (lon) => Math.floor((mod360(lon) % JY.NAK_SPAN) / JY.PADA_SPAN) + 1;
  JY.nakLord = (lon) => D.NAKSHATRA_LORDS[JY.nakIndex(lon)];

  /* Navamsa by the continuous 3 deg 20 min division; verified against the
   * worked example in chapter II of the source. */
  JY.navamsaSignIndex = (lon) => Math.floor(mod360(lon) / JY.PADA_SPAN) % 12;
  JY.navamsaSign = (lon) => D.SIGNS[JY.navamsaSignIndex(lon)];

  JY.houseFrom = (signA, signB) =>
    ((D.SIGNS.indexOf(signB) - D.SIGNS.indexOf(signA)) % 12 + 12) % 12 + 1;

  JY.lordOfSign = (sign) => D.SIGN_LORDS[D.SIGNS.indexOf(sign)];

  JY.dms = function (value, seconds = true) {
    const sign = value < 0 ? "-" : "";
    value = Math.abs(value);
    const d = Math.floor(value);
    const mFull = (value - d) * 60;
    const m = Math.floor(mFull);
    const s = (mFull - m) * 60;
    if (!seconds) return `${sign}${d}\u00b0${String(m).padStart(2, "0")}'`;
    return `${sign}${d}\u00b0${String(m).padStart(2, "0")}'${s.toFixed(1).padStart(4, "0")}"`;
  };

  /* ------------------------------------------------------------------ *
   * Ayanamsa
   * ------------------------------------------------------------------ */
  const LAHIRI_J2000 = 23.0 + 51.0 / 60.0 + 11.5 / 3600.0;   // 23d51'11.5"
  const PREC = [5028.796195, 1.1054348, 0.00007964, -0.000023857, -0.0000000383];

  function precessionInLongitude(jd) {
    const t = (jd - JY.J2000) / 36525.0;
    let arcsec = 0.0;
    for (let i = 0; i < PREC.length; i++) arcsec += PREC[i] * Math.pow(t, i + 1);
    return arcsec / 3600.0;
  }

  function jdToYear(jd) {
    return 2000.0 + (jd - JY.J2000) / 365.25;
  }

  JY.ayanamsa = {
    lahiri: (jd) => LAHIRI_J2000 + precessionInLongitude(jd),
    raman397: (jd, year) =>
      ((year === undefined ? jdToYear(jd) : year) - 397.0) * (50.0 + 1.0 / 3.0) / 3600.0,
    value: function (name, jd, year) {
      if (name === "lahiri") return this.lahiri(jd);
      if (name === "raman_397") return this.raman397(jd, year);
      throw new Error(`unknown ayanamsa model '${name}'`);
    },
    precessionInLongitude,
    jdToYear,
  };
})();
