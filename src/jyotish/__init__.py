"""jyotish -- a Vedic astrology engine.

Public surface::

    from jyotish import BirthData, build_chart
    chart = build_chart(BirthData(date="1990-01-01", time="12:00",
                                  latitude=13.08, longitude=80.27,
                                  tz_offset=5.5, place="Chennai"))
    print(chart.as_dict())

The knowledge the engine encodes is documented under ``docs/``.
"""

from __future__ import annotations

from .chart import BirthData, Chart, PlanetPosition, build_chart
from . import ayanamsa, dasha, ephemeris, houses, interpret, panchanga, strength, transits, yogas, zodiac

__version__ = "1.0.0"

__all__ = [
    "BirthData", "Chart", "PlanetPosition", "build_chart",
    "ayanamsa", "dasha", "ephemeris", "houses", "interpret",
    "panchanga", "strength", "transits", "yogas", "zodiac",
    "__version__",
]
