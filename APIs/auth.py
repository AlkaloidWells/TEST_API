from flask import redirect, request, url_for
from flask import request, jsonify, session
from flask_restful import Resource
from models import User
from functools import wraps
from flask import abort
from flask_login import current_user
from extentions import db



ADMIN_DASHBOARD_URL = '/admin_dashboard'
USER_DASHBOARD_URL = '/user_dashboard'
SUPER_ADMIN_DASHBOARD_URL = '/super_admin_dashboard'
STAFF_DASHBOARD_URL = '/staff_dashboard'

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if user has any of the required roles
            if not any(current_user.has_role(role) for role in roles):
                # Abort with 403 Forbidden error if user does not have any of the required roles
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

@login_required
def get_user_role():
    return current_user.role

@login_required
def get_user_id():
    return current_user.id

def get_tax_number(user_id):
    user = User.query.get(user_id)
    if user:
        return user.tax_number
    else:
        return None 
    
def get_com_no(user_id):
    user = User.query.get(user_id)
    if user:
        return user.com_on
    else:
        return None 

class UserResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')



        new_user = User(username=username, role=role)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201


class UserDetailResource(Resource):
    @login_required
    @role_required(['super_admin'])
    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}, 200
        else:
            return {'error': 'User not found'}, 404
        
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