import cv2
from tkinter import *
from PIL import Image, ImageTk
import time
import mediapipe as mp
from collections import deque

win = Tk()
win.geometry("670x670+300+30")
color = "#581845"

frame_1 = Frame(win, width=670, height=670, bg=color).place(x=0, y=0)

def to_pil(img, label, x, y, w, h):
    image = Image.fromarray(img)
    iago = ImageTk.PhotoImage(image)
    label.configure(image=iago)
    label.image = iago
    label.place(x=x, y=y,width =w,height=h)

prev_time =0

def FPS():
    global prev_time
    current_time = time.time()
    fps = 1/(current_time-prev_time)
    prev_time = current_time
    return fps

label1 = Label(frame_1)
camera = cv2.VideoCapture(1)
label2 = Label(frame_1,bg=color,fg='white',font=('Arial',11))
label2.place(x=10,y=550)

rpoints = [deque(maxlen=512)]

def paint(frame,rpoints):
    points = [rpoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                cv2.line(frame, points[i][j][k - 1], points[i][j][k], (100, 0, 255), 2)

def run():
    _, frame = camera.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (600,500))
    my_hands = mp.solutions.hands
    hands = my_hands.Hands()
    draw = mp.solutions.drawing_utils
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # draw.draw_landmarks(frame, hand_landmarks, my_hands.HAND_CONNECTIONS)
            for id, landm in enumerate(hand_landmarks.landmark):
                h, w, _ = frame.shape
                cx, cy = int(landm.x * w), int(landm.y * h)
                label2['text'] = 'x = '+str(cx)+' '+'y = '+str(cy)
                if hand_landmarks !=0:
                    if id ==8:
                        rpoints[0].append((cx, cy))
                        cv2.circle(frame, (cx, cy), 3, (250, 250, 0), 6)

    paint(frame,rpoints)
    # fps = FPS()
    # cv2.putText(frame, 'FPS = ' + str(int(fps)), (10, 100), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    to_pil(rgb,label1,10,10,600,500)
    label1.after(30,run)

run()
win.mainloop()
cv2.destroyAllWindows()
camera.release()