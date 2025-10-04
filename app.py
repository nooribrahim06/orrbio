from flask import Flask, render_template, request
import math
from decimal import Decimal
from skyfield.api import Loader, EarthSatellite
from datetime import datetime, timezone
from flask import render_template, request
from tle_utils import tle_to_state_km
from datetime import datetime, timezone


app = Flask(__name__)


def distance(a, b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2) ** 0.5

def risk_level(min_dist_km: float) -> str:
    if min_dist_km < 1:   return "🚨 High"
    if min_dist_km < 5:   return "⚠️ Medium"
    return "✅ Low"



load = Loader('./skycache')
ts = load.timescale()


EXPERIMENT_LIBRARY = {
  "Pharma": {
    "Protein Crystallization": {
      "earth_months": 36,
      "leo_months_saved": 12,
      "annual_market_impact": 120_000_000,
      "success_prob": 0.72
    },
    "Vaccine Development": {
      "earth_months": 30,
      "leo_months_saved": 10,
      "annual_market_impact": 80_000_000,
      "success_prob": 0.68
    }
  },
  "Materials": {
    "Alloy Stress Testing": {
      "earth_months": 24,
      "leo_months_saved": 6,
      "annual_market_impact": 15_000_000,
      "success_prob": 0.62
    },
    "ZBLAN Fiber Manufacturing": {
      "earth_months": 20,
      "leo_months_saved": 8,
      "annual_market_impact": 100_000_000,
      "success_prob": 0.70
    }
  },
  "Biotech": {
    "Protein Structure Analysis": {
      "earth_months": 30,
      "leo_months_saved": 12,
      "annual_market_impact": 50_000_000,
      "success_prob": 0.66
    },
    "Stem Cell Growth": {
      "earth_months": 48,
      "leo_months_saved": 15,
      "annual_market_impact": 70_000_000,
      "success_prob": 0.64
    }
  },
  "Electronics": {
    "Semiconductor Radiation Test": {
      "earth_months": 18,
      "leo_months_saved": 8,
      "annual_market_impact": 30_000_000,
      "success_prob": 0.60
    },
    "Quantum Sensor Calibration": {
      "earth_months": 36,
      "leo_months_saved": 12,
      "annual_market_impact": 60_000_000,
      "success_prob": 0.58
    }
  },
  "Climate": {
    "Remote Sensing Instruments": {
      "earth_months": 24,
      "leo_months_saved": 10,
      "annual_market_impact": 40_000_000,
      "success_prob": 0.65
    }
  },
  "Agriculture": {
    "Plant Growth Studies": {
      "earth_months": 30,
      "leo_months_saved": 12,
      "annual_market_impact": 25_000_000,
      "success_prob": 0.63
    }
  },
  "Medical Tech": {
    "Tissue Engineering": {
      "earth_months": 48,
      "leo_months_saved": 18,
      "annual_market_impact": 200_000_000,
      "success_prob": 0.67
    }
  }
}

# Scenario multipliers (Low / Medium / High)
SCENARIOS = {
    0: {"label": "Low",    "mult": Decimal("0.6")},
    1: {"label": "Medium", "mult": Decimal("1.0")},
    2: {"label": "High",   "mult": Decimal("1.4")}
}

def tle_to_state_vectors(tle1: str, tle2: str):
    sat = EarthSatellite(tle1.strip(), tle2.strip(), "obj", ts)
    t = ts.from_datetime(datetime.utcnow().replace(tzinfo=timezone.utc))
    g = sat.at(t)
    x, y, z = g.position.km          # km
    vx, vy, vz = g.velocity.km_per_s # km/s
    return x, y, z, vx, vy, vz

# -------- Scenario-aware probabilities --------
def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))

def scenario_probabilities(base_p: float, investment_usd: float):
    """
    base_p: experiment['success_prob'] in [0,1]
    investment_usd: user-entered investment in $
    Returns probabilities for Low/Medium/High in [0,1]
    """
    p = clamp01(float(base_p))
    # Investment boost: up to +10 pts at $5M+ (tunable)
    invest_boost = min(investment_usd / 5_000_000.0, 0.10)

    # Spread depends on base probability (tighter if strong base)
    if p >= 0.75:
        d_low, d_high = 0.08, 0.05
    elif p >= 0.55:
        d_low, d_high = 0.12, 0.10
    elif p >= 0.35:
        d_low, d_high = 0.15, 0.12
    else:
        d_low, d_high = 0.10, 0.18

    p_low  = clamp01(p - d_low  + 0.30 * invest_boost)
    p_med  = clamp01(p + 0.60 * invest_boost)
    p_high = clamp01(p + d_high + 1.00 * invest_boost)

    return {"Low": p_low, "Medium": p_med, "High": p_high}

