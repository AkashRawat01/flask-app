import collections
from flask import request, jsonify
from flask import Flask, render_template
from dotenv import load_dotenv
import os
import pymongo

load_dotenv()

IP_ADDRESS = os.getenv('IP_ADDRESS')
print(IP_ADDRESS)

MONGO_URL = os.getenv('MONGO_URL')

client = pymongo.MongoClient(MONGO_URL)

db = client.test

collections = db['flask-users']

app = Flask(__name__)


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
    return jsonify(data)


@app.route('/remove/<id>')
def remove(id):
    collections.delete_one({"_id": id})
    return "Deleted successfully"


if __name__ == '__main__':
    app.run(host=IP_ADDRESS, port=9000, debug=True)
