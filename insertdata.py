from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Connection URI
uri = os.getenv("MONGODB_URI")

# Create a new MongoClient
connection_string = "mongodb+srv://inside162544:Z03ys2w6@pythondb.piijqhq.mongodb.net/?retryWrites=true&w=majority&appName=PythonDB"
client = MongoClient(connection_string)


# Define the database and collection
db = client["DormitoryDB"]
collection = db["DDB"]

# Define the list of documents to insert
dormitories = [
    {
        "name": "HappyHouse",
        "imageUrl": "https://example.com/image.jpg",
        "address": "Bangkok Thailand 10120",
        "price": "15000",
        "description": "This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.",
    },
    {
        "name": "CoolingHouse",
        "imageUrl": "https://example.com/image.jpg",
        "address": "Nakhon Pathom Thailand 10122",
        "price": "200000",
        "description": "This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.",
    },
    # Add other documents here
]

# Insert documents into the collection
result = collection.insert_many(dormitories)

# Output the number of documents inserted
print(f"Inserted {len(result.inserted_ids)} documents")


connection_string = "mongodb+srv://inside162544:Z03ys2w6@pythondb.piijqhq.mongodb.net/?retryWrites=true&w=majority&appName=PythonDB"
client = MongoClient(connection_string)
