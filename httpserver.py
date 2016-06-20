#!/usr/bin/env python

from flask import Flask, request, send_file
import os

app = Flask(__name__)

# The /index route returns a JSON object reflecting the most recently read tags received through the TCP connection
@app.route('/index', methods=['POST', 'GET'])
def index():
    output = ""
    with open("reads.json", "r") as f:
        for line in f.readlines():
            output += line + "\n"
    return output

# The /picture route returns a picture corresponding to the name posted. The name should be the epc value of the tag
@app.route('/picture', methods=['POST'])
def return_pic():
    name = request.form['name']
    name = name + ".png"
    directory = os.path.join(os.getcwd(), 'database', 'pictures')
    try:
        return send_file(os.path.join(directory, name))
    except IOError:
        return send_file(os.path.join(directory, 'default.png'))
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
