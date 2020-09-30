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

