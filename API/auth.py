from flask import redirect, request, url_for
from flask import request, jsonify, session
from flask_restful import Resource
from models.models import User
from functools import wraps
from flask import abort
from flask_login import current_user
from utilites.extentions import db
import re

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




def validate_email(email):
    # Regular expression pattern for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))



class UserResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return {'error': 'Username already exists'}, 400

        # If the username is unique, create the new user
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

        if user:
            print("User found:", user.username)  # Debug output
            if user.check_password(password):
                print("Password matched")  # Debug output
                session['user_id'] = user.id
                session['role'] = user.role
                return {'success': 'Login successful', 'role': user.role}, 200
            else:
                print("Password mismatch")  # Debug output
        else:
            print("User not found")  # Debug output

        return {'error': 'Invalid username or password'}, 401


class ViewUsersResource(Resource):
    def get(self):
        users = User.query.all()
        user_list = [{'id': user.id, 'username': user.username, 'role': user.role} for user in users]
        return {'users': user_list}, 200


class ViewUserDetailResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            user_info = {'id': user.id, 'username': user.username, 'role': user.role, 'image_path': user.image_path}
            return {'user': user_info}, 200
        else:
            return {'error': 'User not found'}, 404