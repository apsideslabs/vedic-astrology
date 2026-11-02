"""Panchanga -- the five limbs of the Vedic day.

Computed from the sidereal longitudes of the Sun and Moon.  The source book
does not treat the panchanga, but any working astrology application needs it,
and every element here follows directly from the definitions in chapter I.
"""

from __future__ import annotations

from datetime import datetime

TITHIS = (
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi",
    "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dwadashi",
    "Trayodashi", "Chaturdashi", "Purnima/Amavasya",
)
YOGAS = (
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda",
    "Sukarma", "Dhriti", "Shula", "Ganda", "Vriddhi", "Dhruva", "Vyaghata",
    "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyan", "Parigha", "Shiva",
    "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma", "Indra", "Vaidhriti",
)
KARANAS = (
    "Bava", "Balava", "Kaulava", "Taitila", "Gara", "Vanija", "Vishti",
    "Shakuni", "Chatushpada", "Naga", "Kimstughna",
)
VARAS = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
VARA_LORDS = ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn")


def _karana(index: int) -> str:
    # 60 half-tithis per lunar month; the first is Kimstughna, then the seven
    # movable karanas cycle, and the last three are fixed.
    if index == 0:
        return "Kimstughna"
    if index >= 57:
        return ("Shakuni", "Chatushpada", "Naga")[index - 57]
    return KARANAS[(index - 1) % 7]


def compute(local_dt: datetime, sun_longitude: float, moon_longitude: float) -> dict:
    """Return the five limbs plus a few derived fields."""
    diff = (moon_longitude - sun_longitude) % 360.0

    tithi_index = int(diff // 12.0)              # 0..29
    paksha = "Shukla" if tithi_index < 15 else "Krishna"
    tithi_name = TITHIS[tithi_index % 15]
    tithi_fraction = (diff % 12.0) / 12.0

    yoga_index = int(((sun_longitude + moon_longitude) % 360.0) // (360.0 / 27.0))
    karana_index = int(diff // 6.0)              # 0..59

    vara_index = (local_dt.weekday() + 1) % 7    # Python: Mon=0 -> Sunday=0

    return {
        "vara": {"index": vara_index, "name": VARAS[vara_index], "lord": VARA_LORDS[vara_index]},
        "tithi": {
            "index": tithi_index + 1,
            "name": tithi_name,
            "paksha": paksha,
            "complete_percent": round(tithi_fraction * 100, 1),
        },
        "nakshatra": None,   # filled by the caller, which knows the Moon's nakshatra
        "yoga": {"index": yoga_index + 1, "name": YOGAS[yoga_index]},
        "karana": {"index": karana_index + 1, "name": _karana(karana_index)},
    }
