# 9. Vimshottari dasha — the timing system

**SOURCE:** chapter X, "Timing Events".

## Why this system

> "There are any number of Dasas in vogue in India but we propose to deal with
> Vimshottari or Udu Dasa. In the choice of any particular type of Dasa, the
> guiding factor should be experience. Vimshottari, in our humble opinion, has
> been built upon a firm foundation."

The book notes that some modernising writers reject it for lacking a
"scientific basis", and answers that they "forget the value of experience
which should of course be the true criterion of all knowledge". That is the
whole of its defence; there is no derivation offered, here or anywhere.

## The nine periods

**SOURCE:** chapter X, "Table of Dasas".

| Lord | Years |
|---|---|
| Ketu | 7 |
| Venus | 20 |
| Sun | 6 |
| Moon | 10 |
| Mars | 7 |
| Rahu | 18 |
| Jupiter | 16 |
| Saturn | 19 |
| Mercury | 17 |
| **Total** | **120** |

The order is fixed and cyclic, and it is the same order in which the lords
repeat across the 27 nakshatras: Ashwini is Ketu, Bharani Venus, Krittika Sun,
Rohini Moon, Mrigashira Mars, Ardra Rahu, Punarvasu Jupiter, Pushya Saturn,
Ashlesha Mercury, and then the cycle begins again at Magha with Ketu.

## Finding the ruling period at birth

> "In order to calculate the ruling period at birth and date of its
> commencement it is necessary to obtain the position of the Moon at the time
> of birth. Every constellation covers 13° 20′ of the zodiacal space."

The procedure, from the book's worked example (Moon at Sagittarius 22° 35′):

1. Locate the Moon in its nakshatra. In Sagittarius the first 13° 20′ is Mula,
   the next 13° 20′ is Purva Ashadha, and the last 3° 20′ is Uttara Ashadha.
2. `22° 35′ − 13° 20′ = 9° 15′` — the Moon has passed 9° 15′ of Purva Ashadha.
3. Purva Ashadha is ruled by **Venus**, whose period is 20 years.
4. Find the part of the 20 years already elapsed:

```
13° 20′ (800′) : 9° 15′ (555′) :: 20 years : x
x = 13 years 10 months 15 days     <- expired before birth
20 − 13y 10m 15d = 6 years 1 month 15 days   <- balance at birth
```

So the native is born in **Venus dasha with 6y 1m 15d to run**.

**Implementation note:** the engine converts the degrees to a fraction of the
nakshatra and multiplies, which is the same thing exactly:
`balance = lord_years × (1 − elapsed_fraction)`. It also back-dates the start
of that mahadasha by the elapsed fraction, which is how you get a timeline in
which the first period begins before birth.

## Sub-periods (Bhuktis)

**SOURCE:** chapter X. Each main period is divided into nine sub-periods, in
the same cyclic order starting from the main lord; each sub-period is divided
again into antaras, and so on down to the *swara*, "the period necessary for
the inhaling and exhaling of breath". "Nevertheless for all practical purposes
the sub-period will be found to be quite sufficient."

The book gives an arithmetic shortcut:

> "Multiply together the number of years of the Dasa period of the planet by
> the number of years of the Dasa period of the planet whose sub-period is
> desired. Then cutting off the last figure of the product, multiply it by 3
> and keep that figure as days, the other figures in the product will be
> months."

Worked: Saturn's bhukti inside Mercury's dasha, `19 × 17 = 323` → "32 months
and 9 days".

**That shortcut is exactly the proportional rule.** The bhukti of planet B
inside the dasha of planet A lasts `A × B / 120` years. For 19 and 17:
`323/120 = 2.6917` years = 32.3 months = 32 months 9 days. The engine
therefore computes the proportion directly instead of reproducing the digit
trick, and a test asserts the two agree
(`test_sub_period_matches_book_shortcut`).

## Finding the bhukti at birth

