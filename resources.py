from flask import redirect, request, url_for
from flask import request, jsonify, session
from flask_restful import Resource
from models import User, admin_user, staff_user, Visitor, Vehicle
from functools import wraps
from flask import abort
from flask_login import current_user
from extentions import db
from PIL import Image
from Modules.ocr.ocr import *
import pytesseract


# app.py

ADMIN_DASHBOARD_URL = '/admin_dashboard'
USER_DASHBOARD_URL = '/user_dashboard'
SUPER_ADMIN_DASHBOARD_URL = '/super_admin_dashboard'
STAFF_DASHBOARD_URL = '/staff_dashboard'



def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if user has the required role
            if not current_user.has_role(role):
                # Abort with 403 Forbidden error if user does not have the required role
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in
        if not current_user.is_authenticated:
            # Redirect to login page
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


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
    @login_required
    @role_required('super_admin')
    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}, 200
        else:
            return {'error': 'User not found'}, 404


class VisitorResource(Resource):

    @login_required
    @role_required('user')
    def post(self):
        data = request.get_json()
        new_visitor = Visitor(
            full_name=data['full_name'],
            id_card_number=data['id_card_number'],
            date_of_birth=data['date_of_birth'],
            address=data['address'],
            contact_details=data['contact_details'],
            purpose_of_visit=data['purpose_of_visit'],
            time_in=data['time_in'],
            badge_issued=data['badge_issued']
        )

        db.session.add(new_visitor)
        db.session.commit()

        return {'message': 'Visitor created successfully'}, 201


class VisitorDetailResource(Resource):
    @login_required
    @role_required('user')
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
        
    @login_required
    @role_required('user')
    def delete(self, visitor_id):
        
        visitor = Visitor.query.get(visitor_id)
        if visitor:
            db.session.delete(visitor)
            db.session.commit()
            return {'message': 'Visitor deleted successfully'}, 200
        else:
            return {'error': 'Visitor not found'}, 404


class VehicleResource(Resource):
    @login_required
    @role_required('user')
    def post(self):
        data = request.get_json()
        new_vehicle = Vehicle(
            plate_number=data['plate_number'],
            make=data['make'],
            model=data['model'],
            color=data['color'],
            owner_details=data['owner_details'],
            entry_time=data['entry_time'],
            exit_time=data.get('exit_time'),  # It's optional, so use get() method
            flagged_as_suspicious=data.get('flagged_as_suspicious', False)  # Default to False if not provided
        )

        db.session.add(new_vehicle)
        db.session.commit()

        return {'message': 'Vehicle created successfully'}, 201


class VehicleDetailResource(Resource):
    @login_required
    @role_required('super')
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

    @login_required
    @role_required('user')
    def delete(self, vehicle_id):
        vehicle = Vehicle.query.get(vehicle_id)
        if vehicle:
            db.session.delete(vehicle)
            db.session.commit()
            return {'message': 'Vehicle deleted successfully'}, 200
        else:
            return {'error': 'Vehicle not found'}, 404


class AdminUserResource(Resource):
    @login_required
    @role_required('super_admin')
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

        new_admin_user = admin_user(username=username, role=role, image_path=image_path,
                                   company_name=company_name, reg_no=reg_no, founded_date=founded_date,
                                   address=address, contact_details=contact_details)
        new_admin_user.set_password(password)

        db.session.add(new_admin_user)
        db.session.commit()

        return {'message': 'Admin user created successfully'}, 201


class AdminUserDetailResource(Resource):
    @login_required
    @role_required('super_admin')
    def delete(self, user_id):
        admin_user = admin_user.query.get(user_id)
        if admin_user:
            db.session.delete(admin_user)
            db.session.commit()
            return {'message': 'Admin user deleted successfully'}, 200
        else:
            return {'error': 'Admin user not found'}, 404


