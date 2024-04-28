from flask import Flask, render_template
from flask_restful import Api
from APIs.admin_api import *
from APIs.staff_api import *
from APIs.vircule_api import *
from APIs.visitor_api import *
from APIs.auth import *
from extentions import db, migrate
from config import Config

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
    return render_template('register_user.html')

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

api.add_resource(ViewUsersResource, '/api/view_users')
api.add_resource(ViewUserDetailResource, '/api/view_users/<int:user_id>')
api.add_resource(ViewVehiclesResource, '/api/view_vehicles')
api.add_resource(ViewVehicleDetailResource, '/api/view_vehicles/<int:vehicle_id>')
api.add_resource(ViewVisitorsResource, '/api/view_visitors')
api.add_resource(ViewVisitorDetailResource, '/api/view_visitors/<int:visitor_id>')
api.add_resource(UpdateVisitorByOCRResource, '/api/update_user_by_ocr')
api.add_resource(UpdateViruleByOCRResource, '/api/update_visitor_by_ocr')



if __name__ == '__main__':
    app.run(debug=True)
