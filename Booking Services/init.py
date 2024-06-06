from flask import Flask
from flask_pymongo import PyMongo
from config import Config

app = Flask(__name__)
app.config["MONGO_URI_DORMITORY"] = Config.MONGO_URI_DORMITORY
mongo_dormitory = PyMongo(app, uri="MONGO_URI_DORMITORY")
app.config["MONGO_URI_BOOKING"] = Config.MONGO_URI_BOOKING
mongo_booking = PyMongo(app, uri="MONGO_URI_BOOKING")

from app import routes
