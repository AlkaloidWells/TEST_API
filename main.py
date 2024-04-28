# Import necessary modules and classes
from flask import Flask, render_template
from flask_restful import Api
from API.admin_api import *
from API.staff_api import *
from API.vircule_api import *
from API.visitor_api import *
from API.auth import *
from utilites.extentions import db, migrate
from utilites.config import Config
from models.models import *

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)

# Import models to ensure they are registered with SQLAlchemy
from models.models import *
with app.app_context():
    init_db()

# Routes
@app.route('/')
def index():
    return render_template('login.html')

api = Api(app)

api.add_resource(UserResource, '/api/users')
api.add_resource(UserDetailResource, '/api/users/<int:user_id>')

# Define routes for Admin User-related APIs
api.add_resource(AdminUserResource, '/api/admin_users')
api.add_resource(AdminUserDetailResource, '/api/admin_users/<int:user_id>')

# Define routes for Staff User-related APIs
api.add_resource(StaffUserResource, '/api/staff_users')
api.add_resource(StaffUserDetailResource, '/api/staff_users/<int:user_id>')

# Define routes for Visitor-related APIs
api.add_resource(VisitorResource, '/api/visitors')
api.add_resource(VisitorDetailResource, '/api/visitors/<int:visitor_id>')

# Define routes for Vehicle-related APIs
api.add_resource(VehicleResource, '/api/vehicles')
api.add_resource(VehicleDetailResource, '/api/vehicles/<int:vehicle_id>')

# Define route for Login API
api.add_resource(LoginResource, '/api/login')

# Define routes for viewing users, vehicles, and visitors
api.add_resource(ViewUsersResource, '/api/view/users')
api.add_resource(ViewUserDetailResource, '/api/view/users/<int:user_id>')
api.add_resource(ViewVehiclesResource, '/api/view/vehicles')
api.add_resource(ViewVehicleDetailResource, '/api/view/vehicles/<int:vehicle_id>')
api.add_resource(ViewVisitorsResource, '/api/view/visitors')
api.add_resource(ViewVisitorDetailResource, '/api/view/visitors/<int:visitor_id>')

# Define route for updating user information using OCR
api.add_resource(UpdateVisitorByOCRResource, '/api/update_user_by_ocr')

# Define route for updating visitor information using OCR
api.add_resource(UpdateViruleByOCRResource, '/api/update_visitor_by_ocr')

# Define route for retrieving visitors by company ID
api.add_resource(VisitorsByCompanyResource, '/api/view/visitors/company/<int:user_id>')

# Define route for retrieving staffs by company ID
api.add_resource(StaffByCompanyResource, '/api/view/staffs/company/<int:user_id>')

# Define route for retrieving all admin users
api.add_resource(AdminUsersViewResource, '/api/view/admin_users')


# Start the Flask application
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
