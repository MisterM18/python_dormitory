from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from bson.objectid import ObjectId

app = FastAPI()

connection_string = "mongodb+srv://inside162544:Z03ys2w6@pythondb.piijqhq.mongodb.net/?retryWrites=true&w=majority&appName=PythonDB"
client = MongoClient(connection_string)

db = client["DormitoryDB"]
collection = db["DDB"]


class DDB(BaseModel):
    name : str
    count : int


@app.get("/")
async def root():
    return {"message": "Connected "}


@app.post("/DDB/")
async def Create_Dormitory(DDB : DDB):
    resutl = collection.insert_one(DDB.dict())
    return