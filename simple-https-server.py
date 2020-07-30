# taken from http://www.piware.de/2011/01/creating-an-https-server-in-python/
# generate server.xml with the following command:
#    openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
# run as follows:
#    python simple-https-server.py
# then in your browser, visit:
#    https://localhost:4443

import http.server
import ssl

from flask import Flask
app = Flask(__name__)

def https_server():
    httpd = http.server.HTTPServer(('localhost', 4443), http.server.SimpleHTTPRequestHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='./server3.pem', server_side=True)
    httpd.serve_forever()


@app.route('/save_data')
def hello_world():
    return 'Hello, World!'

if __name__=="__main__":
    https_server()