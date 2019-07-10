from flask import Flask, send_from_directory

import main

#UPLOAD_FOLDER = '/usr/pi/cat-nanny/'

app = Flask(__name__)
app.config['CLIENT_VIDEOS'] = '/home/pi/cat-nanny/'

@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/feed')
def feed():
    main.foodservo()
    return ''


@app.route('/play')
def play():
    main.playservo()
    return ''


@app.route('/treat')
def treat():
    main.treatservo()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
