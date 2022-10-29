from socket import socket
from flask import Flask, request, render_template
from flask_socketio import SocketIO
from subprocess import Popen, PIPE
from util.config import Config
from threading import Thread
from eventlet import sleep, monkey_patch
from PIL import ImageOps
from PIL import Image
from json import loads
import numpy as np


app = Flask(__name__)
app.debug = True
socketio = SocketIO(app, async_mode='eventlet')
config = Config()
IMG_SIZE = 512


def generateTask():
    cmd = "python generate.py --samples 1"
    p = Popen(cmd.split(' '), stdout=PIPE)
    T_maxTime = int(config.T_maxTime + 1)
    config.T_time = 0
    while p.poll() is None and not sleep(1):
        socketio.emit('progress', ["Training", config.T_time, T_maxTime])
        config.T_time += 1
    socketio.emit('progress', ["Training", T_maxTime, T_maxTime])
    config.T_maxTime = (config.T_time + T_maxTime) / 2
    sleep(1)

    cmd = "python generate.py --samples 1"
    p = Popen(cmd.split(' '), stdout=PIPE)
    G_maxTime = int(config.G_maxTime + 1)
    config.G_time = 0
    while p.poll() is None and not sleep(1):
        socketio.emit('progress', ["Generate", config.G_time, G_maxTime])
        config.G_time += 1
    socketio.emit('progress', ["Generate", G_maxTime, G_maxTime])
    config.G_maxTime = (config.G_time + G_maxTime) / 2
    sleep(1)

    socketio.emit("finish", None)


@app.route("/generate", methods=['POST'])
def generate():
    data = list(map(int, loads(list(request.values.keys())[0])))
    data = np.asarray(data, np.uint8).reshape((1160, 1160))
    img = Image.fromarray(data).resize((IMG_SIZE, IMG_SIZE))
    ImageOps.invert(img).save("./input/sketch/result.png")

    task = Thread(target=generateTask)
    task.start()

    return "OK"


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on('test')
def test(data):
    print('foo')
    print(len(data))


if __name__ == '__main__':
    monkey_patch()
    socketio.run(app, debug=False, host="0.0.0.0", port=8080)
    # print("------- Server running -------")
    # app.run(host="0.0.0.0", port=8080)
