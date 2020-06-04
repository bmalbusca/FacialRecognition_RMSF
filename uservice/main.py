#
/usr/bin/env python
from flask import Flask , redirect, url_for, request, render_template, make_response, jsonify
from flask import send_file, abort
import requests as req 
import json
from PIL import Image
from datetime import  *
import base64
from io import *
import jsonpickle 


app = Flask(__name__)
token = "12345"

# door status 
service_st = {}


class Client:
    def __init__(self, name,password, service_id, b_notification=10):
        self.name=name;
        self.password=password;
        self.serviceList=[];
        self.size_pushNotification=b_notification;
        self.nNotifications=0;
        self.pushNotification=[];
        self.addService(service_id);

    def addService(self,service_id):
        if service_id not in self.serviceList:
            self.serviceList.append(service_id)
        else:
            return 404

    def pushData(self,data):
 
        try:
            if self.pushNotification:  
                if self.nNotifications > self.size_pushNotification:
                    self.pushNotification =[]
                    self.nNotifications =0
                    
                    '''recent = self.pushNotification[size//2:]
                    self.pushNotification = recent
                    self.nNotifications -= self.size_pushNotification/2 
                    '''
            self.pushNotification.append(data)
            self.nNotifications += 1
         
            return 201
        except:
            pass  


class Database:
    def __init__(self, data={"client":[], "service":{} }):
        self.datab = data;

    #add new Service to Database
    def addService(self,id, att=None ):
        if id not in self.datab["service"]:
            self.datab["service"][id]=att;
            return 200
        else:
            return 404

    def addServiceClient(self, name, password, service_id):
        if service_id not in self.datab["service"]:
            return 400
        for cl in self.datab["client"]:
            if cl.name == name and cl.password==password:
                cl.addService(service_id)
                #self.datab["service"][service_id]=cl 
                return 200
        return 404


   # Check if Service exists and returns his status
    def findService(self,id):
        try:
            return self.datab["service"][id]
        except:
            return 404

    # Change attribution status
    def changeService(self,id,att):
        try:
            self.datab["service"][id]=att;
            return 202  #Success update
        except:
            return 404

    # Find a Client by primary keys
    def findClient(self,name, password):
        for cl in self.datab["client"]:
            if cl.name == name and cl.password==password:
                return 200
        return 404




    def insertClient(self,name, password, service_id):
        #if service_id not in self.data["service"]:
        #    return 400  #Service does not exists
        
        if (self.findService(service_id) is not None) or (self.findService(service_id) == 404) :
            return 402 #already attributed to other client

        if  self.findClient(name,password) == 200:
            return 400 
        else:
            newClient =Client(name,password, service_id)
            self.datab["client"].append(newClient)
            self.datab["service"][service_id]=newClient 
            return 200
    
    def save(self, namefile ="database.log"):
        obj=jsonpickle.encode(self.datab)
        try:
            with open(namefile, "w") as jsonFile:
                json.dump(obj, jsonFile)
        except:
            pass 
    
    def load(self, namefile ="database.log"):
        try:
            with open(namefile, "r") as jsonFile:
                file_encryp = json.load(jsonFile)
            self.datab = jsonpickle.decode(file_encryp)
        except:
            pass
    
#check if user/service is already used
def check_user(name, password, service_id):
        try: 
            if (service_id  in DB.datab["service"]):
                if (DB.datab["service"][service_id].name == name) and  (DB.datab["service"][service_id].password == password):
                    return 200
                else:
                    return 410
            else:
                return 404
        except:
            return 400




                   
DB= Database()
DB.addService("12345")
DB.addService("54321")
service_st["12345"]=0
service_st["54321"]=0

#debug user register
DB.insertClient("Edgar", "54321", "54321")



@app.errorhandler(404)
def page_not_found(e):
    return  "Sorry, end-point source not available.", 404

@app.route('/')
def index():
    return "SmartLock RMSF API V0.1"



#end-point for open the door
@app.route('/toggle/<path:subpath>', methods = ['POST'])
def toogle(subpath):
     keys = str(subpath).split("/")
     if len(keys)<4:
         abort(404)
     print("Valid header" )
     DB.load()
     if (check_user(keys[0], keys[1], keys[2]) < 400):
         if keys[3]=="on":
             service_st[keys[2]]=1
         elif keys[3]=="off":
             service_st[keys[2]]=0
     else:
         abort(404)
     return  make_response(jsonify({"info": "status flag updated"}), 200) 


#end-point query for  hardware service  (doors status)
@app.route('/door/<path>', methods = ['GET','POST'])
def door(path=None):
    dic ={}
    try:
        dic[path]=service_st[path]
        #service_st[path]=0
    except:
        abort(404)
    
    return json.dumps(dic)

#debug - service images
@app.route('/play/<service>', methods = ['GET','POST'])
def display(service): 
    listImg=[]
    print("play service "+ service )
    print( DB.datab["service"])
    if DB.datab["service"][service] is None:
        abort(404)
    listNoty = DB.datab["service"][service].pushNotification 
    try:
        for noty in listNoty:
            listImg.append(noty["image"]) 
        return render_template('index.html', data= listImg)
    
    except:
        abort(404)
    return render_template('index.html', data= listImg)



#end-point to register
@app.route('/signin/<path:subpath>', methods = ['POST'])
def signin(subpath):
    
    keys = str(subpath).split("/")
   
    if len(keys)<2 :
        return make_response(jsonify({"error": "Request is not valid "}), 400)
    DB.load()
    status = DB.findClient(keys[0],keys[1])
    
    if status == 200:
        res = make_response(jsonify({"message": "This user account exists"}), 200)
        return res
    else:
        abort(404)


    
#end-point to register
@app.route('/register/<path:subpath>', methods = ['POST','PUT'])
def register(subpath):

    
    keys = str(subpath).split("/")
    res = request.get_json()
    
    #not res or res != token 
    if len(keys)<3 :
        return make_response(jsonify({"error": "Request is not valid "}), 400)
    DB.load()
    status = DB.insertClient(keys[0],keys[1],keys[2])
    
    if status == 200:
        DB.save()
        res = make_response(jsonify({"message": "Collection add", "info":{"id":keys[2],"name": DB.datab["service"][keys[2]].name}}), status)
        return res
    elif  status == 400:
        return make_response(jsonify({"error": "This user account configuration is already used"}), status)
    elif status == 402:
        return  make_response(jsonify({"error": "This service is already attributed to other client"}), status) 

    else:
        abort(404)

#end-point to receive info 
@app.route('/get/<path:subpath>', methods = ['GET','POST','PUT'])
def get(subpath):
     keys = str(subpath).split("/")
     if len(keys)<3:
         abort(404)

     dump={}
     listNoty= None

     if (keys[2] in DB.datab["service"]) and (DB.datab["service"][keys[2]] is not None):
        if (DB.datab["service"][keys[2]].name==keys[0]) and  (DB.datab["service"][keys[2]].password==keys[1]):
            try:
                listNoty =DB.datab["service"][keys[2]].pushNotification[0]
            except:
                pass 

            dump={"notification":listNoty}
            print(dump)
        else:
            abort(404)
     else:
         abort(404)
     return  make_response(jsonify(dump), 200) 

#end-point insert data 
@app.route('/add/<path>', methods = ['PUT'])
def insert(path=None):

    print("received path " + path)
    res = request.get_json()
    data = json.loads(res)

    try:
        DB.datab["service"][path].pushData(data)
        print(DB.datab["service"][path].nNotifications) 

    except:
        abort(404)
    
    return make_response(jsonify({"message": "Collection added"}), 201)

if __name__ == '__main__':
    app.run(debug=True)
