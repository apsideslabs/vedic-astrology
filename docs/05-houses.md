# 5. The twelve houses (Bhavas)

**SOURCE:** chapter I, "The Twelve Houses" and "Kinds of Houses".

## Houses are not signs

This is the first thing the book insists on:

> "The twelve houses are not necessarily coincident with the twelve signs of
> the zodiac. They are, in fact, variable. Each sign is always 30° in extent.
> But the length of a house or Bhava depends upon the time of birth and the
> latitude of the place of the birth."

Two different things are therefore being drawn at once, and the book uses both:

1. **The Rasi chakra** — whole signs. The rising sign is the first bhava and
   each following sign is the next bhava. Chapter II says that "for ordinary
   purposes of prediction a zodiacal diagram (Rasi Chakra) with the Ascendant
   marked is sufficient".
2. **The bhava chakra** — houses of unequal extent, whose **mid-points
   (bhavamadhyas)** are obtained by taking Western house cusps and deducting
   the ayanamsa.

The engine defaults to whole signs, and offers Sripati (Porphyry) cusps and
equal houses for the second reading. See [07-calculation.md](07-calculation.md).

## The significations

**SOURCE:** chapter I, transcribed as printed (the scan loses a few words, and
the gaps are shown rather than guessed):

| House | Significations |
|---|---|
| 1st | birth, body, appearance |
| 2nd | family, source of death [sic], property, vision |
| 3rd | intelligence, brothers, sisters |
| 4th | vehicles, general happiness, education, mother and landed properties |
| 5th | fame, children |
| 6th | debts, diseases, misery, enemies |
| 7th | wife or husband, tact, death |
| 8th | longevity, gifts |
| 9th | God, guru, father, travel, piety |
| 10th | occupation, Karma, philosophical knowledge |
| 11th | gains |
| 12th | losses, moksha |

**CAUTION:** "source of death" in the 2nd and "death" in the 7th are the
book's own shorthand — it treats the 2nd and 7th as **maraka** (death-
inflicting) houses in chapter IV. It is not a claim that the 2nd house causes
death.

**STANDARD:** the fuller lists a practitioner expects are these, and the
engine's `zodiac.HOUSE_SIGNIFICATIONS` uses a merged version:

- 2nd: family, speech, wealth, food, right eye
- 3rd: siblings, courage, communication, short journeys, hands
- 4th: mother, home, land, vehicles, education, happiness
- 5th: children, intelligence, past merit, romance, authority
- 6th: enemies, disease, debt, service, litigation, maternal uncle
- 7th: spouse, partnership, business, public dealings
- 8th: longevity, sudden events, inheritance, occult, chronic illness
- 9th: father, guru, dharma, fortune, long journeys, higher learning
- 10th: career, status, karma, authority, father (in some schools)
- 11th: gains, elder siblings, friends, fulfilment of desires
- 12th: loss, expenditure, foreign lands, moksha, sleep, confinement

## Kinds of houses

**SOURCE:** chapter I, "Kinds of Houses".

| Group | Houses | Sanskrit |
|---|---|---|
| Quadrants / angles | 1, 4, 7, 10 | Kendras |
| Trines | 1, 5, 9 | Trikonas |
| Succeedent | 2, 8, 11 | Panaparas |
| Cadent | 3, 6, 12 | Apoklimas |

And the strength rule attached to them:

> "Planets in angles generally become fairly strong; in succeedent houses
> slightly strong and in cadent houses, utterly weak. In trines, they become
> very strong."

That is the whole basis of the engine's house-placement term in
`strength.positional_strength`, and it is why trines carry a bonus on top of
the kendra term.

**CAUTION:** the 6th, 8th and 12th are also the **dusthanas**, the houses of
difficulty, which the book does not name as a group but treats as such
throughout ("lords of 3, 6, 8 and 11 do evil and cause miseries").

## Karakas of the houses

**SOURCE:** chapter I. Each planet is the Karaka of some matter:

| Matter | Karaka |
|---|---|
| father | Sun |
| mother | Moon |
| brother | Mars |
| profession | Mercury |
| children | Jupiter |
| wife or husband | Venus |
| longevity | Saturn |
| maternal relations | Rahu |
| paternal relations | Ketu |

The book pairs each karaka with the house that governs the same matter, and a
judgement requires **all three** to be examined together: the house, its lord,
and the karaka. Chapter IX says it plainly for children — "Favourable
disposition of all these three factors is a great asset for getting good,
long-lived and obedient children" — and chapter VIII does the same for the
parents (4th house, its lord and the Moon; 9th house, its lord and the Sun).

## Reading a house

**SOURCE:** chapter III, "Reading a House". A house is judged from:

1. the strength, aspect and conjunction of the lord of the house;
2. the planets occupying it;
3. the planets aspecting it;
4. the sign on it and the lord of that sign's condition;
5. the same factors in the Navamsa;
6. the same factors counted from the Moon as well as from the Ascendant.

The book repeats "from the Ascendant as well as from the Moon" in chapters IV,
VI, VII, VIII, IX and XII. Any implementation that reads only from the Lagna
is doing half the job; the engine exposes `moon_sign()` and the Navamsa sign
of every planet so that a caller can do both.

## Houses counted from other houses

The book uses derived houses freely and calls them out explicitly:

- the father's finances are "the 2nd from the 9th", his ills "the 6th from the
  9th", his profession "the 10th from the 9th" (chapter VIII);
- children are judged from the 5th from the Ascendant **or from the Moon**
  (chapter IX);
- the Moon's house and "the 8th from the Moon's sign" decide longevity
  (chapter IV);
- the whole of gochara is read from the Janma Rasi, i.e. from the Moon
  (chapter XII).
