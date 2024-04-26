from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from functools import wraps
from flask import abort
import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from resources import *

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db', 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '8IR4M7-R3c74GjTHhKzWODaYVHuPGqn4w92DHLqeYJA'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Import models here as to avoid circular import issue

from models import *
with app.app_context():
    init_db()


@app.route('/')
def index():
    return render_template('index.html')

api = Api(app)



api.add_resource(UserResource, '/api/users')
api.add_resource(UserDetailResource, '/api/users/<int:user_id>')

# Admin User APIs
api.add_resource(AdminUserResource, '/api/admin_users')
api.add_resource(AdminUserDetailResource, '/api/admin_users/<int:user_id>')

# Staff User APIs
api.add_resource(StaffUserResource, '/api/staff_users')
api.add_resource(StaffUserDetailResource, '/api/staff_users/<int:user_id>')

# Visitor APIs
api.add_resource(VisitorResource, '/api/visitors')
api.add_resource(VisitorDetailResource, '/api/visitors/<int:visitor_id>')

# Vehicle APIs
api.add_resource(VehicleResource, '/api/vehicles')
api.add_resource(VehicleDetailResource, '/api/vehicles/<int:vehicle_id>')

# Login API
api.add_resource(LoginResource, '/api/login')


if __name__ == '__main__':
    app.run(debug=True)
