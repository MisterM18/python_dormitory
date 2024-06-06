from flask import Blueprint, jsonify, request, render_template
from pymongo import MongoClient
from bson import ObjectId
from config import Config

dormitory_bp = Blueprint('dormitory', __name__)

# MongoDB Connection
client = MongoClient(Config.MONGO_URI_DORMITORY)
db = client['DormitoryDB']
collection = db['DDB']

@dormitory_bp.route('/')
def index():
    # Example route for Dormitory Service
    items = collection.find({}, {"name": 1, "imageUrl": 1, "price": 1, "address": 1})
    return render_template('index.html', items=items)

@dormitory_bp.route('/dormitory-add-post', methods=['POST'])
def dormitory_add_post():
    data = request.json
    dormitory_data = {
        'name': data['name'],
        'imageUrl': data['imageUrl'],
        'address': data['address'],
        'price': data['price'],
        'description': data['description'],
        'contact': data['contact'],
        'numberOfRoomsAvailable': data.get('numberOfRoomsAvailable', 0)
    }
    result = collection.insert_one(dormitory_data)
    if result.inserted_id:
        return jsonify({'message': 'Data inserted successfully', 'id': str(result.inserted_id)}), 200
    else:
        return jsonify({'error': 'Failed to insert data'}), 500

# Define other routes as necessary
@dormitory_bp.route('/book-room/<item_id>', methods=['POST'])
def book_room(item_id):
    try:
        db = client["DormitoryDB"]
        collection = db["DDB"]
        item = collection.find_one({"_id": ObjectId(item_id)})

        if item['numberOfRoomsAvailable'] > 0:
            new_room_count = item['numberOfRoomsAvailable'] - 1
            collection.update_one(
                {"_id": ObjectId(item_id)},
                {"$set": {"numberOfRoomsAvailable": new_room_count}}
            )
            return jsonify({"message": "Room booked successfully"}), 200
        else:
            return jsonify({"error": "No rooms available"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
