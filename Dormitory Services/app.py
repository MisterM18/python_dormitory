from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
from config import Config
from routes import dormitory_bp
import os

app = Flask(__name__)

# Load config from environment variables
app.config["MONGO_URI_DORMITORY"] = os.getenv("MONGO_URI_DORMITORY", Config.MONGO_URI_DORMITORY)

# Connect to MongoDB
client = MongoClient(app.config["MONGO_URI_DORMITORY"])

ITEMS_PER_PAGE = 100

@app.route("/")
def index():
    db = client["DormitoryDB"]
    collection = db["DDB"]

    page = request.args.get("page", default=1, type=int)
    skip = (page - 1) * ITEMS_PER_PAGE
    items = collection.find().skip(skip).limit(ITEMS_PER_PAGE)
    total_items = collection.count_documents({})
    total_pages = total_items // ITEMS_PER_PAGE + (1 if total_items % ITEMS_PER_PAGE != 0 else 0)

    data = collection.find({}, {"name": 1, "imageUrl": 1, "price": 1, "address": 1})
    item_urls = [url_for("other_page", item_id=str(item["_id"])) for item in data]

    return render_template(
        "index.html",
        items=items,
        item_urls=item_urls,
        total_pages=total_pages,
        current_page=page,
    )

@app.route("/add-data")
def add_data_page():
    return render_template("add-data.html")

@app.route("/update")
def update():
    db = client["DormitoryDB"]
    collection = db["DDB"]
    items = collection.find({}, {"name": 1, "price": 1, "address": 1, "imageUrl": 1, "description": 1, "contact": 1})
    return render_template("update.html", items=items)

@app.route("/other_page/<item_id>")
def other_page(item_id):
    db = client["DormitoryDB"]
    collection = db["DDB"]
    item = collection.find_one({"_id": ObjectId(item_id)})

    return render_template("other_page.html", item=item)

@app.route("/dormitory-add-post", methods=["POST"])
def dormitory_add_post():
    try:
        data = request.json
        required_fields = ["name", "imageUrl", "address", "price", "description", "contact"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        dormitory_data = {
            "name": data["name"],
            "imageUrl": data["imageUrl"],
            "address": data["address"],
            "price": data["price"],
            "description": data["description"],
            "contact": data["contact"],
            "numberOfRoomsAvailable": data.get("numberOfRoomsAvailable", 0)
        }

        db = client["DormitoryDB"]
        collection = db["DDB"]
        result = collection.insert_one(dormitory_data)

        if result.inserted_id:
            return jsonify({"message": "Data inserted successfully", "id": str(result.inserted_id)}), 200
        else:
            return jsonify({"error": "Failed to insert data"}), 500
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {e}"}), 400

@app.route("/Dormitory-delete/<string:id>", methods=["DELETE"])
def Dormitory_delete(id):
    try:
        db = client["DormitoryDB"]
        collection = db["DDB"]
        object_id = ObjectId(id)
        result = collection.delete_one({"_id": object_id})

        if result.deleted_count == 1:
            return jsonify({"message": "Data deleted successfully", "id": id}), 200
        else:
            return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/Dormitory-update/<string:id>", methods=["PUT"])
def Dormitory_update(id):
    try:
        db = client["DormitoryDB"]
        collection = db["DDB"]
        object_id = ObjectId(id)
        update_data = request.json
        result = collection.update_one({"_id": object_id}, {"$set": update_data})

        if result.modified_count == 1:
            return jsonify({"message": "Data updated successfully", "id": id}), 200
        else:
            return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/update_item/<item_id>", methods=["GET", "POST"])
def update_item(item_id):
    db = client["DormitoryDB"]
    collection = db["DDB"]
    if request.method == "GET":
        item = collection.find_one({"_id": ObjectId(item_id)})
        if item:
            return render_template("update_form.html", item=item)
        else:
            return "Item not found"
    elif request.method == "POST":
        try:
            if request.form.get("action") == "delete":
                result = collection.delete_one({"_id": ObjectId(item_id)})
                if result.deleted_count == 1:
                    return redirect(url_for('update'))
                else:
                    return "Failed to delete item"
            else:
                updated_data = {
                    "name": request.form["name"],
                    "price": int(request.form["price"]),
                    "address": request.form["address"],
                    "imageUrl": request.form["imageUrl"],
                    "description": request.form["description"],
                    "contact": request.form["contact"],
                    "numberOfRoomsAvailable": int(request.form["numberOfRoomsAvailable"])
                }
                result = collection.update_one({"_id": ObjectId(item_id)}, {"$set": updated_data})
                if result.modified_count == 1:
                    return redirect(url_for('update'))
                else:
                    return "Failed to update item"
        except Exception as e:
            return f"Error: {str(e)}"

app.register_blueprint(dormitory_bp)

if __name__ == "__main__":
    app.run(debug=True)
