from flask import redirect, request, url_for
from flask import request, jsonify, session
from flask_restful import Resource
from models import Visitor
from extentions import db
from PIL import Image
from Modules.ocr.ocr import *
import pytesseract
from APIs.auth import login_required, role_required



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
                visitor = Visitor.query.filter_by(username=username).first()
                if visitor:
                    visitor(password)  # Assuming password update is required
                    db.session.commit()
                    return {'message': 'User information updated by OCR scan'}, 200
                else:
                    return {'error': 'User not found'}, 404
            except Exception as e:
                return {'error': str(e)}, 500
        else:
            return {'error': 'Unsupported file type'}, 400