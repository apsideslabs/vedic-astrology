"""Tests for the jyotish engine.

The strongest tests here check the engine against the worked example the
source book carries in chapter II, which tabulates the nine grahas and the
Ascendant for a birth at Madras on 2 November 1935.
"""

from __future__ import annotations

import math
from datetime import datetime

import pytest

from jyotish import ayanamsa, dasha, ephemeris, houses, strength, zodiac
from jyotish.chart import BirthData, build_chart

# The source's own example.  Local mean time 05:20 with the place's longitude
# of 5h 10m 20s east gives 00:09:40 UT, i.e. a UT offset of 5.172222 h.
BOOK_BIRTH = BirthData(
    date="1935-11-02", time="05:20:00", latitude=13.0, longitude=77.5833333,
    tz_offset=5.1722222, place="Madras",
)

# Sidereal longitudes as printed in the source, chapter II.
BOOK_POSITIONS = {
    "Sun": 197.0 + 9.0 / 60.0,        # Libra 17 deg 09
    "Moon": 240.0 + 22.0 + 35.0 / 60.0,   # Sagittarius 22 deg 35
    "Mars": 240.0 + 11.0 + 40.0 / 60.0,
    "Mercury": 150.0 + 28.0 + 35.0 / 60.0,
    "Jupiter": 210.0 + 6.0 + 53.0 / 60.0,
    "Venus": 150.0 + 1.0 + 45.0 / 60.0,
    "Saturn": 300.0 + 12.0 + 2.0 / 60.0,
    "Rahu": 240.0 + 24.0 + 34.0 / 60.0,
}


@pytest.fixture(scope="module")
def book_chart():
    return build_chart(BOOK_BIRTH, ayanamsa="raman_397")


# ---------------------------------------------------------------- ephemeris
def test_book_example_positions(book_chart):
    """Every graha within 0.1 degree of the source's printed table."""
    for planet, expected in BOOK_POSITIONS.items():
        got = book_chart.planets[planet].longitude
        diff = abs((got - expected + 180.0) % 360.0 - 180.0)
        assert diff < 0.1, f"{planet}: engine {got:.4f} vs book {expected:.4f}"


def test_book_example_ascendant():
    """Tropical Ascendant should match the source's 29 deg 39 min Libra."""
    jd = ephemeris.julian_day(BOOK_BIRTH.utc_datetime())
    eps = ephemeris.obliquity(jd)
    lst = ephemeris.local_sidereal_degrees(jd, BOOK_BIRTH.longitude)
    asc = ephemeris.ascendant(lst, BOOK_BIRTH.latitude, eps)
    expected = 180.0 + 29.0 + 39.0 / 60.0
    assert abs((asc - expected + 180.0) % 360.0 - 180.0) < 0.25


def test_mean_node_against_book(book_chart):
    """Mean node in 1935 minus the book's ayanamsa reproduces Rahu's position."""
    jd = ephemeris.julian_day(BOOK_BIRTH.utc_datetime())
    node = ephemeris.mean_node_longitude(jd)
    sidereal = (node - ayanamsa.raman_397(jd)) % 360.0
    assert abs(sidereal - BOOK_POSITIONS["Rahu"]) < 0.05


def test_ketu_is_opposite_rahu(book_chart):
    diff = (book_chart.planets["Ketu"].longitude - book_chart.planets["Rahu"].longitude) % 360.0
    assert abs(diff - 180.0) < 1e-6


def test_daily_motions():
    jd = ephemeris.julian_day(datetime(2024, 1, 1, 0, 0, 0))
    pos = ephemeris.tropical_longitudes(jd)
    assert 0.95 < pos["Sun"]["speed"] < 1.05
    assert 11.5 < pos["Moon"]["speed"] < 15.5
    assert pos["Saturn"]["speed"] < 0.3


# ---------------------------------------------------------------- ayanamsa
def test_lahiri_at_j2000():
    value = ayanamsa.lahiri(2451545.0)
    assert abs(value - 23.853194) < 1e-4          # 23 deg 51' 11.5"


def test_lahiri_increases_by_about_50_arcsec_a_year():
    a = ayanamsa.lahiri(2451545.0)
    b = ayanamsa.lahiri(2451545.0 + 36525.0)
    rate = (b - a) * 3600.0 / 100.0               # arcsec per year
    assert 50.2 < rate < 50.4


def test_book_rule_matches_its_own_worked_example():
    """Appendix I: (1935 - 397) * 50 1/3 arcsec = 21 deg 30 min."""
    jd = ephemeris.julian_day(datetime(1935, 6, 1, 0, 0, 0))
    value = ayanamsa.raman_397(jd, year=1935)
    assert abs(value - (21.0 + 30.0 / 60.0)) < 0.01


