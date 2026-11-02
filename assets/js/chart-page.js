/* chart-page.js -- the chart screen: form, tabs, wheel, tables, reading. */
(function () {
  const JY = window.JY;
  const D = JY.D;
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
    ["London", 51.5074, -0.1278, 0],
    ["New York", 40.7128, -74.0060, -5],
    ["Madras 1935 — the book's example", 13.0, 77.5833333, 5.1722222],
  ];

  const SI_ORDER = [
    "Pisces", "Aries", "Taurus", "Gemini",
    "Aquarius", null, null, "Cancer",
    "Capricorn", null, null, "Leo",
    "Sagittarius", "Scorpio", "Libra", "Virgo",
  ];

  const TABS = [
    ["overview", "Overview"],
    ["charts", "Charts"],
    ["grahas", "Grahas"],
    ["bhavas", "Bhavas"],
    ["dashas", "Dashas"],
    ["reading", "Reading"],
    ["transits", "Transits"],
  ];

  function siGrid(chart, navamsa) {
    return SI_ORDER.map((slot) => {
      if (slot === null) return `<div class="cell blank"></div>`;
      let occupants, lagna;
      if (navamsa) {
        occupants = D.PLANETS.filter((p) => chart._planets[p].navamsa_sign === slot);
        lagna = slot === JY.navamsaSign(chart._asc);
      } else {
        occupants = D.PLANETS.filter((p) => chart._planets[p].sign === slot);
        lagna = slot === chart.lagna.sign;
      }
      return `<div class="cell${lagna ? " lagna" : ""}">
        <div class="sg">${D.SIGN_GLYPHS[D.SIGNS.indexOf(slot)]} ${esc(slot.slice(0, 3))}</div>
        ${occupants.map((p) => {
          const pl = chart._planets[p];
          return `<div class="pl">${D.PLANET_GLYPHS[p]} ${esc(p.slice(0, 3))} <span class="d">${pl.degree_in_sign.toFixed(1)}${pl.retrograde ? "R" : ""}</span></div>`;
        }).join("")}
      </div>`;
    }).join("");
  }

  function timeline(chart) {
    const v = chart.vimshottari;
    const now = Date.now();
    const segs = v.mahadashas.map((m) => {
      const s = Date.parse(m.start + "Z"), e = Date.parse(m.end + "Z");
      const cls = now >= e ? "done" : (now >= s && now < e ? "now" : "");
      const pct = (m.years / 120) * 100;
      return `<div class="seg ${cls}" style="width:${pct.toFixed(3)}%" title="${m.lord} ${m.start_date} → ${m.end_date}">${m.lord.slice(0, 3)}</div>`;
    }).join("");
    const first = v.mahadashas[0].start_date.slice(0, 4);
    const last = v.mahadashas[v.mahadashas.length - 1].end_date.slice(0, 4);
    return `<div class="timeline"><div class="bar">${segs}</div>
      <div class="axis"><span>${first}</span><span>120-year Vimshottari cycle</span><span>${last}</span></div></div>`;
  }

  function render(chart, transit, reading) {
    const l = chart.lagna, b = chart.birth, pn = chart.panchanga;
    const cur = chart.vimshottari.current;
    let h = "";

    /* tabs */
    h += `<div class="tabs">` + TABS.map(([id, label], i) =>
      `<a href="#${id}"${i === 0 ? ' class="on"' : ""}>${label}</a>`).join("") + `</div>`;

    /* ---- overview ---- */
    h += `<section id="overview">
      <div class="strip">
        <div class="card"><div class="k">Ascendant</div><div class="v">${esc(l.sign)}</div>
          <div class="s">${JY.dms(l.degree_in_sign)} · ${esc(l.nakshatra)} ${l.pada}</div></div>
        <div class="card"><div class="k">Janma Rasi</div><div class="v">${esc(l.moon_sign)}</div>
          <div class="s">${esc(chart.vimshottari.janma_nakshatra)} · ${esc(chart.vimshottari.janma_nakshatra_lord)}</div></div>
        <div class="card"><div class="k">Ayanamsa</div><div class="v">${esc(chart.ayanamsa.dms)}</div>
          <div class="s">${esc(chart.ayanamsa.model)}</div></div>
        <div class="card"><div class="k">Panchanga</div><div class="v">${esc(pn.tithi.name)}</div>
          <div class="s">${esc(pn.tithi.paksha)} · ${esc(pn.vara.name)}</div></div>
        <div class="card"><div class="k">Current dasha</div>
          <div class="v">${cur.mahadasha ? esc(cur.mahadasha.lord) : "—"}</div>
          <div class="s">${cur.antardasha ? esc(cur.antardasha.lord) + " bhukti" : ""}</div></div>
        <div class="card"><div class="k">Birth (UT)</div><div class="v">${esc(b.utc.slice(11, 16))}</div>
          <div class="s">${esc(b.utc.slice(0, 10))} · JD ${b.jd_ut.toFixed(3)}</div></div>
      </div>

      <div class="charts-row" style="margin-top:18px">
        <div class="figure">
          <div class="cap"><span>Rasi wheel</span><span>${esc(l.sign)} lagna</span></div>
          <div id="wheel"></div>
        </div>
        <div class="figure">
          <div class="cap"><span>Vimshottari cycle</span><span>${esc(chart.vimshottari.balance_at_birth.lord)} at birth</span></div>
          ${timeline(chart)}
          <p class="small muted" style="margin-top:16px">
            Balance of ${esc(chart.vimshottari.balance_at_birth.lord)} at birth:
            ${chart.vimshottari.balance_at_birth.years}y
            ${chart.vimshottari.balance_at_birth.months}m
            ${chart.vimshottari.balance_at_birth.days}d. Years of 365.25 days.
          </p>
        </div>
      </div>
    </section>`;

    /* ---- charts ---- */
    h += `<section id="charts">
      <h2><span class="num">02</span>Rasi and Navamsa</h2>
      <div class="charts-row">
        <div class="figure"><div class="cap"><span>Rasi chakra</span><span>whole sign</span></div>
          <div class="si">${siGrid(chart, false)}</div></div>
        <div class="figure"><div class="cap"><span>Navamsa · D9</span><span>${esc(JY.navamsaSign(chart._asc))} lagna</span></div>
          <div class="si">${siGrid(chart, true)}</div></div>
      </div>
    </section>`;

    /* ---- grahas ---- */
    h += `<section id="grahas">
      <h2><span class="num">03</span>Grahas</h2>
      <div class="scroll"><table><thead><tr>
        <th>Graha</th><th>Sign</th><th>Degree</th><th>Nakshatra</th><th>Pada</th>
        <th>House</th><th>Dignity</th><th>Navamsa</th><th>Strength</th><th></th>
      </tr></thead><tbody>`;
    for (const p of chart.planets) {
      const flags = [];
      if (p.retrograde) flags.push('<span class="flag">R</span>');
      if (p.combust) flags.push('<span class="flag">combust</span>');
      h += `<tr>
        <td>${p.planet_glyph} ${esc(p.planet)}</td>
        <td>${esc(p.sign)}</td>
        <td class="num">${JY.dms(p.degree_in_sign)}</td>
        <td>${esc(p.nakshatra)}</td>
        <td class="num">${p.pada}</td>
        <td class="num">${p.house}</td>
        <td>${esc(p.dignity)}</td>
        <td>${esc(p.navamsa_sign)}</td>
        <td class="num">${p.strength.score}</td>
        <td>${flags.join(" ")}</td>
      </tr>`;
    }
    h += `</tbody></table></div>
      <p class="small muted" style="margin-top:10px">Strength is a simplified positional
      score — dignity, house kind, trine, digbala, retrogression, combustion and
      vargottama — scaled 0–100. It is not Shadbala.</p>
    </section>`;

    /* ---- bhavas ---- */
    h += `<section id="bhavas">
      <h2><span class="num">04</span>Bhavas</h2>
      <div class="scroll"><table><thead><tr>
        <th>House</th><th>Sign</th><th>Lord</th><th>Lord in</th><th>Occupants</th><th>Significations</th>
      </tr></thead><tbody>`;
    for (const row of chart.houses) {
      h += `<tr><td class="num">${row.house}</td><td>${esc(row.sign)}</td>
        <td>${esc(row.lord)}</td><td class="num">${row.lord_house}</td>
        <td>${row.occupants.length ? row.occupants.map(esc).join(", ") : "—"}</td>
        <td class="muted small">${esc(row.significations)}</td></tr>`;
    }
    h += `</tbody></table></div></section>`;

    /* ---- dashas ---- */
    h += `<section id="dashas">
      <h2><span class="num">05</span>Vimshottari dasha</h2>
      ${timeline(chart)}
      <div class="scroll" style="margin-top:18px"><table><thead><tr>
        <th>Mahadasha</th><th>From</th><th>To</th><th>Years</th></tr></thead><tbody>`;
    for (const m of chart.vimshottari.mahadashas) {
      const isNow = cur.mahadasha && cur.mahadasha.lord === m.lord;
      h += `<tr class="${isNow ? "now" : ""}"><td>${esc(m.lord)}</td>
        <td class="num">${esc(m.start_date)}</td><td class="num">${esc(m.end_date)}</td>
        <td class="num">${m.years}</td></tr>`;
    }
    h += `</tbody></table></div>`;
    if (cur.mahadasha && cur.mahadasha.antardashas) {
      h += `<h3>Bhuktis in the current ${esc(cur.mahadasha.lord)} dasha</h3>
        <div class="scroll"><table><thead><tr><th>Bhukti</th><th>From</th><th>To</th></tr></thead><tbody>`;
      for (const s of cur.mahadasha.antardashas) {
        const on = cur.antardasha && cur.antardasha.lord === s.lord;
        h += `<tr class="${on ? "now" : ""}"><td>${esc(s.lord)}</td>
          <td class="num">${esc(s.start_date)}</td><td class="num">${esc(s.end_date)}</td></tr>`;
      }
      h += `</tbody></table></div>`;
    }
    h += `</section>`;

    /* ---- reading ---- */
    const present = chart.yogas.filter((y) => y.present);
    h += `<section id="reading">
      <h2><span class="num">06</span>Reading</h2>`;
    h += `<div class="chips">` + (present.length
      ? present.map((y) => `<span class="chip gold">${esc(y.name)}</span>`).join("")
      : `<span class="chip">no yogas detected</span>`) + `</div>`;
    h += `<div class="reading">`;
    for (const s of reading.sections) {
      h += `<section><h4>${esc(s.title)}</h4><ul>` + s.statements.map((st) =>
        `<li>${esc(st.text)} <span class="src">${esc(st.source)}</span> <span class="rule">${esc(st.rule)}</span></li>`
      ).join("") + `</ul></section>`;
    }
    h += `</div><p class="small muted">${esc(reading.disclaimer)}</p></section>`;

    /* ---- transits ---- */
    h += `<section id="transits">
      <h2><span class="num">07</span>Gochara · transits today</h2>
      <p class="small muted">Read from the Janma Rasi <strong>${esc(transit.janma_rasi)}</strong>.
        As of ${esc(transit.as_of.replace("T", " "))} UTC.</p>
      <div class="scroll"><table><thead><tr>
        <th>Graha</th><th>Transit sign</th><th>House from Moon</th><th>Result</th></tr></thead><tbody>`;
    for (const r of transit.gochara) {
      h += `<tr><td>${esc(r.planet)}</td><td>${esc(r.sign)}</td>
        <td class="num">${r.house_from_moon}</td>
        <td>${r.result ? esc(r.result) : '<span class="chip">not legible in source</span>'}
        ${r.sade_sati ? '<span class="chip bad">Sade Sati</span>' : ""}</td></tr>`;
    }
    h += `</tbody></table></div>
      <p class="small muted" style="margin-top:12px">${esc(transit.weighting)}</p>
    </section>`;

    $("out").innerHTML = h;
    $("out").classList.remove("hidden");
    $("empty").classList.add("hidden");
    JY.wheel.render($("wheel"), chart);
    window.__chart = chart;
  }

  /* ---- shareable URL ---- */
  function writeHash(birth) {
    const p = new URLSearchParams({
      d: birth.date, t: birth.time, la: birth.latitude, lo: birth.longitude,
      tz: birth.tz_offset, ay: birth.ayanamsa, hs: birth.house_system,
      p: birth.place || "",
    });
    history.replaceState(null, "", "#" + p.toString());
  }

  function readHash() {
    if (!location.hash || location.hash.length < 4) return null;
    const p = new URLSearchParams(location.hash.slice(1));
    if (!p.get("d") || !p.get("t")) return null;
    return {
      date: p.get("d"), time: p.get("t"),
      latitude: parseFloat(p.get("la")), longitude: parseFloat(p.get("lo")),
      tz_offset: parseFloat(p.get("tz") || "5.5"),
      ayanamsa: p.get("ay") || "lahiri", house_system: p.get("hs") || "whole_sign",
      place: p.get("p") || "",
    };
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
      const chart = JY.buildChart(birth);
      const transit = JY.transits.analyse(chart);
      const reading = JY.interpret.interpret(chart, transit);
      writeHash(birth);
      render(chart, transit, reading);
    } catch (ex) {
      err.textContent = "Could not cast the chart: " + ex.message;
      err.classList.remove("hidden");
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
    sel.addEventListener("change", () => {
      if (!sel.value) return;
      const [lat, lon, tz] = sel.value.split("|");
      $("lat").value = lat; $("lon").value = lon; $("tz").value = tz;
    });

    const shared = readHash();
    if (shared) {
      $("date").value = shared.date;
      $("time").value = shared.time;
      $("lat").value = shared.latitude;
      $("lon").value = shared.longitude;
      $("tz").value = shared.tz_offset;
      $("ayanamsa").value = shared.ayanamsa;
      $("houses").value = shared.house_system;
    }

    $("f").addEventListener("submit", (e) => { e.preventDefault(); run(); });
    $("share").addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(location.href);
        $("share").textContent = "Link copied";
        setTimeout(() => { $("share").textContent = "Copy link"; }, 1800);
      } catch (_) {
        $("share").textContent = location.href;
      }
    });
    $("json").addEventListener("click", () => {
      if (!window.__chart) return;
      const blob = new Blob([JSON.stringify(window.__chart, (k, v) => k.startsWith("_") ? undefined : v, 2)],
        { type: "application/json" });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "chart.json";
      a.click();
      URL.revokeObjectURL(a.href);
    });
    run();
  });
})();
