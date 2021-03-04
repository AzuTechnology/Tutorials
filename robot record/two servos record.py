import serial  #pyserial
from tkinter import *
import pandas as pd
import xlrd
from xlutils.copy import copy


file = "value.xls"
rd = xlrd.open_workbook(file)
wb = copy(rd)
w_sheet = wb.get_sheet(0)
w_sheet.write(0,0,"servo_one")
w_sheet.write(0,1,"servo_two")
data = pd.read_excel(file)

win = Tk()
win.geometry("400x200")
win.configure(bg="gray")
ser = serial.Serial('COM3', '9600',timeout=5)
var1 = IntVar()
var2 = IntVar()
W = 150
x_axis = Scale(win, label="x-axis", from_=0, to=180, orient=HORIZONTAL, variable=var1, activebackground='#339999')
x_axis.set(2)
x_axis.place(x=10, y=10, width=W)

y_axis = Scale(win, label="y-axis", from_=0, to=180, orient=HORIZONTAL, variable=var2, activebackground='#339999')
y_axis.set(2)
y_axis.place(x=10, y=100, width=W)

counter =0
def send():
    global counter
    counter +=1
    w_sheet.write(counter, 0, str(x_axis.get()))
    w_sheet.write(counter, 1, str(y_axis.get()))
    ser.write(('a'+str(x_axis.get())+'b'+str(y_axis.get())).encode('utf-8'))
    win.after(100,send)
    wb.save(file)

def send_from_file():
    global counter
    counter +=1
    servo_one = data["servo_one"].tolist()
    servo_two = data["servo_two"].tolist()
    if counter >= len(servo_one):
        counter =0
    ser.write(('a'+str(servo_one[counter])+'b'+str(servo_two[counter])).encode('utf-8'))
    win.after(10,send_from_file)

# send()
send_from_file()
win.mainloop()

#Arduino code:
"""
#include<Servo.h>
Servo one;
Servo two;
char ch;
int val;
void setup() 
{
  Serial.begin(9600);
  one.attach(4);
  two.attach(2);
}

void loop() 
{
  if (Serial.available()) 
  {
   ch=Serial.read();
   val =Serial.parseInt();
    
    if(ch =='a'){
      one.write(val);
      }

     if(ch =='b'){
        two.write(val);
     }

    }
      
}"""