# app_booking/__init__.py

from flask import Blueprint

bp = Blueprint('booking', __name__)

from app import routes
