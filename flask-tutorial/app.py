import collections
from flask import request
from flask import Flask, render_template
from datetime import datetime
from dotenv import load_dotenv
import os
import pymongo

load_dotenv()

MONGO_URL = os.getenv('MONGO_URL')

client = pymongo.MongoClient(MONGO_URL)

db = client.test

collections = db['flask-users']

app = Flask(__name__)


@app.route('/signup')
def hello_world():
    return render_template('signup.html')


@app.route('/')
def index():
    today = datetime.today().strftime('%A')
    return render_template('index.html', today=today)


@app.route('/submit-registration', methods=["POST"])
def submit():
    name = request.form['username']
    email = request.form['email']
    password = request.form['password']
    collections.insert_one({
        "name": name,
        "email": email,
        "password": password
    })

    return f"Signed up successfully<br> Hello {name}!<br> Your email is {email}"


@app.route('/api')
def api():
    name = request.values.get('name')
    age = request.values.get('age')
    return f"Hello, {name}! You are {age} years old!:-)"


@app.route('/view')
def view():
    data = collections.find()
    data = list(data)
    for item in data:
        print(item)
        del item['_id']
    data = {
        "data": data
    }
    return data


@app.route('/remove/<id>')
def remove(id):
    collections.delete_one({"_id": id})
    return "Deleted successfully"


if __name__ == '__main__':
    app.run(debug=True)
