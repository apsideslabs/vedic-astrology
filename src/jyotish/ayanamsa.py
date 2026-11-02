"""Ayanamsa (precessional distance) models.

Two models are provided:

``lahiri``
    The Chitrapaksha ayanamsa used by the Indian Astronomical Ephemeris and by
    almost all Indian astrology software.  Anchored at the published value for
    J2000.0 and propagated with the IAU 2006 general precession in longitude.
    Agreement with the Indian Astronomical Ephemeris is a few arcseconds over
    1900-2100 -- far below the 1 arcminute that matters in practice.

``raman_397``
    The arithmetic rule actually given in Appendix I of the source book::

        ayanamsa = (year - 397) * 50 1/3 arcseconds

    It is a rule of thumb, not a rigorous precession model.  For 1935 it gives
    21 deg 30 min, whereas Lahiri gives about 22 deg 57 min -- a difference of
    roughly 1 deg 27 min.  It is kept because the source's own worked example
    (chapter II) is cast with it, and reproducing that example requires it.

Nothing here is a substitute for the Swiss Ephemeris when arcsecond
consistency with other software matters; see ``docs/07-calculation.md``.
"""

from __future__ import annotations

J2000_JD = 2451545.0

# Published Lahiri ayanamsa at J2000.0 (2000-01-01 12:00 TT):
# 23 deg 51 min 11.5 sec.
LAHIRI_J2000 = 23.0 + 51.0 / 60.0 + 11.5 / 3600.0

# IAU 2006 accumulated general precession in longitude, in arcseconds,
# as a polynomial in T (Julian centuries of TT from J2000.0).
# p_A = 5028.796195 T + 1.1054348 T^2 + ...
_PRECESSION_TERMS = (5028.796195, 1.1054348, 0.00007964, -0.000023857, -0.0000000383)


def _centuries(jd: float) -> float:
    return (jd - J2000_JD) / 36525.0


def precession_in_longitude(jd: float) -> float:
    """Accumulated general precession in ecliptic longitude since J2000, in degrees."""
    t = _centuries(jd)
    arcsec = 0.0
    for power, coeff in enumerate(_PRECESSION_TERMS, start=1):
        arcsec += coeff * t ** power
    return arcsec / 3600.0


def lahiri(jd: float) -> float:
    """Lahiri (Chitrapaksha) ayanamsa in degrees."""
    return LAHIRI_J2000 + precession_in_longitude(jd)


def raman_397(jd: float, year: float | None = None) -> float:
    """The source book's arithmetic rule: (year - 397) * 50 1/3 arcsec."""
    if year is None:
        year = jd_to_year(jd)
    return (year - 397.0) * (50.0 + 1.0 / 3.0) / 3600.0


def jd_to_year(jd: float) -> float:
    """Decimal Julian year from a Julian Day number."""
    return 2000.0 + (jd - J2000_JD) / 365.25


MODELS = {
    "lahiri": lahiri,
    "raman_397": raman_397,
}


def value(name: str, jd: float) -> float:
    """Ayanamsa in degrees for the named model."""
    try:
        model = MODELS[name]
    except KeyError:
        raise ValueError(f"unknown ayanamsa model {name!r}; choose from {sorted(MODELS)}") from None
    return model(jd)
