"""Zodiacal constants for the Vedic (Nirayana) system.

Everything here is a plain data table so that it can be inspected, diffed and
overridden without touching the computational code.  The tables marked
``SOURCE`` come from B. V. Raman, *Astrology for Beginners* (see
``docs/source-notes.md``); tables marked ``STANDARD`` are the common
Parashari values, used where the scanned source is illegible.
"""

from __future__ import annotations

# --------------------------------------------------------------------------
# Signs (Rasis)
# --------------------------------------------------------------------------
SIGNS = (
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
)
SIGNS_SA = (
    "Mesha", "Vrishabha", "Mithuna", "Kataka", "Simha", "Kanya",
    "Thula", "Vrischika", "Dhanus", "Makara", "Kumbha", "Meena",
)
SIGN_GLYPHS = ("\u2648", "\u2649", "\u264a", "\u264b", "\u264c", "\u264d",
               "\u264e", "\u264f", "\u2650", "\u2651", "\u2652", "\u2653")

SIGN_LORDS = (
    "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
    "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter",
)

# SOURCE: chapter I, "Peculiarities of the Signs".
# modality / parity / gender / temperament / element / fruitfulness /
# ascension / rising part -- exactly as the source lists them.
SIGN_NATURE = {
    "Aries":       dict(modality="movable", parity="odd",  gender="masculine", temperament="cruel", element="fire",  fruitful=None,     ascension="short", rises="hinder"),
    "Taurus":      dict(modality="fixed",   parity="even", gender="feminine",  temperament="mild",  element="earth", fruitful=True,     ascension="short", rises="hinder"),
    "Gemini":      dict(modality="common",  parity="odd",  gender="masculine", temperament="cruel", element="air",   fruitful=False,    ascension="short", rises="head"),
    "Cancer":      dict(modality="movable", parity="even", gender="feminine",  temperament="mild",  element="water", fruitful=True,     ascension="long",  rises="hinder"),
    "Leo":         dict(modality="fixed",   parity="odd",  gender="masculine", temperament="cruel", element="fire",  fruitful=False,    ascension="long",  rises="head"),
    "Virgo":       dict(modality="common",  parity="even", gender="feminine",  temperament="mild",  element="earth", fruitful=False,    ascension="long",  rises="head"),
    "Libra":       dict(modality="movable", parity="odd",  gender="masculine", temperament="cruel", element="air",   fruitful=None,     ascension="long",  rises="head"),
    "Scorpio":     dict(modality="fixed",   parity="even", gender="feminine",  temperament="mild",  element="water", fruitful=None,     ascension="long",  rises="head"),
    "Sagittarius": dict(modality="common",  parity="odd",  gender="masculine", temperament="cruel", element="fire",  fruitful=None,     ascension="long",  rises="hinder"),
    "Capricorn":   dict(modality="movable", parity="even", gender="feminine",  temperament="mild",  element="earth", fruitful=None,     ascension="long",  rises="hinder"),
    "Aquarius":    dict(modality="fixed",   parity="odd",  gender="masculine", temperament="cruel", element="air",   fruitful=True,     ascension="short", rises="head"),
    "Pisces":      dict(modality="common",  parity="even", gender="feminine",  temperament="mild",  element="water", fruitful=None,     ascension="short", rises="head"),
}

# SOURCE: chapter V -- "the twelve signs ... govern the twelve important
# organs of the human body ... head, face, neck, heart, stomach, waist,
# lower belly, sexual organs, thighs, knees, buttocks, and feet".
SIGN_BODY_PART = {
    "Aries": "head", "Taurus": "face", "Gemini": "neck", "Cancer": "heart",
    "Leo": "stomach", "Virgo": "waist", "Libra": "lower belly",
    "Scorpio": "sexual organs", "Sagittarius": "thighs", "Capricorn": "knees",
    "Aquarius": "buttocks", "Pisces": "feet",
}

