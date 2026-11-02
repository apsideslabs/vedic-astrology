"""Rule-based interpretation.

Every statement this module produces carries a rule id and the chapter of the
source it comes from, so that a reading can be audited instead of taken on
trust.  Nothing here is invented: each rule is a transcription of a rule the
source states, applied to the computed chart.

Where the source gives a conditional ("if the Ascendant lord has anything to
do with the 6th house or its lord, the person will have a sickly
constitution"), the rule below implements exactly that condition.
"""

from __future__ import annotations

from . import zodiac

# --------------------------------------------------------------------------
# Ch. V -- effects of the rising sign (transcribed, lightly condensed)
# --------------------------------------------------------------------------
LAGNA_APPEARANCE = {
    "Aries": "middle stature, weak-kneed, square face, round eyes, ruddy complexion, full nose and forehead; practical and sociable, but with a bad temper, sometimes slow and indolent, and not averse to uttering falsehood",
    "Taurus": "broad thighs, big face, prominent eyes, forgiving disposition, endures hardships; obstinate, behaves like a bull, practical ability, bad temper when aroused",
    "Gemini": "curled hair, black lips, slender and erect figure, long arms and fingers, quick sight, manual dexterity; skilled at reading other people's thoughts, likes music and home-keeping, shy",
    "Cancer": "fleshy neck, short stature, fast in walking, pale complexion, heavy gait; fond of wealth, attached to home life, few sons, with psychic or occult tendencies",
    "Leo": "reddish eyes, large cheeks, broad face, tall; arrogant, angry at trifles, firm-minded, generous, candid and honourable",
    "Virgo": "shoulders and arms drooping, dark hair; truthful and kindly, good mental abilities, methodical and critical, limited number of issues",
    "Libra": "lean and frail body in youth tending to corpulence, round face, fair appearance, regular features; impartial in argument, brave, merciless",
    "Scorpio": "round loins and knees, broad and expansive eyes, broad chest; self-reliance, courage, endurance and executive ability, with envy; suffers disease in early age",
    "Sagittarius": "long face and neck, big ears and nose, short stature, great strength; liberal, cheerful, enterprising, humane, good-hearted, likes physical culture and travelling",
    "Capricorn": "weak in the lower limbs, prominent nose and profile; indolent, vindictive, self-possessed, persistent, lacking humaneness",
    "Aquarius": "tall, sometimes stooping, fair looking, dark hair, big buttocks; intellectual, inclined to occult matters, forgiving temperament",
    "Pisces": "symmetrical and shining body, small and short limbs; learned, fond of wife, reserved, diffident and dependent, indolent",
}

PLANET_ON_LAGNA = {
    "Sun": "The Sun near the Ascendant adds nobleness to the figure and increases the health of the constitution.",
    "Moon": "The Moon near the Ascendant gives better proportion and greater delicacy of figure.",
    "Mars": "Mars near the Ascendant gives a fair ruddiness, a healthy constitution, a sturdy figure and a temperament of heat and dryness.",
    "Mercury": "Mercury near the Ascendant makes the stature proportionate and well shaped, with a hot bodily temperament and yellowish complexion.",
    "Jupiter": "Jupiter near the Ascendant expands the figure and lends dignity to it.",
    "Venus": "Venus near the Ascendant lends softness and greater delicacy, more applicable to female beauty.",
    "Saturn": "Saturn near the Ascendant gives black and curly hair, a tall figure, an inactive and narrow chest.",
    "Rahu": "Rahu near the Ascendant gives an unusual or striking appearance and a temperament drawn to the foreign and the occult.",
    "Ketu": "Ketu near the Ascendant gives a spare figure and a temperament turned inward.",
}