# -------- Core computation (with ROI multiple) --------
def compute_roi(experiment: dict, investment: float, scenario_index: int = 1):
    if not experiment:
        return None

    annual_market_impact = Decimal(experiment["annual_market_impact"])
    leo_months_saved = Decimal(experiment["leo_months_saved"])
    base_success_prob = float(experiment["success_prob"])

    monthly_value = annual_market_impact / Decimal(12)
    base_benefit = leo_months_saved * monthly_value

    scenario = SCENARIOS.get(scenario_index, SCENARIOS[1])
    scenario_benefit = scenario["mult"] * base_benefit
    inv = Decimal(investment)
    profit = scenario_benefit - inv

    if inv > 0:
        roi_percent = (profit / inv) * Decimal(100)
        roi_multiple = (profit / inv) + Decimal(1)
    else:
        roi_percent = Decimal(0)
        roi_multiple = None

    probs = scenario_probabilities(base_success_prob, float(investment))
    scen_label = scenario["label"]
    scen_prob_pct = probs.get(scen_label, probs["Medium"]) * 100.0

    return {
        "scenario_label": scen_label,
        "benefit": float(scenario_benefit),
        "profit": float(profit),
        "roi_percent": float(roi_percent),
        "roi_multiple": float(roi_multiple) if roi_multiple is not None else None,
        "success_prob_percent": float(scen_prob_pct),
        "monthly_value": float(monthly_value),
        "base_benefit": float(base_benefit),
        "all_probs_percent": {k: v * 100.0 for k, v in probs.items()}
    }


def clamp(v, lo, hi):
    try:
        v = float(v)
    except (TypeError, ValueError):
        v = 0.0
    return max(lo, min(hi, v))

def getf(form, key, default=0.0):
    v = form.get(key, None)
    if v in (None, "", "None"):
        return float(default)
    try:
        return float(v)
    except ValueError:
        return float(default)

def total_cost(slot_cost, monthly_ops, ops_months, service_fees):
    return (slot_cost or 0) + (monthly_ops or 0) * (ops_months or 0) + (service_fees or 0)

def benefit_pharma(months_saved, value_per_month, asset_value, improvement_pct, tech_prob_pct):
    v_time = (months_saved or 0) * (value_per_month or 0)
    uplift  = (asset_value or 0) * ((improvement_pct or 0) / 100.0)
    tech_p  = clamp((tech_prob_pct or 0) / 100.0, 0.0, 1.0)
    return (v_time + uplift) * tech_p

def benefit_research(grant_prob_pct, grant_value, pub_value, students_value):
    p = clamp((grant_prob_pct or 0) / 100.0, 0.0, 1.0)
    return p * (grant_value or 0) + (pub_value or 0) + (students_value or 0)

def benefit_mfg(margin_per_unit, improvement_pct, units, adoption_prob_pct):
    uplift_per_unit = (margin_per_unit or 0) * ((improvement_pct or 0) / 100.0)
    adopt = clamp((adoption_prob_pct or 0) / 100.0, 0.0, 1.0)
    return uplift_per_unit * (units or 0) * adopt

def roi(benefit, cost):
    if not cost:
        return float("inf")
    return (benefit - cost) / cost

def scenarios(benefit, cost, spread_pct):
    # costs vary less than benefits
    s = clamp(spread_pct / 100.0, 0.0, 0.95)
    low  = {"benefit": benefit * (1 - s), "cost": cost * (1 + 0.4 * s)}
    base = {"benefit": benefit,           "cost": cost}
    high = {"benefit": benefit * (1 + s), "cost": cost * (1 - 0.2 * s)}
    for d in (low, base, high):
        d["roi"] = roi(d["benefit"], d["cost"])
    return {"low": low, "base": base, "high": high}

