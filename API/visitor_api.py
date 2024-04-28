from flask import redirect, request, url_for
from flask import request, jsonify, session
from flask_restful import Resource
from models.models import Visitor
from utilites.extentions import db
from PIL import Image
from Modules.ocr.ocr import *
import pytesseract
from API.auth import login_required, role_required, get_user_id, get_com_no



class VisitorResource(Resource):

    @login_required
    @role_required(['super_admin', 'admin', 'staff'])
    def post(self):
        data = request.get_json()
        full_name = data.get('full_name')
        id_card_number = data.get('id_card_number')
        date_of_birth = data.get('date_of_birth')
        address = data.get('address')
        contact_details = data.get('contact_details')
        purpose_of_visit = data.get('purpose_of_visit')
        time_in = data.get('time_in')
        badge_issued = data.get('badge_issued')

        user_id = get_user_id()
        com_no = get_com_no(user_id)

        new_visitor = Visitor(
            com_no=com_no,
            full_name=full_name,
            id_card_number=id_card_number,
            date_of_birth=date_of_birth,
            address=address,
            contact_details=contact_details,
            purpose_of_visit=purpose_of_visit,
            time_in=time_in,
            badge_issued=badge_issued
        )

        db.session.add(new_visitor)
        db.session.commit()

        return {'message': 'Visitor created successfully'}, 201


class VisitorDetailResource(Resource):

    @login_required
    @role_required(['super_admin', 'admin', 'staff'])
    def put(self, visitor_id):
        data = request.get_json()
        visitor = Visitor.query.get(visitor_id)
        if visitor:
            for key, value in data.items():
                setattr(visitor, key, value)

            db.session.commit()
            return {'message': 'Visitor updated successfully'}, 200
        else:
            return {'error': 'Visitor not found'}, 404
        
    @login_required
    @role_required(['super_admin', 'admin', 'staff'])
    def delete(self, visitor_id):
        visitor = Visitor.query.get(visitor_id)
        if visitor:
            db.session.delete(visitor)
            db.session.commit()
            return {'message': 'Visitor deleted successfully'}, 200
        else:
            return {'error': 'Visitor not found'}, 404
        

class ViewVisitorsResource(Resource):

    @role_required(['super_admin', 'admin', 'staff'])
    def get(self):
        visitors = Visitor.query.all()
        visitor_list = [{'id': visitor.id, 'full_name': visitor.full_name, 'id_card_number': visitor.id_card_number, 'date_of_birth': visitor.date_of_birth} for visitor in visitors]
        return jsonify(visitor_list), 200


class ViewVisitorDetailResource(Resource):

    @role_required(['super_admin', 'admin', 'staff'])
    def get(self, visitor_id):
        visitor = Visitor.query.get(visitor_id)
        if visitor:
            visitor_info = {'id': visitor.id, 'full_name': visitor.full_name, 'id_card_number': visitor.id_card_number, 'date_of_birth': visitor.date_of_birth}
            return jsonify(visitor_info), 200
        else:
            return {'error': 'Visitor not found'}, 404


class UpdateVisitorByOCRResource(Resource):

    @login_required
    @role_required(['super_admin', 'admin', 'staff'])
    def post(self):
        # Ensure that two files are provided
        if 'file1' not in request.files or 'file2' not in request.files:
            return {'error': 'Two files are required'}, 400

        file1 = request.files['file1']
        file2 = request.files['file2']

        # Ensure that both files are images
        if not all(allowed_file(file.filename) for file in [file1, file2]):
            return {'error': 'Unsupported file type'}, 400

        try:
            # Process the first image
            text1 = self.process_image(file1)
            # Process the second image
            text2 = self.process_image(file2)

            # Extract relevant information from OCR results
            # Assuming process_ocr_result returns relevant information for updating Visitor
            visitor_info1 = process_ocr_result(text1)
            visitor_info2 = process_ocr_result(text2)

            # Ensure that the extracted information from both images match
            if visitor_info1 != visitor_info2:
                return {'error': 'Information extracted from the two images do not match'}, 400

            # Find the visitor in the database
            visitor = Visitor.query.filter_by(username=visitor_info1['username']).first()
            if visitor:
                # Update visitor information
                visitor.full_name = visitor_info1['full_name']
                visitor.id_card_number = visitor_info1['id_card_number']
                # Update other fields similarly as needed
                db.session.commit()
                return {'message': 'Visitor information updated successfully'}, 200
            else:
                return {'error': 'Visitor not found in the database'}, 404
        except Exception as e:
            return {'error': str(e)}, 500

    def process_image(self, file):
        # Open the image and perform OCR using Tesseract
        image = Image.open(file)
        text = pytesseract.image_to_string(image)
        return text

        

class VisitorsByCompanyResource(Resource):

    def get(self, user_id):
        com_no = get_com_no(user_id)
        visitors = Visitor.query.filter_by(com_no=com_no).all()

        if visitors:
            visitor_list = [{
                'id': visitor.id,
                'full_name': visitor.full_name,
                'id_card_number': visitor.id_card_number,
                'date_of_birth': visitor.date_of_birth,
                'address': visitor.address,
                'contact_details': visitor.contact_details,
                'purpose_of_visit': visitor.purpose_of_visit,
                'time_in': visitor.time_in,
                'badge_issued': visitor.badge_issued
            } for visitor in visitors]

            return jsonify(visitor_list), 200
        else:
            return {'message': 'No visitors found for company number {}'.format(com_no)}, 404
