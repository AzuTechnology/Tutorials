import mediapipe as mp
import cv2
from tkinter import *
from PIL import Image, ImageTk

win = Tk()
win.geometry("750x800+400+30")

color = "#581845"
frame_1 = Frame(win, width=750, height=800, bg=color).place(x=0, y=0)
show_ind = Label(frame_1, bg="#581845", fg='white', font=('Times New Roman', 20, 'bold'))
show_ind.place(x=620, y=150)
button = Button(frame_1, text="Print")

label1 = Label(frame_1)
show_ind = Label(frame_1, bg="#581845", fg='white', font=('Times New Roman', 20, 'bold'))
show_ind.place(x=10, y=700)

result =Label(win,bg='blue',fg='white',font=('Arial',20,'bold'))
result.place(x=20,y=600,width=300,height=50)
##############
def clean():
    result['text'] = ""
############
clear = Button(frame_1, text="clear", command=clean)
clear.place(x=400, y=600)

################################
def to_pil(img, label, x, y, w, h):
    img = cv2.resize(img, (w, h))
    image = Image.fromarray(img)
    pic = ImageTk.PhotoImage(image)
    label.configure(image=pic)
    label.image = pic
    label.place(x=x, y=y)
################################
b = 500
def rows(rgb):
    for y in range(1, 6):
        cv2.line(rgb, (100, y * 70), (b, y * 70), (0, 0, 0), 2)

def cols(rgb):
    for x in range(1, 6):
        cv2.line(rgb, (x * 100, 70), (x * 100, b - 150), (0, 0, 0), 2)
################################
def cal(num):
    result['text'] += str(num)
    show_ind['text'] = str(num)
    c = show_ind['text']
    if c == '=':
        for l in result['text']:
            if l == '-':
                num1 = str(result["text"]).split("-")
                # print(num1)
                # print(num1[0], num1[1][0])
                result["text"] = str(float(num1[0]) - float(num1[1][0]))
            if l == 'x':
                num2 = str(result["text"]).split("x")
                result["text"] = str(float(num2[0]) * float(num2[1][0]))
            if l == '/':
                num3 = str(result["text"]).split("/")
                result["text"] = str(float(num3[0]) / float(num3[1][0]))

            if l == '+':
                num4 = str(result["text"]).split("+")
                result["text"] = str(float(num4[0]) + float(num4[1][0]))

counter = 0
def show_rec(rgb, x, y):
    global counter
    time = 30
    col = [100, 200, 300, 400,500]
    row = [70, 140, 220, 290, 360,430]
    index_col_one = '1', '4', '7', '.'
    index_col_two = '2', '5', '8', '0'
    index_col_three = '3', '6', '9', '='
    index_col_four ='+','-','x','/'

    # col one
    color =(0, 0, 0)
    size =0.90
    for i in range(0, 4):
        cv2.putText(rgb, str(index_col_one[i]), (145, row[i] + 40), cv2.FONT_HERSHEY_TRIPLEX, size, color)
        if (x > col[0] and x < col[1]) and (y > row[i] and y  < row[i] + 70):
            if (x  > col[0] and x  < col[1]) and (y > row[i] and y < row[i] + 70):
                counter += 1
                if counter >= time:
                    cal(index_col_one[i])
                    counter = 0
            else:
                counter = 0

    # col two
    for i in range(0, 4):
        cv2.putText(rgb, str(index_col_two[i]), (245, row[i] + 40), cv2.FONT_HERSHEY_TRIPLEX, size, color)
        if (x  > col[1] and x  < col[2]) and (y > row[i] and y < row[i] + 70):
            if (x > col[1] and x < col[2]) and (y > row[i] and y < row[i] + 70):
                counter += 1
                if counter >= time:
                    cal(index_col_two[i])
                    counter = 0
            else:
                counter = 0

    # col three
    for i in range(0, 4):
        cv2.putText(rgb, str(index_col_three[i]), (345, row[i] + 40), cv2.FONT_HERSHEY_TRIPLEX, size, color)
        if (x > col[2] and x < col[3]) and (y > row[i] and y < row[i] + 70):
            if (x > col[2] and x< col[3]) and (y > row[i] and y< row[i] + 70):
                counter += 1
                if counter >= time:
                    cal(index_col_three[i])
                    counter = 0
            else:
                counter = 0
    # col four
    for i in range(0, 4):
        cv2.putText(rgb, str(index_col_four[i]), (445, row[i] + 40), cv2.FONT_HERSHEY_TRIPLEX, size, color)
        if (x > col[3] and x < col[4]) and (y > row[i] and y < row[i] + 70):
            if (x > col[3] and x < col[4]) and (y > row[i] and y < row[i] + 70):
                counter += 1
                if counter >= time:
                    show_ind['text'] = str(index_col_four[i])
                    result['text'] += str(index_col_four[i])
                    counter = 0
            else:
                counter = 0

#################################

cap = cv2.VideoCapture(1)
def display():
    _, img = cap.read()
    img = cv2.flip(img, 1)
    img = cv2.resize(img, (700, 500))
    my_hands = mp.solutions.hands
    hands = my_hands.Hands()
    draw = mp.solutions.drawing_utils
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    cols(rgb)  
    rows(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mylist = []
            # draw.draw_landmarks(rgb, hand_landmarks, my_hands.HAND_CONNECTIONS)
            for id, landm in enumerate(hand_landmarks.landmark):
                h, w, _ = rgb.shape
                cx, cy = int(landm.x * w), int(landm.y * h)
                if id == 8:
                    show_rec(rgb, cx, cy)
                    cv2.circle(rgb, (cx, cy), 10, (255, 0, 0), -1)

    to_pil(rgb, label1, 10, 10, 700, 500)
    win.after(20, display)

display()
win.mainloop()
cv2.destroyAllWindows()
cap.release()

