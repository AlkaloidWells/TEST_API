import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask 
from extentions import db, migrate
from config import Config
# Import db from the app module



app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)

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
       
    def set_username(self, username):
        self.username = username
    
    def check_username(self):

        return self.username

class admin_user(User):
    __tablename__ = 'admin_user'
    company_name = db.Column(db.String(100))
    reg_no = db.Column(db.String(20))
    founded_date = db.Column(db.Date)
    address = db.Column(db.String(200))
    


class staff_user(User):  # Ensure StaffUser inherits from User
    __tablename__ = 'staff_user'  # Specify the table name explicitly
    reg_no = reg_no = db.Column(db.String(20))
    full_name = db.Column(db.String(100))
    date_emp = db.Column(db.Date)
    staff_address = db.Column(db.String(200))

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


    def set_id_card_number(self, id_card_number):
        self.id_card_number = id_card_number
    
    def check_id_card_number(self):

        return self.id_card_number

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

    def set_plate_number(self, plate_number):
        self.plate_number = plate_number
    
    def check_plate_number(self):

        return self.plate_number



def init_db():
    # Create all tables
    db.create_all()
    print("Database tables created successfully.")