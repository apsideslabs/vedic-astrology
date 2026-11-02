"""Command-line interface.

    python -m jyotish.cli --date 1935-11-02 --time 05:20 --lat 13.0 --lon 77.58 \\
        --tz 5.5 --place Madras

    python -m jyotish.cli --date 1990-04-14 --time 08:15 --lat 13.08 --lon 80.27 \\
        --tz 5.5 --json
"""

from __future__ import annotations

import argparse
import json

from . import interpret as interpret_mod
from . import transits as transits_mod
from . import zodiac
from .chart import BirthData, build_chart


def render_text(chart) -> str:
    lines = []
    b = chart.birth
    lines.append("=" * 72)
    lines.append(f"  {b.name or 'Chart'}  {b.date} {b.time} (UT{b.tz_offset:+g})  {b.place}")
    lines.append(f"  Lat {b.latitude:+.4f}  Lon {b.longitude:+.4f}   "
                 f"Ayanamsa {chart.ayanamsa_model} {zodiac.dms(chart.ayanamsa_value)}")
    lines.append("=" * 72)

    asc = chart.ascendant
    lines.append(f"Lagna (Ascendant): {zodiac.sign_of(asc)} {zodiac.dms(asc % 30)}  "
                 f"[{zodiac.nakshatra_name(asc)} pada {zodiac.nakshatra_pada(asc)}]")
    lines.append(f"Janma Rasi (Moon): {chart.moon_sign()}   "
                 f"Nakshatra: {chart.vimshottari['janma_nakshatra']} "
                 f"(lord {chart.vimshottari['janma_nakshatra_lord']})")
    pn = chart.panchanga
    lines.append(f"Panchanga: {pn['vara']['name']}, {pn['tithi']['paksha']} "
                 f"{pn['tithi']['name']}, {pn['yoga']['name']} yoga, {pn['karana']['name']} karana")
    lines.append("")

    header = f"{'Graha':<9}{'Sign':<13}{'Deg':>9} {'Nakshatra':<18}{'Pd':>3} {'Hs':>3}  {'Dignity':<15}{'Navamsa':<12}{'R'}"
    lines.append(header)
    lines.append("-" * len(header))
    for planet in zodiac.PLANETS:
        p = chart.planets[planet]
        lines.append(
            f"{planet:<9}{p.sign:<13}{zodiac.dms(p.degree_in_sign):>9} "
            f"{p.nakshatra:<18}{p.pada:>3} {p.house:>3}  {p.dignity:<15}{p.navamsa_sign:<12}"
            f"{'R' if p.retrograde else ''}"
        )
    lines.append("")

    lines.append("Houses")
    for h in chart.houses:
        occ = ", ".join(h["occupants"]) or "-"
        lines.append(f"  {h['house']:>2}. {h['sign']:<12} lord {h['lord']:<9} "
                     f"(lord in {h['lord_house']})  {occ}")
    lines.append("")

    v = chart.vimshottari
    bal = v["balance_at_birth"]
    lines.append(f"Vimshottari: balance of {bal['lord']} at birth "
                 f"{bal['years']}y {bal['months']}m {bal['days']}d")
    for maha in v["mahadashas"]:
        lines.append(f"  {maha['lord']:<9} {maha['start_date']} -> {maha['end_date']}")
    cur = v["current"]
    if cur.get("mahadasha"):
        lines.append(f"  Now: {cur['mahadasha']['lord']}"
                     + (f" / {cur['antardasha']['lord']}" if cur.get("antardasha") else ""))
    lines.append("")

    present = [y for y in chart.yogas if y["present"]]
    lines.append("Yogas: " + (", ".join(y["name"] for y in present) if present else "none detected"))
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Cast a Vedic (Nirayana) chart.")
    ap.add_argument("--date", required=True, help="local civil date, YYYY-MM-DD")
    ap.add_argument("--time", required=True, help="local civil time, HH:MM[:SS]")
    ap.add_argument("--lat", type=float, required=True, help="latitude, north positive")
    ap.add_argument("--lon", type=float, required=True, help="longitude, east positive")
    ap.add_argument("--tz", type=float, default=5.5, help="UT offset in hours (default 5.5)")
    ap.add_argument("--place", default="", help="place name")
    ap.add_argument("--name", default="", help="native's name")
    ap.add_argument("--ayanamsa", default="lahiri", choices=["lahiri", "raman_397"])
    ap.add_argument("--houses", default="whole_sign",
                    choices=["whole_sign", "sripati", "equal"])
    ap.add_argument("--json", action="store_true", help="emit the full JSON payload")
    ap.add_argument("--no-transits", action="store_true", help="skip transit analysis")
    args = ap.parse_args(argv)

    birth = BirthData(
        date=args.date, time=args.time, latitude=args.lat, longitude=args.lon,
        tz_offset=args.tz, place=args.place, name=args.name,
    )
    chart = build_chart(birth, ayanamsa=args.ayanamsa, house_system=args.houses)
    transit = None if args.no_transits else transits_mod.analyse(chart)

    if args.json:
        payload = chart.as_dict()
        payload["transits"] = transit
        payload["interpretation"] = interpret_mod.interpret(chart, transit)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    print(render_text(chart))
    if transit:
        print()
        print(f"Gochara from Janma Rasi {transit['janma_rasi']} (as of {transit['as_of']} UTC)")
        for row in transit["gochara"]:
            result = row["result"] or "-- not legible in the source scan --"
            flag = "  [SADE SATI]" if row["sade_sati"] else ""
            print(f"  {row['planet']:<9} {row['sign']:<12} {row['house_from_moon']:>2}  {result}{flag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
