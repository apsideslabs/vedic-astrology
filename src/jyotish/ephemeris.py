"""Ephemeris layer: planetary longitudes, sidereal time, obliquity.

Positions come from the ``astronomy-engine`` library, which computes apparent
geocentric positions of the Sun, Moon and planets directly from VSOP87/ELP2000
series without needing data files.  Accuracy is well inside one arcminute for
the bodies used here, which is ample for chart work.

If you have the Swiss Ephemeris available (``pyswisseph``), swap
:func:`tropical_longitudes` for it: the rest of the package only consumes
``{planet: (longitude, latitude, daily_motion)}`` and does not care where the
numbers come from.  See ``docs/07-calculation.md``.

Rahu and Ketu are the *mean* lunar node, which is what Raman's ephemeris
tabulates and what most Indian software uses.  The mean node is always
retrograde.
"""

from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone

import astronomy as astro

from . import zodiac

J2000_JD = 2451545.0

_BODY_MAP = {
    "Sun": astro.Body.Sun,
    "Moon": astro.Body.Moon,
    "Mars": astro.Body.Mars,
    "Mercury": astro.Body.Mercury,
    "Jupiter": astro.Body.Jupiter,
    "Venus": astro.Body.Venus,
    "Saturn": astro.Body.Saturn,
}


# --------------------------------------------------------------------------
# Time
# --------------------------------------------------------------------------
def to_time(dt_utc: datetime) -> astro.Time:
    """Convert an aware (or naive, assumed UTC) datetime to an astronomy Time."""
    if dt_utc.tzinfo is not None:
        dt_utc = dt_utc.astimezone(timezone.utc).replace(tzinfo=None)
    return astro.Time.Make(
        dt_utc.year, dt_utc.month, dt_utc.day,
        dt_utc.hour, dt_utc.minute, dt_utc.second + dt_utc.microsecond / 1e6,
    )


def julian_day(dt_utc: datetime) -> float:
    """Julian Day (UT) for a datetime."""
    return J2000_JD + to_time(dt_utc).ut


def jd_to_datetime(jd: float) -> datetime:
    """Inverse of :func:`julian_day`, returned as a naive UTC datetime."""
    return datetime(2000, 1, 1, 12, 0, 0) + timedelta(days=jd - J2000_JD)


# --------------------------------------------------------------------------
# Longitudes
# --------------------------------------------------------------------------
def _ecliptic_longitude(body: str, t: astro.Time) -> tuple[float, float]:
    if body == "Moon":
        sph = astro.EclipticGeoMoon(t)
        return sph.lon % 360.0, sph.lat
    vec = astro.GeoVector(_BODY_MAP[body], t, True)
    ecl = astro.Ecliptic(vec)
    return ecl.elon % 360.0, ecl.elat


def mean_node_longitude(jd: float) -> float:
    """Mean longitude of the Moon's ascending node (Rahu), in degrees.

    Meeus, *Astronomical Algorithms*, ch. 47.
    """
    t = (jd - J2000_JD) / 36525.0
    omega = (
        125.0445479
        - 1934.1362891 * t
        + 0.0020754 * t ** 2
        + t ** 3 / 467441.0
        - t ** 4 / 60616000.0
    )
    return omega % 360.0


def _signed_delta(later: float, earlier: float) -> float:
    d = (later - earlier) % 360.0
    return d - 360.0 if d > 180.0 else d


def tropical_longitudes(jd: float, with_speed: bool = True) -> dict[str, dict]:
    """Apparent geocentric tropical longitudes for all nine grahas.

    Returns ``{planet: {"longitude", "latitude", "speed"}}`` where ``speed`` is
    degrees per day (negative = retrograde).
    """
    dt = jd_to_datetime(jd)
    t = to_time(dt)
    out: dict[str, dict] = {}

    for planet in zodiac.SEVEN_GRAHAS:
        lon, lat = _ecliptic_longitude(planet, t)
        speed = 0.0
        if with_speed:
            lon_before, _ = _ecliptic_longitude(planet, to_time(dt - timedelta(hours=12)))
            lon_after, _ = _ecliptic_longitude(planet, to_time(dt + timedelta(hours=12)))
            speed = _signed_delta(lon_after, lon_before)
        out[planet] = {"longitude": lon, "latitude": lat, "speed": speed}

    rahu = mean_node_longitude(jd)
    out["Rahu"] = {"longitude": rahu, "latitude": 0.0, "speed": -0.0529539}
    out["Ketu"] = {"longitude": (rahu + 180.0) % 360.0, "latitude": 0.0, "speed": -0.0529539}
    return out


# --------------------------------------------------------------------------
# Frame
# --------------------------------------------------------------------------
def obliquity(jd: float) -> float:
    """Mean obliquity of the ecliptic in degrees (IAU 1980, Meeus 22.2)."""
    t = (jd - J2000_JD) / 36525.0
    arcsec = 84381.448 - 46.8150 * t - 0.00059 * t ** 2 + 0.001813 * t ** 3
    return arcsec / 3600.0


def sidereal_time_hours(jd: float) -> float:
    """Apparent Greenwich sidereal time in hours."""
    return astro.SiderealTime(to_time(jd_to_datetime(jd))) % 24.0


def local_sidereal_degrees(jd: float, longitude_east: float) -> float:
    """Local apparent sidereal time expressed as an angle (RAMC), in degrees."""
    return (sidereal_time_hours(jd) * 15.0 + longitude_east) % 360.0


def ascendant(lst_deg: float, latitude: float, eps_deg: float) -> float:
    """Tropical ecliptic longitude of the Ascendant.

    Standard quadrant formula; validated against the worked example in the
    source (chapter II), which expects 29 deg 39 min Libra for Madras.
    """
    ramc = math.radians(lst_deg)
    eps = math.radians(eps_deg)
    phi = math.radians(latitude)
    y = math.cos(ramc)
    x = -(math.sin(ramc) * math.cos(eps) + math.tan(phi) * math.sin(eps))
    return math.degrees(math.atan2(y, x)) % 360.0


def midheaven(lst_deg: float, eps_deg: float) -> float:
    """Tropical ecliptic longitude of the Midheaven (10th cusp)."""
    ramc = math.radians(lst_deg)
    eps = math.radians(eps_deg)
    return math.degrees(math.atan2(math.sin(ramc), math.cos(ramc) * math.cos(eps))) % 360.0
