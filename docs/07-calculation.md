# 7. Casting a horoscope — the full method

**SOURCE:** chapter II, "Casting the Horoscope"; Appendix I, "Ayanamsa
Determination"; Appendix II, the Nirayana Tables of Houses.

This is the chapter that makes the book usable, and it is reproduced here in
full because it is the specification the engine implements.

## The two zodiacs

> "There is a difference of about 22 degrees between the Western and the Hindu
> zodiacs. That is, according to the Hindu horoscope if a planet is in 20
> degrees Cancer, it will be situated in the 12th or 13th degree of Leo
> according to Western Astrology."

The difference is the **Ayanamsa** or **precessional distance**. The method is
therefore always the same shape:

> "Erect a horoscope as per rules given below and subtract from the positions
> so obtained, the Ayanamsa for the year of birth and the Hindu horoscope
> needed for our purpose, is obtained."

- **Sayana** = the moving zodiac, measured from the shifting vernal equinox
  (Western tropical).
- **Nirayana** = the fixed zodiac, measured from a fixed stellar point (Hindu
  sidereal).

The book holds that "the greatest Hindu astrological writers referred to the
fixed zodiac for predictions, and this fact is borne by experience"
(Appendix I).

## Step 1 — convert local mean time to Greenwich mean time

> "For births west of Greenwich, add four minutes for every degree of
> longitude to the Local Mean Time of birth. For births east of Greenwich,
> subtract four minutes for every degree of longitude from the Local Mean Time
> of birth. The result is the Greenwich Mean Time of Birth."

(Four minutes per degree is 15° = 1 hour, i.e. one minute of time per 15′ of
arc.)

**The book's example, used throughout the rest of this document:** born
2 November 1935, Saturday, 5h 20m 00s a.m. L.M.T., at longitude 5h 10m 20s
East and latitude 13° North.

```
Local Mean Time of birth   5h 20m 00s
Longitude of place (east)  5h 10m 20s   (subtract)
Greenwich Mean Time        0h 09m 40s  = about 0h 10m a.m. GMT
```

## Step 2 — planetary longitudes at birth

Given a modern ephemeris tabulating longitudes at Greenwich Mean Noon:

> "If birth is a.m. or before noon, the difference of longitude between the
> previous noon and the noon of the birth date for the particular planet must
> be noted. If birth is p.m. or afternoon, the difference between the noon of
> the birth date and the next noon must be noted. This difference is the
> motion of the planet in 24 hours. From this, the proportional distance
> covered in the G.M.T. of birth can be easily obtained."

The book's arithmetic for the Sun:

```
Sun's longitude at noon 1-11-1935     Scorpio 8° 08'
Sun's motion in 12h 10m                0° 31'
Sun's longitude at birth              Scorpio 8° 39'      <- Sayana
```

Retrogression is simply noted in the ephemeris and carried through.

The resulting Sayana positions for the example:

| Graha | Sayana (Western) | minus ayanamsa | Nirayana (Hindu) |
|---|---|---|---|
| Sun | Scorpio 8° 39′ | 21° 30′ | **Libra 17° 09′** |
| Moon | Capricorn 14° 05′ | | **Sagittarius 22° 35′** |
| Mars | Sagittarius 3° 10′ | | **Sagittarius 11° 40′** |
| Mercury | Virgo 20° 05′ | | **Virgo 28° 35′** |
| Jupiter | Scorpio 28° 23′ | | **Scorpio 6° 53′** |
| Venus | Virgo 23° 15′ | | **Virgo 1° 45′** |
| Saturn | Aquarius 3° 32′ | | **Aquarius 12° 02′** |
| Rahu | Sagittarius 16° 04′ | | **Sagittarius 24° 34′** |
| Ketu | Gemini 16° 04′ | | **Gemini 24° 34′** |

(The Sayana column is reconstructed by adding the book's 21°30′ ayanamsa back
to the Nirayana figures it prints; only the Nirayana column is printed in the
book.)

