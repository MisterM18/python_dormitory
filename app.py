from dotenv import load_dotenv , find_dotenv
import os
import pprint
from pymongo import MongoClient
load_dotenv(find_dotenv())


password = os.environ.get("MONGODB_PWD")

connection_string = "mongodb+srv://inside162544:Z03ys2w6@dbdormitory.rahvfxt.mongodb.net/?retryWrites=true&w=majority&appName=DBDormitory"
client = MongoClient(connection_string)

dbs = client.list_database_names()
DBdormitory = client.DBdormitory
collections = DBdormitory.list_collection_names()
print(collections)


## สำหรับสร้าง DB กับ Collection in MONGODB และ Collction
Dormitory = client.Dormitory
person_collcetion = Dormitory.person_collection

def create_documents():
    name_dm = ["dormitory1","dormitory2","dormitory3","dormitory4","dormitory5"]
    address = ["bangkok","thai","thai","thai","thai"]
    rent = ["8000","10000","9000","6000","7000"]

    docs = []

    for name_dm,address,rent in zip(name_dm,address,rent):
        doc = {"name_dm":name_dm,"address":address,"rent":rent}
        docs.append(doc)
        # person_collcetion.insert(doc)
    person_collcetion.insert_many(docs)

create_documents()   

from flask import Flask, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a secret key for session management

@app.route('/')
def index():
    if 'id' not in session:
        return render_template('index.html', logged_in=False)
    else:
        return render_template('index.html', logged_in=True, username=session['username'])

# Define a new route for the page you want to redirect to
@app.route('/other_page')
def other_page():
    # You can render a template for this page if needed
    return render_template('dormitory.html')

if __name__ == '__main__':
    app.run(debug=True)
