# tle_utils.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple
from math import sin, cos, pi
from datetime import datetime, timezone
from sgp4.api import Satrec, jday

def _wrap_angle(x: float) -> float:
    twopi = 2.0 * pi
    x = x % twopi
    return x if x >= 0 else x + twopi

def _gmst_rad(jd_ut1: float) -> float:
    # IAU 1982 GMST approximation (good enough for our use)
    T = (jd_ut1 - 2451545.0) / 36525.0
    gmst_sec = (67310.54841
                + (876600.0 * 3600 + 8640184.812866) * T
                + 0.093104 * T**2
                - 6.2e-6 * T**3)
    return _wrap_angle((gmst_sec % 86400.0) * (2.0 * pi / 86400.0))

def _R3(theta: float):
    c, s = cos(theta), sin(theta)
    return (( c,  s, 0.0),
            (-s,  c, 0.0),
            (0.0, 0.0, 1.0))

def _matvec3(M, v):
    return (
        M[0][0]*v[0] + M[0][1]*v[1] + M[0][2]*v[2],
        M[1][0]*v[0] + M[1][1]*v[1] + M[1][2]*v[2],
        M[2][0]*v[0] + M[2][1]*v[1] + M[2][2]*v[2],
    )

@dataclass
class TLEParseResult:
    name: Optional[str]
    line1: str
    line2: str

def parse_tle_block(text: str) -> TLEParseResult:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if len(lines) < 2:
        raise ValueError("TLE must contain at least 2 non-empty lines.")
    if len(lines) >= 3 and not lines[0].startswith(("1 ", "2 ")):
        name, l1, l2 = lines[0], lines[1], lines[2]
    else:
        name, l1, l2 = None, lines[0], lines[1]
    if not (l1.startswith("1 ") and l2.startswith("2 ")):
        l1 = next((x for x in lines if x.startswith("1 ")), None)
        l2 = next((x for x in lines if x.startswith("2 ")), None)
        if not l1 or not l2:
            raise ValueError("Could not find proper TLE Line 1 / Line 2.")
    return TLEParseResult(name=name, line1=l1, line2=l2)

def tle_to_state_km(tle_text: str, when: Optional[datetime] = None) -> Tuple[Tuple[float,float,float], Tuple[float,float,float]]:
    """
    Convert TLE to ECI-like (x,y,z) km and (vx,vy,vz) km/s.
    - Propagates with SGP4 in TEME frame.
    - Rotate TEME->ECI using GMST about Z (sufficient for your distance calc).
    - By default, evaluate at the TLE epoch (deterministic). Pass 'when' (UTC) to override.
    """
    parsed = parse_tle_block(tle_text)
    sat = Satrec.twoline2rv(parsed.line1, parsed.line2)

    if when is None:
        jd = sat.jdsatepoch + sat.jdsatepochF
        jd_int = int(jd)
        jd_frac = jd - jd_int
        e, r_teme_km, v_teme_km_s = sat.sgp4(jd_int, jd_frac)
        gmst = _gmst_rad(jd)
    else:
        if when.tzinfo is None:
            when = when.replace(tzinfo=timezone.utc)
        when = when.astimezone(timezone.utc)
        jd, fr = jday(when.year, when.month, when.day, when.hour, when.minute, when.second + when.microsecond/1e6)
        e, r_teme_km, v_teme_km_s = sat.sgp4(jd, fr)
        gmst = _gmst_rad(jd + fr)

    if e != 0:
        raise ValueError(f"SGP4 propagation error code: {e}")

    R = _R3(gmst)
    r_eci = _matvec3(R, r_teme_km)
    v_eci = _matvec3(R, v_teme_km_s)
    return r_eci, v_eci