**Verification:** the engine reproduces this table to within a couple of
arcminutes from first principles — see `tests/test_engine.py::test_book_example_positions`.
The residual comes from the book rounding its ayanamsa to 21° 30′ exactly.

## Step 3 — sidereal time and the Ascendant

> "Find out the Sidereal Time at G.M.N. ... This is given for 12 noon
> Greenwich Time. Add to this the Local [time elapsed] after the local noon,
> and also add 10 seconds per hour since noon, as this represents the
> difference between the Sidereal Time and the Mean Time. If the place of
> birth is east of Greenwich deduct at the rate of 10 seconds per hour for
> every 15 degrees of longitude (or 1 hour in time) and if the place of birth
> is west of Greenwich add a similar quantity."

```
Sidereal Time for noon preceding the birth (1-11-1935)   14h 39m 23s
Hours passed since previous noon up to birth             17h 20m 00s
Correction between sidereal and mean time                 0h 02m 53s
                                                         -----------
                                                         32h 02m 16s
Less correction for longitude east of Greenwich           0h 00m 52s
                                                         -----------
                                                         32h 01m 24s
Expunging multiples of 24: true local sidereal time      8h 01m 24s
```

This sidereal time, "converted into degrees", is the **R.A.M.C.** (right
ascension of the meridian). Entering the **Tables of Houses** for the nearest
latitude (Madras, 13° N) at that sidereal time gives the cusps:

```
10th  Cancer 28°          1st (Ascendant)  Libra 29° 39'
11th  Leo 29°             2nd              Scorpio 29°
12th  Virgo 30°           3rd              Sagittarius 28°
```

The remaining six cusps are found by adding 180°.

## Step 4 — deduct the ayanamsa to get bhavamadhyas

> "Cusp of the Western House less Ayanamsa will give the Bhavamadhya
> (mid-point) of the house of the Hindus."

```
Cusp of the 1st house (Ascendant)   29° 39′ Libra
Less ayanamsa for 1935              21° 30′
Mid-point of Lagna                   8° 01′ Libra
```

**Note the two different things in play.** The Ascendant *degree* of the Hindu
chart is 8° 01′ Libra (sidereal), but the **Rasi chart** — the one used "for
ordinary purposes of prediction" — simply puts Libra as the 1st house, with
the Sun in it. The engine reports both: `lagna.longitude` (sidereal degree)
and `lagna.sign` (the sign that becomes the 1st bhava).

## The ayanamsa itself

**SOURCE:** Appendix I. Two methods are given.

### Method 1 — the book's arithmetic rule

```
1) Subtract 397 from the year of birth (A.D.)
2) Multiply the remainder by 50 1/3 seconds
3) Reduce the product into degrees, minutes and seconds
```

Worked example for 1935:

```
1935 - 397 = 1538
1538 x 50 1/3" = 77412"
77412" = 21° 30' 12"
```

The book adds that "when exactly the two zodiacs were in the first point is
doubted by a number of astronomers and accordingly the Ayanamsa —
precessional distance — varies from 19° to 23°", and that it "increases about
50 1/3 seconds of arc every year".

**CAUTION — this rule is a rule of thumb, and it is about 1°27′ low.** It
assumes the two zodiacs coincided in 397 CE and that precession is exactly
constant. Compare, for 2 November 1935:

| Model | Ayanamsa |
|---|---|
| Book's rule, (1935−397) × 50⅓″ | 21° 30′ |
| Lahiri (Chitrapaksha), the modern standard | 22° 57′ |
| Difference | 1° 27′ |

That difference is larger than the Moon's daily motion in two hours, so it
moves every cusp and every planet. The book's own worked example is internally
consistent because it uses its own rule throughout — which is why the engine
keeps `raman_397` as a selectable model: without it you cannot reproduce the
book's chart.

### Method 2 — the modern one, used by default

