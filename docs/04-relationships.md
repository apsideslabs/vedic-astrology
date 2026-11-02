# 4. Relations between planets

**SOURCE:** chapter I, "Relations between Planets".

The book says the subject is dealt with fully in Raman's *Hindu Predictive
Astrology*, and gives the outline here. Relations are of **two kinds,
permanent and temporary**.

> "A planet is said to be a friend of the other whose rays it does not
> counteract."

## Permanent (natural) friendship

The book prints the table on pp. 7–8. **The scan is badly damaged across the
page break**: the rows for the Sun, Moon, Mars and Mercury are cut through,
and the Venus, Jupiter and Saturn rows are reordered by the OCR. The table
below is the standard Parashari table, which is what the book is presenting;
the fragments that survive in the scan are consistent with it.

| Planet | Friends | Neutral | Enemies |
|---|---|---|---|
| Sun | Moon, Mars, Jupiter | Mercury | Venus, Saturn |
| Moon | Sun, Mercury | Mars, Jupiter, Venus, Saturn | — |
| Mars | Sun, Moon, Jupiter | Venus, Saturn | Mercury |
| Mercury | Sun, Venus | Mars, Jupiter, Saturn | Moon |
| Jupiter | Sun, Moon, Mars | Saturn | Mercury, Venus |
| Venus | Mercury, Saturn | Mars, Jupiter | Sun, Moon |
| Saturn | Mercury, Venus | Jupiter | Sun, Moon, Mars |
| Rahu | Venus, Saturn, Mercury | — | Sun, Moon, Mars |
| Ketu | Mars, Venus, Saturn | — | Sun, Moon |

**STANDARD:** the Rahu and Ketu rows are not in the book at all — it deals
with the seven grahas. The values above are the common convention.

## Temporary friendship

**SOURCE:** chapter I, verbatim:

> "Planets found in the 2nd, 3rd, 4th, 10th, 11th and 12th signs from any
> other planet become the latter's temporary friends. The others are its
> enemies."

So temporary friendship is a function of **sign position only**:

| Distance from the planet | Temporary relation |
|---|---|
| 2, 3, 4, 10, 11, 12 | friend |
| 5, 6, 7, 8, 9 | enemy |
| same sign | own |

The book's worked illustration: with Jupiter in the 2nd from the Sun, Venus in
the 12th, and the Moon and Mars in the 3rd, "Jupiter, Venus, Moon, Mars and
Mercury are the Sun's temporary friends. Saturn alone is the Sun's enemy,
temporarily."

## Mixed relations

**SOURCE:** chapter I, "Mixed Relations" — "In order to find the strengths of
planets we have to mix the temporary relations and the permanent relations.
Thus a temporary enemy plus a permanent or natural enemy becomes a bitter
enemy."

| Natural relation | Temporary friend | Temporary enemy |
|---|---|---|
| Friend | intimate friend | friend |
| Neutral | friend | enemy |
| Enemy | neutral | bitter enemy |

That is the standard combination table and it is what the engine implements in
`strength.compound_relation`.

The book's caution, which matters more than the table:

> "It is to be understood that a temporary friendship will not entirely
> overcome a radical and constitutional enmity."

## Relations between planets and signs

**SOURCE:** chapter I. Four kinds of relationship are of particular
importance: **ownership, exaltation, debilitation and moolatrikona**. All four
are tabulated in [03-planets.md](03-planets.md).

The engine ranks them in the order the book implies — exaltation outranks
moolatrikona ("the power to do good when in exaltation is greater than when in
its own sign"), which outranks ownership, which outranks friendship:

```
exalted  >  moolatrikona  >  own  >  intimate friend  >  friend
         >  neutral  >  enemy  >  bitter enemy  >  debilitated
```

## Why relations matter

Everything downstream uses them. The book uses friendship to:

- decide whether a planet is "rendered powerful to do good" in a sign
  (chapter I);
- decide the quality of a dasha, since "the relations between the lords of
  the main period and sub-period should be considered when predicting events
  during their time" (chapter X);
- decide longevity, by asking whether the lord of the Lagna and the lord of
  the 8th from the Moon are friendly, inimical or neutral (chapter IV);
- decide whether an aspect is good or bad, since "an aspect is good or bad
  according to the relation between the aspecting and the aspected body"
  (chapter I).