ELEMENTS = ("fire", "earth", "air", "water")

# --------------------------------------------------------------------------
# Planets (Grahas)
# --------------------------------------------------------------------------
PLANETS = ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu")
PLANETS_SA = {
    "Sun": "Ravi", "Moon": "Chandra", "Mars": "Kuja", "Mercury": "Budha",
    "Jupiter": "Guru", "Venus": "Sukra", "Saturn": "Sani",
    "Rahu": "Rahu", "Ketu": "Ketu",
}
PLANET_GLYPHS = {
    "Sun": "\u2609", "Moon": "\u263d", "Mars": "\u2642", "Mercury": "\u263f",
    "Jupiter": "\u2643", "Venus": "\u2640", "Saturn": "\u2644",
    "Rahu": "\u260a", "Ketu": "\u260b",
}
SEVEN_GRAHAS = ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn")
NODES = ("Rahu", "Ketu")

# SOURCE: chapter I, "Planetary Nature and Indications" -- condensed.
PLANET_NATURE = {
    "Sun": dict(gender="masculine", benefic=False, colour="copper", karaka="father",
                significations="royal power, ego, self-reliance, patrimony, bones, fires, political power"),
    "Moon": dict(gender="feminine", benefic=True, colour="white", karaka="mother",
                 significations="mind, popularity, water, blood, pearls, romances, human responsibilities"),
    "Mars": dict(gender="masculine", benefic=False, colour="blood-red", karaka="brother",
                 significations="brothers, military activity, commerce, base metals, vegetation, oratory"),
    "Mercury": dict(gender="hermaphrodite", benefic=True, colour="green", karaka="profession",
                    significations="mercantile activity, intelligence, speech, mathematics, writing"),
    "Jupiter": dict(gender="masculine", benefic=True, colour="bright yellow", karaka="children",
                    significations="devotion, progeny, truthfulness, religious fervour, philosophical wisdom"),
    "Venus": dict(gender="feminine", benefic=True, colour="mixture of all colours", karaka="spouse",
                  significations="wife, love affairs, sensual pleasure, family bliss, vitality, arts"),
    "Saturn": dict(gender="hermaphrodite", benefic=False, colour="dark", karaka="longevity",
                   significations="stubbornness, demoralisation, windy diseases, despondency, gambling, delay"),
    "Rahu": dict(gender="feminine", benefic=False, colour="smoky", karaka="maternal relations",
                 significations="renunciation, corruption, epidemics, occultism, foreign things"),
    "Ketu": dict(gender="hermaphrodite", benefic=False, colour="smoky", karaka="paternal relations",
                 significations="religious and sectarian principles, pride, occultism, mendicancy, moksha"),
}

NATURAL_BENEFICS = ("Jupiter", "Venus", "Mercury", "Moon")
NATURAL_MALEFICS = ("Saturn", "Mars", "Sun", "Rahu", "Ketu")

# SOURCE: chapter I, "Exaltation" -- deep exaltation sign and degree.
EXALTATION = {
    "Sun": ("Aries", 10.0), "Moon": ("Taurus", 3.0), "Mars": ("Capricorn", 28.0),
    "Mercury": ("Virgo", 15.0), "Jupiter": ("Cancer", 5.0), "Venus": ("Pisces", 27.0),
    "Saturn": ("Libra", 20.0), "Rahu": ("Taurus", 20.0), "Ketu": ("Scorpio", 20.0),
}
# Debilitation is derived: the sign 180 degrees away from exaltation.
DEBILITATION = {p: (SIGNS[(SIGNS.index(s) + 6) % 12], d) for p, (s, d) in EXALTATION.items()}

