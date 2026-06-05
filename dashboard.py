from flask import Flask, render_template
import json

app = Flask(__name__)

def get_patients():
    with open("Patients.json", "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/")
def dashboard():
    patients = get_patients()
    return render_template("dashboard.html", patients=patients)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

    