# (You had these extras; keeping them in case you use elsewhere)
def distance(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def risk_level(d):
    if d < 1:
        return "⚠ Very High Risk (Collision Likely)"
    elif d < 10:
        return "Medium Risk (Close Approach)"
    else:
        return "Safe Distance"

# simple formatters for template (avoid Jinja lambdas)
def fmt_usd(v): return "${:,.0f}".format(v or 0)
def fmt_pct(v): return "{:,.1f}%".format((v or 0) * 100)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/safety", methods=["GET","POST"])
def safety():
    result = None
    sat_derived = None
    deb_derived = None
    sat_tle_error = None
    deb_tle_error = None

    if request.method == "POST":
        # ---------- Satellite: prefer TLE if present ----------
        sat_tle = (request.form.get("sat_tle") or "").strip()
        if sat_tle:
            try:
                (sx, sy, sz), (svx, svy, svz) = tle_to_state_km(sat_tle, when=None)  # at TLE epoch
                sat_derived = {"position": (sx, sy, sz), "velocity": (svx, svy, svz)}
            except Exception as e:
                sat_tle_error = f"Satellite TLE error: {e}"
                sx = float(request.form["sat_x"])
                sy = float(request.form["sat_y"])
                sz = float(request.form["sat_z"])
                svx = float(request.form["sat_vx"])
                svy = float(request.form["sat_vy"])
                svz = float(request.form["sat_vz"])
        else:
            sx = float(request.form["sat_x"])
            sy = float(request.form["sat_y"])
            sz = float(request.form["sat_z"])
            svx = float(request.form["sat_vx"])
            svy = float(request.form["sat_vy"])
            svz = float(request.form["sat_vz"])

        # ---------- Debris: prefer TLE if present ----------
        deb_tle = (request.form.get("deb_tle") or "").strip()
        if deb_tle:
            try:
                (dx, dy, dz), (dvx, dvy, dvz) = tle_to_state_km(deb_tle, when=None)  # at TLE epoch
                deb_derived = {"position": (dx, dy, dz), "velocity": (dvx, dvy, dvz)}
            except Exception as e:
                deb_tle_error = f"Debris TLE error: {e}"
                dx = float(request.form["deb_x"])
                dy = float(request.form["deb_y"])
                dz = float(request.form["deb_z"])
                dvx = float(request.form["deb_vx"])
                dvy = float(request.form["deb_vy"])
                dvz = float(request.form["deb_vz"])
        else:
            dx = float(request.form["deb_x"])
            dy = float(request.form["deb_y"])
            dz = float(request.form["deb_z"])
            dvx = float(request.form["deb_vx"])
            dvy = float(request.form["deb_vy"])
            dvz = float(request.form["deb_vz"])

        satellite = {"position": [sx, sy, sz], "velocity": [svx, svy, svz]}
        debris    = {"position": [dx, dy, dz], "velocity": [dvx, dvy, dvz]}

        # ---------- Your original calculation (unchanged) ----------
        min_dist = float("inf")
        time_of_min = 0
        collision = False

        for t in range(0, 3600, 60):  # 1 hour, 60 s step
            sat_pos = [satellite["position"][i] + satellite["velocity"][i]*t for i in range(3)]
            deb_pos = [debris["position"][i] + debris["velocity"][i]*t for i in range(3)]
            dist = distance(sat_pos, deb_pos)

            if dist < min_dist:
                min_dist = dist
                time_of_min = t

            if dist < 1:
                collision = True
                break

        risk_percentage = round(max(0, (10 - min_dist) / 10 * 100), 2)

        result = {
            "min_dist": round(min_dist, 2),
            "time_of_min": time_of_min / 60,
            "risk": risk_level(min_dist),
            "risk_percentage": risk_percentage
        }

    return render_template("safety.html",
                           result=result,
                           sat_derived=sat_derived,
                           deb_derived=deb_derived,
                           sat_tle_error=sat_tle_error,
                           deb_tle_error=deb_tle_error)

@app.route('/investment', methods=["GET","POST"])
def investment():
    items = {
        "Loft Orbital (YAM / Longbow satellites)": {
            "Company": "Loft Orbital",
            "Description": "Provides satellite infrastructure as a service; hosts customer payloads on shared bus architectures (YAM satellites).",
            "Price": "Not publicly disclosed; subscription / in-orbit service model.",
            "Duration": "Multi-year missions (payload stays for the life of the satellite).",
            "Slot capacity / space": "Universal payload interface (Payload Hub) to host multiple sensors; modular system.",
            "Applications": "Earth observation, sensors, data tasks across industries.",
            "Short-term feasibility": "❌ Not supported — missions are multi-year only."
        },

        "Spire Space Services (LEMUR constellation)": {
            "Company": "Spire Global",
            "Description": "Operates the LEMUR nanosatellite fleet. Offers hosted payloads and data-as-a-service.",
            "Price": "Hosted payloads available from 1/3U to 4U (via SatSearch).",
            "Duration": "Mission-lifetime, typically 3–5 years.",
            "Slot capacity / space": "4U: 160×97×97 mm, ~30 W | 8U: 220×200×97 mm, ~60 W | 16U: 220×200×200 mm, ~120 W.",
            "Applications": "Sensors, RF, Earth observation instruments.",
            "Short-term feasibility": "❌ Not supported — contracts are annual or multi-year."
        },

        "Rogue Space Systems": {
            "Company": "Rogue Space Systems",
            "Description": "Developing spacecraft for on-orbit servicing; offers payload hosting options.",
            "Price": "Not publicly documented.",
            "Duration": "Mission-lifetime or negotiated per contract.",
            "Slot capacity / space": "Not publicly documented.",
            "Applications": "Sensors, cameras, experiments.",
            "Short-term feasibility": "⚠ Unclear — early-stage, not designed for very short experiments."
        },

        "Momentus Space (Vigoride transfer vehicle)": {
            "Company": "Momentus Space",
            "Description": "Provides orbital transfer vehicles that can also host payloads in transit.",
            "Price": "Not publicly disclosed (direct quote required).",
            "Duration": "Mission-dependent; payload hosted during transfer (weeks to months).",
            "Slot capacity / space": "Depends on vehicle configuration; modular mounting available.",
            "Applications": "Hosted experiments, sensors, small payloads in transit.",
            "Short-term feasibility": "✅ Yes — transfers can last weeks to a few months."
        },

        "Exolaunch": {
            "Company": "Exolaunch",
            "Description": "Provides rideshare deployment and hosted payloads on partner satellites.",
            "Price": "Variable by mission; not published publicly.",
            "Duration": "Payload remains for the host satellite’s mission (multi-year).",
            "Slot capacity / space": "Based on host satellite bus and payload interface.",
            "Applications": "Sensors, experiments, remote sensing, telecoms.",
            "Short-term feasibility": "❌ Not supported — payloads fly for full mission duration."
        },

        "Sidus Space (LizzieSat)": {
            "Company": "Sidus Space",
            "Description": "Operates the LizzieSat platform designed to host customer payloads.",
            "Price": "Not publicly disclosed.",
            "Duration": "Mission-lifetime (multi-year).",
            "Slot capacity / space": "Depends on satellite bus design.",
            "Applications": "Sensors, data collection, small experiments.",
            "Short-term feasibility": "❌ Not supported — multi-year operation."
        },

        "Intelsat (Hosted Payloads)": {
            "Company": "Intelsat",
            "Description": "GEO/LEO satellite operator; offers hosted payloads for instruments.",
            "Price": "High (million-dollar scale), negotiated case by case.",
            "Duration": "Host satellite lifetime (10–15 years for GEO).",
            "Slot capacity / space": "Varies by available capacity.",
            "Applications": "Communications, sensors, Earth observation, instruments.",
            "Short-term feasibility": "❌ Not supported — designed for very long-term commitments."
        },

        "Satellogic": {
            "Company": "Satellogic",
            "Description": "Earth observation constellation operator; offers data and hosted sensors.",
            "Price": "Not publicly disclosed.",
            "Duration": "Multi-year (life of each satellite).",
            "Slot capacity / space": "Depends on bus; not broadly public.",
            "Applications": "Imaging, sensors, data collection.",
            "Short-term feasibility": "❌ Not supported — service model is data subscription, not short hosting."
        }
    }
    return render_template('investment.html', items=items)

@app.route("/form", methods=["GET", "POST"])
def form():
    return render_template("form.html", active_page="form")

# If this file is run directly:
@app.route("/education")
def education():
    return render_template("education.html")

@app.route("/roi", methods=["GET", "POST"])
def roi():
    # ... keep your same logic ...
    result = None
    field = None
    experiment_name = None
    investment = None
    scenario_index = 1  # default Medium

    if request.method == "POST":
        field = request.form.get("field")
        experiment_name = request.form.get("experiment")
        investment_raw = request.form.get("investment", "0").replace(",", "").strip()
        scenario_index = int(request.form.get("scenario_index", 1))

        try:
            investment = float(investment_raw)
        except ValueError:
            investment = 0.0

        experiment = None
        if field in EXPERIMENT_LIBRARY and experiment_name in EXPERIMENT_LIBRARY[field]:
            experiment = EXPERIMENT_LIBRARY[field][experiment_name]

        if experiment:
            result = compute_roi(experiment, investment, scenario_index)
    return render_template(
        "roi.html",
        data=EXPERIMENT_LIBRARY,
        scenarios=SCENARIOS,
        result=result,
        chosen_field=field,
        chosen_experiment=experiment_name,
        investment=investment,
        scenario_index=scenario_index,
    )
@app.route("/game")
def game():
    return render_template("game.html")

@app.route("/adventure")
def adventure():
    return render_template("adventure.html")

@app.post("/api/convert-tle")
def api_convert_tle():
    # Works with either form-encoded or JSON bodies
    tle1 = (request.form.get("tle1") or (request.json or {}).get("tle1") or "").strip()
    tle2 = (request.form.get("tle2") or (request.json or {}).get("tle2") or "").strip()
    if not tle1 or not tle2:
        return jsonify({"ok": False, "error": "Missing TLE lines (tle1, tle2)."}), 400
    try:
        x, y, z, vx, vy, vz = tle_to_state_vectors(tle1, tle2)
        return jsonify({
            "ok": True,
            "x": round(x, 3), "y": round(y, 3), "z": round(z, 3),
            "vx": round(vx, 4), "vy": round(vy, 4), "vz": round(vz, 4)
        }), 200
    except Exception as e:
        # Always JSON, never HTML
        return jsonify({"ok": False, "error": f"{type(e).__name__}: {e}"}), 500

