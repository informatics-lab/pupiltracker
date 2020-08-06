import boto3
import json
from flask import Flask, request, render_template, make_response
import time
import random
import os

app = Flask(__name__, static_url_path='', static_folder="static")


@app.route('/')
def main_page():
    return app.send_static_file("./landing.html")


@app.route('/get-image-url', methods=['GET'])
def get_an_image_url():
    subdomain = request.headers.get('subdomain')

    s3_client = boto3.client('s3')
    if subdomain != "localhost":
        response = s3_client.list_objects_v2(Bucket=subdomain, Prefix="images/")
        imgs = response["Contents"][1:] # strip off the folker itsself
        img = random.choice(imgs)
        url = "https://"+subdomain+".s3.eu-west-2.amazonaws.com/" + img["Key"]
    else:
        imgs = os.listdir("./static/test_images")
        img = random.choice(imgs)
        url = "test_images/" + img
    return make_response(url)


@app.route('/save-data', methods=['POST'])
def save_data():
    subdomain = request.headers.get('subdomain')

    file_name = time.strftime("%Y%m%d%H%M%S") + ".json"
    pupil_data = request.json

    if subdomain != "localhost":
        with open("/tmp/"+file_name, "w") as f:
            json.dump(pupil_data, f)
            s3_client = boto3.client('s3')
            s3_client.upload_file("/tmp/"+file_name, subdomain, "tracking_data/"+file_name)   
    else:
        with open("/tmp/"+file_name, "w") as f:
            json.dump(pupil_data, f)
    
    return "200"


if __name__ == "__main__":
    app.run()