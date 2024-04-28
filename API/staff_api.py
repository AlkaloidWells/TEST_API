from flask import redirect, request, url_for
from flask import request, jsonify, session
from flask_restful import Resource
from models.models import staff_user 
from utilites.extentions import db
from PIL import Image
from Modules.ocr.ocr import *
from API.auth import login_required, role_required , validate_email, get_com_no


from flask import jsonify

class StaffUserResource(Resource):
    @login_required
    @role_required(['super_admin', 'admin'])
    def post(self):
        data = request.get_json()

        # Validate input data
        required_fields = ['username', 'password', 'full_name', 'staff_email']
        if not all(key in data for key in required_fields):
            return jsonify({'error': 'Required fields are missing'}), 400

        username = data.get('username')
        password = data.get('password')
        full_name = data.get('full_name')
        staff_email = data.get('staff_email')

        # Additional optional fields
        staff_social_link = data.get('staff_social_link')
        staff_role = data.get('staff_role')
        staff_home_address = data.get('staff_home_address')
        staff_department = data.get('staff_department')
        image_path = data.get('image_path')

        # Validate input formats if needed
        if not validate_email(staff_email):
            return {'error': 'Invalid company email format'}, 400

        # Check if username already exists
        existing_user = staff_user.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 409

        # Create a new staff user
        new_staff_user = staff_user(
            username=username,
            role='staff',
            image_path=image_path,
            full_name=full_name,
            staff_email=staff_email,
            staff_social_link=staff_social_link,
            staff_role=staff_role,
            staff_home_address=staff_home_address,
            staff_department=staff_department
        )
        new_staff_user.set_password(password)

        db.session.add(new_staff_user)
        db.session.commit()

        return jsonify({'message': 'Staff user created successfully'}), 201


class StaffUserDetailResource(Resource):
    @login_required
    @role_required(['super_admin', 'admin', 'staff'])
    def delete(self, user_id):
        try:
            staff_user_obj = staff_user.query.get(user_id)
            if staff_user_obj:
                db.session.delete(staff_user_obj)
                db.session.commit()
                return {'message': 'Staff user deleted successfully'}, 200
            else:
                return {'error': 'Staff user not found'}, 404
        except Exception as e:
            db.session.rollback()
            return {'error': 'An error occurred while processing the request'}, 500


class StaffByCompanyResource(Resource):
    @login_required
    @role_required(['super_admin', 'admin'])
    def get(self, user_id):
        com_no = get_com_no(user_id)
        staffs = staff_user.query.filter_by(com_no=com_no).all()

        if staffs:
            staff_list = [{
                'id': staff.id,
                'full_name': staff.full_name,
                'position': staff.position,
                'department': staff.department,
                'contact_details': staff.contact_details,
                'hire_date': staff.hire_date,
                'salary': staff.salary
            } for staff in staffs]

            return jsonify(staff_list), 200
        else:
            return {'message': 'No staffs found for company number {}'.format(com_no)}, 404