# SOURCE: chapter I, "Moolathrikonas".  The source gives the Moon's range as
# Taurus 4-20; most modern references give Taurus 4-30 (see docs/03-planets.md).
MOOLATRIKONA = {
    "Sun": ("Leo", 0.0, 20.0), "Moon": ("Taurus", 4.0, 20.0), "Mars": ("Aries", 0.0, 12.0),
    "Mercury": ("Virgo", 16.0, 20.0), "Jupiter": ("Sagittarius", 0.0, 10.0),
    "Venus": ("Libra", 0.0, 15.0), "Saturn": ("Aquarius", 0.0, 20.0),
}

# STANDARD: natural (permanent) friendship, in the sense the source describes
# on pp. 7-8.  The scanned table is partly illegible; these are the standard
# Parashari values.
NATURAL_FRIENDS = {
    "Sun":     {"friends": ("Moon", "Mars", "Jupiter"), "neutral": ("Mercury",), "enemies": ("Venus", "Saturn")},
    "Moon":    {"friends": ("Sun", "Mercury"), "neutral": ("Mars", "Jupiter", "Venus", "Saturn"), "enemies": ()},
    "Mars":    {"friends": ("Sun", "Moon", "Jupiter"), "neutral": ("Venus", "Saturn"), "enemies": ("Mercury",)},
    "Mercury": {"friends": ("Sun", "Venus"), "neutral": ("Mars", "Jupiter", "Saturn"), "enemies": ("Moon",)},
    "Jupiter": {"friends": ("Sun", "Moon", "Mars"), "neutral": ("Saturn",), "enemies": ("Mercury", "Venus")},
    "Venus":   {"friends": ("Mercury", "Saturn"), "neutral": ("Mars", "Jupiter"), "enemies": ("Sun", "Moon")},
    "Saturn":  {"friends": ("Mercury", "Venus"), "neutral": ("Jupiter",), "enemies": ("Sun", "Moon", "Mars")},
    "Rahu":    {"friends": ("Venus", "Saturn", "Mercury"), "neutral": (), "enemies": ("Sun", "Moon", "Mars")},
    "Ketu":    {"friends": ("Mars", "Venus", "Saturn"), "neutral": (), "enemies": ("Sun", "Moon")},
}

# SOURCE: chapter I -- "Planets very near the Sun become combust".
# STANDARD: the orbs used below are the conventional ones.
COMBUSTION_ORB = {
    "Moon": 12.0, "Mars": 17.0, "Mercury": 14.0, "Jupiter": 11.0,
    "Venus": 10.0, "Saturn": 15.0,
}
COMBUSTION_ORB_RETRO = {"Mercury": 12.0, "Venus": 8.0}

# SOURCE: chapter III, "Digbala".
DIGBALA_HOUSE = {"Jupiter": 1, "Mercury": 1, "Sun": 10, "Mars": 10, "Saturn": 7, "Venus": 4, "Moon": 4}

# SOURCE: chapter I, "Karakas".
KARAKAS = {
    "father": "Sun", "mother": "Moon", "brother": "Mars", "profession": "Mercury",
    "children": "Jupiter", "spouse": "Venus", "longevity": "Saturn",
    "maternal_relations": "Rahu", "paternal_relations": "Ketu",
}

# --------------------------------------------------------------------------
# Nakshatras (constellations) -- SOURCE: chapter I & X
# --------------------------------------------------------------------------
NAKSHATRAS = (
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
)
NAKSHATRA_SPAN = 360.0 / 27.0          # 13 deg 20 min
NAKSHATRA_PADA_SPAN = NAKSHATRA_SPAN / 4  # 3 deg 20 min

# Vimshottari lordship, in the same cyclic order as the nakshatras.
VIMSHOTTARI_ORDER = ("Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury")
VIMSHOTTARI_YEARS = {
    "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
    "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17,
}
VIMSHOTTARI_TOTAL = 120
NAKSHATRA_LORDS = tuple(VIMSHOTTARI_ORDER[i % 9] for i in range(27))

