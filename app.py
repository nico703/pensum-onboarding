from flask import Flask, render_template, request, redirect, url_for
from models import db, Employee
from datetime import datetime
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///employees.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# Step 1: Basisdaten
@app.route("/", methods=["GET"])
def index():
    employees = Employee.query.filter_by(is_active=True).all()
    return render_template("index.html", employees=employees)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        fullname = request.form["fullname"]
        email = request.form["email"]
        birthdate_str = request.form.get("birthdate")
        birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date() if birthdate_str else None
        address = request.form.get("address")
        mobile = request.form.get("mobile")
        department = request.form.getlist("department")
        start_date_str = request.form["start_date"]
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else None

        new_emp = Employee(
            fullname=fullname,
            email=email,
            birthdate=birthdate,
            address=address,
            mobile=mobile,
            department=','.join(department),
            start_date=start_date
        )
        db.session.add(new_emp)
        db.session.commit()

        return redirect(url_for("contract_details", id=new_emp.id))

    return render_template("create.html")

# Step 2: Vertragsdetails
@app.route("/contract/<int:id>", methods=["GET", "POST"])
def contract_details(id):
    employee = Employee.query.get_or_404(id)
    if request.method == "POST":
        employee.position = request.form.get("position")
        employee.location = request.form.get("location")
        employee.employment_type = request.form.get("employment_type")
        employee.vacation_days = request.form.get("vacation_days")
        employee.homeoffice = request.form.get("homeoffice")
        employee.homeoffice_detail = request.form.get("homeoffice_detail")

        db.session.commit()
        return redirect(url_for("equipment", id=id))
    return render_template("contract_details.html", employee=employee)

# Step 3: Equipment
@app.route("/equipment/<int:id>", methods=["GET", "POST"])
def equipment(id):
    employee = Employee.query.get_or_404(id)
    if request.method == "POST":
        # Equipment-Daten speichern
        return redirect(url_for("organization", id=id))
    return render_template("equipment.html", employee=employee)

# Step 4: Organisation
@app.route("/organization/<int:id>", methods=["GET", "POST"])
def organization(id):
    employee = Employee.query.get_or_404(id)
    if request.method == "POST":
        # Organisationsdaten speichern
        return redirect(url_for("summary", id=id))
    return render_template("organization.html", employee=employee)

# Zusammenfassung
@app.route("/summary/<int:id>", methods=["GET", "POST"])
def summary(id):
    employee = Employee.query.get_or_404(id)
    if request.method == "POST":
        # Onboarding abschließen und Aufgaben an Abteilungen weiterleiten
        return redirect(url_for("index"))
    return render_template("summary.html", employee=employee)

# Offboarding
@app.route("/offboard/<int:id>")
def offboard(id):
    employee = Employee.query.get_or_404(id)
    employee.is_active = False
    db.session.commit()
    return redirect(url_for("index"))

# Admin
@app.route("/admin")
def admin():
    active_employees = Employee.query.filter_by(is_active=True).all()
    recent_employees = Employee.query.order_by(Employee.id.desc()).limit(5).all()
    return render_template("admin.html", active_employees=active_employees, recent_employees=recent_employees)

# Easter Egg
@app.route("/about-dev")
def about_dev():
    return {
        "crafted_by": "Nico",
        "powered_by": "HoodIQ",
        "message": "Guck, Guck"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))