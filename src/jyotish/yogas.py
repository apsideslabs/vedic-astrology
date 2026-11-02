"""Yoga detection.

SOURCE: chapter III, "Yogas" and "Important Yogas".  Every yoga below is one
the source names and defines; the only additions are flagged as such in the
``source`` field, because the source's opening list of yogas is partly cut
away by the page break in the scan.

Detection is sign-based (whole-sign), which is how the source works.
"""

from __future__ import annotations

from . import zodiac


def _relative(sign_a: str, sign_b: str) -> int:
    return zodiac.house_from(sign_a, sign_b)


def _yoga(name: str, present: bool, planets: list[str], description: str, source: str) -> dict:
    return {
        "name": name,
        "present": present,
        "planets": planets,
        "description": description,
        "source": source,
    }


def detect(chart) -> list[dict]:
    """Return every yoga the engine knows about, with present=True/False."""
    signs = chart.sign_map()
    lagna = chart.lagna_sign
    moon = signs["Moon"]
    sun = signs["Sun"]
    out: list[dict] = []

    benefics = [p for p in zodiac.NATURAL_BENEFICS if p in signs and p != "Moon"]
    malefics = [p for p in zodiac.NATURAL_MALEFICS if p in signs and p not in ("Rahu", "Ketu")]
    malefics = ["Sun", "Mars", "Saturn"]

    # -- Papakarthari / Subhakarthari: lagna hemmed in by malefics / benefics
    second = zodiac.SIGNS[(zodiac.SIGNS.index(lagna) + 1) % 12]
    twelfth = zodiac.SIGNS[(zodiac.SIGNS.index(lagna) - 1) % 12]
    occ2 = [p for p in zodiac.PLANETS if signs.get(p) == second]
    occ12 = [p for p in zodiac.PLANETS if signs.get(p) == twelfth]
    mal2 = [p for p in occ2 if p in malefics]
    mal12 = [p for p in occ12 if p in malefics]
    ben2 = [p for p in occ2 if p in zodiac.NATURAL_BENEFICS]
    ben12 = [p for p in occ12 if p in zodiac.NATURAL_BENEFICS]

    out.append(_yoga(
        "Papakarthari", bool(mal2 and mal12), mal2 + mal12,
        "The Ascendant is hemmed in between two malefics. The source says this "
        "subjects the native to a chequered career.",
        "ch. III",
    ))
    out.append(_yoga(
        "Subhakarthari", bool(ben2 and ben12), ben2 + ben12,
        "Benefics on either side of the Ascendant, which augments the good.",
        "ch. III",
    ))

    # -- Moon yogas: Sunapha, Anapha, Durdhura, Kemadruma
    moon_second = zodiac.SIGNS[(zodiac.SIGNS.index(moon) + 1) % 12]
    moon_twelfth = zodiac.SIGNS[(zodiac.SIGNS.index(moon) - 1) % 12]
    in_second = [p for p in zodiac.PLANETS if signs.get(p) == moon_second and p != "Sun"]
    in_twelfth = [p for p in zodiac.PLANETS if signs.get(p) == moon_twelfth and p != "Sun"]

    out.append(_yoga(
        "Sunapha", len(in_second) >= 2, in_second,
        "Two or more planets (except the Sun) in the 2nd from the Moon: "
        "intelligent and reputed, occupies a high position, earns well by his own exertions.",
        "ch. III",
    ))
    out.append(_yoga(
        "Anapha", len(in_twelfth) >= 2, in_twelfth,
        "Two or more planets (except the Sun) in the 12th from the Moon: enjoys "
        "worldly pleasure of every kind and possesses an unruffled temper.",
        "ch. III",
    ))
    out.append(_yoga(
        "Durdhura", bool(in_second and in_twelfth), in_second + in_twelfth,
        "Planets on either side of the Moon: self-sacrifice, good servants, wealth and conveyances.",
        "ch. III",
    ))

    # Kemadruma is cancelled by any planet in a quadrant from the Moon.
    kendra_from_moon = [
        p for p in zodiac.PLANETS
        if p != "Moon" and _relative(moon, signs.get(p, moon)) in zodiac.KENDRAS
    ]
    kemadruma = (not in_second) and (not in_twelfth)
    out.append(_yoga(
        "Kemadruma", kemadruma and not kendra_from_moon, [],
        "No planets on either side of the Moon: dirty habits, subservient and "
        "sorrowful. Cancelled if a planet occupies a quadrant from the Moon.",
        "ch. III",
    ))
    if kemadruma and kendra_from_moon:
        out.append(_yoga(
            "Kemadruma-bhanga", True, kendra_from_moon,
            "Kemadruma is formed but cancelled by planets in a quadrant from the Moon.",
            "ch. III",
        ))

    # -- Adhiyoga: benefics in the 6th, 7th and 8th from the Moon
    houses = [zodiac.SIGNS[(zodiac.SIGNS.index(moon) + d - 1) % 12] for d in (6, 7, 8)]
    adhi = []
    for h_sign in houses:
        adhi += [p for p in zodiac.NATURAL_BENEFICS if signs.get(p) == h_sign]
    out.append(_yoga(
        "Adhiyoga", len({signs[p] for p in adhi}) == 3, sorted(set(adhi)),
        "Benefics in the 6th, 7th and 8th from the Moon: happy, fearless, high "
        "position, influential and long-lived.",
        "ch. III",
    ))

    # -- Gurumangala: Jupiter and Mars together (the source names it in ch. VI)
    out.append(_yoga(
        "Gurumangala", signs.get("Jupiter") == signs.get("Mars"), ["Jupiter", "Mars"],
        "Jupiter and Mars together; the source cites it as a wealth-producing "
        "combination when it falls in the 2nd from the Moon.",
        "ch. VI",
    ))

    # -- Rajayoga: a trine lord joined to a quadrant lord, connected to lagna lord
    lagna_lord = chart.lord_of_sign(lagna)
    raja_pairs = []
    for t in zodiac.TRIKONAS:
        t_sign = zodiac.SIGNS[(zodiac.SIGNS.index(lagna) + t - 1) % 12]
        t_lord = chart.lord_of_sign(t_sign)
        for k in zodiac.KENDRAS:
            k_sign = zodiac.SIGNS[(zodiac.SIGNS.index(lagna) + k - 1) % 12]
            k_lord = chart.lord_of_sign(k_sign)
            if t_lord == k_lord:
                continue
            if signs.get(t_lord) == signs.get(k_lord):
                if lagna_lord in (t_lord, k_lord) or signs.get(lagna_lord) == signs.get(t_lord):
                    raja_pairs.append((t_lord, k_lord))
    out.append(_yoga(
        "Rajayoga", bool(raja_pairs),
        [p for pair in raja_pairs for p in pair],
        "A lord of a trine combines with a lord of a quadrant, with a connection "
        "to the lord of the 1st: high power and authority.",
        "ch. III",
    ))

    # -- Yogakaraka (a single planet owning both a quadrant and a trine)
    yogakarakas = []
    for planet in zodiac.SEVEN_GRAHAS:
        owned = [s for s in zodiac.SIGNS if zodiac.SIGN_LORDS[zodiac.SIGNS.index(s)] == planet]
        owned_houses = {zodiac.house_from(lagna, s) for s in owned}
        if owned_houses & set(zodiac.KENDRAS) and owned_houses & set(zodiac.TRIKONAS):
            yogakarakas.append(planet)
    out.append(_yoga(
        "Yogakaraka", bool(yogakarakas), yogakarakas,
        "A planet owning both a quadrant and a trine from the Ascendant. The "
        "source calls such a planet a Rajayoga karaka.",
        "ch. III",
    ))

    return out
