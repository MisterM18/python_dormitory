from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel

app = FastAPI()

connection_string = "mongodb+srv://inside162544:Z03ys2w6@pythondb.piijqhq.mongodb.net/?retryWrites=true&w=majority&appName=PythonDB"
client = MongoClient(connection_string)

db = client["DormitoryDB"]
collection = db["DDB"]  # Ensure this matches your collection name


class DormitoryDB(BaseModel):
    name: str
    imageUrl: str
    address: str
    price: int
    description: str
    contact: str  # Changed to str for phone number


@app.get("/")
async def root():
    return {"message": "Hello world"}


@app.post("/DormitoryDB/")
async def create_dormitory(dormitory: DormitoryDB):
    result = collection.insert_one(dormitory.dict())  # Corrected method name to dict()
    return {
        "Id": str(result.inserted_id),
        "name": dormitory.name,
        "imageUrl": dormitory.imageUrl,
        "address": dormitory.address,
        "price": dormitory.price,
        "description": dormitory.description,
        "contact": dormitory.contact
    }
