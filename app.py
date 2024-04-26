from flask import Flask, render_template
from flask_restful import Api
from resources import *
from extentions import db, migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)

# Import models to ensure they are registered with SQLAlchemy
from models import *

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
