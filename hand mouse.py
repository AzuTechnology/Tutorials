import cv2
import mediapipe as mp
import pyautogui as pg

camera = cv2.VideoCapture(1)

def Map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

while True:
    _, frame = camera.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (500, 500))
    my_hands = mp.solutions.hands
    hands = my_hands.Hands()
    draw = mp.solutions.drawing_utils
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mylist = []
            draw.draw_landmarks(frame, hand_landmarks, my_hands.HAND_CONNECTIONS)
            for id, landm in enumerate(hand_landmarks.landmark):
                h, w, _ = frame.shape
                cx, cy = int(landm.x * w), int(landm.y * h)
                mylist.append([id, cx, cy])
                x = Map(cx, 0, 500, 0, 1920)
                y = Map(cy, 0, 500, 0, 1080)
                # print(mylist)
                if id == 5:
                    # pg.FAILSAFE = False
                    pg.moveTo(int(x), int(y))

            if len(mylist) != 0:
                if mylist[12][2] > mylist[11][2]:
                    pg.click(button='right')
                else:
                    pass
                if mylist[8][2] > mylist[7][2]:
                    pg.click(button='left')
                else:
                    pass

    cv2.imshow('img',frame)
    cv2.waitKey(1)

cv2.destroyAllWindows()
camera.release()