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
        new_vehicle = Vehicle(
            plate_number=data['plate_number'],
            make=data['make'],
            model=data['model'],
            color=data['color'],
            owner_details=data['owner_details'],
            entry_time=data['entry_time'],
            exit_time=data.get('exit_time'),  # It's optional, so use get() method
            flagged_as_suspicious=data.get('flagged_as_suspicious', False)  # Default to False if not provided
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