def test_lahiri_and_book_rule_differ_by_about_one_and_a_half_degrees():
    jd = ephemeris.julian_day(datetime(1935, 11, 2, 0, 10, 0))
    assert 1.3 < ayanamsa.lahiri(jd) - ayanamsa.raman_397(jd, year=1935) < 1.6


def test_mesha_sankranti():
    """The Sun enters sidereal Aries in mid-April: a physical check on the frame."""
    jd = ephemeris.julian_day(datetime(2026, 4, 14, 12, 0, 0))
    ay = ayanamsa.lahiri(jd)
    sun = (ephemeris.tropical_longitudes(jd)["Sun"]["longitude"] - ay) % 360.0
    assert sun < 1.0 or sun > 359.0


# ---------------------------------------------------------------- zodiac
def test_navamsa_matches_book_example():
    """Libra 20 deg 10 min falls in the 7th navamsa of Libra, i.e. Aries."""
    longitude = 180.0 + 20.0 + 10.0 / 60.0
    assert zodiac.navamsa_sign(longitude) == "Aries"


def test_nakshatra_span():
    assert zodiac.nakshatra_name(0.0) == "Ashwini"
    assert zodiac.nakshatra_pada(0.0) == 1
    assert zodiac.nakshatra_pada(3.5) == 2
    assert zodiac.nakshatra_name(360.0 - 0.001) == "Revati"
    assert zodiac.nakshatra_name(13.34) == "Bharani"


def test_nakshatra_lords_start_with_ketu():
    assert zodiac.NAKSHATRA_LORDS[0] == "Ketu"
    assert zodiac.NAKSHATRA_LORDS[1] == "Venus"
    assert zodiac.NAKSHATRA_LORDS[8] == "Mercury"
    assert zodiac.NAKSHATRA_LORDS[9] == "Ketu"


def test_exaltation_and_debilitation_are_opposite():
    for planet, (sign, _) in zodiac.EXALTATION.items():
        deb_sign, _ = zodiac.DEBILITATION[planet]
        assert zodiac.SIGNS.index(deb_sign) == (zodiac.SIGNS.index(sign) + 6) % 12


def test_dignity():
    assert strength.dignity("Sun", 10.0) == "exalted"            # Aries 10
    assert strength.dignity("Sun", 190.0) == "debilitated"       # Libra 10
    assert strength.dignity("Sun", 125.0) == "moolatrikona"      # Leo 5
    assert strength.dignity("Saturn", 305.0) == "moolatrikona"   # Aquarius 5


# ---------------------------------------------------------------- dasha
def test_vimshottari_years_total_120():
    assert sum(zodiac.VIMSHOTTARI_YEARS.values()) == 120


def test_book_example_dasha_balance(book_chart):
    """The source works out a balance of 6y 1m 15d of Venus at this birth."""
    balance = book_chart.vimshottari["balance_at_birth"]
    assert balance["lord"] == "Venus"
    decimal = balance["decimal_years"]
    # The source rounds its ayanamsa to 21 deg 30 min; that alone moves the
    # balance by a few weeks.
    assert abs(decimal - 6.125) < 0.1


def test_sub_period_matches_book_shortcut():
    """Saturn's bhukti in Mercury's dasha: 19 x 17 -> 32 months 9 days."""
    subs = dasha.antardashas("Mercury", datetime(2000, 1, 1), 17)
    saturn = next(s for s in subs if s["lord"] == "Saturn")
    assert abs(saturn["years"] - (19 * 17 / 120)) < 1e-9
    assert saturn["years"] > 2.6
    assert abs(saturn["years"] * 12 - 32.3) < 0.05


def test_antardashas_cover_the_mahadasha():
    start = datetime(2000, 1, 1)
    subs = dasha.antardashas("Jupiter", start, 16)
    assert len(subs) == 9
    total = sum(s["years"] for s in subs)
    assert abs(total - 16.0) < 1e-9
    assert subs[0]["lord"] == "Jupiter"
    assert datetime.fromisoformat(subs[-1]["end"]).year >= 2015


# ---------------------------------------------------------------- chart
def test_book_chart_structure(book_chart):
    assert book_chart.lagna_sign == "Libra"
    assert book_chart.planets["Sun"].house == 1
    assert book_chart.planets["Jupiter"].house == 2
    assert set(book_chart.planets_in_house(3)) == {"Moon", "Mars", "Rahu"}
    assert book_chart.planets["Saturn"].house == 5
    assert book_chart.planets["Ketu"].house == 9
    assert set(book_chart.planets_in_house(12)) == {"Mercury", "Venus"}


def test_book_chart_dignities(book_chart):
    """The source notes: Sun and Venus debilitated, Mercury exalted, Saturn own."""
    assert book_chart.planets["Sun"].dignity == "debilitated"
    assert book_chart.planets["Venus"].dignity == "debilitated"
    assert book_chart.planets["Mercury"].dignity == "exalted"
    assert book_chart.planets["Saturn"].dignity in ("own", "moolatrikona")


