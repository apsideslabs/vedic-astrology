# 8. Strength

**SOURCE:** chapter III, "Hints on Judgment".

## The six Shadbalas

> "Six sources of strength and weakness (Shadbalas) should be determined for
> each planet in order to evaluate the worth of a horoscope properly. For the
> information of the reader, I shall make a passing reference to these sources
> of strength."

The book then names them and stops, deferring the measurement to its companion
volume *Graha and Bhava Balas*. They are:

### 1. Sthanabala — positional strength

> "The strength acquired due to residence in friendly, own and exaltation
> signs not only in the zodiacal diagram (Rasi Chakra) but also in the Navamsa
> and other subdivisions."

So the same dignity test is run twice: once on the Rasi sign, once on the
Navamsa sign, and a planet dignified in both (vargottama, when the two signs
coincide) is strongest.

### 2. Digbala — directional strength

> "Jupiter and Mercury are powerful in the Ascendant. The Sun and Mars get
> directional strength in the 10th house. Saturn is powerful in the 7th house,
> and Venus and the Moon become strong in the 4th house."

| Planet | Digbala house |
|---|---|
| Jupiter, Mercury | 1st |
| Sun, Mars | 10th |
| Saturn | 7th |
| Venus, Moon | 4th |

### 3. Chestabala — motional strength

> "The Sun and the Moon in Capricorn, Aquarius, Pisces, Aries, Taurus and
> Gemini constituting Uttrayana or summer solstice and Mars, Mercury, Jupiter,
> Venus and Saturn in retrogression or conjunction with the Full Moon get
> Chestabala."

Two conditions, and they are different for the luminaries and for the rest:

- **Sun and Moon:** in Capricorn through Gemini (Uttarayana, the northern
  course).
- **Mars through Saturn:** retrograde, or conjunct the Full Moon.

**Note:** retrogression *adds* strength here. That is consistent with the
Avastha "Sakta or retrogression: courage, wealth, reputation" in chapter I, and
it is the opposite of the modern Western instinct.

### 4. Kalabala — temporal strength

> "The Moon, Mars and Saturn are powerful during the night. The Sun, Jupiter
> and Venus are powerful during the day. Mercury is always powerful. Malefics
> and benefics are powerful during dark half and bright half of the lunar month
> respectively. Planets in their weekdays, months and years are said to be
> powerful."

| Condition | Strong |
|---|---|
| night | Moon, Mars, Saturn |
| day | Sun, Jupiter, Venus |
| always | Mercury |
| dark half (Krishna paksha) | malefics |
| bright half (Shukla paksha) | benefics |
| own weekday, month, year | that planet |

The lunar-month half is the same fact as "the Moon is benefic when waxing,
malefic when waning" from chapter I, seen from the strength side.

### 5. Drukbala — aspect strength

> "Aspects of benefics give full Drukbala while aspects of malefics take away
> Drukbala."

The engine already records every aspect with its sign distance and sight
fraction; Drukbala is the sum over incoming aspects, signed by the aspecting
planet's nature.

### 6. Saisargikabala — natural strength

> "Each planet is supposed to produce a particular measure of strength
> permanently irrespective of its position. The Sun, Moon, Venus, Jupiter,
> Mercury, Mars and Saturn are strong in descending order. The Sun is the most
> powerful and Saturn is the least powerful."

So the fixed order is Sun > Moon > Venus > Jupiter > Mercury > Mars > Saturn.

## What this engine actually computes

**This is important and is stated plainly in the API too.** The engine computes
a **simplified positional strength**, not Shadbala. It is an additive score
with every component reported separately, so a reading can be audited:

| Component | Value |
|---|---|
| dignity (exalted … debilitated) | +2.0 … −2.0 |
| house kind — kendra / panapara / apoklima | +0.75 / 0 / −0.5 |
| trine (1, 5, 9) | +0.5 |
| Digbala (in its directional house) | +0.5 |
| Chestabala (retrograde) | +0.25 |
| combustion | −0.75 |
| vargottama (Navamsa sign = Rasi sign) | +0.5 |

The raw total is mapped onto 0–100 for display only. What is **not**
implemented: the full Sthanabala sub-divisions (Saptavargaja etc.), the
Kala/Digbala hour-and-minute measures, Drukbala as a numeric sum, and
Saisargikabala's calibrated units. Anyone who needs Shadbala should use a
dedicated library, or port *Graha and Bhava Balas*.

## The judgement rules of chapter III

These are the rules the book gives for actually using strength, and they are
more valuable than the Shadbala list:

> "The lords of trines are always auspicious and produce good. When benefics
> own quadrants, they produce evil. When malefics own quadrants they produce
> good."

> "The good and evil planets become more and more powerful as they are lords of
> the 1st, the 4th, the 7th or the 10th houses."

> "Lords of 3, 6, 8 and 11 do evil and cause miseries."

> "The lords of the 2nd and the 12th houses give good results if they are in
> conjunction with favourable planets."

> "The lord of the 8th, if he chances to be the lord of the 1st or is in
> conjunction with a benefic, becomes good."

> "Rahu and Ketu produce good results when they are posited in the sign of the
> benefic planets."

> "Jupiter and Venus owning quadrants become very inauspicious. Mercury as the
> lord of a quadrant is less malefic than Jupiter and Venus, and the Moon
> lesser than Mercury. Mars does not become good when he owns only the 10th
> house. He must own the 5th also to become thoroughly good."

> "If the lords of Kendras (quadrants) without being associated with the lords
> of other houses, they become powerful in producing good results."

That last sequence is the classical **Kendradhipati dosha** — the blemish of
owning an angle — and it is why a benefic ruling a quadrant turns malefic. It
also explains the **Yogakaraka**: a planet that owns both a quadrant and a
trine escapes the dosha and becomes the best planet in the chart. The textbook
example is Saturn for Taurus (9th and 10th) and for Libra (4th and 5th); the
engine derives yogakarakas from ownership rather than from a table, so the
answer falls out of the Ascendant.

## The book's caution about judgement itself

> "The judgment of a horoscope forms the most important and difficult task of
> an astrologer. It must be borne in mind that, at the outset no hard and fast
> rules can be laid down for the guidance of the reader. In order to examine a
> horoscope, good power of judgment is required."

> "Unskilful manipulation of co-ordinates employed may lead to erroneous
> conclusions."

Any software that presents a reading as a verdict is working against the
book's own instruction.
