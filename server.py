import json
from flask import Flask, request, render_template
app = Flask(__name__, static_url_path='', static_folder="static")


@app.route('/')
def main_page():
    return app.send_static_file("./main.html")

@app.route('/save-data', methods=['POST'])
def save_data():
    pupil_data = request.json

    with open("./analysis/pupil_data.json", "w") as f:
        json.dump(pupil_data, f)

    return "200"


if __name__ == "__main__":
    app.run(ssl_context='adhoc') # this line for local deployment
    # app.run()                  # this line for zappa cloud deployment 