def test_mars_jupiter_exchange(book_chart):
    """The source notes that Mars and Jupiter have exchanged places."""
    signs = book_chart.sign_map()
    assert signs["Mars"] == "Sagittarius" and signs["Jupiter"] == "Scorpio"
    assert zodiac.SIGN_LORDS[zodiac.SIGNS.index("Sagittarius")] == "Jupiter"
    assert zodiac.SIGN_LORDS[zodiac.SIGNS.index("Scorpio")] == "Mars"


def test_aspects_include_special_ones(book_chart):
    # Saturn in Aquarius aspects the 3rd and the 10th from itself; the 10th
    # from Aquarius is Scorpio, where Jupiter sits.
    saturn_to_jupiter = [a for a in book_chart.aspects
                         if a["from"] == "Saturn" and a["to"] == "Jupiter"]
    assert saturn_to_jupiter
    assert saturn_to_jupiter[0]["house_distance"] == 10
    # Jupiter in Scorpio throws sight on the 5th (Pisces), 7th (Taurus) and
    # 9th (Cancer) from itself -- all empty here, so it makes no planet pair,
    # but the house aspects must still be recorded.
    houses_seen = {h["house"] for h in book_chart.aspected_houses("Jupiter")}
    assert houses_seen == {5, 7, 9}
    assert {h["house"] for h in book_chart.aspected_houses("Saturn")} == {3, 7, 10}
    assert {h["house"] for h in book_chart.aspected_houses("Mars")} == {4, 7, 8}
    assert {h["house"] for h in book_chart.aspected_houses("Venus")} == {7}
    # Partial sight fractions follow the source's table.
    sight = {h["house"]: h["sight"] for h in book_chart.aspected_houses("Saturn")}
    assert sight == {3: 0.25, 7: 1.0, 10: 0.25}
    # Every planet-to-planet aspect is at an allowed distance for its source.
    for a in book_chart.aspects:
        allowed = zodiac.SPECIAL_ASPECTS.get(a["from"], zodiac.DEFAULT_ASPECTS)
        assert a["house_distance"] in allowed
    # The 7th aspect is mutual.
    for a in book_chart.aspects:
        if a["house_distance"] == 7:
            assert any(b["from"] == a["to"] and b["to"] == a["from"]
                       for b in book_chart.aspects)


def test_all_nine_planets_present(book_chart):
    assert set(book_chart.planets) == set(zodiac.PLANETS)


def test_house_systems_agree_on_the_ascendant():
    jd = ephemeris.julian_day(BOOK_BIRTH.utc_datetime())
    eps = ephemeris.obliquity(jd)
    lst = ephemeris.local_sidereal_degrees(jd, BOOK_BIRTH.longitude)
    asc = ephemeris.ascendant(lst, BOOK_BIRTH.latitude, eps)
    for system in houses.HOUSE_SYSTEMS:
        cusps = houses.cusps(system, lst, BOOK_BIRTH.latitude, eps)
        assert set(cusps) == set(range(1, 13))
        if system == "whole_sign":
            assert cusps[1] == math.floor(asc / 30.0) * 30.0
        else:
            assert abs((cusps[1] - asc + 180.0) % 360.0 - 180.0) < 1e-9


def test_modern_chart_is_sane():
    chart = build_chart(BirthData(
        date="1990-04-14", time="08:15", latitude=13.0827, longitude=80.2707,
        tz_offset=5.5, place="Chennai",
    ))
    assert chart.ayanamsa_model == "lahiri"
    assert 23.5 < chart.ayanamsa_value < 24.5
    for pos in chart.planets.values():
        assert 0.0 <= pos.longitude < 360.0
        assert 1 <= pos.house <= 12
        assert 1 <= pos.pada <= 4
        assert 0.0 <= pos.strength["score"] <= 100.0
    assert chart.vimshottari["mahadashas"][0]["lord"] == chart.vimshottari["janma_nakshatra_lord"]


def test_panchanga_consistency(book_chart):
    pn = book_chart.panchanga
    assert pn["tithi"]["paksha"] in ("Shukla", "Krishna")
    assert 1 <= pn["tithi"]["index"] <= 30
    assert 1 <= pn["yoga"]["index"] <= 27
    assert pn["vara"]["name"] == "Saturday"     # 2 November 1935 was a Saturday


def test_transits_and_interpretation(book_chart):
    from jyotish import interpret, transits

    t = transits.analyse(book_chart, datetime(2026, 11, 2, 0, 0, 0))
    assert t["janma_rasi"] == "Sagittarius"
    assert len(t["gochara"]) == 9
    reading = interpret.interpret(book_chart, t)
    assert reading["sections"]
    assert all("rule" in s and "source" in s for sec in reading["sections"] for s in sec["statements"])
