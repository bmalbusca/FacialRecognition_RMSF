import cv2 
# opencv-python-headless
# opencv-contrib-python
# opencv-python


video_capture = cv2.VideoCapture(0)
while True:
    ret, frame = video_capture.read()
    cv2.imshow('Video', frame)
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
