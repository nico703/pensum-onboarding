from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Persönliche Daten
    fullname = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.Date)
    address = db.Column(db.String(200))
    mobile = db.Column(db.String(20))
    private_email = db.Column(db.String(120))

    # Vertragsdaten
    department = db.Column(db.Text)  # falls Mehrfachauswahl: CSV oder Liste
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    contact_person = db.Column(db.String(100))
    location = db.Column(db.String(100))
    position = db.Column(db.String(100))
    employment_type = db.Column(db.String(50))
    vacation_days = db.Column(db.Integer)
    homeoffice = db.Column(db.String(10))
    homeoffice_detail = db.Column(db.String(50))

    # IT & Ausstattung
    laptop = db.Column(db.String(50))
    laptop_source = db.Column(db.String(50))
    laptop_special = db.Column(db.String(200))
    laptop_ordered_on = db.Column(db.Date)
    laptop_ordered_by = db.Column(db.String(100))
    laptop_returned_on = db.Column(db.Date)
    laptop_returned_to = db.Column(db.String(100))

    phone = db.Column(db.String(50))
    phone_source = db.Column(db.String(50))
    phone_ordered_on = db.Column(db.Date)
    phone_ordered_by = db.Column(db.String(100))
    phone_returned_on = db.Column(db.Date)
    phone_returned_to = db.Column(db.String(100))

    headset = db.Column(db.String(10))
    monitors = db.Column(db.String(10))
    monitor_count = db.Column(db.Integer)
    desk_phone = db.Column(db.String(10))
    desk_phone_extension = db.Column(db.String(10))
    printer = db.Column(db.String(10))
    printer_source = db.Column(db.String(50))
    printer_special = db.Column(db.String(200))

    # Software / Zugänge
    access_server = db.Column(db.Boolean, default=False)
    access_zvoove = db.Column(db.Boolean, default=False)
    access_teams = db.Column(db.Boolean, default=False)
    access_lapid = db.Column(db.Boolean, default=False)
    access_absence = db.Column(db.Boolean, default=False)
    email_internal = db.Column(db.String(120))
    email_distribution = db.Column(db.String(120))
    email_distribution_other = db.Column(db.String(120))
    email_forward_to = db.Column(db.String(120))

    # Organisation
    access_card = db.Column(db.Boolean, default=False)
    parking_space = db.Column(db.Boolean, default=False)
    keys = db.Column(db.Boolean, default=False)
    locker = db.Column(db.Boolean, default=False)
    tankkarte = db.Column(db.String(10))
    tankkarten_nummer = db.Column(db.String(50))
    dsgvo_schulung = db.Column(db.Boolean, default=False)
    visitenkarten = db.Column(db.Boolean, default=False)

    # Einarbeitung
    welcome_mail_sent = db.Column(db.Boolean, default=False)
    welcome_package_ready = db.Column(db.Boolean, default=False)
    training_plan_created = db.Column(db.Boolean, default=False)
    trial_feedback_meeting = db.Column(db.Date)

    # Sonstiges
    notes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)