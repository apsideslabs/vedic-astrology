"""Gochara -- transits read from the Janma Rasi (the radical Moon).

SOURCE: chapter XII.  The results below are transcribed from that chapter.
The scan is damaged at a few page breaks, so some cells are ``None``: those
items are simply not legible in the source and are marked as gaps rather than
filled in from other books.  ``docs/12-transits.md`` lists the gaps.
"""

from __future__ import annotations

from datetime import datetime, timezone

from . import ayanamsa as ayanamsa_mod
from . import ephemeris, zodiac

# house from Janma Rasi -> result
GOCHARA = {
    "Sun": {
        1: "change of place",
        2: "loss of wealth",
        3: "advent of money and success",
        4: "dishonour",
        5: "sorrow, ill-health and embarrassment",
        6: "ruin to foes",
        7: "travelling and ill-health",
        8: "quarrels and unpleasantness",
        9: None,
        10: None,
        11: "earnings",
        12: "quarrels and pecuniary loss",
    },
    "Moon": {
        1: "good disposition and food",
        2: "expenditure",
        3: "gain of money",
        4: "accidents or ill-health",
        5: "unpleasantness",
        6: "auspicious results",
        7: "friendship and gains",
        8: "trouble and expenses",
        9: "intimidation and worry",
        10: "gains and well-being",
        11: "happiness and pecuniary gain",
        12: "misery and loss",
    },
    "Mars": {
        1: "sorrow and accidents",
        2: "loss and expenses",
        3: "pecuniary gain and pleasure",
        4: "trouble from foes",
        5: "loss of money and illness to children",
        6: "gain of money",
        7: "quarrelling, fatigue, accident to wife",
        8: "fear and danger",
        9: "indisposition and expenses",
        10: "change and sorrow",
        11: "acquisition of money and peace of mind",
        12: "disease and falls from elevations",
    },
    "Mercury": {
        1: "trouble and servitude",
        2: "gain of money",
        3: "ill-luck",
        4: "good fortune",
        5: "poverty and loss",
        6: "success",
        7: "illness and vice",
        8: "pleasure and auspicious events",
        9: None,
        10: None,
        11: "happiness",
        12: "misunderstandings",
    },
    "Jupiter": {
        1: "travelling and fear, rewards",
        2: "profits and gain of money",
        3: "obstacles, ill-health",
        4: "loss of money and expenses",
        5: "happiness, birth of children and pleasure",
        6: "grief and misery",
        7: "good health and fortune",
        8: "danger and dissatisfaction",
        9: "access to wealth and risk of losing position and reputation",
        10: "separation, loss of health and wealth",
        11: "profit and success in undertakings",
        12: "affliction, unexpected troubles and mental worry",
    },
    "Venus": {
        1: "good health and pleasure",
        2: "gain of money and good luck in general",
        3: "happiness and pleasant associations",
        4: "pecuniary gain",
        5: "happiness and birth of a son",
        6: "fear of foes and unexpected expenses",
        7: "worry, grief and quarrels with wife",
        8: "good income",
        9: "gain of money, apparel and friends",
        10: "indisposition and scandal",
        11: "pleasure and profit",
        12: "good finance and peace of mind",
    },
    "Saturn": {
        1: "danger and loss of money",
        2: "sorrow and accidents",
        3: "gain and prosperity",
        4: "expenses, sickness",
        5: None,
        6: None,
        7: "mental and physical affliction and great suffering",
        8: "fear, bad reputation and worry",
        9: "loss of money, ill-health and misfortune",
        10: "loss of wealth",
        11: "cruelty and access to money",
        12: "danger, worry and financial strain",
    },
    "Rahu": {
        1: "sickness and fear",
        2: "loss of wealth, quarrelling and misunderstandings",
        3: "happiness and good finances",
        4: "sickness, danger and sorrow",
        5: "financial loss and worry",
        6: "pleasure and happiness",
        7: "loss and fear",
        8: "danger to life",
        9: "quarrelling, mental worry and loss",
        10: "enmity",
        11: "happiness and acquisition of money",
        12: "expenses and danger",
    },
}
GOCHARA["Ketu"] = dict(GOCHARA["Rahu"])

SADE_SATI_HOUSES = (12, 1, 2)


def current_positions(jd: float, ayanamsa: str = "lahiri") -> dict[str, dict]:
    """Sidereal longitudes at a moment, in the chart's ayanamsa."""
    ay = ayanamsa_mod.value(ayanamsa, jd)
    trop = ephemeris.tropical_longitudes(jd)
    out = {}
    for planet, data in trop.items():
        sid = (data["longitude"] - ay) % 360.0
        out[planet] = {
            "longitude": round(sid, 4),
            "dms": zodiac.dms(sid),
            "sign": zodiac.sign_of(sid),
            "degree_in_sign": round(zodiac.degree_in_sign(sid), 4),
            "nakshatra": zodiac.nakshatra_name(sid),
            "retrograde": data["speed"] < 0,
        }
    return out


def gochara(janma_rasi: str, positions: dict[str, dict]) -> list[dict]:
    """Read the transit of each graha from the Janma Rasi."""
    out = []
    for planet in zodiac.PLANETS:
        pos = positions[planet]
        house = zodiac.house_from(janma_rasi, pos["sign"])
        result = GOCHARA.get(planet, {}).get(house)
        out.append({
            "planet": planet,
            "sign": pos["sign"],
            "house_from_moon": house,
            "result": result,
            "gap_in_source": result is None,
            "sade_sati": planet == "Saturn" and house in SADE_SATI_HOUSES,
        })
    return out


def analyse(chart, at: datetime | None = None) -> dict:
    """Transit analysis for a chart at a given moment."""
    if at is None:
        at = datetime.now(timezone.utc).replace(tzinfo=None)
    if at.tzinfo is not None:
        at = at.astimezone(timezone.utc).replace(tzinfo=None)

    jd = ephemeris.julian_day(at)
    positions = current_positions(jd, chart.ayanamsa_model)
    janma = chart.moon_sign()
    rows = gochara(janma, positions)
    saturn = next(r for r in rows if r["planet"] == "Saturn")
    return {
        "as_of": at.isoformat(timespec="seconds"),
        "janma_rasi": janma,
        "positions": positions,
        "gochara": rows,
        "sade_sati": {
            "active": saturn["sade_sati"],
            "saturn_house_from_moon": saturn["house_from_moon"],
            "note": "Saturn in the 12th, 1st or 2nd from the radical Moon is "
                    "Sade Sati, the '7 1/2 years' Saturn of the source.",
        },
        "weighting": "The source insists transits must never be read without the "
                     "prevailing dasha and bhukti (ch. XII).",
    }
