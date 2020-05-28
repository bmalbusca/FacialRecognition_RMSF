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

datab=[]

def j2im(data_image):
    img = base64.b64decode(data_image)
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
    return render_template('index.html', data=datab)

@app.route('/img', methods = ['GET','POST'])
def img():
    #with open("./images.json", "w") as jsonFile:
    #    json.dump(datab[0], jsonFile)
    #f= open("test_images.txt","w+")
    #f.write(datab[0])

    print(datab[0])
    return json.dumps(datab)


@app.route('/get/', methods = ['PUT'])
def insert():        
    
    res = request.get_json()
    dic = json.loads(res)
    #print(dic["time"])
    #image = j2im(dic["image"])
    datab.append(dic["image"])
    

    return make_response(jsonify({"message": "Collection created"}), 201)

if __name__ == '__main__':
    app.run()
