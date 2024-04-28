from flask import redirect, request, url_for
from flask import request, jsonify, session
from flask_restful import Resource
from models import Visitor
from extentions import db
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
        if 'file' not in request.files:
            return {'error': 'No file provided'}, 400

        file = request.files['file']

        if file.filename == '':
            return {'error': 'No file selected'}, 400
        if file and allowed_file(file.filename):
            try:
                image = Image.open(file)
                text = pytesseract.image_to_string(image)

                username, password = process_ocr_result(text)

                visitor = Visitor.query.filter_by(username=username).first()
                if visitor:
                    visitor.password = password
                    db.session.commit()
                    return {'message': 'User information updated by OCR scan'}, 200
                else:
                    return {'error': 'User not found'}, 404
            except Exception as e:
                return {'error': str(e)}, 500
        else:
            return {'error': 'Unsupported file type'}, 400
        

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
