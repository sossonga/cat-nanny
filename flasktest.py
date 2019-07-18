from flask import Flask, request, jsonify

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


@app.route('/read_db')
def read_db():
    sensor = request.args.get('sensor')
    print(sensor)
    return str(catnanny.query(sensor))
    #return ''


@app.route('/login', methods=['GET','POST'])
def login():
    # check if entered credentials match an entry in DB
    data = request.get_json()
    email = data['email']
    password = data['password']
    login = catnanny.login(email, password)
    print(login)
    print(jsonify(login))
#    return jsonify(login)
    account_exists = False
    if login == 1:
        account_exists = True

    response = jsonify({'account_exists': account_exists})
    print(response.data)

    return response


@app.route('/signup')
def signup():
    # insert entered credentials into DB
    data = request.get_json()
    email = data['email']
    password = data['password']
    catnanny.signup(email, password)
    return 'Signup Successful!'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
