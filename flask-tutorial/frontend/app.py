import requests
from flask import request
from flask import Flask, render_template
from datetime import datetime
import collections

app = Flask(__name__)

BACKEND_URL = 'http://0.0.0.0:9000'


@app.route('/signup')
def hello_world():
    return render_template('signup.html')


@app.route('/')
def index():
    today = datetime.today().strftime('%A')
    return render_template('index.html', today=today)


@app.route('/submit-registration', methods=['POST'])
def submit():
    name = request.form['username']
    email = request.form['email']
    password = request.form['password']

    requests.post(BACKEND_URL + '/submit-registration',
                  data={"username": name, "email": email, "password": password})

    return 'Data submitted successfully'


@app.route('/get-data')
def get_data():
    response = requests.get(BACKEND_URL + '/view')

    return response.json()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
