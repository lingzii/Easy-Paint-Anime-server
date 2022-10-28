from flask import Flask, request, render_template
from flask_socketio import SocketIO
from json import loads
from PIL import Image
from PIL import ImageOps
import numpy as np

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)
IMG_SIZE = 512


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=['POST'])
def generate():
    data = list(map(int, loads(list(request.values.keys())[0])))
    data = np.asarray(data, np.uint8).reshape((1160, 1160))
    img = Image.fromarray(data).resize((IMG_SIZE, IMG_SIZE))
    img = ImageOps.invert(img)
    img.save("./input/sketch/result.png")
    return "200"


@socketio.on('test')
def test(data):
    print('foo')
    print(len(data))


if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=8080)
    # app.run(host="0.0.0.0", port=8080)
