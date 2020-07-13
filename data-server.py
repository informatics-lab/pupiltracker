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
    my_json = request.json
    path = "./pupil_data.json"

    with open(path, "w") as f:
        json.dump(my_json, f)
    return "200"


if __name__ == "__main__":
    app.run()