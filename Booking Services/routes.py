from flask import Blueprint, request, jsonify, current_app
from .models import get_booking_collection

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/add', methods=['POST'])
def add_booking():
    data = request.get_json()
    booking_collection = get_booking_collection(current_app.mongo)
    booking_collection.insert_one(data)
    return jsonify({"message": "Booking added successfully!"}), 201

@booking_bp.route('/all', methods=['GET'])
def get_all_bookings():
    booking_collection = get_booking_collection(current_app.mongo)
    bookings = booking_collection.find()
    booking_list = []
    for booking in bookings:
        booking_list.append(booking)
    return jsonify(booking_list), 200
