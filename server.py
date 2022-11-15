from flask import Flask, request, render_template, send_file
from flask_socketio import SocketIO
from subprocess import Popen, PIPE
from util.config import Config
from util.smtp import sendEmail
from threading import Thread
from eventlet import sleep, monkey_patch
from PIL import ImageOps
from PIL import Image
from json import loads
import numpy as np

app = Flask(__name__)
# app.debug = True
socketio = SocketIO(app, async_mode='eventlet')
config = Config()
ORI_SIZE = 600
IMG_SIZE = 512


def trainingTask():
    cmd = 'python train.py --name animate --batch 1 --max_iter 10 --disable_eval --no_wandb --dataroot_sketch ./input/sketch --dataroot_image ./input/image --g_pretrained ./pretrained/g_net.pth --d_pretrained ./pretrained/d_net.pth'
    p = Popen(cmd.split(' '), stdout=PIPE)
    T_maxTime = int(config.T_maxTime + .5)
    config.T_time = 0
    while p.poll() is None and not sleep(1):
        socketio.emit('progress', config.bar("Training", T_maxTime))
        config.T_time += 1
    socketio.emit('progress', config.bar("Training"))
    config.T_maxTime = (config.T_time + T_maxTime) / 2
    sleep(0.5)
    generateTask()


def generateTask():
    cmd = "python generate.py --samples 10"
    p = Popen(cmd.split(' '), stdout=PIPE)
    G_maxTime = int(config.G_maxTime + .5)
    config.G_time = 0
    while p.poll() is None and not sleep(1):
        socketio.emit('progress', config.bar("Generate", G_maxTime))
        config.G_time += 1
    socketio.emit('progress', config.bar("Generate"))
    config.G_maxTime = (config.G_time + G_maxTime) / 2
    sleep(1)

    socketio.emit("finish")


@app.route("/training", methods=['POST'])
def generate():
    data = list(map(int, loads(list(request.values.keys())[0])))
    data = np.asarray(data, np.uint8).reshape((-1, ORI_SIZE))
    img = Image.fromarray(data).resize((IMG_SIZE//2, IMG_SIZE//2))
    ImageOps.invert(img).save("./input/sketch/result.png")

    config.task = Thread(target=trainingTask)
    # config.task = Thread(target=generateTask)  # Skip use GPU

    config.task.start()
    return "OK"


@app.route("/image/<int:index>.png", methods=['GET'])
def image(index):
    file = f"./output/{index:06}.png"
    return send_file(file, mimetype='image/png')


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("generate")
def generate():
    config.task = Thread(target=generateTask)
    config.task.start()


@socketio.on("email")
def email(data):
    sendEmail(data[0], f"output/{data[1]:06}.png")


if __name__ == '__main__':
    monkey_patch()
    socketio.run(app, host="0.0.0.0", port=8080)
