from flask import Flask, render_template, request, redirect, url_for
from models import db, Employee
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///employees.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    employees = Employee.query.filter_by(is_active=True).all()
    return render_template("index.html", employees=employees)

from datetime import datetime

@app.route("/onboard", methods=["GET", "POST"])
def onboard():
    if request.method == "POST":
        fullname = request.form["fullname"]
        email = request.form["email"]
        department = request.form["department"]
        notes = request.form.get("notes", "")

        # Datum umwandeln, wenn angegeben
        start_date_str = request.form["start_date"]
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else None

        # Neues Objekt erstellen
        new_emp = Employee(
            fullname=fullname,
            email=email,
            department=department,
            start_date=start_date,
            notes=notes
        )
        db.session.add(new_emp)
        db.session.commit()

        # Weiterleiten zur Equipment-Seite
        return redirect(url_for("equipment", id=new_emp.id))

    return render_template("create.html")

@app.route("/offboard/<int:id>")
def offboard(id):
    employee = Employee.query.get_or_404(id)
    employee.is_active = False
    db.session.commit()
    return redirect(url_for("index"))

# Easter Egg
@app.route("/about-dev")
def about_dev():
    return {
        "crafted_by": "Nico",
        "powered_by": "Pensum – Onboarding",
        "message": "Guck, Guck"
    }

@app.route('/equipment/<int:id>', methods=['GET', 'POST'])
def equipment(id):
    employee = Employee.query.get_or_404(id)

    if request.method == 'POST':
        # Hier speichern wir die Ausstattung
        employee.laptop = request.form.get('laptop')
        employee.handy = request.form.get('handy')
        employee.software = request.form.get('software')
        employee.ausweis = request.form.get('ausweis')
        employee.parkplatz = request.form.get('parkplatz')
        db.session.commit()
        return redirect(url_for('final_step', id=id))

    return render_template('equipment.html', employee=employee)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))