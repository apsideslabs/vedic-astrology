"""Build the static site's documentation pages.

Converts docs/*.md into site/docs/*.html with the application shell, and writes
site/knowledge.html as the index.  Run from the repository root:

    python3 tools/build_site.py
"""

from __future__ import annotations

import os
import re
import sys

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
SITE = os.path.join(ROOT, "site")
OUT = os.path.join(SITE, "docs")

# (source file, short title, one-line description, source chapter)
ORDER = [
    ("01-foundations.md", "Foundations",
     "The premises of the system, the zodiac, the 27 nakshatras.", "ch. I"),
    ("02-signs.md", "The twelve signs",
     "Rasis, their natures, elements and the organs they govern.", "ch. I, V"),
    ("03-planets.md", "The nine planets",
     "Grahas, karakas, exaltation, moolatrikona, the ten avasthas.", "ch. I"),
    ("04-relationships.md", "Relations between planets",
     "Permanent, temporary and mixed friendship; why they matter.", "ch. I"),
    ("05-houses.md", "The twelve houses",
     "Bhavas, kendras and trines, karakas, how to read a house.", "ch. I"),
    ("06-aspects.md", "Aspects",
     "Drishti, the graded sight, and the special aspects of Mars, Jupiter and Saturn.", "ch. I"),
    ("07-calculation.md", "Casting a horoscope",
     "The full method: GMT, sidereal time, houses, ayanamsa, navamsa, with the worked example.", "ch. II, App. I–II"),
    ("08-strength.md", "Strength",
     "The six Shadbalas, the judgement rules, and what this engine actually computes.", "ch. III"),
    ("09-dasha.md", "Vimshottari dasha",
     "The nine periods, the arithmetic, the balance at birth, how to judge a period.", "ch. X"),
    ("10-interpretation.md", "Interpretation",
     "Longevity, appearance, health, education, wealth, livelihood, parents, marriage, children.", "ch. IV–IX"),
    ("11-yogas.md", "Yogas",
     "Papakarthari, Sunapha, Anapha, Durdhura, Kemadruma, Adhiyoga, Rajayoga.", "ch. III"),
    ("12-transits.md", "Transits",
     "Gochara from the Janma Rasi, planet by planet, and Sade Sati.", "ch. XII"),
    ("13-horary.md", "Horary",
     "Prasna: answering questions from the moment of asking.", "ch. XI"),
    ("14-dasha-results.md", "Dasha results",
     "What each planet's period gives, house by house.", "ch. X"),
    ("source-notes.md", "Source notes",
     "Provenance, the OCR damage catalogued, what was reconstructed and why.", "—"),
]

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Jyotish</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="../assets/css/app.css">
</head>
<body data-page="knowledge" data-root="../">

<main class="shell">
<div class="docwrap">
  <aside class="docnav">
    <div class="grp"><h4>Knowledge base</h4><a href="../knowledge.html">All documents</a></div>
    <div class="grp"><h4>Documents</h4>{sidebar}</div>
    <div class="grp"><h4>Elsewhere</h4>
      <a href="../chart.html">Cast a chart</a>
      <a href="../panchanga.html">Panchanga</a>
      <a href="../transits.html">Transits</a>
    </div>
  </aside>
  <article class="prose">
    <p class="eyebrow">{eyebrow}</p>
    {body}
  </article>
</div>
</main>

<footer class="site"><div class="shell">
  <div class="cols">
    <div>Jyotish · engine v1.0.0 · MIT<br>
      <span class="mono">extracted from B. V. Raman, Astrology for Beginners</span></div>
    <div class="mono">For study and self-reflection — not medical, financial or legal advice.</div>
  </div>
</div></footer>

<script src="../assets/js/nav.js"></script>
</body>
</html>
"""


def slug(name: str) -> str:
    return name[:-3] + ".html"


def title_of(text: str, fallback: str) -> str:
    m = re.search(r"^#\s+(.+)$", text, re.M)
    return m.group(1).strip() if m else fallback


def strip_first_h1(text: str) -> str:
    return re.sub(r"^#\s+.+\n+", "", text, count=1, flags=re.M)


def sidebar(current: str) -> str:
    out = []
    for i, (fname, short, _d, _s) in enumerate(ORDER, start=1):
        on = ' class="on"' if fname == current else ""
        out.append(f'<a href="{slug(fname)}"{on}>{i:02d} · {short}</a>')
    return "".join(out)


KNOWLEDGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Knowledge base — Jyotish</title>
<meta name="description" content="The extracted knowledge of B. V. Raman's Astrology for Beginners: signs, planets, houses, aspects, calculation, dashas, interpretation, yogas, transits, horary.">
<link rel="stylesheet" href="assets/css/app.css">
</head>
<body data-page="knowledge" data-root="">

<main class="shell">
  <p class="eyebrow">Reference · 05</p>
  <h1>Knowledge base</h1>
  <p class="lede">Fifteen documents extracted from the book and reorganised by subject,
    because the book keeps circling back — friendship appears in chapters I and III, the
    Navamsa in II and IX, Saturn in IV, X and XII.</p>

  <div class="chips">
    <span class="chip teal">source — stated in the book</span>
    <span class="chip">standard — practice it assumes</span>
    <span class="chip bad">caution — not the last word</span>
  </div>

  <div class="doclist">
{cards}
  </div>

  <h2><span class="num">A</span>How the engine uses this</h2>
  <p>Every rule the reading applies carries an id and a chapter reference, so a statement
    in a chart can be traced back to a page here. The rule ids live in
    <span class="mono">src/jyotish/interpret.py</span>; the data tables the engine runs
    on — exaltations, moolatrikonas, friendships, house significations, the gochara
    cells — are in <span class="mono">src/jyotish/zodiac.py</span> and
    <span class="mono">src/jyotish/transits.py</span>. The browser build shares them
    through <span class="mono">site/assets/js/data.js</span>, which is generated from the
    Python source so the two cannot drift apart.</p>
</main>

<footer class="site"><div class="shell">
  <div class="cols">
    <div>Jyotish · engine v1.0.0 · MIT<br>
      <span class="mono">extracted from B. V. Raman, Astrology for Beginners</span></div>
    <div class="mono"><a href="chart.html">cast a chart</a> · <a href="about.html">provenance</a></div>
  </div>
</div></footer>

<script src="assets/js/nav.js"></script>
</body>
</html>
"""


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "attr_list"])

    built = 0
    for fname, short, desc, src in ORDER:
        path = os.path.join(DOCS, fname)
        if not os.path.exists(path):
            print("missing", path, file=sys.stderr)
            continue
        text = open(path, encoding="utf-8").read()
        md.reset()
        body = md.convert(strip_first_h1(text))
        html = PAGE.format(
            title=title_of(text, short), desc=desc,
            eyebrow=f"Document {ORDER.index((fname, short, desc, src)) + 1:02d} · {src}",
            sidebar=sidebar(fname), body=body,
        )
        with open(os.path.join(OUT, slug(fname)), "w", encoding="utf-8") as f:
            f.write(html)
        built += 1

    cards = []
    for i, (fname, short, desc, src) in enumerate(ORDER, start=1):
        cards.append(
            f'      <a href="docs/{slug(fname)}">'
            f'<div class="n">{i:02d}</div>'
            f'<div><strong>{short}</strong><span class="d">{desc}</span><br>'
            f'<span class="src">{src}</span></div></a>'
        )

    with open(os.path.join(SITE, "knowledge.html"), "w", encoding="utf-8") as f:
        f.write(KNOWLEDGE.format(cards="\n".join(cards)))

    print(f"built {built} document pages + knowledge.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
