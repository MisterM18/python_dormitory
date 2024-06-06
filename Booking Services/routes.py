from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from config import Config
from bson import ObjectId

booking_bp = Blueprint('booking_bp', __name__)

client = MongoClient(Config.MONGO_URI_BOOKING)
db = client.get_database()
collection = db['BookingCollection']

@booking_bp.route('/bookings', methods=['GET'])
def get_bookings():
    bookings = list(collection.find())
    return jsonify(bookings)

@booking_bp.route('/bookings', methods=['POST'])
def create_booking():
    booking_data = request.json
    result = collection.insert_one(booking_data)
    return jsonify({"message": "Booking created", "id": str(result.inserted_id)}), 201

@booking_bp.route('/bookings/<string:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    result = collection.delete_one({"_id": ObjectId(booking_id)})
    if result.deleted_count == 1:
        return jsonify({"message": "Booking deleted"}), 200
    else:
        return jsonify({"error": "Booking not found"}), 404
