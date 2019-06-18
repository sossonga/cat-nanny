from flask import Flask, send_from_directory

import main
import videocap

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

@app.route('/video/<video_name>')
def vid(video_name):
    #videocap.videocap()
    return send_from_directory(app.config['CLIENT_VIDEOS'], filename=video_name, as_attachment=True)
    #try:
    #    videocap.videocap()
    #    return send_from_directory(app.config['CLIENT_VIDEOS'], filename=image_name, as_attachment=True)
    #except FileNotFoundError:
    #    abort(404)


@app.route('/treat')
def treat():
    main.treatservo()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
