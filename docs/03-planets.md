# 3. The nine planets (Grahas)

**SOURCE:** chapter I, "The Planets" and "Planetary Nature and Indications".

## What counts as a "planet"

Hindu astrology takes cognizance of **nine grahas**. The book is explicit that
the word is used "in the sense of a celestial body or point which has the
property of attraction":

| Sanskrit | English | Note |
|---|---|---|
| Ravi | the Sun | a star |
| Chandra | the Moon | a satellite of the earth |
| Kuja | Mars | |
| Budha | Mercury | |
| Guru | Jupiter | |
| Sukra | Venus | |
| Sani | Saturn | |
| Rahu | Dragon's Head | an imaginary point — the concourse of the orbits of the earth and the Moon |
| Ketu | Dragon's Tail | the opposite point |

Hence the Sun, a star, the Moon, a satellite, and Rahu and Ketu, two
imaginary points, are all referred to "under the somewhat forced name of
planets". Uranus, Neptune and Pluto "are considered to have no effect on
human affairs".

**Note on Rahu and Ketu:** the book treats them as the nodes of the Moon's
orbit, which is exactly what the engine computes. The engine uses the **mean**
node, which is what Raman's own ephemeris tabulates; the true node differs by
up to about 1°40′.

## Nature and indications

Transcribed from the book, condensed but not altered:

**The Sun** — masculine, malefic, copper colour, philosophical tendency,
royal, ego, father, sons, patrimony, self-reliance, political power, windy and
bilious temperament, month, places of worship, money-lenders, goldsmith,
bones, fires, coronation chambers, doctoring capacity.

**The Moon** — mind, mother; **benefic when waxing, malefic when waning**;
feminine, white colour, women, sea-men, pearls, gems, water, fishermen,
stubbornness, romances, bath-rooms, blood, popularity, human responsibilities.

**Mars** — brothers, masculine, blood-red colour, malefic, refined taste, base
metals, vegetation, rotten things, orators, ambassadors, military activities,
commerce, aerial journeys, weaving, public speakers.

**Mercury** — **benefic if well associated**, hermaphrodite, green colour,
mercantile activity, public speakers, cold, nervous, intelligence.

**Jupiter** — masculine, benefic, bright yellow colour, devotion, progeny,
truthfulness, religious fervour, philosophical wisdom, corpulence.

**Venus** — feminine, benefic, mixture of all colours, wife, love affairs,
sensual pleasure, family bliss, vitality.

**Saturn** — malefic, hermaphrodite, dark colour, stubbornness, impetuosity,
demoralisation, windy diseases, despondency, gambling.

**Rahu** — malefic, feminine, renunciation, corruption, epidemics.

**Ketu** — hermaphrodite, malefic, religious, sectarian principles, pride,
selfishness, occultism, mendicancy.

The book adds the governing caution: "Malefics are always inclined to do
harm; but under certain conditions, the intensity of the mischief is
tempered. Benefics, on the other hand, tend to do good; but sometimes they
also become capable of doing harm."

**Note that Mercury and the Moon are conditional.** Mercury is a benefic only
when well associated; the Moon is benefic when waxing and malefic when waning.
The engine keeps them in the benefic list (they are benefics by nature) but
the reading rules test for affliction separately.

## Karakas — what each planet signifies

**SOURCE:** chapter I, "Karakas".

| Karaka of | Planet |
|---|---|
| father | Sun |
| mother | Moon |
| brother | Mars |
| profession | Mercury |
| children (Putrakaraka) | Jupiter |
| wife or husband (Kalatrakaraka) | Venus |
| longevity (Ayushkaraka) | Saturn |
| maternal relations | Rahu |
| paternal relations | Ketu |

## Exaltation

**SOURCE:** chapter I, "Exaltation". A planet is exalted in a particular sign;
within that sign one degree is its point of **deep exaltation**. The power to
do good when exalted is greater than when in its own sign.

| Planet | Deep exaltation |
|---|---|
| Sun | Aries 10° |
| Moon | Taurus 3° |
| Mars | Capricorn 28° |
| Mercury | Virgo 15° |
| Jupiter | Cancer 5° |
| Venus | Pisces 27° |
| Saturn | Libra 20° |
| Rahu | Taurus 20° |
| Ketu | Scorpio 20° |

**Results of exaltation** as the book gives them:

