from flask import Flask, render_template, request, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
4
# เชื่อมต่อ MongoDB
connection_string = "mongodb+srv://inside162544:Z03ys2w6@pythondb.piijqhq.mongodb.net/?retryWrites=true&w=majority&appName=PythonDB"
client = MongoClient(connection_string)

ITEMS_PER_PAGE = 6


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


if __name__ == "__main__":
    app.run(debug=True)