class StaffUserResource(Resource):
    @login_required
    @role_required('admin')
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = 'staff'  # Fixed role for staff users
        image_path = data.get('image_path')
        full_name = data.get('full_name')
        date_emp = data.get('date_emp')
        staff_address = data.get('address')
        contact_details = data.get('contact_details')

        new_staff_user = staff_user(username=username, role=role, image_path=image_path,
                                   full_name=full_name, date_emp=date_emp, address=staff_address,
                                   contact_details=contact_details)
        new_staff_user.set_password(password)

        db.session.add(new_staff_user)
        db.session.commit()

        return {'message': 'Staff user created successfully'}, 201


class StaffUserDetailResource(Resource):
    @login_required
    @role_required('sadmin')
    def delete(self, user_id):
        staff_user = staff_user.query.get(user_id)
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
    

class ViewUsersResource(Resource):
    def get(self):
        users = User.query.all()
        user_list = [{'id': user.id, 'username': user.username, 'role': user.role, 'image_path': user.image_path} for user in users]
        return jsonify(user_list), 200

class ViewUserDetailResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            user_info = {'id': user.id, 'username': user.username, 'role': user.role, 'image_path': user.image_path}
            return jsonify(user_info), 200
        else:
            return {'error': 'User not found'}, 404

class ViewVehiclesResource(Resource):
    def get(self):
        vehicles = Vehicle.query.all()
        vehicle_list = [{'id': vehicle.id, 'plate_number': vehicle.plate_number, 'make': vehicle.make, 'model': vehicle.model, 'color': vehicle.color} for vehicle in vehicles]
        return jsonify(vehicle_list), 200

class ViewVehicleDetailResource(Resource):
    def get(self, vehicle_id):
        vehicle = Vehicle.query.get(vehicle_id)
        if vehicle:
            vehicle_info = {'id': vehicle.id, 'plate_number': vehicle.plate_number, 'make': vehicle.make, 'model': vehicle.model, 'color': vehicle.color}
            return jsonify(vehicle_info), 200
        else:
            return {'error': 'Vehicle not found'}, 404

class ViewVisitorsResource(Resource):
    def get(self):
        visitors = Visitor.query.all()
        visitor_list = [{'id': visitor.id, 'full_name': visitor.full_name, 'id_card_number': visitor.id_card_number, 'date_of_birth': visitor.date_of_birth} for visitor in visitors]
        return jsonify(visitor_list), 200

class ViewVisitorDetailResource(Resource):
    def get(self, visitor_id):
        visitor = Visitor.query.get(visitor_id)
        if visitor:
            visitor_info = {'id': visitor.id, 'full_name': visitor.full_name, 'id_card_number': visitor.id_card_number, 'date_of_birth': visitor.date_of_birth}
            return jsonify(visitor_info), 200
        else:
            return {'error': 'Visitor not found'}, 404



class UpdateVisitorByOCRResource(Resource):
    @login_required
    @role_required('user')
    def post(self):
        # Ensure that the request contains a file
        if 'file' not in request.files:
            return {'error': 'No file provided'}, 400

        file = request.files['file']

        # Ensure that the file is an image
        if file.filename == '':
            return {'error': 'No file selected'}, 400
        if file and allowed_file(file.filename):
            try:
                # Read the image file and perform OCR using Tesseract
                image = Image.open(file)
                text = pytesseract.image_to_string(image)

                # Extract relevant information from OCR result
                # For example, assuming OCR result contains username and password
                # You may need to adjust this based on your OCR result format
                username, password = process_ocr_result(text)

                # Update user information in the database
                user = User.query.filter_by(username=username).first()
                if user:
                    user.set_password(password)  # Assuming password update is required
                    db.session.commit()
                    return {'message': 'User information updated by OCR scan'}, 200
                else:
                    return {'error': 'User not found'}, 404
            except Exception as e:
                return {'error': str(e)}, 500
        else:
            return {'error': 'Unsupported file type'}, 400



class UpdateViruleByOCRResource(Resource):
    def post(self):
        # Process OCR scan and update visitor information
        # Replace this with your OCR processing logic
        return {'message': 'Visitor information updated by OCR scan'}, 200