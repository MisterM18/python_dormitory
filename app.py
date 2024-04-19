from dotenv import load_dotenv, find_dotenv
import os 
import pprint
from pymongo import MongoClient
load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb+srv://inside162544:{password}@dbdormitory.wvpb5mt.mongodb.net/?retryWrites=true&w=majority&appName=DBDormitory"

dbs = client.list.database_names()
PythonDB = client.test
print(dbs)


# from flask import Flask, render_template, session, redirect, url_for

# app = Flask(__name__)
# app.secret_key = 'your_secret_key_here'  # Set a secret key for session management

# @app.route('/')
# def index():
#     if 'id' not in session:
#         return render_template('index.html', logged_in=False)
#     else:
#         return render_template('index.html', logged_in=True, username=session['username'])

# # Define a new route for the page you want to redirect to
# @app.route('/other_page')
# def other_page():
#     # You can render a template for this page if needed
#     return render_template('dormitory.html')

# if __name__ == '__main__':
#     app.run(debug=True)
