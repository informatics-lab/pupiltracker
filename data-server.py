import json
from flask import Flask, request
from flask_cors import cross_origin
app = Flask(__name__)


@app.route('/', methods=['GET'])
def hi():
    print("hello world")
    return "200"


@app.route('/save-data', methods=['POST'])
@cross_origin()
def save_data():
    viewport = request.headers["viewport"]
    pupil_data = request.json

    with open("./analysis/pupil_data.json", "w") as f:
        json.dump(pupil_data, f)

    with open("./analysis/viewport.json", "w") as f:
        json.dump(viewport, f)

    return "200"


if __name__ == "__main__":
    app.run()