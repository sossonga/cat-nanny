from flask import Flask, request

import catnanny

app = Flask(__name__)
app.config['CLIENT_VIDEOS'] = '/home/pi/cat-nanny/'

@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/feed')
def feed():
    catnanny.foodservo()
    return ''


@app.route('/play')
def play():
    catnanny.playservo()
    return ''


@app.route('/treat')
def treat():
    catnanny.treatservo()
    return ''


@app.route('/read_db/<sensor>')
def read_db():
    catnanny.query(sensor)
    return ''


@app.route('/login')
def login():
    # check if entered credentials match an entry in DB
    data = request.get_json()
    print(data)
    email = data['email']
    password = data['password']
    catnanny.login(email, password)
    return 'Lookup Successful!'


@app.route('/signup')
def signup(email, password):
    # insert entered credentials into DB
    catnanny.signup(email, password)
    return 'Signup Successful!'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