# --------------------------------------------------------------------------
# Houses (Bhavas)
# --------------------------------------------------------------------------
HOUSE_SIGNIFICATIONS = {
    1: "body, appearance, birth, self, vitality",
    2: "family, source of wealth, property, vision, speech",
    3: "intelligence, brothers, sisters, courage, communication",
    4: "vehicles, general happiness, education, mother, landed property",
    5: "fame, children, authority, past merit",
    6: "debts, diseases, misery, enemies, service",
    7: "wife or husband, partnership, tact, death",
    8: "longevity, gifts, sudden events, inheritance",
    9: "God, guru, father, travel, piety, fortune",
    10: "occupation, karma, status, philosophical knowledge",
    11: "gains, elder siblings, fulfilment of desires",
    12: "losses, expenditure, moksha, foreign lands",
}

KENDRAS = (1, 4, 7, 10)      # angles / quadrants
TRIKONAS = (1, 5, 9)         # trines
PANAPARAS = (2, 8, 11)       # succeedent
APOKLIMAS = (3, 6, 12)       # cadent
DUSTHANAS = (6, 8, 12)

HOUSE_KIND = {}
for _h in range(1, 13):
    if _h in KENDRAS:
        HOUSE_KIND[_h] = "kendra"
    elif _h in PANAPARAS:
        HOUSE_KIND[_h] = "panapara"
    else:
        HOUSE_KIND[_h] = "apoklima"

# SOURCE: chapter I, "Drishti or Aspect" -- special (full) aspects.
SPECIAL_ASPECTS = {
    "Mars": (4, 7, 8),
    "Jupiter": (5, 7, 9),
    "Saturn": (3, 7, 10),
}
DEFAULT_ASPECTS = (7,)

# SOURCE: chapter I -- partial sight (drishti pinda) by house distance.
PARTIAL_SIGHT = {3: 0.25, 10: 0.25, 5: 0.5, 9: 0.5, 4: 0.75, 8: 0.75, 7: 1.0}


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def sign_of(longitude: float) -> str:
    """Sign name for a sidereal longitude in degrees."""
    return SIGNS[int(longitude % 360.0 // 30.0)]


def sign_index(longitude: float) -> int:
    return int(longitude % 360.0 // 30.0)


def degree_in_sign(longitude: float) -> float:
    return longitude % 30.0


def nakshatra_index(longitude: float) -> int:
    return int(longitude % 360.0 // NAKSHATRA_SPAN)


def nakshatra_name(longitude: float) -> str:
    return NAKSHATRAS[nakshatra_index(longitude)]


def nakshatra_pada(longitude: float) -> int:
    return int((longitude % NAKSHATRA_SPAN) // NAKSHATRA_PADA_SPAN) + 1


def nakshatra_lord(longitude: float) -> str:
    return NAKSHATRA_LORDS[nakshatra_index(longitude)]


def navamsa_sign_index(longitude: float) -> int:
    """Navamsa sign, by the continuous 3 deg 20 min division of the zodiac.

    Verified against the worked example in the source (chapter II): a planet
    at Libra 20 deg 10 min falls in the 7th navamsa of Libra, whose lord is
    Mars -- i.e. the navamsa sign is Aries.
    """
    return int((longitude % 360.0) // NAKSHATRA_PADA_SPAN) % 12


def navamsa_sign(longitude: float) -> str:
    return SIGNS[navamsa_sign_index(longitude)]


def dms(value: float, seconds: bool = True) -> str:
    """Format a decimal degree value as deg/min/sec (or deg/min)."""
    sign = "-" if value < 0 else ""
    value = abs(value)
    d = int(value)
    m_full = (value - d) * 60
    m = int(m_full)
    s = (m_full - m) * 60
    if seconds:
        return f"{sign}{d}\u00b0{m:02d}'{s:04.1f}\""
    return f"{sign}{d}\u00b0{m:02d}'"


def house_from(sign_a: str, sign_b: str) -> int:
    """Whole-sign house number of ``sign_b`` counted from ``sign_a``."""
    return (SIGNS.index(sign_b) - SIGNS.index(sign_a)) % 12 + 1
