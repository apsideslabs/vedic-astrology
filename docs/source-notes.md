# Source notes

## The source

**B. V. Raman, *Astrology for Beginners*** — 135 pages, 12 chapters and two
appendices. Published by UBS Publishers' Distributors Ltd., 5 Ansari Road,
New Delhi 110 002.

The file this knowledge base was extracted from is a scan of the book held by
the Internet Archive:

```
title:    Astrology for Beginners - BV Raman
creator:  Digitized by the Internet Archive
producer: Recoded by LuraDocument PDF v2.65
created:  2017-05-07
pages:    135
size:     2.29 MB
```

The scan carries an OCR text layer of about 147,000 characters. Every page has
text; pages 1, 6, 8 and 10 are near-empty (the cover plate and blank versos),
and pages 60–63 are duplicated in the source scan (page 60 repeats as 62, page
61 as 63).

## What was done to it

1. The text layer was extracted page by page.
2. The running watermark (`jyotishbooks.tk`, `jyoti hb ok;`) was stripped.
3. The one-word-per-line OCR layout was reflowed into paragraphs.
4. The chapters were segmented by page range and read in full.
5. The content was reorganised by *subject* rather than by chapter, because the
   book returns to the same topics repeatedly (friendship appears in I and III,
   the Navamsa in II and IX, Saturn in IV, X and XII).
6. Every table was transcribed by hand from the reflowed text.

Nothing was paraphrased into a claim the book does not make. Where the book is
wrong or dated, it is marked **CAUTION** rather than silently corrected.

## The OCR damage, catalogued

This matters because it determines which tables are complete and which are not.

| Location | Damage | How it was handled |
|---|---|---|
| pp. 7–8, natural friendship table | columns interleaved, rows cut through the page break | replaced with the standard Parashari table, flagged **STANDARD** |
| p. 11, moolatrikona of Mars | printed "0° to it" | reconstructed as 12°, the only consistent value |
| p. 11, moolatrikona of the Moon | printed "Taurus 4° to 20°" | kept as printed; the standard value 4°–30° is noted |
| p. 24, Navamsa construction table | completely destroyed (a jumble of single characters) | the classical rule was stated in prose in the same chapter and is implemented from that |
| pp. 30–31, table of benefics / malefics / yogakarakas / marakas | columns interleaved, several rows unreadable | not transcribed; the engine **derives** yogakaraka and maraka from ownership instead |
| p. 33, first "Important Yoga" | cut in half by the page break | identified as unidentifiable; listed in 11-yogas.md as missing |
| pp. 52–54, chapter VI and VII horoscope diagrams | glyph soup | not transcribed; the worked examples were used only where the prose states the conclusion |
| p. 69, dasha table | reordered by the OCR into a jumble of sign / nakshatra / years | rebuilt from the plain list of years given two pages later ("Jupiter 16 yrs. Saturn 19. Merc. 17") and from the standard nakshatra cycle |
| pp. 75–76, "General Results" items 3 and 4 | lost across a page break | numbered items 3 and 4 are missing; noted in 09-dasha.md |
| pp. 96–100, gochara tables | Sun houses 9–11, Mercury 9–10, Saturn 5–6 lost at page breaks | left blank and marked "not legible in the source"; never filled from another book |
| pp. 103–117, dasha results | scattered single-line losses | marked "line lost in the scan" in 14-dasha-results.md |
| throughout | roman numerals garbled (xiv → "xlv", xxii → "xx ii"), chapter numbers ("CHAPTER n", "CHAPTER m"), page numbers ("1ft", "4^"), word-level slips ("Redemplion", "himslelf", "caclulated") | corrected silently where obvious, since they carry no astrological content |

## What is in the book but not in this repository

- **Ashtakavarga** — chapter XII refers to Raman's separate book on it. Not
  implemented.
- **Full Shadbala** — chapter III refers to *Graha and Bhava Balas*. Not
  implemented; see 08-strength.md for what is implemented instead.
- **Varshaphala, muhurta, electional astrology** — other books in the series.
- **The Navamsa-count methods** for the number of brothers and the number of
  children — the rules are recorded in 10-interpretation.md but deliberately not
  implemented, because they are the rules most likely to be read as a prediction
  about a real family.
- **The Sade Sati first/second/third passage reading** — recorded in
  12-transits.md, not implemented; see the caution there.

## What is not in the book but is in this repository

Flagged **STANDARD** wherever it appears:

- the natural friendship rows for Rahu and Ketu;
- the combustion orbs;
- the fuller house significations;
- the conventional Parashari exaltation degrees for Rahu and Ketu (Taurus 20°
  and Scorpio 20° are actually the book's, but they are the standard values
  too);
- the IAU 2006 precession polynomial behind the Lahiri ayanamsa;
- the mean-node formula (Meeus, ch. 47);
- the ascendant and midheaven formulae;
- the Porphyry/Sripati house cusps;
- the panchanga (the book does not treat it at all).

## Copyright

The *book* is under copyright and this repository does not reproduce it. What
is here is a structured summary of its rules — the kind of extraction a student
would make for their own study — together with code that was written from
scratch. Do not redistribute the scanned PDF with this repository.

The code is MIT licensed (see `LICENSE`). The prose in `docs/` is a derivative
summary of a copyrighted work and is provided for study and commentary; if you
intend to publish it commercially, take your own view on the permissions you
need.

## Verifying the extraction

The strongest check available is that the book carries a fully worked example,
and the engine reproduces it. Chapter II prints the nine grahas and the
Ascendant for a birth at Madras on 2 November 1935; `tests/test_engine.py`
asserts every one of them, plus the Rasi chart's structure, the dignities, the
Mars–Jupiter exchange, the navamsa rule, and the Vimshottari balance of 6y 1m
15d.

If a transcription error had crept into the exaltation table, the ayanamsa, the
nakshatra spans, the navamsa formula or the dasha arithmetic, those tests would
fail. They pass to within a couple of arcminutes.
