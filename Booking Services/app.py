from flask import Flask
from flask_pymongo import PyMongo
from config import Config
from .routes import booking_bp

app = Flask(__name__)


from pymongo import MongoClient

# ใช้ URI ของ MongoDB Atlas
connection_string = "mongodb+srv://inside162544:Z03ys2w6@pythondb.piijqhq.mongodb.net/?retryWrites=true&w=majority&appName=PythonDB"
client = MongoClient(connection_string)


# เลือกฐานข้อมูล
db = client["BookingDB"]
collection = db["BookingData"]

# ตัวอย่างการเพิ่มข้อมูล
data = {"key": "value"}
collection.insert_one(data)

app.config["MONGO_URI"] = Config.MONGO_URI_BOOKING

mongo = PyMongo(app)

app.register_blueprint(booking_bp, url_prefix='/booking')

if __name__ == '__main__':
    app.run(port=5002, debug=True)