> "With the expired portion of Dasa there are certain sub-periods ruling under
> the period which have also expired. After determining them we can say under
> what sub-period one's [birth] falls. Add together the Bhuktis from the
> beginning of Janma Dasa (ruling period), one by one, till the total is a
> little in excess over the expired period of Dasa at birth. Diminish the
> aggregate by the expired Dasa and the remainder gives the balance of
> unexpired Bhukti at birth."

The book's worked table, for Venus dasha with 13y 10m 15d expired:

| Bhukti | Years | Months | Days |
|---|---|---|---|
| Venus | 3 | 4 | 0 |
| Sun | 1 | 0 | 0 |
| Moon | 1 | 8 | 0 |
| Mars | 1 | 2 | 0 |
| Rahu | 3 | 0 | 0 |
| Jupiter | 2 | 8 | 0 |
| Saturn | 3 | 1 | 0 |
| **Total** | **16** | **0** | **0** |

`16y 0m 0d − 13y 10m 15d = 2y 1m 15d` — the balance of **Saturn's** bhukti in
Venus's dasha at birth.

## The year

The book's arithmetic is in years, months and days of 30 days. The engine uses
a **solar year of 365.25 days**, the convention of Indian ephemerides, and
exposes it as `YEAR_DAYS` so that 360-day and 365.2425-day variants can be
swapped in.

## How to judge a dasha

**SOURCE:** chapter X, "Judgment" and "General Results".

The core principle:

> "As a general proposition it may be stated that a planet during its Dasa
> generally gives the results pertaining to the houses it rules or aspects.
> Provided the lord is well placed, that is, in its own sign, exaltation,
> moolatrikona or friendly house, or conjunction with a yogakaraka or otherwise
> powerful, it will give rise to good results during its Dasa."

And the worked illustration: Jupiter, lord of the 2nd and 11th, placed in the
10th, aspected by the Moon (lord of the 6th), Saturn (lord of the Lagna and
12th) and Mars (lord of the 3rd and 10th). The book's reading: during Jupiter's
dasha the native "will amass considerable fortune" and there will be
"considerable professional success", because Jupiter chiefly gives the results
of the 2nd (wealth, family, influence) and the 10th (professional advancement,
livelihood) — but "he will also produce results due to the 1st, 6th and 3rd
houses", so the native is likely to be "ortu[ned] as regards Jupiter course in
Astrology" (the scan is damaged here) — i.e. the malefic ownerships dilute it.

The numbered rules:

1. "The Dasa periods of the lords of the 6th and the 8th produce harmful
   results unless they obtain beneficence otherwise."
2. "The effects of the ruling planets are intensified at such time as the Sun
   may be passing through the signs occupied by them or the signs over which
   they [rule]."
3. (The book's items 3 and 4 are lost in the scan.)
4. "…stand to be modified by the effect of Gochara or transiting planets."
5. "The periods of the lord of 5 and 9 are said to give rise to good results."
6. "Unfavourable results will be realised when the sub-lord and major lord are
   situated in the 6th and the 8th or the 12th and the 2nd from each other
   respectively."
7. "The general effects of the planets thus related must be taken into account,
   and their natural relation, as well as their temporary relation in the
   horoscope must be well considered."

The book's own caution about the whole enterprise:

> "It is certainly difficult to lay down any particular result which will apply
> to all. Conclusions should be drawn having regard to strength and propensity
> of the planet. The prediction should always be consistent with the person for
> whom it is intended, under the condition of life in which he is brought up as
> well as the physical possibility at the time."

## Transits must be combined with the dasha

**SOURCE:** chapter XII.

> "The Gochara results should never be interpreted without reference to the
> ruling period and sub-period. Suppose illness is indicated according to the
> prevailing Dasa and Bhukti; if, according to Gochara the period is likely to
> be bad then the illness would be of serious type. The results of the
> prevailing Dasa and Bhukti should be combined with the effects of Gochara
> before any predictions are ventured."

The engine's transit module carries this warning in its output and the reading
places the dasha section before the transit section for the same reason.

The planet-by-planet, house-by-house results a dasha is expected to give are
in [14-dasha-results.md](14-dasha-results.md).
