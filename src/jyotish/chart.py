"""The chart: birth data in, a fully computed Rasi/Navamsa chart out."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta

from . import ayanamsa as ayanamsa_mod
from . import dasha as dasha_mod
from . import ephemeris, houses, panchanga, strength, zodiac
from . import yogas as yogas_mod


@dataclass
class BirthData:
    """Everything needed to cast a chart."""

    date: str                 # "YYYY-MM-DD", local civil date
    time: str                 # "HH:MM" or "HH:MM:SS", local civil time
    latitude: float           # degrees, north positive
    longitude: float          # degrees, east positive
    tz_offset: float = 5.5    # hours ahead of UT
    place: str = ""
    name: str = ""

    def local_datetime(self) -> datetime:
        parts = [int(p) for p in self.time.split(":")]
        while len(parts) < 3:
            parts.append(0)
        y, m, d = (int(p) for p in self.date.split("-"))
        return datetime(y, m, d, parts[0], parts[1], parts[2])

    def utc_datetime(self) -> datetime:
        return self.local_datetime() - timedelta(hours=self.tz_offset)


@dataclass
class PlanetPosition:
    planet: str
    longitude: float          # sidereal, degrees 0-360
    tropical_longitude: float
    latitude: float
    speed: float
    retrograde: bool
    sign: str
    sign_index: int
    degree_in_sign: float
    nakshatra: str
    nakshatra_index: int
    pada: int
    nakshatra_lord: str
    navamsa_sign: str
    house: int
    dignity: str
    combust: bool
    strength: dict

    def as_dict(self) -> dict:
        d = dict(self.__dict__)
        d["longitude_dms"] = zodiac.dms(self.longitude)
        d["degree_in_sign_dms"] = zodiac.dms(self.degree_in_sign)
        d["sign_glyph"] = zodiac.SIGN_GLYPHS[self.sign_index]
        d["planet_glyph"] = zodiac.PLANET_GLYPHS.get(self.planet, "")
        return d


@dataclass
class Chart:
    birth: BirthData
    jd: float
    ayanamsa_model: str
    ayanamsa_value: float
    house_system: str
    ascendant: float          # sidereal
    ascendant_tropical: float
    mc_tropical: float
    cusps_tropical: dict
    lagna_sign: str
    planets: dict[str, PlanetPosition]
    houses: list
    panchanga: dict
    vimshottari: dict
    yogas: list
    aspects: list
    meta: dict = field(default_factory=dict)

    # -- convenience -------------------------------------------------------
    def sign_map(self) -> dict[str, str]:
        return {p: pos.sign for p, pos in self.planets.items()}

    def planets_in_house(self, house: int) -> list[str]:
        return [p for p, pos in self.planets.items() if pos.house == house]

    def planets_in_sign(self, sign: str) -> list[str]:
        return [p for p, pos in self.planets.items() if pos.sign == sign]

    def house_lord(self, house: int) -> str:
        sign = self.houses[house - 1]["sign"]
        return zodiac.SIGN_LORDS[zodiac.SIGNS.index(sign)]

    def lord_of_sign(self, sign: str) -> str:
        return zodiac.SIGN_LORDS[zodiac.SIGNS.index(sign)]

    def moon_sign(self) -> str:
        return self.planets["Moon"].sign

    def aspected_houses(self, planet: str) -> list[dict]:
        """Houses a planet throws its sight on, with the fraction of sight.

        SOURCE: chapter I, "Drishti or Aspect" -- the 7th is a full sight, the
        3rd and 10th a quarter, the 5th and 9th a half, the 4th and 8th three
        quarters; Mars adds 4 and 8, Jupiter 5 and 9, Saturn 3 and 10.
        """
        sign = self.planets[planet].sign
        out = []
        for distance in zodiac.SPECIAL_ASPECTS.get(planet, zodiac.DEFAULT_ASPECTS):
            target = zodiac.SIGNS[(zodiac.SIGNS.index(sign) + distance - 1) % 12]
            out.append({
                "house": distance,
                "sign": target,
                "sight": 1.0 if distance == 7 else zodiac.PARTIAL_SIGHT.get(distance, 1.0),
                "special": distance in zodiac.SPECIAL_ASPECTS.get(planet, ()),
            })
        return out

    def as_dict(self) -> dict:
        return {
            "birth": {
                "name": self.birth.name,
                "place": self.birth.place,
                "local": self.birth.local_datetime().isoformat(),
                "tz_offset": self.birth.tz_offset,
                "utc": self.birth.utc_datetime().isoformat() + "Z",
                "jd_ut": round(self.jd, 6),
                "latitude": self.birth.latitude,
                "longitude": self.birth.longitude,
            },
            "ayanamsa": {
                "model": self.ayanamsa_model,
                "value": round(self.ayanamsa_value, 6),
                "dms": zodiac.dms(self.ayanamsa_value),
            },
            "house_system": self.house_system,
            "lagna": {
                "longitude": round(self.ascendant, 6),
                "dms": zodiac.dms(self.ascendant),
                "sign": self.lagna_sign,
                "sign_index": zodiac.SIGNS.index(self.lagna_sign),
                "degree_in_sign": round(self.ascendant % 30.0, 6),
                "nakshatra": zodiac.nakshatra_name(self.ascendant),
                "pada": zodiac.nakshatra_pada(self.ascendant),
                "lord": self.lord_of_sign(self.lagna_sign),
                "navamsa_sign": zodiac.navamsa_sign(self.ascendant),
                "moon_sign": self.moon_sign(),
            },
            "planets": [p.as_dict() for p in self.planets.values()],
            "houses": self.houses,
            "panchanga": self.panchanga,
            "vimshottari": self.vimshottari,
            "yogas": self.yogas,
            "aspects": self.aspects,
            "aspects_by_house": {
                p: self.aspected_houses(p) for p in zodiac.PLANETS
            },
            "meta": self.meta,
        }


# --------------------------------------------------------------------------
# Aspect computation (sign based) -- SOURCE: chapter I, "Drishti or Aspect"
# --------------------------------------------------------------------------
def _compute_aspects(signs: dict[str, str]) -> list[dict]:
    out = []
    for a in zodiac.PLANETS:
        if a not in signs:
            continue
        allowed = zodiac.SPECIAL_ASPECTS.get(a, zodiac.DEFAULT_ASPECTS)
        for b in zodiac.PLANETS:
            if a == b or b not in signs:
                continue
            distance = zodiac.house_from(signs[a], signs[b])
            if distance in allowed:
                full = distance in zodiac.DEFAULT_ASPECTS or distance in zodiac.SPECIAL_ASPECTS.get(a, ())
                out.append({
                    "from": a,
                    "to": b,
                    "house_distance": distance,
                    "kind": "special" if distance != 7 and distance in zodiac.SPECIAL_ASPECTS.get(a, ()) else "full",
                    "sight": zodiac.PARTIAL_SIGHT.get(distance, 1.0) if full else 0.0,
                    "benefic": a in zodiac.NATURAL_BENEFICS,
                })
    return out


def build_chart(
    birth: BirthData,
    *,
    ayanamsa: str = "lahiri",
    house_system: str = "whole_sign",
) -> Chart:
    """Cast a chart.  This is the single entry point for the whole engine."""
    dt_utc = birth.utc_datetime()
    jd = ephemeris.julian_day(dt_utc)

    ay = ayanamsa_mod.value(ayanamsa, jd)
    tropical = ephemeris.tropical_longitudes(jd)

    eps = ephemeris.obliquity(jd)
    lst = ephemeris.local_sidereal_degrees(jd, birth.longitude)
    asc_trop = ephemeris.ascendant(lst, birth.latitude, eps)
    mc_trop = ephemeris.midheaven(lst, eps)
    cusp_map = houses.cusps(house_system, lst, birth.latitude, eps)

    asc = (asc_trop - ay) % 360.0
    lagna_sign = zodiac.sign_of(asc)
    cusps_sidereal = {h: (v - ay) % 360.0 for h, v in cusp_map.items()}

    signs = {p: zodiac.sign_of((v["longitude"] - ay) % 360.0) for p, v in tropical.items()}
    sun_lon = (tropical["Sun"]["longitude"] - ay) % 360.0

    positions: dict[str, PlanetPosition] = {}
    for planet in zodiac.PLANETS:
        data = tropical[planet]
        sid = (data["longitude"] - ay) % 360.0
        retro = data["speed"] < 0
        house = zodiac.house_from(lagna_sign, zodiac.sign_of(sid))
        nav = zodiac.navamsa_sign(sid)
        combust = strength.is_combust(planet, sid, sun_lon, retro)
        st = strength.positional_strength(
            planet, sid, house, signs=signs, retrograde=retro,
            combust=combust, navamsa_sign=nav,
        )
        positions[planet] = PlanetPosition(
            planet=planet,
            longitude=sid,
            tropical_longitude=data["longitude"],
            latitude=data["latitude"],
            speed=round(data["speed"], 5),
            retrograde=retro,
            sign=zodiac.sign_of(sid),
            sign_index=zodiac.sign_index(sid),
            degree_in_sign=zodiac.degree_in_sign(sid),
            nakshatra=zodiac.nakshatra_name(sid),
            nakshatra_index=zodiac.nakshatra_index(sid),
            pada=zodiac.nakshatra_pada(sid),
            nakshatra_lord=zodiac.nakshatra_lord(sid),
            navamsa_sign=nav,
            house=house,
            dignity=st["dignity"],
            combust=combust,
            strength=st,
        )

    house_rows = []
    for h in range(1, 13):
        sign = zodiac.sign_of(cusps_sidereal[h]) if house_system != "whole_sign" else zodiac.SIGNS[(zodiac.SIGNS.index(lagna_sign) + h - 1) % 12]
        occupants = [p for p, pos in positions.items() if pos.house == h]
        house_rows.append({
            "house": h,
            "sign": sign,
            "sign_index": zodiac.SIGNS.index(sign),
            "lord": zodiac.SIGN_LORDS[zodiac.SIGNS.index(sign)],
            "lord_house": positions[zodiac.SIGN_LORDS[zodiac.SIGNS.index(sign)]].house,
            "cusp_tropical": round(cusp_map[h], 4),
            "cusp_sidereal": round(cusps_sidereal[h], 4),
            "occupants": occupants,
            "kind": zodiac.HOUSE_KIND[h],
            "significations": zodiac.HOUSE_SIGNIFICATIONS[h],
        })

    aspects = _compute_aspects(signs)

    chart = Chart(
        birth=birth,
        jd=jd,
        ayanamsa_model=ayanamsa,
        ayanamsa_value=ay,
        house_system=house_system,
        ascendant=asc,
        ascendant_tropical=asc_trop,
        mc_tropical=mc_trop,
        cusps_tropical=cusp_map,
        lagna_sign=lagna_sign,
        planets=positions,
        houses=house_rows,
        panchanga=panchanga.compute(birth.local_datetime(), positions["Sun"].longitude, positions["Moon"].longitude),
        vimshottari=dasha_mod.vimshottari(positions["Moon"].longitude, dt_utc),
        yogas=[],
        aspects=aspects,
        meta={
            "engine": "jyotish",
            "ephemeris": "astronomy-engine",
            "node": "mean",
            "note": "Strength figures are a simplified positional score, not Shadbala.",
        },
    )
    chart.yogas = yogas_mod.detect(chart)
    return chart
