"""Vimshottari (Udu) dasha.

SOURCE: chapter X.  The nine periods, their lengths, the rule that the
nakshatra of the Moon determines the ruling period at birth, and the
proportional division into bhuktis are all taken from that chapter.

The source gives a shortcut for sub-periods -- "multiply together the number
of years of the Dasa period of the planet by the number of years of the Dasa
period of the planet whose sub-period is desired.  Then cutting off the last
figure of the product, multiply it by 3 and keep that figure as days, the
other figures in the product will be months."  That is an exact statement of
the proportional rule (Saturn 19 x Mercury 17 = 323 -> 32 months 9 days, and
19*17/120 years is indeed 32 months 9 days), so this module computes the
proportional division directly rather than reproducing the arithmetic trick.

Years are taken as 365.25 days, the convention used by Indian ephemerides.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from . import zodiac

YEAR_DAYS = 365.25


def _add_years(dt: datetime, years: float) -> datetime:
    return dt + timedelta(days=years * YEAR_DAYS)


def _period(lord: str, start: datetime, years: float) -> dict:
    end = _add_years(start, years)
    return {
        "lord": lord,
        "years": years,
        "start": start.isoformat(timespec="seconds"),
        "end": end.isoformat(timespec="seconds"),
        "start_date": start.date().isoformat(),
        "end_date": end.date().isoformat(),
    }


def antardashas(maha_lord: str, start: datetime, maha_years: float) -> list[dict]:
    """Bhuktis inside a mahadasha, in the same cyclic order from its lord."""
    order = zodiac.VIMSHOTTARI_ORDER
    i = order.index(maha_lord)
    out = []
    cursor = start
    for k in range(9):
        sub = order[(i + k) % 9]
        years = maha_years * zodiac.VIMSHOTTARI_YEARS[sub] / zodiac.VIMSHOTTARI_TOTAL
        out.append(_period(sub, cursor, years))
        cursor = _add_years(cursor, years)
    return out


def vimshottari(
    moon_longitude: float,
    birth_utc: datetime,
    *,
    at: datetime | None = None,
    year_days: float = YEAR_DAYS,
    include_antardashas: bool = True,
) -> dict:
    """Full Vimshottari timeline from the Moon's sidereal longitude."""
    if at is None:
        at = datetime.now(timezone.utc).replace(tzinfo=None)
    if birth_utc.tzinfo is not None:
        birth_utc = birth_utc.astimezone(timezone.utc).replace(tzinfo=None)

    nak_index = zodiac.nakshatra_index(moon_longitude)
    lord = zodiac.NAKSHATRA_LORDS[nak_index]
    span = zodiac.NAKSHATRA_SPAN
    elapsed_fraction = (moon_longitude % span) / span
    lord_years = zodiac.VIMSHOTTARI_YEARS[lord]
    balance_years = lord_years * (1.0 - elapsed_fraction)

    # The current mahadasha began before birth, by the elapsed fraction.
    cursor = birth_utc - timedelta(days=elapsed_fraction * lord_years * year_days)

    order = zodiac.VIMSHOTTARI_ORDER
    i = order.index(lord)
    mahadashas = []
    for k in range(9):
        maha = order[(i + k) % 9]
        years = zodiac.VIMSHOTTARI_YEARS[maha]
        entry = _period(maha, cursor, years)
        if include_antardashas:
            entry["antardashas"] = antardashas(maha, cursor, years)
        mahadashas.append(entry)
        cursor = _add_years(cursor, years)

    def find_current():
        for maha in mahadashas:
            start = datetime.fromisoformat(maha["start"])
            end = datetime.fromisoformat(maha["end"])
            if start <= at < end:
                for sub in maha.get("antardashas", []):
                    s_start = datetime.fromisoformat(sub["start"])
                    s_end = datetime.fromisoformat(sub["end"])
                    if s_start <= at < s_end:
                        return {"mahadasha": maha, "antardasha": sub}
                return {"mahadasha": maha, "antardasha": None}
        return {"mahadasha": None, "antardasha": None}

    return {
        "system": "Vimshottari",
        "year_days": year_days,
        "janma_nakshatra": zodiac.NAKSHATRAS[nak_index],
        "janma_nakshatra_index": nak_index + 1,
        "janma_nakshatra_lord": lord,
        "elapsed_fraction": round(elapsed_fraction, 6),
        "balance_at_birth": {
            "lord": lord,
            "years": int(balance_years),
            "months": int((balance_years % 1) * 12),
            "days": int(((balance_years * 12) % 1) * 30),
            "decimal_years": round(balance_years, 6),
            "ends_on": _add_years(birth_utc, balance_years).date().isoformat(),
        },
        "mahadashas": mahadashas,
        "current": find_current(),
        "as_of": at.isoformat(timespec="seconds"),
    }
