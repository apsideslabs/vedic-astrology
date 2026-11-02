import json, sys, os
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from jyotish.chart import BirthData, build_chart
from jyotish import transits, interpret

b = BirthData(date="1935-11-02", time="05:20:00", latitude=13.0, longitude=77.5833333,
              tz_offset=5.1722222, place="Madras")
c = build_chart(b, ayanamsa="raman_397", house_system="whole_sign")
t = transits.analyse(c, datetime(2026, 11, 2, 0, 0, 0))
r = interpret.interpret(c, t)
out = {
 "ayanamsa": c.ayanamsa_value,
 "ascendant_tropical": c.ascendant_tropical,
 "lagna_sign": c.lagna_sign,
 "lagna_deg": c.ascendant % 30.0,
 "planets": {p.planet: {"longitude": round(p.longitude,4), "sign": p.sign, "house": p.house,
                        "dignity": p.dignity, "nakshatra": p.nakshatra, "pada": p.pada,
                        "navamsa": p.navamsa_sign, "retrograde": p.retrograde,
                        "score": p.strength["score"]} for p in c.planets.values()},
 "houses": [{"house": h["house"], "sign": h["sign"], "lord": h["lord"],
             "lord_house": h["lord_house"], "occupants": h["occupants"]} for h in c.houses],
 "dasha_balance": {k: c.vimshottari["balance_at_birth"][k] for k in
                   ("lord","years","months","days","decimal_years","ends_on")},
 "janma_nakshatra": c.vimshottari["janma_nakshatra"],
 "panchanga": {"vara": c.panchanga["vara"]["name"], "tithi": c.panchanga["tithi"]["name"],
               "paksha": c.panchanga["tithi"]["paksha"], "yoga": c.panchanga["yoga"]["name"],
               "karana": c.panchanga["karana"]["name"]},
 "yogas_present": sorted(y["name"] for y in c.yogas if y["present"]),
 "interpretation_sections": len(r["sections"]),
 "interpretation_statements": sum(len(s["statements"]) for s in r["sections"]),
 "aspects": len(c.aspects),
 "sade_sati": t["sade_sati"]["active"],
 "gochara": [[row["planet"], row["house_from_moon"], row["result"]] for row in t["gochara"]],
}
json.dump(out, open(os.path.join(os.path.dirname(__file__), "py_out.json"), "w"), indent=1)
print("python ok")
