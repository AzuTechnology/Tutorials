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
  one.write(90);
  two.write(90);
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
      
}
