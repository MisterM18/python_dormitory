import os

class Config:
    MONGO_URI_DORMITORY = os.getenv("MONGO_URI_DORMITORY", "default_connection_string")
