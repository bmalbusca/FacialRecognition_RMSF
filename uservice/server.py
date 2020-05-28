#!/usr/bin/env python
from flask import Flask , redirect, url_for, request, render_template, make_response, jsonify
from flask import send_file
import requests as req 
import json
from PIL import Image
from datetime import  *
import base64
from io import *

app = Flask(__name__)

datab=None

def j2im(data):
    img = base64.b64decode(data['image'])
    #image = Image.open(BytesIO(imdata))
    return img 
@app.route('/')
def index():
    return "Hello"

@app.route('/download', methods = ['GET','POST'])
def video():
    filename = './User.1.edgar.1.jpg'     
    return send_file(filename, mimetype='image/jpg')

@app.route('/play/', methods = ['GET','POST'])
def display(): 
    return render_template('index.html', source=datab)


@app.route('/get/', methods = ['PUT'])
def insert():        
    
    res = request.get_json()
    dic = json.loads(res)
    print(dic["time"])
    image = j2im(dic)
    datab=image 
    print(type(image))
    return make_response(jsonify({"message": "Collection created"}), 201)

if __name__ == '__main__':
    app.run(debug=True)
