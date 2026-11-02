"""FastAPI application.

Run it with::

    uvicorn app.main:app --reload

Endpoints
    GET  /             the single-page app
    POST /api/chart    full chart payload (JSON)
    GET  /api/health   liveness plus engine versions
"""

from __future__ import annotations

import sys
from datetime import date as _date
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, field_validator

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from jyotish import __version__, interpret, transits  # noqa: E402
from jyotish.chart import BirthData, build_chart  # noqa: E402
from jyotish import zodiac  # noqa: E402

app = FastAPI(
    title="Jyotish API",
    version=__version__,
    description="Vedic (Nirayana) chart calculation and rule-based interpretation.",
)
templates = Jinja2Templates(directory=str(ROOT / "templates"))

PRESETS = [
    {"name": "Chennai", "lat": 13.0827, "lon": 80.2707, "tz": 5.5},
    {"name": "Delhi", "lat": 28.6139, "lon": 77.2090, "tz": 5.5},
    {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777, "tz": 5.5},
    {"name": "Kolkata", "lat": 22.5726, "lon": 88.3639, "tz": 5.5},
    {"name": "Bengaluru", "lat": 12.9716, "lon": 77.5946, "tz": 5.5},
    {"name": "Hyderabad", "lat": 17.3850, "lon": 78.4867, "tz": 5.5},
    {"name": "Ahmedabad", "lat": 23.0225, "lon": 72.5714, "tz": 5.5},
    {"name": "Pune", "lat": 18.5204, "lon": 73.8567, "tz": 5.5},
    {"name": "Jaipur", "lat": 26.9124, "lon": 75.7873, "tz": 5.5},
    {"name": "Madras (1935)", "lat": 13.0, "lon": 77.5833, "tz": 5.172222},
]


class ChartRequest(BaseModel):
    date: str = Field(..., examples=["1990-04-14"], description="local civil date, YYYY-MM-DD")
    time: str = Field(..., examples=["08:15"], description="local civil time, HH:MM[:SS]")
    latitude: float = Field(..., ge=-90, le=90, description="degrees, north positive")
    longitude: float = Field(..., ge=-180, le=180, description="degrees, east positive")
    tz_offset: float = Field(5.5, ge=-14, le=14, description="UT offset in hours")
    place: str = ""
    name: str = ""
    ayanamsa: Literal["lahiri", "raman_397"] = "lahiri"
    house_system: Literal["whole_sign", "sripati", "equal"] = "whole_sign"

    @field_validator("date")
    @classmethod
    def _check_date(cls, v: str) -> str:
        try:
            _date.fromisoformat(v)
        except ValueError:
            raise ValueError("date must be YYYY-MM-DD") from None
        return v

    @field_validator("time")
    @classmethod
    def _check_time(cls, v: str) -> str:
        parts = v.split(":")
        if len(parts) not in (2, 3) or not all(p.isdigit() for p in parts):
            raise ValueError("time must be HH:MM or HH:MM:SS")
        if not (0 <= int(parts[0]) <= 23 and 0 <= int(parts[1]) <= 59):
            raise ValueError("time out of range")
        return v


def _payload(req: ChartRequest) -> dict:
    birth = BirthData(
        date=req.date, time=req.time, latitude=req.latitude, longitude=req.longitude,
        tz_offset=req.tz_offset, place=req.place, name=req.name,
    )
    chart = build_chart(birth, ayanamsa=req.ayanamsa, house_system=req.house_system)
    transit = transits.analyse(chart)
    data = chart.as_dict()
    data["transits"] = transit
    data["interpretation"] = interpret.interpret(chart, transit)
    data["south_indian"] = _south_indian(chart)
    data["navamsa_grid"] = _south_indian(chart, navamsa=True)
    return data


SOUTH_INDIAN_ORDER = (
    "Pisces", "Aries", "Taurus", "Gemini",
    "Aquarius", None, None, "Cancer",
    "Capricorn", None, None, "Leo",
    "Sagittarius", "Scorpio", "Libra", "Virgo",
)


def _south_indian(chart, navamsa: bool = False) -> list[dict]:
    """Cells of the South Indian (fixed-sign) diagram."""
    cells = []
    for slot in SOUTH_INDIAN_ORDER:
        if slot is None:
            cells.append({"kind": "blank"})
            continue
        if navamsa:
            occupants = [
                p for p in zodiac.PLANETS
                if chart.planets[p].navamsa_sign == slot
            ]
            lagna = slot == zodiac.navamsa_sign(chart.ascendant)
        else:
            occupants = [p for p in zodiac.PLANETS if chart.planets[p].sign == slot]
            lagna = slot == chart.lagna_sign
        cells.append({
            "kind": "sign",
            "sign": slot,
            "glyph": zodiac.SIGN_GLYPHS[zodiac.SIGNS.index(slot)],
            "lagna": lagna,
            "planets": [
                {
                    "planet": p,
                    "glyph": zodiac.PLANET_GLYPHS[p],
                    "degree": round(chart.planets[p].degree_in_sign, 2),
                    "retrograde": chart.planets[p].retrograde,
                }
                for p in occupants
            ],
        })
    return cells


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request, "index.html",
        {"version": __version__, "presets": PRESETS},
    )


@app.post("/api/chart")
def api_chart(req: ChartRequest):
    try:
        return JSONResponse(_payload(req))
    except Exception as exc:  # surfaced to the client with a readable message
        raise HTTPException(status_code=400, detail=f"{type(exc).__name__}: {exc}") from exc


@app.get("/api/health")
def health():
    import astronomy

    return {
        "status": "ok",
        "engine": __version__,
        "ephemeris": "astronomy-engine",
        "ephemeris_version": getattr(astronomy, "__version__", "unknown"),
        "ayanamsas": ["lahiri", "raman_397"],
        "house_systems": ["whole_sign", "sripati", "equal"],
    }
