#!/usr/bin/env python

# MIT License
# 
# Copyright (c) [2016] [Ross Bunker]
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
