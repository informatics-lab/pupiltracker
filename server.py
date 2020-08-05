import boto3
import json
from flask import Flask, request, render_template
import time

app = Flask(__name__, static_url_path='', static_folder="static")


@app.route('/')
def main_page():
    return app.send_static_file("./main.html")

@app.route('/save-data', methods=['POST'])
def save_data():
    file_name = time.strftime("%Y%m%d%H%M%S") + ".json"

    pupil_data = request.json
    with open("/tmp/"+file_name, "w") as f:
        json.dump(pupil_data, f)
    
    s3_client = boto3.client('s3')
    s3_client.upload_file("/tmp/"+file_name, "pupiltracking", "tracking_data/"+file_name)
    print("tracking_data"+file_name)
    
    return "200"


if __name__ == "__main__":
    app.run()