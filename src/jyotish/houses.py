"""House systems.

Three systems are provided:

``whole_sign`` (default)
    The Rasi chakra of the source: the rising sign is the first bhava and each
    following sign is the next bhava, 30 degrees each.  Chapter II of the
    source says plainly that "for ordinary purposes of prediction a zodiacal
    diagram (Rasi Chakra) with the Ascendant marked is sufficient".

``sripati``
    Porphyry cusps derived from the MC and the Ascendant, which is the
    structure Raman's *Nirayana Tables of Houses* tabulate as bhava madhyas
    (chapter II, Appendix II).

``equal``
    Equal 30 degree bhavas measured from the exact Ascendant degree.
"""

from __future__ import annotations

from . import ephemeris

HOUSE_SYSTEMS = ("whole_sign", "sripati", "equal")


def cusps(system: str, lst_deg: float, latitude: float, eps_deg: float) -> dict[int, float]:
    """Tropical longitudes of the twelve house cusps (house 1 = Ascendant).

    For ``whole_sign`` the cusps are the boundaries of the rising sign.
    """
    if system not in HOUSE_SYSTEMS:
        raise ValueError(f"unknown house system {system!r}; choose from {HOUSE_SYSTEMS}")

    asc = ephemeris.ascendant(lst_deg, latitude, eps_deg)
    mc = ephemeris.midheaven(lst_deg, eps_deg)
    ic = (mc + 180.0) % 360.0
    desc = (asc + 180.0) % 360.0

    if system == "whole_sign":
        start = (asc // 30.0) * 30.0
        return {h: (start + 30.0 * (h - 1)) % 360.0 for h in range(1, 13)}

    if system == "equal":
        return {h: (asc + 30.0 * (h - 1)) % 360.0 for h in range(1, 13)}

    # sripati / porphyry: trisect each quadrant between the angles
    def arc(a: float, b: float) -> float:
        return (b - a) % 360.0

    q1 = arc(mc, asc)      # 10th -> 1st
    q2 = arc(asc, ic)      # 1st -> 4th
    c = {10: mc, 1: asc, 4: ic, 7: desc}
    c[11] = (mc + q1 / 3.0) % 360.0
    c[12] = (mc + 2.0 * q1 / 3.0) % 360.0
    c[2] = (asc + q2 / 3.0) % 360.0
    c[3] = (asc + 2.0 * q2 / 3.0) % 360.0
    c[5] = (c[4] + arc(ic, desc) / 3.0) % 360.0
    c[6] = (c[4] + 2.0 * arc(ic, desc) / 3.0) % 360.0
    c[8] = (desc + arc(desc, mc) / 3.0) % 360.0
    c[9] = (desc + 2.0 * arc(desc, mc) / 3.0) % 360.0
    return c


def house_of_longitude(longitude: float, cusp_map: dict[int, float]) -> int:
    """Which bhava a longitude falls in, given cusp longitudes."""
    for h in range(1, 13):
        start = cusp_map[h]
        end = cusp_map[(h % 12) + 1]
        span = (end - start) % 360.0
        if (longitude - start) % 360.0 < span:
            return h
    return 1
