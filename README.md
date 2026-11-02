# jyotish

**Live site:** https://apsideslabs.github.io/vedic-astrology/ — the chart
calculator runs the whole engine in your browser, so there is no server to wait
for.

A working Vedic (Nirayana) astrology engine and web app, built on the rules in
**B. V. Raman, *Astrology for Beginners*** — and on nothing else that the book
does not contain.

- **docs/** — the extracted knowledge: principles, signs, planets, houses,
  aspects, the full calculation method, Vimshottari, interpretation rules,
  yogas, transits, horary. Every rule is tagged SOURCE (in the book) or
  STANDARD (common practice the book assumes).
- **src/jyotish/** — the engine: sidereal positions, whole-sign and Sripati
  houses, Navamsa, aspects, Vimshottari with sub-periods, yoga detection,
  gochara transits, panchanga, and a rule-based reading whose every statement
  carries a rule id and a chapter reference.
- **site/** — the static site served on GitHub Pages: overview, chart
  calculator (the engine compiled to JS, running client-side), the knowledge
  base rendered as 15 pages, API reference and provenance. Multi-page, no
  build step, no framework.
- **app/** — a FastAPI service with the same engine in Python, plus a CLI.
- **tests/** — 34 tests, including a full reproduction of the book's worked
  example.

## Quick start

```bash
pip install -r requirements.txt
pip install -e .                 # optional; or just use PYTHONPATH=src

# command line
python -m jyotish.cli --date 1990-04-14 --time 08:15 \
    --lat 13.0827 --lon 80.2707 --tz 5.5 --place Chennai

# web app
uvicorn app.main:app --reload     # http://127.0.0.1:8000

# tests
python -m pytest tests -q
```

## The book's own example, reproduced

The strongest thing this repository can claim is that it rebuilds the chart the
book works out by hand. Chapter II casts a chart for 2 November 1935, 05:20
L.M.T. at Madras (13° N, 77°35′ E), and prints the nine grahas. The engine
reproduces all of them:

| Graha | Book | Engine | Δ |
|---|---|---|---|
| Sun | Libra 17°09′ | Libra 17°08′ | 1′ |
| Moon | Sagittarius 22°35′ | Sagittarius 22°32′ | 3′ |
| Mars | Sagittarius 11°40′ | Sagittarius 11°39′ | 1′ |
| Mercury | Virgo 28°35′ | Virgo 28°33′ | 2′ |
| Jupiter | Scorpio 6°53′ | Scorpio 6°56′ | 3′ |
| Venus | Virgo 1°45′ | Virgo 1°40′ | 5′ |
| Saturn | Aquarius 12°02′ | Aquarius 12°01′ | 1′ |
| Rahu | Sagittarius 24°34′ | Sagittarius 24°35′ | 1′ |
| Ketu | Gemini 24°34′ | Gemini 24°35′ | 1′ |
| Ascendant | Libra 8°01′ | Libra 8°15′ | 14′ |

The residual is the book's ayanamsa, which it rounds to 21°30′; the engine
computes 21°30′55″ for the same date. The Rasi chart, the dignities, the
Mars–Jupiter exchange and the Vimshottari balance of 6y 1m 15d all match too,
and all of them are asserted in `tests/test_engine.py`.

## The library stack

| Layer | Choice | Why |
|---|---|---|
| Ephemeris | [`astronomy-engine`](https://github.com/cosinekitty/astronomy) | pure Python, no data files, ~1′ accuracy, MIT |
| Web | FastAPI + Uvicorn | typed request models, automatic validation, OpenAPI |
| Validation | Pydantic v2 | range and format checks on every input |
| Templates | Jinja2 | server-rendered shell, no build step |
| Tests | pytest + httpx | includes the FastAPI test client |

**On the ephemeris choice.** The industry standard for astrology software is
the **Swiss Ephemeris** (`pyswisseph`), which is what commercial packages use
and which implements ~40 ayanamsas natively. It is a C extension; this
environment has no compiler, so it could not be installed here. `astronomy-engine`
is used instead and `ephemeris.py` is deliberately a thin adapter — it returns
`{planet: {longitude, latitude, speed}}` and nothing else — so swapping in
`pyswisseph` is a one-function change with no effect on the rest of the engine.

For production use, install the Swiss Ephemeris:

```python
import swisseph as swe
swe.set_sid_mode(swe.SIDM_LAHIRI)
# then replace ephemeris.tropical_longitudes and ephemeris.sidereal_time_hours
```

## Design decisions worth knowing

**Whole-sign houses by default.** The book says "for ordinary purposes of
prediction a zodiacal diagram (Rasi Chakra) with the Ascendant marked is
sufficient". Sripati (Porphyry) and equal houses are also available; the book
itself obtains bhava *mid-points* by taking Western cusps and deducting the
ayanamsa, which is the Sripati convention.

**Mean lunar node.** Rahu and Ketu are computed as the mean node (Meeus ch. 47),
which is what Raman's ephemeris tabulates. The true node differs by up to ~1°40′.

**Two ayanamsas.** `lahiri` (default, the modern standard) and `raman_397` (the
book's own arithmetic rule, `(year − 397) × 50⅓″`). The two differ by about
1°27′ for 1935, and you need the second one to reproduce the book's worked
example. This is documented at length in `docs/07-calculation.md`.

**Strength is not Shadbala.** The engine computes a transparent additive
positional score — dignity, house kind, trine, digbala, retrogression,
combustion, vargottama — scaled 0–100 for display. It is labelled as such in
the API output and in the UI, because presenting it as Shadbala would be a lie.

**Interpretation is rule-based, not generative.** Each statement is a
transcription of a rule the book states, applied to the computed chart, and
carries `{rule, text, source}`. No language model is involved, so a reading is
reproducible and auditable — you can read the rule and disagree with it.

**Gaps are left as gaps.** Where the scan of the book is damaged, the transit
tables have `null` cells and the docs say "not legible in the source". Nothing
was filled in from another book without being flagged.

## API

```
POST /api/chart
{
  "date": "1990-04-14", "time": "08:15",
  "latitude": 13.0827, "longitude": 80.2707, "tz_offset": 5.5,
  "place": "Chennai", "name": "",
  "ayanamsa": "lahiri",            // or "raman_397"
  "house_system": "whole_sign"     // or "sripati", "equal"
}
```

Returns birth data, ayanamsa, lagna, nine planets with sign/degree/nakshatra/
pada/navamsa/dignity/strength, twelve bhavas, panchanga, the full Vimshottari
timeline with sub-periods, yogas, aspects (planet-to-planet and by house),
gochara transits with Sade Sati state, and the reading.

`GET /api/health` returns engine and ephemeris versions.

## The live site

`site/` is a plain multi-page static site — `index.html`, `chart.html`,
`knowledge.html`, `api.html`, `about.html`, plus `docs/*.html` generated from
the markdown by `tools/build_site.py`. It is published from the `gh-pages`
branch, which holds the built site only (`.nojekyll` is present so Pages serves
the files as-is rather than running them through Jekyll).

To redeploy after editing anything under `docs/` or `site/`:

```bash
python3 tools/build_site.py                  # regenerate site/docs/*.html
git add -A && git commit -m "..." && git push
# then copy site/* to the root of gh-pages and push that branch
```

The chart page computes everything in the browser: `site/assets/js/` is a port
of `src/jyotish/` and `site/assets/js/data.js` is generated from the Python
source by `tools/export_data.py`, so the two implementations cannot drift apart.
`tools/verify_js.js` and `tools/verify_py.py` dump the same chart from both and
compare them field by field; they currently agree exactly.

```bash
python3 tools/export_data.py     # regenerate the JS data tables
python3 tools/build_site.py      # regenerate site/docs/*.html
node tools/verify_js.js          # JS engine vs Python engine
node tools/verify_page.js        # render chart.html in a DOM and check it
```

## Layout

```
site/                  the static site (published to GitHub Pages)
  index.html           overview
  chart.html           the calculator
  knowledge.html       index of the knowledge base
  docs/                the 15 documents, rendered from markdown
  assets/js/           the browser engine (port of src/jyotish)
  assets/css/site.css
docs/                  the extracted knowledge (15 documents, markdown)
src/jyotish/
  zodiac.py            all data tables: signs, planets, nakshatras, houses
  ayanamsa.py          Lahiri and the book's rule
  ephemeris.py         positions, sidereal time, obliquity, ascendant, MC
  houses.py            whole-sign, Sripati, equal cusps
  strength.py          dignity, relations, simplified positional strength
  chart.py             the chart builder and its dataclasses
  dasha.py             Vimshottari with bhuktis
  yogas.py             the eight yogas the book defines
  transits.py          gochara from the Janma Rasi, Sade Sati
  panchanga.py         tithi, vara, nakshatra, yoga, karana
  interpret.py         the rule engine (rule ids + chapter references)
  cli.py               command line
app/
  main.py              FastAPI service
  templates/index.html the single-page UI
tests/                 engine and API tests
```

## Honest limits

This is a faithful implementation of **one 1930s primer**. It is not a
professional-grade astrology package: it has no Ashtakavarga, no full Shadbala,
no divisional charts beyond D9, no compatibility matching, no muhurta, and its
interpretation covers the topics the book covers and no others.

The book's own caution is worth keeping in front of the software:

> "The judgment of a horoscope forms the most important and difficult task of an
> astrologer. It must be borne in mind that, at the outset no hard and fast
> rules can be laid down for the guidance of the reader."

Present readings as material for study and self-reflection. Not as medical,
financial or legal advice, and not as a factual prediction about any person.

## Licence

MIT for the code — see `LICENSE`. `docs/` is a derivative summary of a
copyrighted book; see `docs/source-notes.md`.
