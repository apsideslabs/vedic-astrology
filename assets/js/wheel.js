/* wheel.js -- the sidereal Rasi wheel as inline SVG.
 *
 * The Ascendant sits at the left (9 o'clock) and longitude runs anticlockwise,
 * which is the convention practitioners expect.  Signs are fixed to the
 * sidereal frame, so the wheel rotates with the Ascendant rather than being
 * pinned to Aries.
 */
(function () {
  const JY = window.JY;
  const D = JY.D;

  const CX = 200, CY = 200;
  const R_OUT = 192, R_SIGN = 152, R_HOUSE = 138, R_PLANET = 112;

  const rad = (deg) => (deg * Math.PI) / 180;

  /* longitude -> screen angle (deg, math convention, anticlockwise from +x) */
  function screenAngle(lon, asc) {
    return 180 + (lon - asc);
  }

  function pt(lon, asc, r) {
    const a = rad(screenAngle(lon, asc));
    return [CX + r * Math.cos(a), CY - r * Math.sin(a)];
  }

  function polarLabel(lon, asc, r) {
    const [x, y] = pt(lon, asc, r);
    return { x, y };
  }

  const esc = (s) => String(s).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));

  function render(container, chart) {
    const asc = chart.lagna.longitude;
    const out = [];

    out.push(`<svg class="wheel" viewBox="0 0 400 400" role="img" aria-label="Rasi wheel: ${esc(chart.lagna.sign)} ascendant">`);

    /* base rings */
    out.push(`<circle class="ring" cx="${CX}" cy="${CY}" r="${R_OUT}"/>`);
    out.push(`<circle class="ring" cx="${CX}" cy="${CY}" r="${R_SIGN}"/>`);
    out.push(`<circle class="ring-thin" cx="${CX}" cy="${CY}" r="${R_HOUSE}"/>`);

    /* sign spokes and labels */
    for (let i = 0; i < 12; i++) {
      const boundary = i * 30;
      const [x1, y1] = pt(boundary, asc, R_SIGN);
      const [x2, y2] = pt(boundary, asc, R_OUT);
      out.push(`<line class="spoke" x1="${x1.toFixed(2)}" y1="${y1.toFixed(2)}" x2="${x2.toFixed(2)}" y2="${y2.toFixed(2)}"/>`);

      const signName = D.SIGNS[i];
      const mid = boundary + 15;
      const lab = polarLabel(mid, asc, (R_SIGN + R_OUT) / 2);
      out.push(
        `<text class="signlabel" x="${lab.x.toFixed(2)}" y="${(lab.y + 5).toFixed(2)}" text-anchor="middle">${D.SIGN_GLYPHS[i]}</text>`
      );
      const sub = polarLabel(mid, asc, R_SIGN + 12);
      out.push(
        `<text class="signtext" x="${sub.x.toFixed(2)}" y="${(sub.y + 3).toFixed(2)}" text-anchor="middle">${esc(signName.slice(0, 3))}</text>`
      );

      /* house number (whole-sign houses) */
      const hn = ((i - D.SIGNS.indexOf(chart.lagna.sign) + 12) % 12) + 1;
      const hp = polarLabel(mid, asc, R_HOUSE + 6);
      out.push(`<text class="house-num" x="${hp.x.toFixed(2)}" y="${(hp.y + 3).toFixed(2)}" text-anchor="middle">${hn}</text>`);

      /* house cusp, dashed, from the sign ring inwards */
      const [cx1, cy1] = pt(boundary, asc, 56);
      const [cx2, cy2] = pt(boundary, asc, R_SIGN);
      out.push(`<line class="cusp" x1="${cx1.toFixed(2)}" y1="${cy1.toFixed(2)}" x2="${cx2.toFixed(2)}" y2="${cy2.toFixed(2)}"/>`);
    }

    /* ascendant marker */
    const [ax1, ay1] = pt(asc, asc, R_OUT + 4);
    const [ax2, ay2] = pt(asc, asc, R_SIGN);
    out.push(`<line class="lagna-line" x1="${ax1.toFixed(2)}" y1="${ay1.toFixed(2)}" x2="${ax2.toFixed(2)}" y2="${ay2.toFixed(2)}"/>`);
    out.push(`<text class="lagna-text" x="8" y="14">ASC</text>`);

    /* planets, with simple collision stacking */
    const placed = D.PLANETS.map((p) => ({
      p,
      lon: chart._planets[p].longitude,
      glyph: D.PLANET_GLYPHS[p],
      retro: chart._planets[p].retrograde,
      benefic: D.NATURAL_BENEFICS.includes(p),
      deg: chart._planets[p].degree_in_sign,
    })).sort((a, b) => a.lon - b.lon);

    let cluster = [];
    const flush = () => {
      cluster.forEach((item, k) => {
        const r = R_PLANET - k * 21;
        const pos = polarLabel(item.lon, asc, r);
        const colour = item.benefic ? "#17454e" : "#9a3b1b";
        out.push(
          `<text class="planet" x="${pos.x.toFixed(2)}" y="${(pos.y + 6).toFixed(2)}" text-anchor="middle" fill="${colour}">${item.glyph}</text>`
        );
        out.push(
          `<text class="planet-label" x="${pos.x.toFixed(2)}" y="${(pos.y + 18).toFixed(2)}" text-anchor="middle">${item.deg.toFixed(1)}°${item.retro ? "R" : ""}</text>`
        );
      });
      cluster = [];
    };
    for (const item of placed) {
      if (cluster.length && Math.abs(item.lon - cluster[cluster.length - 1].lon) < 9) {
        cluster.push(item);
      } else {
        flush();
        cluster.push(item);
      }
    }
    flush();

    /* centre label */
    out.push(`<text x="${CX}" y="${CY - 2}" text-anchor="middle" style="font-family:var(--serif);font-size:13px;fill:#6e6558">RASI</text>`);
    out.push(`<text x="${CX}" y="${CY + 13}" text-anchor="middle" style="font-family:var(--mono);font-size:8px;letter-spacing:.1em;fill:#948a79">${esc(chart.ayanamsa.model.toUpperCase())}</text>`);

    out.push("</svg>");
    container.innerHTML = out.join("");
  }

  JY.wheel = { render };
})();
