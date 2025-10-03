from flask import Flask, render_template, request



app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/education")
def education():
    return render_template("education.html")

@app.route("/safety", methods=["GET","POST"])
def safety():
    return render_template("safety.html", result=result)

@app.route('/investment', methods=["GET","POST"])
def investment():
    return render_template('investment.html', items=items)

@app.route("/form", methods=["GET", "POST"])
def form():
    return render_template("form.html", active_page="form", **ctx)