- **Sun:** learned, religious, strong, placid, charitable.
- **Moon:** rich, sedulous, a man of letters.
- **Mars:** possessing great fervour, educated, famous, princely.
- **Mercury:** learned, cheerful, fortunate, respected.
- **Jupiter:** chief of men, strong, respected, given to anger, supporting a
  large number of men.
- **Venus:** charitable, lives to a good old age, many qualities.
- **Saturn:** skilful, charitable, opulence, long life, loving husband.
- **Rahu or Ketu:** wealthy.

## Debilitation

**SOURCE:** chapter I. "The debilitation or depression points are found by
adding 180° to the maximum points given above." While in a state of fall,
planets give results **contrary** to those when in exaltation.

So: Sun debilitated in Libra 10°, Moon in Scorpio 3°, Mars in Cancer 28°,
Mercury in Pisces 15°, Jupiter in Capricorn 5°, Venus in Virgo 27°, Saturn in
Aries 20°, Rahu in Scorpio 20°, Ketu in Taurus 20°.

## Moolatrikona

**SOURCE:** chapter I, "Moolathrikonas". A planet's own special division of
its own sign, stronger than mere ownership.

| Planet | Moolatrikona |
|---|---|
| Sun | Leo 0°–20° |
| Moon | Taurus 4°–20° |
| Mars | Aries 0°–12° |
| Mercury | Virgo 16°–20° |
| Jupiter | Sagittarius 0°–10° |
| Venus | Libra 0°–15° |
| Saturn | Aquarius 0°–20° |

**STANDARD:** most modern references give the Moon's moolatrikona as Taurus
4°–30°. The engine uses the book's 4°–20°; change `zodiac.MOOLATRIKONA` if you
want the other convention. Mars's upper bound is printed as "0° to it" in the
scan and is reconstructed as 12°, which is the only value that makes sense of
the standard table.

## Ownership

**SOURCE:** chapter I, "Ownership".

| Planet | Rules |
|---|---|
| Sun | Leo |
| Moon | Cancer |
| Mars | Aries, Scorpio |
| Mercury | Gemini, Virgo |
| Jupiter | Sagittarius, Pisces |
| Venus | Taurus, Libra |
| Saturn | Capricorn, Aquarius |

"A planet situated in its own sign is rendered powerful to do good."

## The ten Avasthas (states)

**SOURCE:** chapter I, "Planetary Avasthas" — "Avasthas are states of
existence which planets get when occupying certain positions. They are 10 in
number."

| Avastha | Condition | Result given |
|---|---|---|
| Deeptha | exaltation | good progeny, gains, respect from elders, wealth |
| Swastha | own house | fame, position, lands, happiness |
| Muditha | a friendly house | happiness, good temper, good wife |
| Santha | auspicious divisions | strength and courage, comfort and happiness |
| Sakta | retrogression | courage, wealth, reputation |
| Peedya | residence in the last quarter of a sign (inauspicious subdivision) | incarceration, criminal tendencies, evil nature |
| Deena | unfriendly house | mental worry, sickness, degradation |
| Pikala | combustion — "planets very near the Sun become combust" | disease, disgrace, loss of children |
| Khala | debilitation | losses, mean birth, quarrels, unpleasantness |
| Bheetha | in acceleration | losses from various sources, torture, mean habits |

Note that **retrogression is a strength, not a weakness** in this scheme
(Sakta: courage, wealth, reputation), and that **acceleration is the bad
state** (Bheetha). That is the opposite of the modern Western instinct, and it
matches the book's treatment of Chestabala in chapter III
(see [08-strength.md](08-strength.md)).

The engine implements Deeptha, Swastha, Muditha, Deena, Pikala and Khala
directly through its dignity ladder; Santha, Peedya, Sakta and Bheetha are
not yet wired into the reading.

## Combustion

**SOURCE:** chapter I mentions the phenomenon only — "planets very near the
Sun become combust". **STANDARD:** the orbs used by the engine are the
conventional ones: Moon 12°, Mars 17°, Mercury 14° (12° when retrograde),
Jupiter 11°, Venus 10° (8° retrograde), Saturn 15°.

## Planetary days and colours

The book uses colour and weekday as signifiers in the dasha and transit
chapters (Saturn produces death by chills; Mars by fevers and haemorrhage)
rather than as a systematic table, so they are recorded above with each
planet's nature and not tabulated separately.
