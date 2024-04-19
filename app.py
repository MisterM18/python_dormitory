from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# เชื่อมต่อ MongoDB
connection_string = "mongodb+srv://inside162544:Z03ys2w6@pythondb.piijqhq.mongodb.net/?retryWrites=true&w=majority&appName=PythonDB"
client = MongoClient(connection_string)

@app.route('/')
def index():
    # ดึงข้อมูลจากฐานข้อมูล MongoDB
    db = client['DormitoryDB']
    collection = db['DDB']
    data = collection.find({}, {'_id': 0, 'name': 1, 'price': 1, 'address': 1})  # ดึงเฉพาะฟิลด์ที่ต้องการ
    
    # ส่งข้อมูลไปยังเทมเพลต
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
