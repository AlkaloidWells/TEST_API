from flask import redirect, request, url_for
from flask import request, jsonify, session
from flask_restful import Resource
from models import  Vehicle
from extentions import db
from PIL import Image
from Modules.ocr.ocr import *
from API.auth import login_required, role_required, get_user_id, get_com_no

class VehicleResource(Resource):
    @login_required
    @role_required(['super_admin', 'admin' 'staff'])
    def post(self):
        data = request.get_json()
        
        plate_number = data.get('plate_number')
        make = data.get('make')
        model = data.get('model')
        color = data.get('color')
        owner_details = data.get('owner_details')
        entry_time = data.get('entry_time')
        exit_time = data.get('exit_time')
        flagged_as_suspicious = data.get('flagged_as_suspicious', False)
        
        user_id =get_user_id()
        com_no = get_com_no(user_id)

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
    @role_required(['super_admin', 'admin' 'staff'])
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
    @role_required(['super_admin', 'admin' 'staff'])
    def delete(self, vehicle_id):
        vehicle = Vehicle.query.get(vehicle_id)
        if vehicle:
            db.session.delete(vehicle)
            db.session.commit()
            return {'message': 'Vehicle deleted successfully'}, 200
        else:
            return {'error': 'Vehicle not found'}, 404



class ViewVehiclesResource(Resource):
    @role_required(['super_admin', 'admin' 'staff'])
    def get(self):
        vehicles = Vehicle.query.all()
        vehicle_list = [{'id': vehicle.id, 'plate_number': vehicle.plate_number, 'make': vehicle.make, 'model': vehicle.model, 'color': vehicle.color} for vehicle in vehicles]
        return jsonify(vehicle_list), 200


class ViewVehicleDetailResource(Resource):
    @login_required
    @role_required(['super_admin', 'admin' 'staff'])
    def get(self, vehicle_id):
        vehicle = Vehicle.query.get(vehicle_id)
        if vehicle:
            vehicle_info = {'id': vehicle.id, 'plate_number': vehicle.plate_number, 'make': vehicle.make, 'model': vehicle.model, 'color': vehicle.color}
            return jsonify(vehicle_info), 200
        else:
            return {'error': 'Vehicle not found'}, 404



class UpdateViruleByOCRResource(Resource):
    @login_required
    @role_required(['super_admin', 'admin' 'staff'])
    def post(self):
        # Process OCR scan and update visitor information
        # Replace this with your OCR processing logic
        return {'message': 'Visitor information updated by OCR scan'}, 200
    

class VehiclesByCompanyResource(Resource):
    @login_required
    @role_required(['super_admin', 'admin' 'staff'])
    def get(self, user_id):
        
        com_no = get_com_no(user_id)
        vehicles = Vehicle.query.filter_by(com_no=com_no).all()

        # Check if vehicles were found
        if vehicles:
            # Serialize the vehicle data
            vehicle_list = [{
                'id': vehicle.id,
                'plate_number': vehicle.plate_number,
                'make': vehicle.make,
                'model': vehicle.model,
                'color': vehicle.color,
                'owner_details': vehicle.owner_details,
                'entry_time': vehicle.entry_time,
                'exit_time': vehicle.exit_time,
                'flagged_as_suspicious': vehicle.flagged_as_suspicious
            } for vehicle in vehicles]

            # Return the serialized vehicle data as JSON
            return jsonify(vehicle_list), 200
        else:
            # Return a message indicating no vehicles were found for the given company number
            return {'message': 'No vehicles found for company number {}'.format(com_no)}, 404
