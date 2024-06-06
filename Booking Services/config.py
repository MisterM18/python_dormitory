from pymongo import MongoClient

class Config:
    MONGO_USERNAME = "inside162544"  # Your MongoDB Atlas username
    MONGO_PASSWORD = "Z03ys2w6"      # Your MongoDB Atlas password
    CLUSTER_NAME = "pythondb.piijqhq.mongodb.net"  # Your MongoDB Atlas cluster name

    # Construct the MongoDB URI
    MONGO_URI_DORMITORY = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{CLUSTER_NAME}/dormitory_db"
    MONGO_URI_BOOKING = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{CLUSTER_NAME}/BookingDB"

    # Establish MongoDB connection
    client = MongoClient(MONGO_URI_DORMITORY)
    db_dormitory = client.get_database()
    bookings_collection = db_dormitory['BookingData']
