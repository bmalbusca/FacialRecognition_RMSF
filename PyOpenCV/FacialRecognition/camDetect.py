''''
Capture multiple Faces from multiple users to be stored on a DataBase (dataset directory)
        ==> Faces will be stored on a directory: dataset/ (if does not exist, pls create one)
        ==> Each face will have a unique numeric integer ID as 1, 2, 3, etc                       

Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    

Developed by Marcelo Rovai - MJRoBot.org @ 21Feb18    

'''

import cv2
import os
import time 

class Detection: 
    def __init__(self, model='haarcascade_frontalface_default.xml'):
        self.model = model;
        self.image= {"color":'grey',"scale":1.3, "min_neighbors":5, "local":"./dataset/" } 
        self.nclasses=None;
        self.classes={};


    def parse_data(self):
        if not (os.path.exists("dataset/")):
            print(" dataset folder does not exits\n")
            exit(0)
        for data in os.listdir("dataset/"):
            filename = data.split(".")
            try:
                self.classes[filename[1]]['size']+= 1 
            except:
                try:
                    self.classes[filename[1]]={'size':1,'name':filename[2]}
                except:
                    pass

        self.nclasses = len(self.classes)
        #print(self.classes)

    def updateData(self,face_id,face_name):
        if not self.classes:
            self.parse_data()
 
        #try: 
        if (self.classes[str(face_id)]['name'] == face_name):
            self.capture(face_name, str(face_id))
        else:
            print("*ERROR* this id and label name does not match.")
            print(self.classes[str(face_id)]['name']," diff > " ,face_name )
        #except:
        #    print("*ERROR* This id not exists.")



    def capture(self,face_name, face_id=None, nclips=80):
        cam = cv2.VideoCapture(0)
        cam.set(3, 640) # set video width
        cam.set(4, 480) # set video height

        face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
        if face_id == None:
            print("New training label")
            face_id = self.nclasses+1
            for face_id in range(self.nclasses+1,100,1):
                if str(face_id) not in self.classes:                 #string_name in data:
                    break
            if self.nclasses>99:
                print("Data set indexes number was exceeded\n")
                exit(0)
            count=0
        else:
            try:
                print("Updating " + "User." + str(face_id) + '.' + str(face_name)  )
                count=self.classes[str(face_id)]["size"]+1 
                print(count , " clips")
            except:
                print("*ERROR* Check the input arguments, they can be wrong")
                exit(0)
        string_name = "User." + str(face_id) + '.' + str(face_name)  
        print("\n [INFO] Initializing face capture. Look the camera and wait ...")
        #Initialize individual sampling face count
    

        i=count 
        while(True):

            ret, img = cam.read()
            img = cv2.flip(img, 1) # flip video image vertically
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)


            for (x,y,w,h) in faces:

                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
                i += 1

                # Save the captured image into the datasets folder
                # cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
                # -----------------------------------------------------
                wstatus=cv2.imwrite("dataset/User." + str(face_id) + '.' + str(face_name) + '.' + str(i) + ".jpg", gray[y:y+h,x:x+w])
                # -----------------------------------------------------
                if wstatus is False:
                    print("Issue found at Saving data");


                cv2.imshow('image', img)

            k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                break
            elif i >= count + nclips: # Take 80 face sample and stop video ( quantos mais melhor )
                break

          #Do a bit of cleanup
        print("\n [INFO] Exiting Program and cleanup stuff")
        cam.release()
        cv2.destroyAllWindows() 

''' example ''' 
a=Detection()
a.parse_data()
#a.updateData(5, 'bruno')
a.capture("Bruno", nclips=90)


