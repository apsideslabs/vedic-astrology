# 11. Yogas

**SOURCE:** chapter III, "Yogas" and "Important Yogas".

> "Yogas are formed when one planet or sign is related to another of the same or
> different kind by way of aspect or conjunction."

## The preliminary examination

Before any yoga is read, the book requires two checks:

> "In forming a general judgment of a horoscope, it is important to examine that
> the Ascendant and its lord are powerful, well associated, and have no malefic
> aspects. A similar examination with regard to the Moon is also essential."

Everything below is subordinate to that.

## Papakarthari and Subhakarthari

> "If the Ascendant is hemmed in between two malefics, such a combination goes
> under the name of Papakarthari Yoga. Benefics on either side will give rise to
> Subhakarthari Yoga. The former tends to subject the native to a chequered
> career and the latter will augment the good."

"Hemmed in" means planets in the 12th and the 2nd from the Ascendant.

The book reuses Papakarthari in chapter IX: "If the 7th house is hemmed in
between two malefics (Papakarthari Yoga), then married life proves burdensome
and miserable."

## Rajayoga

> "If the lords of the trines combine with the lords of the angles, with some
> connection with the lord of the 1st house, it leads to a Rajayoga indicating
> high power and authority."

Three conditions, all required:

1. a lord of a trine (1, 5 or 9) and a lord of an angle (1, 4, 7 or 10) are
   **combined** — conjunct in one sign;
2. there is a **connection with the lord of the 1st** — either one of the pair
   *is* the 1st lord, or the 1st lord is in the same sign;
3. "The proper situation of such planets in Rasi and Navamsa results in a
   Rajayoga" — so the Navamsa position strengthens or weakens the claim.

The engine implements exactly conditions 1 and 2 and reports the Navamsa
position of each participant without gating on it.

## Yogakaraka

> "Each Ascendant has a key planet, Yogakaraka (planets causing beneficial
> results) and Maraka (death-inflicting planets)."

A yogakaraka is a single planet that owns **both an angle and a trine** from the
Ascendant. Because it escapes the Kendradhipati dosha described in chapter III
("when benefics own quadrants, they produce evil"), such a planet becomes the
best planet in the chart. The book gives a table of Kruras (malefics), Soumyas
(benefics), Yogakarakas and Marakas for each Ascendant on pp. 30–31.

**The scan of that table is heavily damaged** — the columns are interleaved by
the OCR and several rows are unreadable. Rather than transcribe a corrupted
table, the engine **derives** the yogakaraka from ownership, which is the rule
the table encodes, and **derives** the marakas as the lords of the 2nd and 7th
(the two houses chapter IV names as death-inflicting). If you want the book's
printed table verbatim, it needs the paper copy.

## The Moon yogas

These are the most-used yogas in the book, and all four are defined from the
2nd and 12th from the Moon.

| Yoga | Condition | Result (as given) |
|---|---|---|
| **Sunapha** | two or more planets (excepting the Sun) in the 2nd from the Moon | intelligent and reputed, occupies a high position, earns well by his own exertions |
| **Anapha** | two or more planets (excepting the Sun) in the 12th from the Moon | enjoys worldly pleasure of every kind, unruffled temper |
| **Durdhura** | planets on either side of the Moon | rare characteristics of self-sacrifice, good servants, wealth and conveyances |
| **Kemadruma** | absence of planets on either side of the Moon | dirty habits, sinful, wicked, subservient, sorrowful |

**Kemadruma's cancellation:** "This Yoga gets counteracted if there is a planet
in a quadrant from the Moon." The engine reports a separate
`Kemadruma-bhanga` yoga when the cancellation applies, so the two are never
confused.

## Adhiyoga

> "Benefics in the 6th, the 7th and the 8th house from the Moon. Results —
> happy, fearless, high position, influential and long-lived."

Note that this uses houses that are otherwise difficult — 6, 7, 8 — which is
unusual and is exactly why the book calls it out.

## Gurumangala

Chapter VI names it in passing while discussing wealth: "In the Navamsa, Mars
and Jupiter (Gurumangala Yoga) are in the 2nd from the Moon." The engine detects
Jupiter and Mars in the same sign and flags it, noting that the book's instance
is the 2nd from the Moon.

## What is missing

The book says: "There are any number of Yogas in relation to the Sun, in
relation to the Moon, in relation to the Ascendant and in relation to the
planets and so forth. To include [them all]…" — and then the page turns and the
list is lost. The first entry of the "Important Yogas" section is cut in half by
the page break; only its tail survives ("in an angle from each other. RESULTS —
long life, fame, influential relations, general success, head of a political,
social or religious organisation"), which reads like the result of a
Sun/Moon-based yoga but cannot be identified with confidence.

So the book names eight yogas in full — Papakarthari, Subhakarthari,
Rajayoga, Adhiyoga, Sunapha, Anapha, Durdhura and Kemadruma — plus Gurumangala
in passing, and that is what the engine detects. It does **not** implement the
larger classical corpus (Gajakesari, Panchamahapurusha, the Nabhasa yogas,
Dharma-Karmadhipati, Viparita Raja) because the book does not contain them. A
production app should add them from a fuller source and keep the same
`{name, present, planets, description, source}` shape.
