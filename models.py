import os
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    image_path = db.Column(db.String(20), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class admin_user(User):
    company_name = db.Column(db.String(100), nullable=False)
    reg_no = db.Column(db.String(20), nullable=False)
    founded_date = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    contact_details = db.Column(db.String(50), nullable=False)


class staff_user(User):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    date_emp = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    contact_details = db.Column(db.String(50), nullable=False)

class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    id_card_number = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    contact_details = db.Column(db.String(50), nullable=False)
    purpose_of_visit = db.Column(db.String(200), nullable=False)
    time_in = db.Column(db.DateTime, nullable=False)
    badge_issued = db.Column(db.Boolean, default=False)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String(20), nullable=False)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    owner_details = db.Column(db.String(100), nullable=False)
    entry_time = db.Column(db.DateTime, nullable=False)
    exit_time = db.Column(db.DateTime)
    flagged_as_suspicious = db.Column(db.Boolean, default=False)


def init_db():
    # Create all tables
    db.create_all()
    print("Database tables created successfully.")