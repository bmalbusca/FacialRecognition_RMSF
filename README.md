#   Smart Door Lock 

##  Architecture

-   Micro-service (Flask): REST End-points; Handles the interaction between the User and the Smart Door; Also, Verifies and validates the service registration

-   SmartLock (Raspberry Pi 3, PiCam, OpenCV): API Requests to send (status and camera's images data) and receive (remote operations) ; Facial Recognition with OpenCV; Circuit Lock control

-  User Client App (Flutter): Remote control; Streaming viewer  service; Event notification

```bash
.
├── App
│   ├── README.md
│   ├── android
│   │   ├── app
├── PyOpenCV
│   ├── FacialRecognition
│   │   ├── camDetect.py
│   │   ├── dataset
│   │   ├── faceRecog.py
│   │   ├── haarcascade_frontalface_default.xml
│   │   └── trainer
│   │       └── trainer.yml
│   └── environment.yml
├── README.md
└── uservice
    ├── app.yaml
    ├── database.log
    ├── main.py
    ├── requirements.txt
    └── templates
        └── index.html

```
## How to run this in your local machine?

-   Microservice (Local computer or cloud service):
        
     1.   install requirements (using `requirements.txt` and python) or just install manually the required packages
        
     2. run the application: `python3 main.py`
    
-   Facial Recogn App (Raspberry Pi 3 B+):
        
     1. install requirements (`requirements.yml`)
      
     2. run `python3 camDetect.py` to collect images (dataset). The default user is "Bruno".You can import the `Detection object` from `camDetect.py` and run it in your python console.
        
        ```
            ''' example ''' 
            
            a=Detection()                       
            a.parse_data()                      #if dataset folder exists will collect info 

            a.capture("Bruno",5, nclips=60)     #name is "Bruno", ID=5 and number of captures is 60 
        
        ```
       
        
     3. run `python3 faceRecog.py` to train and for image classification  
     
     If you notice, the `faceRecog.py` is responsable to classify the capture, sending resquests to the microservice and opening the door. In this version,  the door is simulated with a [LED circuit connected to GPIO 17](https://github.com/bmalbusca/FacialRecognition_RMSF/blob/5458f2e687a75e4a3331f75037c7bec8538f5523/PyOpenCV/FacialRecognition/faceRecog.py#L11) (Uncomment and try it). The service should the registered at the microservice,this means if the `service_id` does not exists in your microservice, the raspberry pi will not receive/send requests. 


