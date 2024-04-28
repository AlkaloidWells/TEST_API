# Import necessary modules and classes
from flask import Flask, render_template
from flask_restful import Api
from API.admin_api import *
from API.staff_api import *
from API.vircule_api import *
from API.visitor_api import *
from API.auth import *
from extentions import db, migrate
from config import Config
from models import *




app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)


from models import *


# Import models to ensure they are registered with SQLAlchemy
with app.app_context():
    init_db()



@app.route('/')
def index():
    return render_template('login.html')

api = Api(app)





# Define routes for User-related APIs
api.add_resource(UserResource, '/api/auth')
api.add_resource(UserDetailResource, '/api/auth/<int:user_id>')

# Define routes for Admin User-related APIs
api.add_resource(AdminUserResource, '/api/admin_api')
api.add_resource(AdminUserDetailResource, '/api/admin_api/<int:user_id>')

# Define routes for Staff User-related APIs
api.add_resource(StaffUserResource, '/api/staff_api')
api.add_resource(StaffUserDetailResource, '/api/staff_api/<int:user_id>')

# Define routes for Visitor-related APIs
api.add_resource(VisitorResource, '/api/visitors')
api.add_resource(VisitorDetailResource, '/api/visitors_api/<int:visitor_id>')

# Define routes for Vehicle-related APIs
api.add_resource(VehicleResource, '/api/vehicles')
api.add_resource(VehicleDetailResource, '/api/vircul_api/<int:vehicle_id>')

# Define route for Login API
api.add_resource(LoginResource, '/api/auth')

# Define routes for viewing users, vehicles, and visitors
api.add_resource(ViewUsersResource, '/api/auth')
api.add_resource(ViewUserDetailResource, '/api/auth/<int:user_id>')
api.add_resource(ViewVehiclesResource, '/api/vircul_api')
api.add_resource(ViewVehicleDetailResource, '/api/vircul_api/<int:vehicle_id>')
api.add_resource(ViewVisitorsResource, '/api/view/visitors_api')
api.add_resource(ViewVisitorDetailResource, '/api/visitors_api/<int:visitor_id>')

# Define route for updating user information using OCR
api.add_resource(UpdateVisitorByOCRResource, '/api/visitor_api/')

# Define route for updating visitor information using OCR
api.add_resource(UpdateViruleByOCRResource, '/api/vircule_api')

# Define route for retrieving visitors by company ID
api.add_resource(VisitorsByCompanyResource, '/api/visitor_api/<int:user_id>')

# Define route for retrieving staffs by company ID
api.add_resource(StaffByCompanyResource, '/api/staff_api/<int:com_no>')

# Define route for retrieving all admin users
api.add_resource(AdminUsersViewResource, '/api/admin_api')

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
