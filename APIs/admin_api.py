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
        tax_number = data.get('tax_number')
        industry = data.get('industry')
        company_size = data.get('company_size')
        company_tel = data.get('company_tel')
        company_email = data.get('company_email')
        company_gps = data.get('company_gps')
        company_address = data.get('company_address')
        managed_by = data.get('managed_by')
        manager_role = data.get('manager_role')
        manager_tel = data.get('manager_tel')
        manager_email = data.get('manager_email')

        existing_user = admin_user.query.filter_by(username=username).first()
        if existing_user:
            return {'error': 'Username already exists'}, 400

        new_admin_user = admin_user(username=username, role=role, image_path=image_path,
                                    company_name=company_name, tax_number=tax_number, industry=industry,
                                    company_size=company_size, company_tel=company_tel, company_email=company_email,
                                    Company_gps=company_gps, company_address=company_address,
                                    managed_by=managed_by, manager_role=manager_role,
                                    manager_tel=manager_tel, manager_email=manager_email)
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