SEVENTH_HOUSE_PARTNER = {
    "Sun": "a proud, firm-minded partner, with delays in marriage",
    "Moon": "a kind and domesticated partner with a wavering mind",
    "Mars": "a quarrelsome, domineering partner, with frequent separation by quarrels and misunderstandings",
    "Mercury": "a quick-minded partner, bad-tempered if Mercury is afflicted",
    "Jupiter": "a good partner and, in general, a happy marriage",
    "Venus": "a happy marriage if Venus is unafflicted; otherwise quarrels, with strong attraction to the opposite sex",
    "Saturn": "a difference of age or station between native and partner, and generally an unhappy married life",
    "Rahu": "tragic conditions in marriage",
    "Ketu": "tragic conditions in marriage",
}

TENTH_SIGN_CAREER = {
    "fire": "work involving factories, fires, the army, iron, metallurgy or printing",
    "water": "work connected with the sea, navigation, inn-keeping, wine or fish",
    "earth": "landed property, agriculture, cloth trade, shopkeeping or gardening",
    "air": "oratory, journalism, astrology and avocations requiring technical knowledge",
}

TENTH_LORD_CAREER = {
    "Sun": "kings, political office, ministers, magistrates, lawyers and civil servants",
    "Moon": "nursing, midwifery, jewellery, pearls and precious metals, and governmental activity",
    "Mars": "soldiers, carpenters, mechanics, surveyors, chemists, lawyers, bankers, commanders and insurance",
    "Mercury": "teaching, mathematics, authorship, printing, secretaryship, bookselling and accountancy",
    "Jupiter": "the priesthood, the law, councillorship, judgeship, scholarship and public life",
    "Venus": "artists, musicians, actors, perfumers, jewellers, wine sellers and solicitors",
    "Saturn": "work involving responsibility and subordination, mills, composing, hawking and factory labour",
    "Rahu": "unconventional or foreign work, and occupations touching drugs, chemicals or the occult",
    "Ketu": "research, the religious life, and work done in seclusion",
}

DASHA_HOUSE_RESULT = {
    2: "success to the family, marriage if not already married, good earnings and generally favourable results",
    3: "help and co-operation from brothers and relations, honour and approbation from others",
    4: "help to relations, acquisition of vehicles, land and houses, and higher status",
    5: "merriment, birth of a son and general prosperity",
    6: "enjoyment of good health and success over enemies and litigation -- but disease, debt and the machinations of enemies if the lord is ill-disposed",
    7: "marriage if not married, or marital happiness, pleasure trips and family happiness",
    8: "discharge of debts, acquisition of amenities and general good",
    9: "enjoyment of prosperity, birth of grandchildren, happiness and wealth",
    10: "professional prosperity, pilgrimage, reputation, respect and realisation of ambitions",
    11: "influx of wealth, domestic happiness and gains",
    12: "spending money for good purposes and religious inclination",
    1: "physical happiness and a happier placing in life, with prosperity on the increase -- provided the lord of the Ascendant is strong",
}


def _stmt(rule: str, text: str, source: str, **extra) -> dict:
    d = {"rule": rule, "text": text, "source": source}
    d.update(extra)
    return d


def _house_of(chart, planet: str) -> int:
    return chart.planets[planet].house


def _aspects_on(chart, planet: str) -> list[str]:
    return [a["from"] for a in chart.aspects if a["to"] == planet]


def _aspected_by_malefic(chart, planet: str) -> bool:
    return any(a["from"] in ("Saturn", "Mars", "Sun", "Rahu", "Ketu") for a in chart.aspects if a["to"] == planet)


def _aspected_by_benefic(chart, planet: str) -> bool:
    return any(a["from"] in ("Jupiter", "Venus", "Mercury") for a in chart.aspects if a["to"] == planet)


