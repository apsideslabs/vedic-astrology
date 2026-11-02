/* panchanga-page.js -- the almanac screen: the five limbs for a date and place. */
(function () {
  const JY = window.JY;
  const D = JY.D;
  const A = window.Astronomy;
  const $ = (id) => document.getElementById(id);
  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  const PRESETS = [
    ["Chennai", 13.0827, 80.2707, 5.5],
    ["Delhi", 28.6139, 77.2090, 5.5],
    ["Mumbai", 19.0760, 72.8777, 5.5],
    ["Kolkata", 22.5726, 88.3639, 5.5],
    ["Bengaluru", 12.9716, 77.5946, 5.5],
    ["Hyderabad", 17.3850, 78.4867, 5.5],
    ["Ahmedabad", 23.0225, 72.5714, 5.5],
    ["Pune", 18.5204, 73.8567, 5.5],
    ["Jaipur", 26.9124, 75.7873, 5.5],
    ["Varanasi", 25.3176, 82.9739, 5.5],
    ["Ujjain", 23.1765, 75.7885, 5.5],
    ["London", 51.5074, -0.1278, 0],
  ];

  const fmtTime = (ms, tz) => {
    if (!ms) return "—";
    const d = new Date(ms + tz * 3600000);
    return String(d.getUTCHours()).padStart(2, "0") + ":" +
           String(d.getUTCMinutes()).padStart(2, "0");
  };
  const fmtDate = (ms, tz) => {
    const d = new Date(ms + tz * 3600000);
    return d.toISOString().slice(0, 10);
  };

  function compute() {
    const tz = parseFloat($("tz").value);
    const lat = parseFloat($("lat").value);
    const lon = parseFloat($("lon").value);
    const dateStr = $("date").value;
    const [y, m, d] = dateStr.split("-").map(Number);

    /* local midnight as an instant */
    const localMidnightUtc = Date.UTC(y, m - 1, d, 0, 0, 0) - tz * 3600000;
    const jdMidnight = JY.J2000 + (localMidnightUtc - Date.UTC(2000, 0, 1, 12, 0, 0)) / 86400000;

    const observer = new A.Observer(lat, lon, 10);
    const start = A.MakeTime(new Date(localMidnightUtc - 6 * 3600000));
    const rise = A.SearchRiseSet(A.Body.Sun, observer, +1, start, 1.5);
    const set = A.SearchRiseSet(A.Body.Sun, observer, -1, start, 1.5);
    const moonRise = A.SearchRiseSet(A.Body.Moon, observer, +1, start, 1.5);
    const moonSet = A.SearchRiseSet(A.Body.Moon, observer, -1, start, 1.5);

    /* the panchanga is reckoned from sunrise; fall back to local 06:00 */
    const refMs = rise ? rise.date.getTime() : (localMidnightUtc + 6 * 3600000);
    const jdRef = JY.J2000 + (refMs - Date.UTC(2000, 0, 1, 12, 0, 0)) / 86400000;

    const ay = JY.ayanamsa.lahiri(jdRef);
    const sun = JY.mod360(JY.ephemeris.longitudeOf("Sun", jdRef) - ay);
    const moon = JY.mod360(JY.ephemeris.longitudeOf("Moon", jdRef) - ay);
    const pn = JY.panchanga.compute(localMidnightUtc + 12 * 3600000, sun, moon);

    const dayLengthMin = (rise && set) ? Math.round((set.date.getTime() - rise.date.getTime()) / 60000) : null;
    const phase = ((moon - sun) % 360) / 360;   /* 0 = new, 0.5 = full */
    const illum = (1 - Math.cos(2 * Math.PI * phase)) / 2;

    return { tz, lat, lon, dateStr, rise, set, moonRise, moonSet, refMs, sun, moon,
             pn, dayLengthMin, illum, ay, jdRef };
  }

  function render(r) {
    const pn = r.pn;
    const tithiPct = pn.tithi.complete_percent;
    const phasePct = Math.round(r.illum * 100);

    let h = `<div class="strip">
      <div class="card"><div class="k">Sunrise</div><div class="v">${fmtTime(r.rise ? r.rise.date.getTime() : 0, r.tz)}</div>
        <div class="s">local time</div></div>
      <div class="card"><div class="k">Sunset</div><div class="v">${fmtTime(r.set ? r.set.date.getTime() : 0, r.tz)}</div>
        <div class="s">${r.dayLengthMin ? r.dayLengthMin + " min of daylight" : ""}</div></div>
      <div class="card"><div class="k">Moonrise</div><div class="v">${fmtTime(r.moonRise ? r.moonRise.date.getTime() : 0, r.tz)}</div>
        <div class="s">moonset ${fmtTime(r.moonSet ? r.moonSet.date.getTime() : 0, r.tz)}</div></div>
      <div class="card"><div class="k">Vara</div><div class="v">${esc(pn.vara.name)}</div>
        <div class="s">lord ${esc(pn.vara.lord)}</div></div>
      <div class="card"><div class="k">Moon illum.</div><div class="v">${phasePct}%</div>
        <div class="s">${esc(pn.tithi.paksha)} paksha</div></div>
      <div class="card"><div class="k">Ayanamsa</div><div class="v">${esc(JY.dms(r.ay))}</div>
        <div class="s">Lahiri, at sunrise</div></div>
    </div>`;

    h += `<h2><span class="num">02</span>The five limbs</h2>
      <div class="scroll"><table><thead><tr><th>Anga</th><th>Value</th><th>Detail</th></tr></thead><tbody>
      <tr><td>Tithi</td><td>${esc(pn.tithi.paksha)} ${esc(pn.tithi.name)}</td>
        <td class="muted small">${pn.tithi.index} of 30 · ${tithiPct}% elapsed</td></tr>
      <tr><td>Vara</td><td>${esc(pn.vara.name)}</td>
        <td class="muted small">lord ${esc(pn.vara.lord)}</td></tr>
      <tr><td>Nakshatra</td><td>${esc(JY.nakName(r.moon))}</td>
        <td class="muted small">pada ${JY.pada(r.moon)} · lord ${esc(JY.nakLord(r.moon))} · Moon ${JY.dms(JY.degreeInSign(r.moon))} ${esc(JY.signOf(r.moon))}</td></tr>
      <tr><td>Yoga</td><td>${esc(pn.yoga.name)}</td>
        <td class="muted small">${pn.yoga.index} of 27</td></tr>
      <tr><td>Karana</td><td>${esc(pn.karana.name)}</td>
        <td class="muted small">${pn.karana.index} of 60</td></tr>
      </tbody></table></div>`;

    h += `<h2><span class="num">03</span>Sidereal positions at sunrise</h2>
      <div class="scroll"><table><thead><tr>
        <th>Graha</th><th>Sign</th><th>Degree</th><th>Nakshatra</th><th>Pada</th></tr></thead><tbody>
      <tr><td>Sun</td><td>${esc(JY.signOf(r.sun))}</td>
        <td class="num">${JY.dms(JY.degreeInSign(r.sun))}</td>
        <td>${esc(JY.nakName(r.sun))}</td><td class="num">${JY.pada(r.sun)}</td></tr>
      <tr><td>Moon</td><td>${esc(JY.signOf(r.moon))}</td>
        <td class="num">${JY.dms(JY.degreeInSign(r.moon))}</td>
        <td>${esc(JY.nakName(r.moon))}</td><td class="num">${JY.pada(r.moon)}</td></tr>
      </tbody></table></div>
      <p class="small muted" style="margin-top:12px">Reckoned at sunrise
        (${fmtTime(r.refMs, r.tz)} local), which is the convention for the panchanga.
        Computed in the browser; no request leaves the page.</p>`;

    $("out").innerHTML = h;
    $("out").classList.remove("hidden");
    $("empty").classList.add("hidden");
  }

  function run() {
    try {
      render(compute());
    } catch (ex) {
      $("err").textContent = "Could not compute the panchanga: " + ex.message;
      $("err").classList.remove("hidden");
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    const sel = $("preset");
    for (const [name, lat, lon, tz] of PRESETS) {
      const o = document.createElement("option");
      o.value = `${lat}|${lon}|${tz}|${name}`;
      o.textContent = name;
      sel.appendChild(o);
    }
    sel.value = `${PRESETS[0][1]}|${PRESETS[0][2]}|${PRESETS[0][3]}|${PRESETS[0][0]}`;
    sel.addEventListener("change", () => {
      if (!sel.value) return;
      const [lat, lon, tz] = sel.value.split("|");
      $("lat").value = lat; $("lon").value = lon; $("tz").value = tz;
      run();
    });
    $("date").value = new Date().toISOString().slice(0, 10);
    $("f").addEventListener("submit", (e) => { e.preventDefault(); run(); });
    for (const id of ["date", "lat", "lon", "tz"]) {
      $(id).addEventListener("change", run);
    }
    run();
  });
})();
