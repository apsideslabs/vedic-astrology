# The knowledge base

This directory is the extracted, organised content of **B. V. Raman,
*Astrology for Beginners*** (UBS Publishers' Distributors, 135 pp.), together
with the parts of standard practice the book assumes but does not spell out.

| Document | Covers | Source chapter |
|---|---|---|
| [01-foundations.md](01-foundations.md) | the premises of the system, the zodiac, the constellations | I, Introduction |
| [02-signs.md](02-signs.md) | the twelve Rasis, their natures and body parts | I, V |
| [03-planets.md](03-planets.md) | the nine grahas, karakas, exaltation, moolatrikona, avasthas | I |
| [04-relationships.md](04-relationships.md) | permanent, temporary and mixed friendship | I |
| [05-houses.md](05-houses.md) | the twelve Bhavas, kendras/panaparas/apoklimas, karakas | I |
| [06-aspects.md](06-aspects.md) | Drishti, special aspects, partial sight | I |
| [07-calculation.md](07-calculation.md) | ayanamsa, GMT, sidereal time, houses, navamsa — the full method | II, Appendix I, II |
| [08-strength.md](08-strength.md) | the six Shadbalas, and what this engine actually computes | III |
| [09-dasha.md](09-dasha.md) | Vimshottari: the table, the arithmetic, the balance at birth | X |
| [10-interpretation.md](10-interpretation.md) | longevity, appearance, health, education, wealth, livelihood, parents, marriage, children | IV–IX |
| [11-yogas.md](11-yogas.md) | Papakarthari, Sunapha, Anapha, Durdhura, Kemadruma, Adhiyoga, Rajayoga | III |
| [12-transits.md](12-transits.md) | Gochara from the Janma Rasi, Sade Sati | XII |
| [13-horary.md](13-horary.md) | Prasna: answering questions from the moment of asking | XI |
| [14-dasha-results.md](14-dasha-results.md) | planet by planet, house by house, what a dasha gives | X |
| [source-notes.md](source-notes.md) | provenance, OCR damage, what was reconstructed and why | — |

## How to read these documents

Statements are tagged with where they come from:

- **SOURCE** — stated in the book. The wording is condensed, not altered.
- **STANDARD** — standard Parashari practice, used where the book assumes it
  (the natural-friendship table, the combustion orbs, the fuller house
  significations) or where the scan is illegible.
- **CAUTION** — a place where the book is a beginner's primer and a modern
  practitioner would not stop there.

The engine in `src/jyotish/` implements exactly what is written here, and the
rule ids in `interpret.py` (`R-MARRIAGE-MARS`, `R-TRANSIT-SADESATI`, …) point
back to these documents.

## What this is not

The book is a 1930s primer. It gives no derivations, its ayanamsa rule is a
rule of thumb (see 07), and its longevity and marriage rules are stated
without the caveats a modern astrologer would attach. The knowledge is
reproduced faithfully; it is not endorsed. Nothing here should be used in
place of medical, financial or legal advice.
