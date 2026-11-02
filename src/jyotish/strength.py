"""Planetary strength and dignity.

The source (chapter III) names the six sources of strength -- Sthanabala,
Digbala, Chestabala, Kalabala, Drukbala and Saisargikabala -- and then says
that measuring them properly belongs in a dedicated work (*Graha and Bhava
Balas*).  This module therefore implements a *simplified positional strength*:
dignity, house placement, directional strength, retrogression, combustion and
navamsa agreement.

It is a transparent, additive score, not Shadbala.  Every component is
reported separately so that a reading can be audited, and the total is scaled
to 0-100 purely for convenience of display.  Do not present it as Shadbala.
"""

from __future__ import annotations

from . import zodiac

# Dignity ladder and the points each rung contributes.
DIGNITY_POINTS = {
    "exalted": 2.0,
    "moolatrikona": 1.75,
    "own": 1.5,
    "intimate friend": 1.0,
    "friend": 0.5,
    "neutral": 0.0,
    "enemy": -0.5,
    "bitter enemy": -1.0,
    "debilitated": -2.0,
}
DIGNITY_ORDER = tuple(DIGNITY_POINTS)

HOUSE_POINTS = {"kendra": 0.75, "panapara": 0.0, "apoklima": -0.5}
TRINE_BONUS = 0.5          # "In trines, they become very strong."


def natural_relation(planet: str, other: str) -> str:
    """Permanent friendship of ``planet`` towards ``other``."""
    if planet == other:
        return "own"
    table = zodiac.NATURAL_FRIENDS.get(planet)
    if not table:
        return "neutral"
    if other in table["friends"]:
        return "friend"
    if other in table["enemies"]:
        return "enemy"
    return "neutral"


def temporary_relation(planet_sign: str, other_sign: str) -> str:
    """Temporary friendship: 2nd, 3rd, 4th, 10th, 11th, 12th are friends.

    SOURCE: chapter I, "Temporary Friendship".
    """
    if planet_sign == other_sign:
        return "own"
    distance = zodiac.house_from(planet_sign, other_sign)
    return "friend" if distance in (2, 3, 4, 10, 11, 12) else "enemy"


def compound_relation(planet: str, other: str, signs: dict[str, str] | None) -> str:
    """Mixed relation -- SOURCE: chapter I, "Mixed Relations".

    A temporary friend plus a natural friend is an intimate friend; a
    temporary enemy plus a natural enemy is a bitter enemy; anything else
    lands on the intervening rungs.
    """
    if planet == other:
        return "own"
    nat = natural_relation(planet, other)
    if signs is None or planet not in signs or other not in signs:
        return nat
    temp = temporary_relation(signs[planet], signs[other])

    if nat == "friend" and temp == "friend":
        return "intimate friend"
    if nat == "friend":
        return "friend" if temp == "enemy" else "friend"
    if nat == "enemy" and temp == "enemy":
        return "bitter enemy"
    if nat == "enemy":
        return "neutral" if temp == "friend" else "enemy"
    # natural neutral
    return "friend" if temp == "friend" else "enemy"


def dignity(planet: str, longitude: float, signs: dict[str, str] | None = None) -> str:
    """Dignity of ``planet`` at a sidereal ``longitude``.

    SOURCE: chapter I, "Relations between Planets and Signs" -- ownership,
    exaltation, debilitation and moolatrikona.
    """
    sign = zodiac.sign_of(longitude)
    deg = zodiac.degree_in_sign(longitude)

    exalt_sign, exalt_deg = zodiac.EXALTATION.get(planet, (None, None))
    if exalt_sign == sign:
        return "exalted"
    deb_sign, _ = zodiac.DEBILITATION.get(planet, (None, None))
    if deb_sign == sign:
        return "debilitated"

    mool = zodiac.MOOLATRIKONA.get(planet)
    if mool and mool[0] == sign and mool[1] <= deg <= mool[2]:
        return "moolatrikona"

    if zodiac.SIGN_LORDS[zodiac.SIGNS.index(sign)] == planet:
        return "own"

    sign_lord = zodiac.SIGN_LORDS[zodiac.SIGNS.index(sign)]
    return compound_relation(planet, sign_lord, signs)


def is_combust(planet: str, longitude: float, sun_longitude: float, retrograde: bool = False) -> bool:
    """Whether a planet is combust (asta).

    SOURCE: chapter I notes the phenomenon; the orbs are the conventional ones.
    """
    if planet in ("Sun", "Rahu", "Ketu"):
        return False
    orb = zodiac.COMBUSTION_ORB.get(planet)
    if orb is None:
        return False
    if retrograde and planet in zodiac.COMBUSTION_ORB_RETRO:
        orb = zodiac.COMBUSTION_ORB_RETRO[planet]
    diff = abs((longitude - sun_longitude + 180.0) % 360.0 - 180.0)
    return diff <= orb


def has_digbala(planet: str, house: int) -> bool:
    """Directional strength -- SOURCE: chapter III, Digbala."""
    return zodiac.DIGBALA_HOUSE.get(planet) == house


def positional_strength(
    planet: str,
    longitude: float,
    house: int,
    *,
    signs: dict[str, str] | None = None,
    retrograde: bool = False,
    combust: bool = False,
    navamsa_sign: str | None = None,
) -> dict:
    """Simplified strength breakdown for one planet."""
    dig = dignity(planet, longitude, signs)
    components = {"dignity": DIGNITY_POINTS[dig]}

    kind = zodiac.HOUSE_KIND.get(house, "apoklima")
    components["house"] = HOUSE_POINTS[kind]
    if house in zodiac.TRIKONAS:
        components["trine"] = TRINE_BONUS
    components["digbala"] = 0.5 if has_digbala(planet, house) else 0.0
    components["chestabala"] = 0.25 if retrograde else 0.0
    components["combustion"] = -0.75 if combust else 0.0

    vargottama = False
    if navamsa_sign is not None:
        vargottama = navamsa_sign == zodiac.sign_of(longitude)
        components["vargottama"] = 0.5 if vargottama else 0.0

    raw = sum(components.values())
    # Map the plausible range (-3.25 .. 4.5) onto 0..100.
    score = max(0.0, min(100.0, (raw + 3.25) / 7.75 * 100.0))
    return {
        "dignity": dig,
        "dignity_points": DIGNITY_POINTS[dig],
        "house_kind": kind,
        "vargottama": vargottama,
        "components": components,
        "raw": round(raw, 2),
        "score": round(score, 1),
    }
