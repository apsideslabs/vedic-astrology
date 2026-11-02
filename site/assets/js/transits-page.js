/* transits-page.js -- the transit board: where the nine grahas are right now,
 * which house that is from a chosen Janma Rasi, and when each next changes sign. */
(function () {
  const JY = window.JY;
  const D = JY.D;
  const $ = (id) => document.getElementById(id);
  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  const STEP = { Moon: 0.2, Sun: 0.5, Mercury: 0.5, Venus: 1, Mars: 2, Jupiter: 4, Saturn: 6, Rahu: 8, Ketu: 8 };

  function siderealAt(planet, jd, ayModel) {
    const ay = JY.ayanamsa.value(ayModel, jd);
    return JY.mod360(JY.ephemeris.longitudeOf(planet, jd) - ay);
  }

  /* Scan forward for the next sign change, then bisect to the minute. */
  function nextIngress(planet, jd0, ayModel) {
    const startSign = JY.signIndex(siderealAt(planet, jd0, ayModel));
    const step = STEP[planet] || 2;
    let prev = jd0;
    for (let i = 1; i <= 900; i++) {
      const cur = jd0 + i * step;
      if (JY.signIndex(siderealAt(planet, cur, ayModel)) !== startSign) {
        let lo = prev, hi = cur;
        for (let k = 0; k < 24; k++) {
          const mid = (lo + hi) / 2;
          if (JY.signIndex(siderealAt(planet, mid, ayModel)) === startSign) lo = mid;
          else hi = mid;
        }
        return { jd: hi, sign: JY.signOf(siderealAt(planet, hi, ayModel)) };
      }
      prev = cur;
    }
    return null;
  }

  function fmtDate(ms) {
    return new Date(ms).toISOString().slice(0, 10);
  }

  function run() {
    try {
      const janma = $("rasi").value;
      const ayModel = $("ayanamsa").value;
      const nowMs = Date.now();
      const jd = JY.J2000 + (nowMs - Date.UTC(2000, 0, 1, 12, 0, 0)) / 86400000;
      const positions = JY.transits.currentPositions(jd, ayModel);
      const rows = JY.transits.gochara(janma, positions);
      const saturn = rows.find((r) => r.planet === "Saturn");

      let h = `<div class="strip">
        <div class="card"><div class="k">Janma Rasi</div><div class="v">${esc(janma)}</div>
          <div class="s">gochara is read from the Moon</div></div>
        <div class="card"><div class="k">Sade Sati</div>
          <div class="v">${saturn.sade_sati ? "Active" : "Not active"}</div>
          <div class="s">Saturn ${saturn.house_from_moon}th from the Moon</div></div>
        <div class="card"><div class="k">As of</div>
          <div class="v">${esc(new Date(nowMs).toISOString().slice(11, 16))}</div>
          <div class="s">${esc(fmtDate(nowMs))} UTC</div></div>
        <div class="card"><div class="k">Ayanamsa</div>
          <div class="v">${esc(JY.dms(JY.ayanamsa.value(ayModel, jd)))}</div>
          <div class="s">${esc(ayModel)}</div></div>
      </div>`;

      h += `<h2><span class="num">02</span>Gochara from ${esc(janma)}</h2>
        <div class="scroll"><table><thead><tr>
        <th>Graha</th><th>Transit sign</th><th>Degree</th><th>From Moon</th><th>Result</th></tr></thead><tbody>`;
      for (const r of rows) {
        const pos = positions[r.planet];
        h += `<tr><td>${D.PLANET_GLYPHS[r.planet]} ${esc(r.planet)}</td>
          <td>${esc(r.sign)}</td>
          <td class="num">${JY.dms(pos.degree_in_sign)}</td>
          <td class="num">${r.house_from_moon}</td>
          <td>${r.result ? esc(r.result) : '<span class="chip">not legible in source</span>'}
          ${r.sade_sati ? '<span class="chip bad">Sade Sati</span>' : ""}</td></tr>`;
      }
      h += `</tbody></table></div>`;

      h += `<h2><span class="num">03</span>Next sign ingress</h2>
        <div class="scroll"><table><thead><tr>
        <th>Graha</th><th>Now in</th><th>Enters</th><th>Date</th></tr></thead><tbody>`;
      for (const planet of D.PLANETS) {
        const ing = nextIngress(planet, jd, ayModel);
        const nowSign = positions[planet].sign;
        if (!ing) {
          h += `<tr><td>${esc(planet)}</td><td>${esc(nowSign)}</td><td>—</td><td>—</td></tr>`;
          continue;
        }
        const ms = (ing.jd - JY.J2000) * 86400000 + Date.UTC(2000, 0, 1, 12, 0, 0);
        const days = Math.round((ms - nowMs) / 86400000);
        h += `<tr><td>${esc(planet)}</td><td>${esc(nowSign)}</td>
          <td>${esc(ing.sign)}</td>
          <td class="num">${fmtDate(ms)} <span class="muted small">in ${days}d</span></td></tr>`;
      }
      h += `</tbody></table></div>
        <p class="small muted" style="margin-top:12px">Ingress dates are computed by
        scanning forward and bisecting to the minute in the selected ayanamsa. They
        are indicative to within a few hours for the slow planets near a station.</p>`;

      $("out").innerHTML = h;
      $("out").classList.remove("hidden");
    } catch (ex) {
      $("err").textContent = "Could not compute transits: " + ex.message;
      $("err").classList.remove("hidden");
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    const sel = $("rasi");
    for (const s of D.SIGNS) {
      const o = document.createElement("option");
      o.value = s;
      o.textContent = s;
      sel.appendChild(o);
    }
    /* default to the reader's own Janma Rasi if they arrive from a chart link */
    sel.value = "Aries";
    $("f").addEventListener("submit", (e) => { e.preventDefault(); run(); });
    sel.addEventListener("change", run);
    $("ayanamsa").addEventListener("change", run);
    run();
  });
})();
