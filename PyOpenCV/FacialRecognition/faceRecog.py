import cv2
import numpy as np
from PIL import Image
import os
import requests as req 
import json
from datetime import  *
import base64
#import gpiozero  # The GPIO library for Raspberry Pi
import time  # Enables Python to manage timing
 
#led = gpiozero.LED(17) # Reference GPIO17
class ImageRecogn:
    def __init__(self,path = 'dataset'):
        # Path for face image database
        self.path = 'dataset'
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");
        self.names =  { 0:'none'}

    # function to get the images and label data
    def getImagesAndLabels(self,path):

        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
        faceSamples=[]
        ids = []
        names = []

        for imagePath in imagePaths:
            try:
                PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
                img_numpy = np.array(PIL_img,'uint8')

                id = int(os.path.split(imagePath)[1].split(".")[1])
                name = str(os.path.split(imagePath)[1].split(".")[2])
        
                faces = self.detector.detectMultiScale(img_numpy)

                for (x,y,w,h) in faces:
                    faceSamples.append(img_numpy[y:y+h,x:x+w])
                    ids.append(id)
                    names.append(name)
            except:
                print('*Alert* Fail to read '+ imagePath)
        return faceSamples,ids,names


    def fit(self):
        print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
        faces,ids,names = self.getImagesAndLabels(self.path)
        self.recognizer.train(faces, np.array(ids))

        for i in range(1, len(np.unique(ids)) + 1):
    
            index = ids.index(i) 
            self.recognizer.setLabelInfo(i, str(names[index]))  
        
        # Save the model into trainer/trainer.yml
        self.recognizer.write('trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi    
        # Print the numer of faces trained and end program
        print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))



    def getLabels(self, max=100):

        print("Getting labels %i \n" %(max))
        for i in range(1, max):
            retval = self.recognizer.getLabelInfo(i)
            if retval == "":
                print('*Alert* empty labels')
                break
            else:
                self.names[i]=retval

    def classify(self,id,confidence=101):
        # Check if confidence is less them 100 ==> "0" is perfect match
        if (confidence < 65):
            label = self.names[id]
        elif (confidence > 65 and confidence < 101):
            label = str(self.names[id]) + " no match"
        else:
            label  = "unknown"

        return label 
            



    def preditct(self):
        
        self.recognizer.read('trainer/trainer.yml')
        font = cv2.FONT_HERSHEY_SIMPLEX
        _historic={}
        delta=0
        #iniciate id counter
        id = 0
        # names related to ids: example ==> Marcelo: id=1,  etc
        self.getLabels(100)

        # Initialize and start realtime video capture
        cam = cv2.VideoCapture(0)
        cam.set(3, 640) # set video widht
        cam.set(4, 480) # set video height
        # Define min window size to be recognized as a face
        minW = 0.1*cam.get(3)
        minH = 0.1*cam.get(4)

        while True:
            ret, img =cam.read()
            img = cv2.flip(img, 1) # Flip vertically
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            
            faces = self.detector.detectMultiScale(
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(minW), int(minH)),
            )

            for(x,y,w,h) in faces:

                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                id, confidence = self.recognizer.predict(gray[y:y+h,x:x+w])
                label = self.classify(id,confidence)
                time=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                time_com=datetime.now()
               
                
                if _historic and  (label in _historic):
                    delta = (time_com - _historic[label])
                    if (delta.total_seconds() > 10):
                        try:
                            #led.on() # Turn the LED on
                            print("Preparing to send: " + label)
                            _historic={label:time_com}
                            _, imdata = cv2.imencode('.JPG',img)
                            jpac = json.dumps({"image": base64.b64encode(imdata).decode('utf-8'), "time":time, "token":12345, "name":label})
                            try:
                                req.put("http://127.0.0.1:5000/add/12345", headers = {'Content-type': 'application/json'}, json=jpac)
                            except:
                                pass 
                        except:
                            pass 

                if not _historic:
                    try:
                        led.on() # Turn the LED on
                        print("Preparing to send 2: " + label)
                        _historic={label:time_com}
                        _, imdata = cv2.imencode('.JPG',img)
                        jpac = json.dumps({"image": base64.b64encode(imdata).decode('utf-8'), "time":time, "token":12345, "name":label})
                        try:
                            req.put("http://127.0.0.1:5000/add/12345", headers = {'Content-type': 'application/json'}, json=jpac)
                        except:
                            pass

                    except:
                        pass

                #time.sleep(1)
                #led.off() # Turn the LED off

                try:
                    door=req.get("http://127.0.0.1:5000/door/12345").text
                    print("DOOR: ", door)
                    if(door["door"]>0):
                         led.on() # Turn the LED 
                         time.sleep(1)
                         led.off()
                            

                except:
                    pass 

                cv2.putText(img, label, (x+5,y-5), font, 1, (255,255,255), 2)
                confidence = "  {0}%".format(confidence)
                cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)

            cv2.imshow('camera',img)
    
            k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                break

        # Do a bit of cleanup
        print("\n [INFO] Exiting Program and cleanup stuff")
        cam.release()
        cv2.destroyAllWindows()
        




a=ImageRecogn()
#a.fit()
a.preditct()
