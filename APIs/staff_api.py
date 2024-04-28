from flask import redirect, request, url_for
from flask import request, jsonify, session
from flask_restful import Resource
from models import staff_user 
from flask_login import current_user
from extentions import db
from PIL import Image
from Modules.ocr.ocr import *
from APIs.auth import login_required, role_required


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
        com_no = data.get('com_no')
        staff_email = data.get('staff_email')
        staff_social_link = data.get('staff_social_link')
        staff_role = data.get('staff_role')
        staff_home_address = data.get('staff_home_address')
        staff_department = data.get('staff_department')

        new_staff_user = staff_user(username=username, role=role, image_path=image_path,
                                    full_name=full_name, com_no=com_no, staff_email=staff_email,
                                    staff_social_link=staff_social_link, staff_role=staff_role,
                                    staff_home_address=staff_home_address, staff_department=staff_department)
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