The **Lahiri (Chitrapaksha)** ayanamsa is the value tabulated in the *Indian
Astronomical Ephemeris* and used by essentially all Indian astrology software.
Its definition is the tropical longitude of Spica (Chitra) minus 180°: the
star Chitra is held to be at 0° Libra of the sidereal zodiac.

The engine computes it as

```
ayanamsa(t) = 23° 51' 11.5"  +  p_A(t)
```

where 23° 51′ 11.5″ is the published Lahiri value at J2000.0 and `p_A(t)` is
the **IAU 2006 accumulated general precession in ecliptic longitude** since
J2000:

```
p_A = 5028.796195 T + 1.1054348 T² + 0.00007964 T³ − 0.000023857 T⁴ − 0.0000000383 T⁵   [arcsec]
```

with T in Julian centuries of TT from J2000.0. Agreement with the Indian
Astronomical Ephemeris is within a few arcseconds across 1900–2100.

**CAUTION:** if you need arcsecond-for-arcsecond agreement with commercial
software, use the Swiss Ephemeris, which implements Lahiri natively along with
about forty other ayanamsas. `ephemeris.py` is deliberately a thin layer: it
returns `{planet: (longitude, latitude, speed)}` and nothing else, so a
`pyswisseph` backend is a drop-in replacement.

## Step 5 — the Navamsa

**SOURCE:** chapter II.

> "When a sign is divided into 9 equal parts each part measuring 3° 20′ is
> called a Navamsa. The nine Navamsas are governed by the lords of the nine
> signs from Aries, in the case of Aries, Leo and Sagittarius; from Capricorn
> in the case of Taurus, Virgo and Capricorn; from Libra in the case of Gemini,
> Libra and Aquarius; and in the case of Cancer, Scorpio and Pisces from
> Cancer."

That is the classical rule: for **movable** signs the navamsa series starts
from the sign itself; for **fixed** signs from the 9th from it; for **common**
signs from the 5th from it. All three reduce to one continuous formula, which
is what the engine uses:

```
navamsa_sign = floor(sidereal_longitude / 3°20′) mod 12
```

**Check against the book's own example:** "a planet is in Libra 20° 10′. This
means the seventh Navamsa. In Libra the lord of the seventh Navamsa is the
lord of the seventh from Libra, that is lord of Aries, viz., Mars."

```
longitude = 180° + 20°10′ = 200.1667°
200.1667 / 3.3333 = 60.05  ->  floor = 60
60 mod 12 = 0  ->  Aries, whose lord is Mars   ✓
```

And the book's verdict on its importance:

> "In Hindu Astrology constant reference is made to Navamsa positions of
> planets. In a way Navamsa is much more important than the usual Rasi or
> zodiacal diagram."

The engine computes the navamsa sign of every planet, of the Ascendant, and
draws the D9 diagram alongside the Rasi.

## Step 6 — what the finished chart looks like

The book's own Rasi diagram, read out in its own words:

> "Lagna is Libra. Sun is in the 1st house; Jupiter in the 2nd; Moon, Mars and
> Rahu in the 3rd; Saturn in the 5th; Ketu in the 9th; and Mercury and Venus
> in the 12th. Sun and Venus are debilitated; Mercury is exalted; Saturn is in
> his own house; Mars and Jupiter have exchanged places."

Every one of those statements is asserted in `tests/test_engine.py`
(`test_book_chart_structure`, `test_book_chart_dignities`,
`test_mars_jupiter_exchange`). The engine reproduces the whole chart.

## The short route

**SOURCE:** Appendix II. Raman's *Nirayana Tables of Houses* (with R. V.
Vaidya) tabulate the sidereal bhavamadhyas directly, so that no ayanamsa
subtraction is needed:

```
Sidereal Time = Y + D − I − K − C
```

where Y is the tabulated value for the year, D for the day, I the interval
between mean noon and birth, K the 10-seconds-per-hour correction, and C the
longitudinal correction between Ujjain (77° 3′) and the place of birth. The
book works its example through this route as well and reaches
8h 01m 25s — one second from the long route.
