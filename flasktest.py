from multiprocessing import Process

from flask import Flask, request, jsonify, Response

import catnanny

app = Flask(__name__)
app.config['CLIENT_VIDEOS'] = '/home/pi/cat-nanny/'

@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/servo')
def servo():
    servo_type = request.args.get('type')
    print("Testing")
    process = Process(target=catnanny.servo, args=(servo_type,))
    process.start()
    return Response('', status=200)


@app.route('/read_db')
def read_db():
    sensor = request.args.get('sensor')
    #process = Process
    motion = False
    result = str(catnanny.query(sensor))
    print(result)
    print(type(result))
    if sensor == 'temperature':
        return Response(
            result,
            status=200)
    else:
        if result == 1:
            motion = True
            return Response(
                motion,
                status=200)
        else:
            return Response(
                '',
                status=200)


@app.route('/stats')
def get_stats():
    stat = request.args.get('stat')
    result_stat = str(catnanny.stat_query(stat)[0])
    return Response(
        result_stat,
        status=200)


@app.route('/login', methods=['GET','POST'])
def login():
    # check if entered credentials match an entry in DB
    data = request.get_json()
    email = data['email']
    password = data['password']
    login = catnanny.login(email, password)
    account_exists = False
    if login == 1:
        account_exists = True

    response = jsonify({'account_exists': account_exists})

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
