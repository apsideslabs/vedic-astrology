/* ui.js -- the chart page: read the form, run the engine in the browser, render. */
(function () {
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
    ["Madras, 1935 (the book's example)", 13.0, 77.5833333, 5.1722222],
  ];

  const SOUTH_INDIAN_ORDER = [
    "Pisces", "Aries", "Taurus", "Gemini",
    "Aquarius", null, null, "Cancer",
    "Capricorn", null, null, "Leo",
    "Sagittarius", "Scorpio", "Libra", "Virgo",
  ];

  function gridHTML(cells, title) {
    return `<div class="chartbox"><h3>${esc(title)}</h3><div class="si">` +
      cells.map((c) => {
        if (c.kind === "blank") return `<div class="cell blank"></div>`;
        return `<div class="cell${c.lagna ? " lagna" : ""}">
          <div class="sg">${c.glyph} ${esc(c.sign)}</div>
          ${c.lagna ? `<div class="lag">LAGNA</div>` : ""}
          ${c.planets.map((p) =>
            `<div class="pl">${p.glyph} ${esc(p.planet.slice(0, 3))} <span class="d">${p.degree.toFixed(1)}${p.retrograde ? "R" : ""}</span></div>`
          ).join("")}
        </div>`;
      }).join("") + `</div></div>`;
  }

  function southIndian(chart, navamsa) {
    const D = window.JY.D;
    return SOUTH_INDIAN_ORDER.map((slot) => {
      if (slot === null) return { kind: "blank" };
      let occupants, lagna;
      if (navamsa) {
        occupants = D.PLANETS.filter((p) => chart._planets[p].navamsa_sign === slot);
        lagna = slot === window.JY.navamsaSign(chart._asc);
      } else {
        occupants = D.PLANETS.filter((p) => chart._planets[p].sign === slot);
        lagna = slot === chart.lagna.sign;
      }
      return {
        kind: "sign", sign: slot, glyph: D.SIGN_GLYPHS[D.SIGNS.indexOf(slot)], lagna,
        planets: occupants.map((p) => ({
          planet: p,
          glyph: D.PLANET_GLYPHS[p],
          degree: chart._planets[p].degree_in_sign,
          retrograde: chart._planets[p].retrograde,
        })),
      };
    });
  }

  function render(chart, transit, reading) {
    const l = chart.lagna, b = chart.birth, pn = chart.panchanga;
    const cur = chart.vimshottari.current;
    const D = window.JY.D;
    let html = "";

    html += `<div class="strip">
      <div class="card"><div class="k">Ascendant</div><div class="v">${esc(l.sign)} ${window.JY.dms(l.degree_in_sign)}</div>
        <div class="s">${esc(l.nakshatra)} pada ${l.pada} · lord ${esc(l.lord)}</div></div>
      <div class="card"><div class="k">Moon (Janma Rasi)</div><div class="v">${esc(l.moon_sign)}</div>
        <div class="s">${esc(chart.vimshottari.janma_nakshatra)} · lord ${esc(chart.vimshottari.janma_nakshatra_lord)}</div></div>
      <div class="card"><div class="k">Birth</div><div class="v">${esc(b.local.replace("T", " "))}</div>
        <div class="s">UT ${esc(b.utc)} · ${b.latitude.toFixed(3)}, ${b.longitude.toFixed(3)}</div></div>
      <div class="card"><div class="k">Ayanamsa</div><div class="v">${esc(chart.ayanamsa.dms)}</div>
        <div class="s">${esc(chart.ayanamsa.model)} · JD ${b.jd_ut.toFixed(5)}</div></div>
      <div class="card"><div class="k">Panchanga</div><div class="v">${esc(pn.tithi.paksha)} ${esc(pn.tithi.name)}</div>
        <div class="s">${esc(pn.vara.name)} · ${esc(pn.yoga.name)} yoga · ${esc(pn.karana.name)}</div></div>
      <div class="card"><div class="k">Current period</div>
        <div class="v">${cur.mahadasha ? esc(cur.mahadasha.lord) : "—"}${cur.antardasha ? " / " + esc(cur.antardasha.lord) : ""}</div>
        <div class="s">${cur.mahadasha ? esc(cur.mahadasha.start_date) + " → " + esc(cur.mahadasha.end_date) : ""}</div></div>
    </div>`;

    html += `<h2>Rasi and Navamsa</h2><div class="grids">
      ${gridHTML(southIndian(chart, false), "Rasi chakra (whole sign)")}
      ${gridHTML(southIndian(chart, true), "Navamsa (D9)")}
    </div>`;

    html += `<h2>Grahas</h2><div class="scroll"><table><thead><tr>
      <th>Graha</th><th>Sign</th><th>Degree</th><th>Nakshatra</th><th>Pada</th>
      <th>House</th><th>Dignity</th><th>Navamsa</th><th>Strength</th><th>Flags</th>
      </tr></thead><tbody>`;
    for (const p of chart.planets) {
      const flags = [];
      if (p.retrograde) flags.push("retrograde");
      if (p.combust) flags.push("combust");
      html += `<tr>
        <td>${p.planet_glyph} ${esc(p.planet)}</td>
        <td>${esc(p.sign)}</td>
        <td class="num">${window.JY.dms(p.degree_in_sign)}</td>
        <td>${esc(p.nakshatra)}</td>
        <td class="num">${p.pada}</td>
        <td class="num">${p.house}</td>
        <td>${esc(p.dignity)}</td>
        <td>${esc(p.navamsa_sign)}</td>
        <td class="num">${p.strength.score}</td>
        <td>${flags.map((f) => `<span class="pill">${f}</span>`).join(" ") || "—"}</td>
      </tr>`;
    }
    html += `</tbody></table></div>`;

    html += `<h2>Bhavas</h2><div class="scroll"><table><thead><tr>
      <th>House</th><th>Sign</th><th>Lord</th><th>Lord in</th><th>Occupants</th><th>Significations</th>
      </tr></thead><tbody>`;
    for (const h of chart.houses) {
      html += `<tr><td class="num">${h.house}</td><td>${esc(h.sign)}</td><td>${esc(h.lord)}</td>
        <td class="num">${h.lord_house}</td>
        <td>${h.occupants.length ? h.occupants.map(esc).join(", ") : "—"}</td>
        <td class="muted">${esc(h.significations)}</td></tr>`;
    }
    html += `</tbody></table></div>`;

    const v = chart.vimshottari, bal = v.balance_at_birth;
    html += `<h2>Vimshottari dasha</h2>
      <p class="muted small">Balance of ${esc(bal.lord)} at birth: ${bal.years}y ${bal.months}m ${bal.days}d.
      Years of 365.25 days.</p>
      <div class="scroll"><table><thead><tr><th>Mahadasha</th><th>From</th><th>To</th></tr></thead><tbody>`;
    for (const m of v.mahadashas) {
      const isNow = cur.mahadasha && cur.mahadasha.lord === m.lord;
      html += `<tr class="${isNow ? "now" : ""}"><td>${esc(m.lord)}</td>
        <td>${esc(m.start_date)}</td><td>${esc(m.end_date)}</td></tr>`;
    }
    html += `</tbody></table></div>`;

    const present = chart.yogas.filter((y) => y.present);
    html += `<h2>Yogas</h2>`;
    if (!present.length) {
      html += `<p class="muted">None of the yogas this engine detects are present.</p>`;
    } else {
      html += `<ul class="prose">` + present.map((y) =>
        `<li><strong>${esc(y.name)}</strong> — ${esc(y.description)} <span class="tag">(${esc(y.source)})</span></li>`
      ).join("") + `</ul>`;
    }

    html += `<h2>Reading</h2>`;
    for (const s of reading.sections) {
      html += `<div style="margin-bottom:18px"><h4>${esc(s.title)}</h4><ul class="prose">` +
        s.statements.map((st) =>
          `<li>${esc(st.text)} <span class="tag">(${esc(st.source)})</span></li>`
        ).join("") + `</ul></div>`;
    }
    html += `<p class="muted small">${esc(reading.disclaimer)}</p>`;

    html += `<h2>Gochara — transits from Janma Rasi ${esc(transit.janma_rasi)}</h2>
      <div class="scroll"><table><thead><tr>
      <th>Graha</th><th>Transit sign</th><th>House from Moon</th><th>Result</th></tr></thead><tbody>`;
    for (const r of transit.gochara) {
      html += `<tr><td>${esc(r.planet)}</td><td>${esc(r.sign)}</td>
        <td class="num">${r.house_from_moon}</td>
        <td>${r.result ? esc(r.result) : '<span class="pill">not legible in source</span>'}
        ${r.sade_sati ? '<span class="pill bad">Sade Sati</span>' : ""}</td></tr>`;
    }
    html += `</tbody></table></div>
      <p class="muted small" style="margin-top:10px">${esc(transit.weighting)}</p>`;

    $("out").innerHTML = html;
    $("out").classList.remove("hidden");
    $("empty").classList.add("hidden");
    window.scrollTo({ top: $("out").offsetTop - 70, behavior: "smooth" });
  }

  function run() {
    const err = $("err");
    err.classList.add("hidden");
    try {
      const birth = {
        name: $("name").value,
        date: $("date").value,
        time: $("time").value,
        latitude: parseFloat($("lat").value),
        longitude: parseFloat($("lon").value),
        tz_offset: parseFloat($("tz").value),
        place: ($("preset").selectedOptions[0] ? $("preset").selectedOptions[0].text : ""),
        ayanamsa: $("ayanamsa").value,
        house_system: $("houses").value,
      };
      if (!birth.date || !birth.time) throw new Error("give a date and a time");
      if (!isFinite(birth.latitude) || !isFinite(birth.longitude)) {
        throw new Error("latitude and longitude must be numbers");
      }
      const chart = window.JY.buildChart(birth);
      const transit = window.JY.transits.analyse(chart);
      const reading = window.JY.interpret.interpret(chart, transit);
      render(chart, transit, reading);
    } catch (ex) {
      err.textContent = "Could not cast the chart: " + ex.message;
      err.classList.remove("hidden");
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    const sel = $("preset");
    if (sel) {
      for (const [name, lat, lon, tz] of PRESETS) {
        const o = document.createElement("option");
        o.value = `${lat}|${lon}|${tz}|${name}`;
        o.textContent = name;
        sel.appendChild(o);
      }
      sel.addEventListener("change", () => {
        if (!sel.value) return;
        const [lat, lon, tz] = sel.value.split("|");
        $("lat").value = lat; $("lon").value = lon; $("tz").value = tz;
      });
    }
    const form = $("f");
    if (form) {
      form.addEventListener("submit", (e) => { e.preventDefault(); run(); });
      run();
    }
  });
})();
