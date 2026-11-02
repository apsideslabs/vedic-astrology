"""Build the static site's documentation pages.

Converts docs/*.md into site/docs/*.html with a shared shell and sidebar, and
writes site/knowledge.html as the index.  Run from the repository root:

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
     "The premises of the system, the zodiac, the 27 nakshatras.", "ch. I, Introduction"),
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
     "The full method: GMT, sidereal time, houses, ayanamsa, navamsa — with the worked example.", "ch. II, App. I–II"),
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

NAV = """<div class="topbar"><div class="inner">
  <a class="brand" href="{p}index.html">Jyoti<span>sh</span></a>
  <nav>
    <a href="{p}index.html">Overview</a>
    <a href="{p}chart.html">Cast a chart</a>
    <a href="{p}knowledge.html"{knowledge_on}>Knowledge base</a>
    <a href="{p}api.html">API</a>
    <a href="{p}about.html">Provenance</a>
  </nav>
</div></div>"""

FOOT = """<footer class="site"><div class="inner">
  Jyotish · engine v1.0.0 · extracted from B. V. Raman, <em>Astrology for Beginners</em>.
  For study and self-reflection — not medical, financial or legal advice.
</div></footer>"""

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Jyotish</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="{p}assets/css/site.css">
</head>
<body>
{nav}
<main>
<div class="docwrap">
  <aside class="docnav">{sidebar}</aside>
  <article class="prose">
    {body}
  </article>
</div>
</main>
{foot}
</body>
</html>
"""


def slug(name: str) -> str:
    return name[:-3].replace(".md", "") + ".html"


def title_of(text: str, fallback: str) -> str:
    m = re.search(r"^#\s+(.+)$", text, re.M)
    return m.group(1).strip() if m else fallback


def sidebar(current: str) -> str:
    rows = ['<div class="grp"><h4>Knowledge base</h4>',
            f'<a href="../knowledge.html">All documents</a></div>',
            '<div class="grp"><h4>Documents</h4>']
    for fname, short, _desc, _src in ORDER:
        on = ' class="on"' if fname == current else ""
        rows.append(f'<a href="{slug(fname)}"{on}>{short}</a>')
    rows.append("</div>")
    rows.append('<div class="grp"><h4>Elsewhere</h4>'
                '<a href="../chart.html">Cast a chart</a>'
                '<a href="../api.html">API</a></div>')
    return "".join(rows)


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "attr_list", "toc"])
    nav = NAV.format(p="../", knowledge_on=' class="on"')

    built = 0
    for fname, short, desc, _src in ORDER:
        path = os.path.join(DOCS, fname)
        if not os.path.exists(path):
            print("missing", path, file=sys.stderr)
            continue
        text = open(path, encoding="utf-8").read()
        md.reset()
        body = md.convert(text)
        html = PAGE.format(
            title=title_of(text, short), desc=desc, p="../", nav=nav,
            sidebar=sidebar(fname), body=body, foot=FOOT,
        )
        with open(os.path.join(OUT, slug(fname)), "w", encoding="utf-8") as f:
            f.write(html)
        built += 1

    # the index page
    cards = []
    for fname, short, desc, src in ORDER:
        cards.append(
            f'<a href="docs/{slug(fname)}"><strong>{short}</strong>'
            f'<span>{desc} <em>— {src}</em></span></a>'
        )
    index = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Knowledge base — Jyotish</title>
<meta name="description" content="The extracted knowledge of B. V. Raman's Astrology for Beginners: signs, planets, houses, aspects, calculation, dashas, interpretation, yogas, transits, horary.">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body>
{NAV.format(p="", knowledge_on=' class="on"')}
<main>
  <h1>Knowledge base</h1>
  <p class="lede">Fifteen documents extracted from the book and reorganised by subject,
    because the book keeps circling back — friendship appears in chapters I and III, the
    Navamsa in II and IX, Saturn in IV, X and XII.</p>

  <p>Statements are tagged with where they come from: <span class="pill">SOURCE</span>
    is stated in the book, <span class="pill">STANDARD</span> is common practice the
    book assumes but does not spell out, and <span class="pill bad">CAUTION</span> marks
    a place where a 1930s primer should not be anyone's last word. Where the scan is
    damaged, the gap is shown rather than filled from another book.</p>

  <div class="doclist">
    {''.join(cards)}
  </div>

  <h2>How the engine uses this</h2>
  <p>Every rule the reading applies has an id and a chapter reference, so a statement
    in a chart can be traced back to a page here. The rule ids are listed in
    <code>src/jyotish/interpret.py</code>, and the data tables the engine runs on —
    exaltations, moolatrikonas, friendships, house significations, the gochara
    tables — are in <code>src/jyotish/zodiac.py</code> and
    <code>src/jyotish/transits.py</code>. The browser build shares them through
    <code>site/assets/js/data.js</code>, which is generated from the Python source so
    the two cannot drift apart.</p>
</main>
{FOOT}
</body>
</html>
"""
    with open(os.path.join(SITE, "knowledge.html"), "w", encoding="utf-8") as f:
        f.write(index)

    print(f"built {built} document pages + knowledge.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
