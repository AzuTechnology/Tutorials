import cv2
import dlib
import numpy as np


detector = dlib.get_frontal_face_detector()
def MyRec(rgb,x,y,w,h,v=20,color=(200,0,0),thikness =2):
    """To draw stylish rectangle around the objects"""
    cv2.line(rgb, (x,y),(x+v,y), color, thikness)
    cv2.line(rgb, (x,y),(x,y+v), color, thikness)

    cv2.line(rgb, (x+w,y),(x+w-v,y), color, thikness)
    cv2.line(rgb, (x+w,y),(x+w,y+v), color, thikness)

    cv2.line(rgb, (x,y+h),(x,y+h-v), color, thikness)
    cv2.line(rgb, (x,y+h),(x+v,y+h), color, thikness)

    cv2.line(rgb, (x+w,y+h),(x+w,y+h-v), color, thikness)
    cv2.line(rgb, (x+w,y+h),(x+w-v,y+h), color, thikness)
# to detect faces from video
def read_video():
    cam =cv2.VideoCapture(1)
    while True:
        _,frame =cam.read()
        frame = cv2.flip(frame,1)
        
        gray =cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        # detect the face
        for face in faces:
            x1 =face.left()
            y1 =face.top()
            x2 = face.right()
            y2 = face.bottom()
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)

        cv2.imshow('img',frame)
        key = cv2.waitKey(1)
        if key ==ord('q'):
            break

win = np.zeros((500,800,3),np.uint8)
def faces():
    frame =cv2.imread('img.jpg')
    frame =cv2.resize(frame,(800,500))
    gray =cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    # detect the face
    for face in faces:
        x1 =face.left()
        y1 =face.top()
        x2 = face.right()
        y2 = face.bottom()
        MyRec(frame, x1, y1, x2 - x1, y2 - y1, 20, (200,200,255), 6)
        cv2.rectangle(win,(x1,y1),(x2,y2),(0,255,0),-1)
    frame =  cv2.addWeighted(frame,1,win,0.3,0)

    cv2.imshow('img',frame)
    cv2.waitKey(0)

faces()
# read_video()