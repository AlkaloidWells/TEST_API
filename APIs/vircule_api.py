from flask import redirect, request, url_for
from flask import request, jsonify, session
from flask_restful import Resource
from models import  Vehicle
from extentions import db
from PIL import Image
from Modules.ocr.ocr import *
from APIs.auth import login_required, role_required

class VehicleResource(Resource):
    @login_required
    @role_required('user')
    def post(self):
        data = request.get_json()
        com_no = data.get('com_no')
        plate_number = data.get('plate_number')
        make = data.get('make')
        model = data.get('model')
        color = data.get('color')
        owner_details = data.get('owner_details')
        entry_time = data.get('entry_time')
        exit_time = data.get('exit_time')
        flagged_as_suspicious = data.get('flagged_as_suspicious', False)

        new_vehicle = Vehicle(
            com_no=com_no,
            plate_number=plate_number,
            make=make,
            model=model,
            color=color,
            owner_details=owner_details,
            entry_time=entry_time,
            exit_time=exit_time,
            flagged_as_suspicious=flagged_as_suspicious
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



class UpdateViruleByOCRResource(Resource):
    def post(self):
        # Process OCR scan and update visitor information
        # Replace this with your OCR processing logic
        return {'message': 'Visitor information updated by OCR scan'}, 200