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
    return render_template('investment.html', items=items)

@app.route("/form", methods=["GET", "POST"])
def form():
    return render_template("form.html", active_page="form", **ctx)

if __name__ == "__main__":
    app.run(debug=True)

