from flask import Flask, request, render_template
from flask_socketio import SocketIO
from json import loads
from PIL import Image
import numpy as np
import os

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)
IMG_SIZE = 1024


@app.route("/")
def index():
    return render_template("index.html")


# @app.route("/generate", methods=['POST'])
# def generate():
#     val = list(request.values.keys())[0]
#     data = np.asarray(list(map(int, loads(val))), np.uint8)
#     img = Image.fromarray(data.reshape(IMG_SIZE, IMG_SIZE))

    # def scaleDown(image, size):
    #     image = image.resize((size, size), Image.Resampling.LANCZOS)
    #     if size == 28:
    #         return image
    #     pixels = image.load()
    #     for i in range(size):
    #         for j in range(size):
    #             if pixels[i, j] != 0:
    #                 pixels[i, j] = 255
    #     return image

    # for i in [512, 256, 128, 28]:
    #     img = scaleDown(img, i)

    # img.save("result.png")

    # img = np.asarray(img).reshape(1, 28, 28, 1)
    # result = model.predict(img).argmax()
    # print(result)

    # return f"{result}"


@socketio.on('test')
def test(data):
    print(type(data))


if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=8080)
    # app.run(host="0.0.0.0", port=80)
