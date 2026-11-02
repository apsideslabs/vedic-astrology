# 6. Aspects (Drishti)

**SOURCE:** chapter I, "Drishti or Aspect".

## The basic rule

> "For a beginner it is enough to know that according to Hindu Astrology,
> aspects are counted from sign to sign. An aspect is good or bad according to
> the relation between the aspecting and the aspected body."

Sign to sign, not degree to degree. A planet in Aries aspects the whole of the
7th sign from it (Libra) and everything in it. That is why the engine's
`aspects` list is built from sign distances and carries no orb.

## The grades of sight

The book gives a graded sight, which is the *drishti pinda* used in the
stronger calculations:

| Distance | Sight |
|---|---|
| 3rd, 10th | a quarter sight (0.25) |
| 5th, 9th | a half sight (0.5) |
| 4th, 8th | three-quarters of a sight (0.75) |
| 7th | a full sight (1.0) |

## Special aspects

> "Saturn, Jupiter and Mars have special aspects. Saturn powerfully aspects
> the 3rd and the 10th houses, Jupiter the 5th and the 9th houses, and Mars,
> the 4th and the 8th."

Every graha has the full 7th aspect. In addition:

| Planet | Additional full aspects |
|---|---|
| Mars | 4th, 8th |
| Jupiter | 5th, 9th |
| Saturn | 3rd, 10th |
| Sun, Moon, Mercury, Venus, Rahu, Ketu | none — 7th only |

The engine implements this in `zodiac.SPECIAL_ASPECTS`; the partial-sight
fractions are in `zodiac.PARTIAL_SIGHT` and are reported per house by
`Chart.aspected_houses`.

## The book's worked illustration

> "If the Sun is in Cancer and Saturn in Taurus, we say that the Sun is in the
> 3rd from Saturn and consequently receives the powerful aspect (3rd house
> aspect) of Saturn."

Worth checking the arithmetic: Taurus → Cancer is 3 signs, so Cancer is the
3rd from Taurus, and Saturn's special 3rd-house aspect falls there. The engine
reproduces this — see `test_aspects_include_special_ones`.

## How to judge an aspect

The book gives these rules for reading an aspect once found:

1. **By nature of the aspecting planet.** "The opposition (7th house) aspect
   becomes extremely good when it is produced by Jupiter and the Moon. It is
   held to be good when benefics aspect each other." "As a natural malefic his
   [Saturn's] aspects are bad. But they produce good in case Saturn acquires
   beneficence by temporal situations."
2. **By ownership.** "If Mars is the lord of the 4th and the 9th houses, he
   gets special qualifications to produce good aspects (by the 4th house
   aspect)." A planet aspecting its own house — by the 7th or by a special
   aspect — "will naturally increase the signification of that house". The
   book's example: "Venus aspecting the 7th house gives a good and fair-looking
   wife and happiness on that account."
3. **By relation.** See [04-relationships.md](04-relationships.md): the aspect
   is good or bad according to the relation between the aspecting and the
   aspected body.
4. **By the nature of the aspect.** The 4th-house aspect of Mars is "a square
   aspect and sometimes this is evil and sometimes beneficial"; Jupiter's 5th
   and 9th are trines and therefore benefic in nature.
5. **The opposition has the same power as conjunction.** "The opposition
   aspect has the same power to do good or bad as conjunction, according to the
   nature of the planet involved."

## Where aspects are used downstream

- **Strength.** Drukbala: "Aspects of benefics give full Drukbala while
  aspects of malefics take away Drukbala" (chapter III).
- **Papakarthari and Subhakarthari** — the Ascendant hemmed in by malefics or
  benefics (chapter III).
- **Marriage:** "If the 7th house is hemmed in between two malefics
  (Papakarthari Yoga), then married life proves burdensome and miserable"
  (chapter IX).
- **Health:** "If the Moon is in Cancer or Scorpio in Rasi or in Navamsa and is
  powerfully aspected by malefics, the person suffers from diseases in the
  anus" (chapter V).
- **Longevity:** "The Ascendant and the 8th from the Moon's sign being aspected
  by malefics" produces Balarishta (chapter IV).
- **The dasha:** "a planet during its Dasa generally gives the results
  pertaining to the houses it rules **or aspects**" (chapter X).