def interpret(chart, transit: dict | None = None) -> dict:
    """Build the reading."""
    sections: list[dict] = []
    lagna = chart.lagna_sign
    lagna_lord = chart.lord_of_sign(lagna)
    p = chart.planets
    signs = chart.sign_map()

    # ---------------- Lagna and appearance ----------------
    stmts = [
        _stmt("R-LAGNA-SIGN", f"{lagna} rises: {LAGNA_APPEARANCE[lagna]}.", "ch. V"),
    ]
    for planet in zodiac.PLANETS:
        if _house_of(chart, planet) == 1:
            stmts.append(_stmt(f"R-LAGNA-{planet.upper()}", PLANET_ON_LAGNA[planet], "ch. V"))
    if _aspected_by_benefic(chart, "Moon") and not _aspected_by_malefic(chart, "Moon"):
        stmts.append(_stmt("R-LAGNA-MOON-CLEAR", "The Moon is free of malefic aspect, which the source treats as a mark of a settled mind.", "ch. V"))
    lord_pos = p[lagna_lord]
    stmts.append(_stmt(
        "R-LAGNA-LORD",
        f"The lord of the Ascendant, {lagna_lord}, is in {lord_pos.sign} "
        f"({lord_pos.dignity}) in the {lord_pos.house}th house"
        + (" and is combust" if lord_pos.combust else "")
        + (" and retrograde" if lord_pos.retrograde else "") + ".",
        "ch. III, ch. V",
    ))
    sections.append({"title": "Ascendant, appearance and character", "statements": stmts})

    # ---------------- Mind ----------------
    moon = p["Moon"]
    stmts = [_stmt(
        "R-MIND-MOON",
        f"The Moon, which the source makes the seat of the mind, is in {moon.sign} "
        f"in the {moon.house}th house, in {moon.nakshatra} pada {moon.pada}.",
        "ch. V",
    )]
    if _aspected_by_malefic(chart, "Moon") or moon.combust:
        stmts.append(_stmt(
            "R-MIND-AFFLICTED",
            "The Moon is afflicted by malefic aspect or conjunction. The source says this "
            "inclines the subject to pessimism and constant worry, and that affliction of "
            "the Moon and Mercury together makes a quick, restless and imaginative "
            "temperament most liable to mental disturbance.",
            "ch. V",
        ))
    if _aspected_by_benefic(chart, "Moon"):
        stmts.append(_stmt("R-MIND-SUPPORTED", "The Moon receives benefic aspect, which steadies it.", "ch. V"))
    sections.append({"title": "Mind and temperament", "statements": stmts})

    # ---------------- Health ----------------
    stmts = []
    sixth = chart.houses[5]
    sixth_lord = sixth["lord"]
    if sixth["occupants"]:
        stmts.append(_stmt(
            "R-HEALTH-6OCC",
            f"The 6th house holds {', '.join(sixth['occupants'])}. The source: malefics in "
            "the 6th always indicate illness.",
            "ch. V",
        ))
    if p[lagna_lord].house in (6, 8, 12) or signs[lagna_lord] == chart.houses[5]["sign"]:
        stmts.append(_stmt(
            "R-HEALTH-LORD",
            f"The lord of the Ascendant has to do with the 6th house, which the source "
            "reads as a sickly constitution.",
            "ch. V",
        ))
    if p["Sun"].house == 6:
        stmts.append(_stmt("R-HEALTH-SUN6", "The Sun is in the 6th, which brings enteric and bowel disorders when malefics also afflict it.", "ch. V"))
    if not stmts:
        stmts.append(_stmt(
            "R-HEALTH-CLEAR",
            "The Ascendant and its lord are clear of the 6th house and its lord, which "
            "the source requires for sound health.",
            "ch. V",
        ))
    sections.append({"title": "Health", "statements": stmts})

    # ---------------- Longevity ----------------
    benefics_in_kendra = [q for q in ("Jupiter", "Venus", "Mercury") if p[q].house in zodiac.KENDRAS]
    if len(benefics_in_kendra) >= 2:
        text = (f"{', '.join(benefics_in_kendra)} occupy angles. The source: according as "
                "benefics and the lord of the Lagna are in kendras, panaparas or apoklimas, "
                "life is long, medium or short.")
        longevity = "long"
    elif p[lagna_lord].house in zodiac.KENDRAS:
        text = "The lord of the Ascendant occupies an angle, which supports a long life."
        longevity = "long"
    elif p[lagna_lord].house in zodiac.PANAPARAS:
        text = "The lord of the Ascendant occupies a panapara, which the source reads as medium life."
        longevity = "medium"
    else:
        text = "The lord of the Ascendant occupies an apoklima, which the source reads as short life."
        longevity = "short"
    stmts = [_stmt("R-LONGEVITY", text, "ch. IV", longevity=longevity)]
    stmts.append(_stmt(
        "R-LONGEVITY-CAVEAT",
        "The source's longevity rules are stated for a beginner and are the most "
        "contested part of the book; treat this as an indicator, not a prediction.",
        "ch. IV",
    ))
    sections.append({"title": "Longevity indicators", "statements": stmts})

    # ---------------- Education ----------------
    fourth_lord = chart.houses[3]["lord"]
    stmts = []
    if any(q in ("Mars", "Saturn", "Sun", "Rahu", "Ketu") for q in chart.houses[3]["occupants"]):
        stmts.append(_stmt("R-EDU-4MALEFIC", "A malefic occupies the 4th house, which the source reads as broken education.", "ch. VI"))
    if p["Jupiter"].house in (4, 10):
        stmts.append(_stmt("R-EDU-JUPITER", "Jupiter is in the 4th or the 10th, which the source says gives high legal education.", "ch. VI"))
    if p["Mercury"].house in zodiac.KENDRAS:
        stmts.append(_stmt("R-EDU-MERCURY", "Mercury is in an angle, which gives good knowledge of men and matters.", "ch. VI"))
    if p[fourth_lord].house in (3, 6, 11):
        stmts.append(_stmt("R-EDU-4LORD", f"The lord of the 4th, {fourth_lord}, sits in the {p[fourth_lord].house}th house, which the source says obstructs a sound educational career.", "ch. VI"))
    if not stmts:
        stmts.append(_stmt("R-EDU-OPEN", "The 4th house, its lord and Jupiter are free of the afflictions the source names for education.", "ch. VI"))
    sections.append({"title": "Education", "statements": stmts})

    # ---------------- Wealth ----------------
    second = chart.houses[1]
    eleventh = chart.houses[10]
    stmts = []
    if "Jupiter" in second["occupants"]:
        stmts.append(_stmt("R-WEALTH-JUP2", "Jupiter occupies the 2nd, which the source singles out as giving considerable wealth.", "ch. VI"))
    if p["Venus"].house == 10:
        stmts.append(_stmt("R-WEALTH-VEN11", "Venus occupies the 11th, which is a strong mark for gains.", "ch. VI"))
    if second["lord"] in ("Saturn", "Rahu", "Ketu") or any(q in ("Saturn", "Rahu", "Ketu") for q in second["occupants"]):
        stmts.append(_stmt(
            "R-WEALTH-SATURN",
            "Saturn, Rahu or Ketu touches the 2nd house. The source: this shows complications "
            "in finance, loss by fraud, and many ups and downs of fortune.",
            "ch. VI",
        ))
    if p[second["lord"]].house in zodiac.TRIKONAS + zodiac.KENDRAS:
        stmts.append(_stmt("R-WEALTH-2LORD", f"The lord of the 2nd, {second['lord']}, is in a trine or quadrant, which the source reads as a sign of good fortune.", "ch. VI"))
    if not stmts:
        stmts.append(_stmt("R-WEALTH-NEUTRAL", "The 2nd and 11th houses carry none of the strong markers or afflictions the source names for wealth.", "ch. VI"))
    sections.append({"title": "Financial prospects", "statements": stmts})

    # ---------------- Livelihood ----------------
    tenth = chart.houses[9]
    tenth_lord = tenth["lord"]
    element = zodiac.SIGN_NATURE[tenth["sign"]]["element"]
    stmts = [_stmt(
        "R-CAREER-SIGN",
        f"The 10th house is {tenth['sign']}, a {element} sign: {TENTH_SIGN_CAREER[element]}.",
        "ch. VII",
    ), _stmt(
        "R-CAREER-LORD",
        f"The lord of the 10th is {tenth_lord}, which points to {TENTH_LORD_CAREER[tenth_lord]}.",
        "ch. VII",
    )]
    if tenth["occupants"]:
        stmts.append(_stmt(
            "R-CAREER-OCC",
            f"The 10th holds {', '.join(tenth['occupants'])}, whose own significations colour the profession.",
            "ch. VII",
        ))
    nav_lord = chart.lord_of_sign(p[tenth_lord].navamsa_sign)
    stmts.append(_stmt(
        "R-CAREER-NAVAMSA",
        f"The navamsa occupied by the lord of the 10th is {p[tenth_lord].navamsa_sign}, whose "
        f"lord is {nav_lord}; the source reads that lord as a further indication of the calling "
        f"({TENTH_LORD_CAREER[nav_lord]}).",
        "ch. VII",
    ))
    sections.append({"title": "Means of livelihood", "statements": stmts})

    # ---------------- Parents and siblings ----------------
    fourth = chart.houses[3]
    ninth = chart.houses[8]
    stmts = []
    if "Sun" in ninth["occupants"] and "Saturn" in ninth["occupants"]:
        stmts.append(_stmt("R-FATHER-EARLY", "The Sun and Saturn together in the 9th indicate early death of the father.", "ch. VIII"))
    if "Saturn" in fourth["occupants"] and "Moon" in fourth["occupants"]:
        stmts.append(_stmt("R-MOTHER-EARLY", "Saturn with the Moon in the 4th denotes early death to the mother.", "ch. VIII"))
    if _aspected_by_malefic(chart, "Sun"):
        stmts.append(_stmt("R-FATHER-AFFLICTED", "The Sun is afflicted, which the source reads as trouble to the father.", "ch. VIII"))
    if _aspected_by_malefic(chart, "Moon"):
        stmts.append(_stmt("R-MOTHER-AFFLICTED", "The Moon is afflicted, which touches the mother's condition.", "ch. VIII"))
    if "Mars" in chart.houses[2]["occupants"]:
        stmts.append(_stmt("R-BROTHERS-MARS3", "Mars in the 3rd does not indicate many brothers.", "ch. VIII"))
    if not stmts:
        stmts.append(_stmt("R-PARENTS-OPEN", "Neither luminary is afflicted and neither the 4th nor the 9th carries the combinations the source names for the parents.", "ch. VIII"))
    sections.append({"title": "Parents, brothers and debts", "statements": stmts})

    # ---------------- Marriage ----------------
    seventh = chart.houses[6]
    stmts = []
    for occupant in seventh["occupants"]:
        stmts.append(_stmt(
            f"R-MARRIAGE-{occupant.upper()}",
            f"{occupant} is in the 7th: the partner is {SEVENTH_HOUSE_PARTNER[occupant]}.",
            "ch. IX",
        ))
    if "Venus" in seventh["occupants"] and (seventh["occupants"].count("Venus") and _aspected_by_malefic(chart, "Venus")):
        stmts.append(_stmt("R-MARRIAGE-VENUS-AFFLICTED", "Venus is in the 7th but afflicted, which the source reads as an unsatisfactory marriage.", "ch. IX"))
    if p[seventh["lord"]].house == 6:
        stmts.append(_stmt("R-MARRIAGE-7LORD6", "The lord of the 7th occupies the 6th, which the source warns against for marital happiness.", "ch. IX"))
    if _aspected_by_malefic(chart, "Venus"):
        stmts.append(_stmt("R-MARRIAGE-VENUS", "Venus is afflicted by a malefic; the source reads this as little emotional calm and prolonged separation when Mars is the afflictor.", "ch. IX"))
    if not stmts:
        stmts.append(_stmt("R-MARRIAGE-OPEN", "The 7th house and its lord carry none of the afflictions the source names for marriage.", "ch. IX"))
    sections.append({"title": "Marriage", "statements": stmts})

    # ---------------- Children ----------------
    fifth = chart.houses[4]
    stmts = []
    if "Saturn" in fifth["occupants"]:
        stmts.append(_stmt("R-CHILDREN-SATURN5", "Saturn in the 5th is among the afflictions the source names for children.", "ch. IX"))
    if any(q in ("Mars", "Saturn", "Rahu", "Ketu") for q in fifth["occupants"]):
        stmts.append(_stmt("R-CHILDREN-MALEFIC", "A malefic occupies the 5th, which the source says produces results opposite to those of a well-aspected 5th.", "ch. IX"))
    if _aspected_by_benefic(chart, "Jupiter") or p["Jupiter"].house in (5, 9):
        stmts.append(_stmt("R-CHILDREN-JUPITER", "Jupiter, the Putrakaraka, is well placed, which supports progeny.", "ch. IX"))
    if not stmts:
        stmts.append(_stmt("R-CHILDREN-OPEN", "The 5th house, its lord and Jupiter carry none of the afflictions the source names for children.", "ch. IX"))
    sections.append({"title": "Children", "statements": stmts})

    # ---------------- Yogas ----------------
    present = [y for y in chart.yogas if y["present"]]
    stmts = [
        _stmt(f"R-YOGA-{y['name'].upper()}", f"{y['name']}: {y['description']}", y["source"])
        for y in present
    ]
    if not stmts:
        stmts.append(_stmt("R-YOGA-NONE", "None of the yogas this engine detects are present in the chart.", "ch. III"))
    sections.append({"title": "Yogas present", "statements": stmts})

    # ---------------- Dasha ----------------
    current = chart.vimshottari["current"]
    maha = current.get("mahadasha")
    stmts = []
    if maha:
        lord = maha["lord"]
        house = p[lord].house
        base = DASHA_HOUSE_RESULT.get(house, "")
        stmts.append(_stmt(
            "R-DASHA-MAHA",
            f"The mahadasha of {lord} runs from {maha['start_date']} to {maha['end_date']}. "
            f"{lord} rules the {house}th house and is {p[lord].dignity}. The source expects: {base}.",
            "ch. X",
        ))
        if p[lord].dignity in ("debilitated", "enemy", "bitter enemy"):
            stmts.append(_stmt(
                "R-DASHA-WEAK",
                f"{lord} is weak by dignity, so the source would temper the above and expect "
                "ailment, unhappiness or obstruction instead.",
                "ch. X",
            ))
        sub = current.get("antardasha")
        if sub:
            stmts.append(_stmt(
                "R-DASHA-ANTAR",
                f"The bhukti of {sub['lord']} runs from {sub['start_date']} to {sub['end_date']}. "
                "The source says the relations between the major lord and the sub-lord decide "
                "the result, and that a temporary friendship does not overcome a radical enmity.",
                "ch. X",
            ))
    sections.append({"title": "Current period (Vimshottari)", "statements": stmts})

    # ---------------- Transits ----------------
    if transit:
        stmts = []
        slow = [r for r in transit["gochara"] if r["planet"] in ("Jupiter", "Saturn", "Rahu")]
        for row in slow:
            if row["result"]:
                stmts.append(_stmt(
                    f"R-TRANSIT-{row['planet'].upper()}",
                    f"{row['planet']} transits {row['sign']}, the {row['house_from_moon']}th from the "
                    f"Janma Rasi {transit['janma_rasi']}: {row['result']}.",
                    "ch. XII",
                ))
        if transit["sade_sati"]["active"]:
            stmts.append(_stmt(
                "R-TRANSIT-SADESATI",
                "Sade Sati is running: Saturn transits the 12th, 1st or 2nd from the radical Moon. "
                "The source warns of quarrels, litigation, failure of business, restlessness, "
                "change of place, sickness in the family and mental worry -- unless the ruling "
                "period is powerful.",
                "ch. XII",
            ))
        stmts.append(_stmt("R-TRANSIT-CAVEAT", transit["weighting"], "ch. XII"))
        sections.append({"title": "Transits (gochara) as of today", "statements": stmts})

    return {
        "sections": sections,
        "disclaimer": (
            "This is a rule-based reading of a single classical primer, produced by software. "
            "It is presented for study and self-reflection, not as medical, financial or legal "
            "advice, and not as a factual prediction about any person."
        ),
    }
