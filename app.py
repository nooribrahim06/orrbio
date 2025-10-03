from flask import Flask, render_template, request
import math

app = Flask(__name__)

# ---------- Helpers ----------
def distance(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def risk_level(d):
    if d < 1:
        return "⚠ Very High Risk (Collision Likely)"
    elif d < 10:
        return "Medium Risk (Close Approach)"
    else:
        return "Safe Distance"

# ---------- Routes ----------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/education")
def education():
    return render_template("education.html")

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

        for t in range(0, 10800, 90):
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

    return render_template("form.html", active_page="form")


if __name__ == "__main__":
    app.run(debug=True)

