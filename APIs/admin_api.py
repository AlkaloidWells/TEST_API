from flask import redirect, request, url_for
from flask import request, jsonify, session
from flask_restful import Resource
from models import admin_user
from extentions import db
from PIL import Image
from Modules.ocr.ocr import *
from APIs.auth import login_required, role_required




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