# 12. Transits (Gochara)

**SOURCE:** chapter XII, "Transits or Gochara".

## The principle

> "In predicting Gochara results the Moon and the birth constellation play a
> prominent part. The sign in which the Moon is situated in the birth horoscope
> is the Janma Rasi. The passage of planets through certain angular positions
> from the radical Moon is technically termed Gochara."

So **every gochara result is read from the Janma Rasi**, not from the
Ascendant. A planet transiting the sign the Moon occupied at birth is "in the
1st house" for gochara purposes, whatever it is doing in the Rasi chart.

The book's physical account of why transits matter: planetary movement "gives
rise to the stimulation of radioactive disintegration which on falling on the
individual produces psycho-physical changes in his character, disposition and
surroundings". That is the book's model, not a finding.

## The tables

Each table reads: house from the Janma Rasi → result. Cells marked **—** are
where the scan is damaged at a page break; they are left blank rather than
filled from another book.

### The Sun

| House | Result |
|---|---|
| 1 | change of place |
| 2 | loss of wealth |
| 3 | advent of money and success |
| 4 | dishonour |
| 5 | sorrow, ill-health and embarrassment |
| 6 | ruin to foes |
| 7 | travelling and ill-health |
| 8 | quarrels and unpleasantness |
| 9 | — |
| 10 | — |
| 11 | earnings *(fragment survives)* |
| 12 | quarrels and pecuniary loss |

### The Moon

| House | Result |
|---|---|
| 1 | good disposition and food |
| 2 | expenditure |
| 3 | gain of money |
| 4 | accidents or ill-health |
| 5 | unpleasantness |
| 6 | auspicious results |
| 7 | friendship and gains |
| 8 | trouble and expenses |
| 9 | intimidation and worry |
| 10 | gains and well-being |
| 11 | happiness and pecuniary gain |
| 12 | misery and loss |

### Mars

| House | Result |
|---|---|
| 1 | sorrow and accidents |
| 2 | loss and expenses |
| 3 | pecuniary gain and pleasure |
| 4 | trouble from foes |
| 5 | loss of money and illness to children |
| 6 | gain of money |
| 7 | quarrelling, fatigue, accident to wife |
| 8 | fear and danger |
| 9 | indisposition and expenses |
| 10 | change and sorrow |
| 11 | acquisition of money and peace of mind |
| 12 | disease and falls from elevations |

### Mercury

| House | Result |
|---|---|
| 1 | trouble and servitude |
| 2 | gain of money |
| 3 | ill-luck |
| 4 | good fortune |
| 5 | poverty and loss |
| 6 | success |
| 7 | illness and vice |
| 8 | pleasure and auspicious events |
| 9 | — |
| 10 | — |
| 11 | happiness |
| 12 | misunderstandings |

### Jupiter

| House | Result |
|---|---|
| 1 | travelling and fear, rewards |
| 2 | profits and gain of money |
| 3 | obstacles, ill-health |
| 4 | loss of money and expenses |
| 5 | happiness, birth of children and pleasure |
| 6 | grief and misery |
| 7 | good health and fortune |
| 8 | danger and dissatisfaction |
| 9 | access to wealth and risk of losing position and reputation |
| 10 | separation, loss of health and wealth |
| 11 | profit and success in undertakings |
| 12 | affliction, unexpected troubles and mental worry |

### Venus

| House | Result |
|---|---|
| 1 | good health and pleasure |
| 2 | gain of money and good luck in general |
| 3 | happiness and pleasant associations |
| 4 | pecuniary gain |
| 5 | happiness and birth of a son |
| 6 | fear of foes and unexpected expenses |
| 7 | worry, grief and quarrels with wife |
| 8 | good income |
| 9 | gain of money, apparel and friends |
| 10 | indisposition and scandal |
| 11 | pleasure and profit |
| 12 | good finance and peace of mind |

### Saturn

| House | Result |
|---|---|
| 1 | danger and loss of money |
| 2 | sorrow and accidents |
| 3 | gain and prosperity |
| 4 | expenses, sickness |
| 5 | — |
| 6 | — *(the fragment "…and access to property" survives)* |
| 7 | mental and physical affliction and great suffering |
| 8 | fear, bad reputation and worry |
| 9 | loss of money, ill-health and misfortune |
| 10 | loss of wealth |
| 11 | cruelty and access to money |
| 12 | danger, worry and financial strain |

### Rahu and Ketu

The book gives one table for both.

| House | Result |
|---|---|
| 1 | sickness and fear |
| 2 | loss of wealth, quarrelling and misunderstandings |
| 3 | happiness and good finances |
| 4 | sickness, danger and sorrow |
| 5 | financial loss and worry |
| 6 | pleasure and happiness |
| 7 | loss and fear |
| 8 | danger to life |
| 9 | quarrelling, mental worry and loss |
| 10 | enmity |
| 11 | happiness and acquisition of money |
| 12 | expenses and danger |

## Sade Sati

> "Regarding Saturn, his transit in the 12th, the 1st and the 2nd from the
> radical Moon has special significance as it goes under the technical name of
> Sade Sati (7½ years' Saturn), as, to pass through the signs, in his usual
> course it takes 7½ years. This particular period is dreaded by many as highly
> malefic; unless the ruling period is powerful, the subject of the horoscope is
> bound to suffer unexpected miseries."

The summarised results for those three houses: "quarrels and misunderstandings,
implication, entanglement in litigation, failure of business, restlessness of
mind, change of place, sickness among family members, death of children and
mental worry."

And the book's striking claim about repetition:

> "One having good longevity can come under the sway of '7½ years' Saturn'
> thrice in his lifetime. During the first time most of the above results will
> manifest; the second time, no evil results will occur while during the third
> time the death of the native is invariably caused, unless ruling Dasa does
> not warrant death."

**CAUTION:** the third-passage claim is the single most alarming sentence in the
book. It is not something any software should assert about a person. The engine
reports Sade Sati as *active or not*, with the source's description of the
period, and stops there — it does not implement the first/second/third passage
reading at all.

## How to weight transits

> "Of the different planets, the transiting effects of the slow moving ones,
> viz., Jupiter, Saturn and Rahu are universally held to be most powerful. The
> triennial influence may be read from Saturn, the yearly influence from Jupiter,
> the monthly influence from the Sun and Mercury, and the daily influence from
> the Moon."

The engine's reading reports Jupiter, Saturn and Rahu (and Ketu, which moves
with Rahu) by default, for exactly this reason.

## Degree conditions and exceptions

> "There are exceptions under which certain planets said to produce malefic
> effect while transiting certain houses, do not manifest anything unfavourable
> at all."

> "Mars and the Sun produce effects during their transit when they are in the
> first 10 degrees of a sign. Jupiter and Venus become effective when they are
> in the 2nd ten degrees while Rahu produces results throughout the entire sign."

So a transit result only bites in a particular third of the sign for some
planets. The engine reports the degree in sign so that this can be applied by
the reader; it does not gate on it.

> "Timing events according to transits in the light of the Ashtakavarga has been
> enumerated in my book *The Ashtakavarga System of Prediction*."

Ashtakavarga is not in this book and is not implemented.

## The standing rule

> "The Gochara results should never be interpreted without reference to the
> ruling period and sub-period."

Every transit reading this engine produces carries that sentence with it.
