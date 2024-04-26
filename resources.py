from flask import request
from flask import request, jsonify, session
from flask_restful import Resource
from models import User, admin_user, staff_user, Visitor, Vir



class UserResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        image_path = data.get('image_path')

        new_user = User(username=username, role=role, image_path=image_path)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201


class UserDetailResource(Resource):
    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}, 200
        else:
            return {'error': 'User not found'}, 404


class VisitorResource(Resource):
    def post(self):
        data = request.get_json()
        # Extract data from JSON and create Visitor instance
        new_visitor = Visitor(**data)

        db.session.add(new_visitor)
        db.session.commit()

        return {'message': 'Visitor created successfully'}, 201


class VisitorDetailResource(Resource):
    def put(self, visitor_id):
        data = request.get_json()
        visitor = Visitor.query.get(visitor_id)
        if visitor:
            # Update visitor fields with data from JSON
            for key, value in data.items():
                setattr(visitor, key, value)

            db.session.commit()
            return {'message': 'Visitor updated successfully'}, 200
        else:
            return {'error': 'Visitor not found'}, 404

    def delete(self, visitor_id):
        visitor = Visitor.query.get(visitor_id)
        if visitor:
            db.session.delete(visitor)
            db.session.commit()
            return {'message': 'Visitor deleted successfully'}, 200
        else:
            return {'error': 'Visitor not found'}, 404


class VehicleResource(Resource):
    def post(self):
        data = request.get_json()
        # Extract data from JSON and create Vehicle instance
        new_vehicle = Vehicle(**data)

        db.session.add(new_vehicle)
        db.session.commit()

        return {'message': 'Vehicle created successfully'}, 201


class VehicleDetailResource(Resource):
    def put(self, vehicle_id):
        data = request.get_json()
        vehicle = Vehicle.query.get(vehicle_id)
        if vehicle:
            # Update vehicle fields with data from JSON
            for key, value in data.items():
                setattr(vehicle, key, value)

            db.session.commit()
            return {'message': 'Vehicle updated successfully'}, 200
        else:
            return {'error': 'Vehicle not found'}, 404

    def delete(self, vehicle_id):
        vehicle = Vehicle.query.get(vehicle_id)
        if vehicle:
            db.session.delete(vehicle)
            db.session.commit()
            return {'message': 'Vehicle deleted successfully'}, 200
        else:
            return {'error': 'Vehicle not found'}, 404


class AdminUserResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = 'admin'  # Fixed role for admin users
        image_path = data.get('image_path')
        company_name = data.get('company_name')
        reg_no = data.get('reg_no')
        founded_date = data.get('founded_date')
        address = data.get('address')
        contact_details = data.get('contact_details')

        new_admin_user = AdminUser(username=username, role=role, image_path=image_path,
                                   company_name=company_name, reg_no=reg_no, founded_date=founded_date,
                                   address=address, contact_details=contact_details)
        new_admin_user.set_password(password)

        db.session.add(new_admin_user)
        db.session.commit()

        return {'message': 'Admin user created successfully'}, 201


class AdminUserDetailResource(Resource):
    def delete(self, user_id):
        admin_user = AdminUser.query.get(user_id)
        if admin_user:
            db.session.delete(admin_user)
            db.session.commit()
            return {'message': 'Admin user deleted successfully'}, 200
        else:
            return {'error': 'Admin user not found'}, 404


class StaffUserResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = 'staff'  # Fixed role for staff users
        image_path = data.get('image_path')
        full_name = data.get('full_name')
        date_emp = data.get('date_emp')
        address = data.get('address')
        contact_details = data.get('contact_details')

        new_staff_user = StaffUser(username=username, role=role, image_path=image_path,
                                   full_name=full_name, date_emp=date_emp, address=address,
                                   contact_details=contact_details)
        new_staff_user.set_password(password)

        db.session.add(new_staff_user)
        db.session.commit()

        return {'message': 'Staff user created successfully'}, 201


class StaffUserDetailResource(Resource):
    def delete(self, user_id):
        staff_user = StaffUser.query.get(user_id)
        if staff_user:
            db.session.delete(staff_user)
            db.session.commit()
            return {'message': 'Staff user deleted successfully'}, 200
        else:
            return {'error': 'Staff user not found'}, 404


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['role'] = user.role
            
            if user.role == 'admin':
                return {'message': 'Admin logged in successfully', 'redirect_url': ADMIN_DASHBOARD_URL}, 200
            elif user.role == 'user':
                return {'message': 'User logged in successfully', 'redirect_url': USER_DASHBOARD_URL}, 200
            elif user.role == 'super_admin':
                return {'message': 'Super admin logged in successfully', 'redirect_url': SUPER_ADMIN_DASHBOARD_URL}, 200
            elif user.role == 'staff':
                return {'message': 'Staff logged in successfully', 'redirect_url': STAFF_DASHBOARD_URL}, 200
        else:
            return {'error': 'Invalid username or password'}, 401