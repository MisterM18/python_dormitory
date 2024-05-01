from flask import Flask, render_template, request, url_for, jsonify
from pymongo import MongoClient
from bson import ObjectId


app = Flask(__name__)

# เชื่อมต่อ MongoDB
connection_string = "mongodb+srv://inside162544:Z03ys2w6@pythondb.piijqhq.mongodb.net/?retryWrites=true&w=majority&appName=PythonDB"
client = MongoClient(connection_string)

ITEMS_PER_PAGE = 100


@app.route("/")
def index():
    # ดึงข้อมูลจากฐานข้อมูล MongoDB
    db = client["DormitoryDB"]
    collection = db["DDB"]

    # ค่าหน้าปัจจุบัน
    page = request.args.get("page", default=1, type=int)

    # ดึงข้อมูลของหน้านั้นๆ และหน้าทั้งหมด
    skip = (page - 1) * ITEMS_PER_PAGE
    items = collection.find().skip(skip).limit(ITEMS_PER_PAGE)
    total_items = collection.count_documents({})
    total_pages = total_items // ITEMS_PER_PAGE + (
        1 if total_items % ITEMS_PER_PAGE != 0 else 0
    )

    # ดึงข้อมูลทั้งหมด
    data = collection.find({}, {"name": 1, "imageUrl": 1, "price": 1, "address": 1})

    # สร้าง URL สำหรับแต่ละรายการ
    item_urls = [url_for("other_page", item_id=str(item["_id"])) for item in data]

    # ส่งข้อมูลไปยังเทมเพลต
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




@app.route("/other_page/<item_id>")
def other_page(item_id):
    # ดึงข้อมูลจากฐานข้อมูล MongoDB โดยใช้ item_id เพื่อค้นหารายการที่เกี่ยวข้อง
    db = client["DormitoryDB"]
    collection = db["DDB"]
    item = collection.find_one(
        {"_id": ObjectId(item_id)}
    )  # ใช้ ObjectId เพื่อแปลง item_id เป็น ObjectId

    # ส่งข้อมูลไปยังเทมเพลต other_page.html เพื่อแสดงรายละเอียดของรายการนั้น
    return render_template("other_page.html", item=item)


# use for ADD Data in Database from Object_id #


@app.route("/dormitory-add-post", methods=["POST"])
def dormitory_add_post():
    try:
        data = request.json

        # Access JSON fields using keys
        name = data["name"]
        imageUrl = data["imageUrl"]
        address = data["address"]
        price = data["price"]
        description = data["description"]
        contact = data["contact"]

        # Create a dictionary to store the data
        dormitory_data = {
            "name": name,
            "imageUrl": imageUrl,
            "address": address,
            "price": price,
            "description": description,
            "contact": contact,
        }

        # Connect to the MongoDB database and collection
        db = client["DormitoryDB"]
        collection = db["DDB"]

        # Insert the document into the MongoDB collection
        result = collection.insert_one(dormitory_data)

        if result.inserted_id:
            return (
                jsonify(
                    {
                        "message": "Data inserted successfully",
                        "id": str(result.inserted_id),
                    }
                ),
                200,
            )
        else:
            return jsonify({"error": "Failed to insert data"}), 500
    except KeyError as e:
        # Handle missing fields
        error_message = f"Missing required field: {e}"
        return jsonify({"error": error_message}), 400


# use for Detele Data base from Object_id #


@app.route(
    "/Dormitory-delete/<string:id>", methods=["DELETE"]
)  # Specify the type of id parameter
def Dormitory_delete(id):
    try:
        # Connect to the MongoDB database and collection
        db = client["DormitoryDB"]
        collection = db["DDB"]

        # Convert the id string to ObjectId
        object_id = ObjectId(id)

        # Delete the document with the given ObjectId
        result = collection.delete_one({"_id": object_id})

        # Check if the document was successfully deleted
        if result.deleted_count == 1:
            return (
                jsonify({"message": "Data deleted successfully", "id": id}),
                200,
            )
        else:
            return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# use for update Data base from Object_id#


@app.route("/Dormitory-update/<string:id>", methods=["PUT"])
def Dormitory_update(id):
    try:
        # Connect to the MongoDB database and collection
        db = client["DormitoryDB"]
        collection = db["DDB"]

        # Convert the id string to ObjectId
        object_id = ObjectId(id)

        # Get the update data from the request
        update_data = request.json

        # Update the document with the given ObjectId
        result = collection.update_one({"_id": object_id}, {"$set": update_data})

        # Check if the document was found and updated
        if result.modified_count == 1:
            return (
                jsonify({"message": "Data updated successfully", "id": id}),
                200,
            )
        else:
            return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
