from flask_pymongo import PyMongo

def get_booking_collection(mongo: PyMongo):
    return mongo.db.BookingData  # ใช้ชื่อคอลเลกชันใหม่
