/* panchanga.js -- the five limbs of the Vedic day (port of panchanga.py). */
(function () {
  const JY = window.JY;
  const D = JY.D;

  function karana(index) {
    if (index === 0) return "Kimstughna";
    if (index >= 57) return ["Shakuni", "Chatushpada", "Naga"][index - 57];
    return D.KARANAS[(index - 1) % 7];
  }

  function compute(localMs, sunLongitude, moonLongitude) {
    const diff = JY.mod360(moonLongitude - sunLongitude);
    const tithiIndex = Math.floor(diff / 12);
    const paksha = tithiIndex < 15 ? "Shukla" : "Krishna";
    const tithiName = D.TITHIS[tithiIndex % 15];
    const tithiFraction = (diff % 12) / 12;
    const yogaIndex = Math.floor(JY.mod360(sunLongitude + moonLongitude) / (360 / 27));
    const karanaIndex = Math.floor(diff / 6);
    /* JS: Sunday = 0, Python weekday(): Monday = 0 -> (wd + 1) % 7 */
    const varaIndex = (new Date(localMs).getUTCDay()) % 7;

    return {
      vara: { index: varaIndex, name: D.VARAS[varaIndex], lord: D.VARA_LORDS[varaIndex] },
      tithi: {
        index: tithiIndex + 1,
        name: tithiName,
        paksha,
        complete_percent: Math.round(tithiFraction * 1000) / 10,
      },
      nakshatra: null,
      yoga: { index: yogaIndex + 1, name: D.YOGAS_PANCHANGA[yogaIndex] },
      karana: { index: karanaIndex + 1, name: karana(karanaIndex) },
    };
  }

  JY.panchanga = { compute };
})();
