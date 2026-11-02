/* wheel.js -- the sidereal Rasi wheel as inline SVG.
 *
 * The Ascendant sits at 9 o'clock and longitude runs anticlockwise, which is
 * the convention practitioners expect.  Planets that fall within a few degrees
 * of each other are displaced along the ring so their glyphs stay legible, with
 * a tick left at the true longitude.
 */
(function () {
  const JY = window.JY;
  const D = JY.D;

  const SIZE = 460, CX = 230, CY = 230;
  const R_OUT = 200;      /* outer rim                    */
  const R_SIGN = 162;     /* inner edge of the sign band  */
  const R_HOUSE = 146;    /* house numbers                */
  const R_PLANET = 114;   /* glyphs                       */
  const R_DEG = 97;       /* degree labels                */
  const R_CORE = 72;      /* inner frame                  */
  const MIN_SEP = 18.0;   /* minimum glyph spacing, deg   */

  const rad = (deg) => (deg * Math.PI) / 180;
  const screenAngle = (lon, asc) => 180 + (lon - asc);
  const xy = (angleDeg, r) => [
    CX + r * Math.cos(rad(angleDeg)),
    CY - r * Math.sin(rad(angleDeg)),
  ];
  const n = (v) => Number(v).toFixed(2);
  const esc = (s) => String(s).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));

  /* Spread clustered longitudes apart along the ring, keeping their order. */
  function spread(longitudes) {
    const order = longitudes.map((v, i) => i).sort((a, b) => longitudes[a] - longitudes[b]);
    const out = new Array(longitudes.length);
    let prev = -Infinity;
    for (const i of order) {
      let v = longitudes[i];
      if (v - prev < MIN_SEP) v = prev + MIN_SEP;
      out[i] = v;
      prev = v;
    }
    /* if the spread ran past a full turn, walk it back */
    const first = out[order[0]], last = out[order[order.length - 1]];
    const overflow = last - (first + 360 - MIN_SEP);
    if (overflow > 0) {
      for (let k = order.length - 1; k >= 1; k--) {
        out[order[k]] = Math.min(out[order[k]], out[order[k - 1]] + MIN_SEP);
      }
      for (let k = 1; k < order.length; k++) {
        out[order[k]] = Math.max(out[order[k]], out[order[k - 1]] + MIN_SEP);
      }
    }
    return out;
  }

  function render(container, chart) {
    const asc = chart.lagna.longitude;
    const out = [];
    out.push(`<svg class="wheel" viewBox="0 0 ${SIZE} ${SIZE}" role="img" ` +
             `aria-label="Rasi wheel, ${esc(chart.lagna.sign)} ascendant">`);

    out.push(`<circle class="ring" cx="${CX}" cy="${CY}" r="${R_OUT}"/>`);
    out.push(`<circle class="ring" cx="${CX}" cy="${CY}" r="${R_SIGN}"/>`);
    out.push(`<circle class="ring-thin" cx="${CX}" cy="${CY}" r="${R_CORE}"/>`);

    /* degree ticks around the rim */
    for (let d = 0; d < 360; d += 5) {
      const a = screenAngle(d, asc);
      const major = d % 30 === 0;
      const [x1, y1] = xy(a, R_OUT);
      const [x2, y2] = xy(a, R_OUT - (major ? 9 : 4));
      out.push(`<line x1="${n(x1)}" y1="${n(y1)}" x2="${n(x2)}" y2="${n(y2)}" ` +
               `stroke="#cec3ab" stroke-width="${major ? 1 : 0.6}"/>`);
    }

    /* sign sectors, glyphs, labels, house numbers */
    for (let i = 0; i < 12; i++) {
      const boundary = i * 30;
      const [x1, y1] = xy(screenAngle(boundary, asc), R_SIGN);
      const [x2, y2] = xy(screenAngle(boundary, asc), R_OUT);
      out.push(`<line class="spoke" x1="${n(x1)}" y1="${n(y1)}" x2="${n(x2)}" y2="${n(y2)}"/>`);

      const mid = boundary + 15;
      const g = xy(screenAngle(mid, asc), 183);
      out.push(`<text class="signlabel" x="${n(g[0])}" y="${n(g[1] + 5.5)}" text-anchor="middle">${D.SIGN_GLYPHS[i]}</text>`);
      const t = xy(screenAngle(mid, asc), 167);
      out.push(`<text class="signtext" x="${n(t[0])}" y="${n(t[1] + 3)}" text-anchor="middle">${esc(D.SIGNS[i].slice(0, 3))}</text>`);

      const hn = ((i - D.SIGNS.indexOf(chart.lagna.sign) + 12) % 12) + 1;
      const hp = xy(screenAngle(mid, asc), R_HOUSE + 6);
      out.push(`<text class="house-num" x="${n(hp[0])}" y="${n(hp[1] + 3)}" text-anchor="middle">${hn}</text>`);
    }

    /* ascendant: triangle outside the rim, accent tick across the sign band */
    out.push(`<path d="M ${n(CX - R_OUT - 12)} ${CY} l 8 -4.5 v 9 z" fill="#9a3b1b"/>`);
    const [ax1, ay1] = xy(180, R_OUT);
    const [ax2, ay2] = xy(180, R_SIGN);
    out.push(`<line class="lagna-line" x1="${n(ax1)}" y1="${n(ay1)}" x2="${n(ax2)}" y2="${n(ay2)}" opacity="0.5"/>`);
    out.push(`<text class="lagna-text" x="${n(CX - R_OUT - 6)}" y="${CY - 15}" text-anchor="start">ASC</text>`);

    /* planets */
    const planets = D.PLANETS.map((p) => ({
      p,
      lon: chart._planets[p].longitude,
      glyph: D.PLANET_GLYPHS[p],
      retro: chart._planets[p].retrograde,
      benefic: D.NATURAL_BENEFICS.includes(p),
      deg: chart._planets[p].degree_in_sign,
    }));
    const display = spread(planets.map((x) => x.lon));

    /* Alternate the degree-label radius within each cluster, in longitude
     * order, so two numbers can never sit on the same line and run together. */
    const byDisplay = planets.map((_, i) => i).sort((a, b) => display[a] - display[b]);
    const stagger = new Array(planets.length).fill(false);
    let run = 0, prevAngle = null;
    for (const i of byDisplay) {
      if (prevAngle !== null && display[i] - prevAngle < 24) run += 1; else run = 0;
      stagger[i] = run % 2 === 1;
      prevAngle = display[i];
    }

    planets.forEach((item, i) => {
      const colour = item.benefic ? "#17454e" : "#9a3b1b";

      /* tick at the true longitude */
      const aTrue = screenAngle(item.lon, asc);
      const [t1x, t1y] = xy(aTrue, R_SIGN - 2);
      const [t2x, t2y] = xy(aTrue, R_SIGN - 11);
      out.push(`<line x1="${n(t1x)}" y1="${n(t1y)}" x2="${n(t2x)}" y2="${n(t2y)}" ` +
               `stroke="${colour}" stroke-width="1.6" opacity="0.7"/>`);

      /* glyph and its degree label, displaced together */
      const aDisp = screenAngle(display[i], asc);
      const [gx, gy] = xy(aDisp, R_PLANET);
      out.push(`<text class="planet" x="${n(gx)}" y="${n(gy + 6)}" text-anchor="middle" fill="${colour}">${item.glyph}</text>`);
      const [dx, dy] = xy(aDisp, stagger[i] ? R_DEG - 13 : R_DEG);
      out.push(`<text class="planet-label" x="${n(dx)}" y="${n(dy + 3)}" text-anchor="middle">` +
               `${item.deg.toFixed(1)}${item.retro ? "R" : ""}</text>`);
    });

    out.push(`<text x="${CX}" y="${CY - 1}" text-anchor="middle" style="font-family:var(--serif);font-size:13px;fill:#6e6558">Rasi</text>`);
    out.push(`<text x="${CX}" y="${CY + 14}" text-anchor="middle" style="font-family:var(--mono);font-size:7.5px;letter-spacing:.12em;fill:#948a79">${esc(chart.ayanamsa.model.toUpperCase())}</text>`);

    out.push("</svg>");
    container.innerHTML = out.join("");
  }

  JY.wheel = { render };
})();
