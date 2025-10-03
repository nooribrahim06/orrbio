from flask import Flask, render_template, request
import math

app = Flask(__name__)

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
    if request.method == "POST":
        # Satellite data
        sat_x = float(request.form["sat_x"])
        sat_y = float(request.form["sat_y"])
        sat_z = float(request.form["sat_z"])
        sat_vx = float(request.form["sat_vx"])
        sat_vy = float(request.form["sat_vy"])
        sat_vz = float(request.form["sat_vz"])

        # Debris data
        deb_x = float(request.form["deb_x"])
        deb_y = float(request.form["deb_y"])
        deb_z = float(request.form["deb_z"])
        deb_vx = float(request.form["deb_vx"])
        deb_vy = float(request.form["deb_vy"])
        deb_vz = float(request.form["deb_vz"])

        satellite = {"position": [sat_x, sat_y, sat_z], "velocity": [sat_vx, sat_vy, sat_vz]}
        debris = {"position": [deb_x, deb_y, deb_z], "velocity": [deb_vx, deb_vy, deb_vz]}

        min_dist = float("inf")
        time_of_min = 0
        collision = False

        # Simulate one hour (3600s) with 60s step
        for t in range(0, 3600, 60):
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

    return render_template("safety.html", result=result)

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
    ctx = {
        "category": "pharma",
        # shared costs defaults
        "slotCost": 2_000_000,
        "monthlyOps": 50_000,
        "opsMonths": 6,
        "serviceFees": 150_000,
        # pharma defaults
        "ph_monthsSaved": 6,
        "ph_valuePerMonth": 8_000_000,
        "ph_assetValue": 120_000_000,
        "ph_improvementPct": 3,
        "ph_techProb": 70,
        # research defaults
        "re_grantProb": 40,
        "re_grantValue": 300_000,
        "re_pubValue": 30_000,
        "re_studentsValue": 200_000,
        # manufacturers defaults
        "mf_marginPerUnit": 50,
        "mf_improvementPct": 120,
        "mf_units": 200_000,
        "mf_adoptionProb": 35,
        # scenario
        "scenarioSpread": 25,
        # results
        "sc": None,
        "total_cost_fmt": None,
        "expected_benefit_fmt": None,
    }

    if request.method == "POST":
        category = request.form.get("category", "pharma")
        ctx["category"] = category

        # common costs
        slot_cost   = ctx["slotCost"]    = getf(request.form, "slotCost", ctx["slotCost"])
        monthly_ops = ctx["monthlyOps"]  = getf(request.form, "monthlyOps", ctx["monthlyOps"])
        ops_months  = ctx["opsMonths"]   = getf(request.form, "opsMonths", ctx["opsMonths"])
        service_fee = ctx["serviceFees"] = getf(request.form, "serviceFees", ctx["serviceFees"])
        cost = total_cost(slot_cost, monthly_ops, ops_months, service_fee)

        # category specifics
        if category == "pharma":
            months_saved = ctx["ph_monthsSaved"]    = getf(request.form, "ph_monthsSaved", ctx["ph_monthsSaved"])
            value_month  = ctx["ph_valuePerMonth"]  = getf(request.form, "ph_valuePerMonth", ctx["ph_valuePerMonth"])
            asset_value  = ctx["ph_assetValue"]     = getf(request.form, "ph_assetValue", ctx["ph_assetValue"])
            improve_pct  = ctx["ph_improvementPct"] = getf(request.form, "ph_improvementPct", ctx["ph_improvementPct"])
            tech_prob    = ctx["ph_techProb"]       = getf(request.form, "ph_techProb", ctx["ph_techProb"])
            benefit = benefit_pharma(months_saved, value_month, asset_value, improve_pct, tech_prob)

        elif category == "research":
            grant_prob     = ctx["re_grantProb"]     = getf(request.form, "re_grantProb", ctx["re_grantProb"])
            grant_value    = ctx["re_grantValue"]    = getf(request.form, "re_grantValue", ctx["re_grantValue"])
            pub_value      = ctx["re_pubValue"]      = getf(request.form, "re_pubValue", ctx["re_pubValue"])
            students_value = ctx["re_studentsValue"] = getf(request.form, "re_studentsValue", ctx["re_studentsValue"])
            benefit = benefit_research(grant_prob, grant_value, pub_value, students_value)

        else:  # mfg
            margin_per  = ctx["mf_marginPerUnit"]  = getf(request.form, "mf_marginPerUnit", ctx["mf_marginPerUnit"])
            improve_pct = ctx["mf_improvementPct"] = getf(request.form, "mf_improvementPct", ctx["mf_improvementPct"])
            units       = ctx["mf_units"]          = getf(request.form, "mf_units", ctx["mf_units"])
            adopt_prob  = ctx["mf_adoptionProb"]   = getf(request.form, "mf_adoptionProb", ctx["mf_adoptionProb"])
            benefit = benefit_mfg(margin_per, improve_pct, units, adopt_prob)

        spread = ctx["scenarioSpread"] = getf(request.form, "scenarioSpread", ctx["scenarioSpread"])
        sc = scenarios(benefit, cost, spread)

        # pre-format for template (no lambdas in Jinja)
        for k in sc:
            sc[k]["cost_fmt"] = fmt_usd(sc[k]["cost"])
            sc[k]["benefit_fmt"] = fmt_usd(sc[k]["benefit"])
            sc[k]["roi_fmt"] = fmt_pct(sc[k]["roi"])
            sc[k]["roi_ok"] = (sc[k]["roi"] >= 0)

        ctx["sc"] = sc
        ctx["total_cost_fmt"] = fmt_usd(cost)
        ctx["expected_benefit_fmt"] = fmt_usd(benefit)

    # pass active_page exactly ONCE
    return render_template("form.html", active_page="form", **ctx)

# If this file is run directly:
@app.route("/education")
def education():
    return render_template("education.html")
