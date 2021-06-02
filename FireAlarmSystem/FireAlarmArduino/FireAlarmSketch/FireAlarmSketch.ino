#include <Servo.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <stdio.h>

#define MQ2pin A1;
#define temperatureMeter A0;
 

LiquidCrystal_I2C lcd(0x27, 20, 4);
Servo Myservo;
int buzzerPin = 12;
int redLED = 8;
int yellowLED = 9;
int blueLED = 10;

//float temp;
int tempvalue = 0;
int smokeValue = 0;

bool buzzleToggle;
bool watersprinkleToggle;
char buffer[30];

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
  //LCD Display
  lcd.begin();
  lcd.backlight();
  lcd.setCursor(0,0);
  delay(1000);
 
  buzzleToggle = true;
  watersprinkleToggle = true;
  //Servo motor
  Myservo.attach(2);

  Myservo.write(0);

  //Buzzer and LED
  pinMode(buzzerPin, OUTPUT);
  pinMode(redLED,OUTPUT);
  pinMode(yellowLED, OUTPUT);
  pinMode(blueLED,OUTPUT);
  delay(500);

}

void loop() {
  // put your main code here, to run repeatedly:
  
  tempvalue = map(analogRead(A0),0,1023,0,200);

  //Gas sensor
  smokeValue = analogRead(A1);
  
  
  sprintf(buffer, "%02d,%02d",tempvalue,smokeValue);
  Serial.println(buffer);
  delay(500);
  
  if(Serial.available()>0){

    String case_command = Serial.readStringUntil('\n');
      if(case_command == "normaltemp_and_normalsmokevalue")
      {
         
          lcd.setCursor(0,1);
          lcd.print("     NO SMOKE   ");
          noTone(buzzerPin);
          digitalWrite(redLED,LOW);
          digitalWrite(yellowLED, LOW);
          digitalWrite(blueLED,HIGH);
      }
      else if(case_command == "normaltemp_and_highsmokevalue")
      {
       
          lcd.setCursor(0,1);
          lcd.print("SMOKE DETECTED!!!");
          digitalWrite(redLED,LOW);
          digitalWrite(yellowLED,HIGH);
          digitalWrite(blueLED,LOW);
      }
      else if(case_command == "hightemp_and_normalsmokevalue")
      {
        
          lcd.setCursor(0,1);
          lcd.print("    NO SMOKE    ");
          digitalWrite(redLED,LOW);
          digitalWrite(yellowLED,HIGH);
          digitalWrite(blueLED,LOW);
      }
      else if(case_command == "hightemp_and_highsmokevalue")
      {
          if(buzzleToggle == true)
          {
            tone(buzzerPin,800);
          }
          if(watersprinkleToggle == true)
          {
             Myservo.write(180);
          }
            delay(900);    
        
            noTone(buzzerPin);
            Myservo.write(0);
      
            
          if(buzzleToggle != true)
          {
            noTone(buzzerPin);
          }
          if(watersprinkleToggle != true)
          {
               Myservo.write(0);
          }
          delay(1000);
    
          lcd.setCursor(0,1);
          lcd.print("SMOKE DETECTED!!");
          digitalWrite(redLED,HIGH);
          digitalWrite(yellowLED,LOW);
          digitalWrite(blueLED,LOW);
      }
       
      else if(case_command == "open_buzzer")
      {
           buzzleToggle = true;
           tone(buzzerPin,800);
      }
      else if(case_command == "open_watersprinkle")
      {
           watersprinkleToggle = true;
         
              Myservo.write(180);
            
              delay(1000);    
        
              Myservo.write(0); 
      }
      
      else if(case_command == "close_buzzer")
      {
           buzzleToggle = false;
           delay(900);    
           noTone(buzzerPin);
      }
      else if(case_command == "close_watersprinkle")
      {
           watersprinkleToggle = false;  
           if(watersprinkleToggle != true)
            {
              Myservo.write(0);
            }
            delay(1000);  
      }
      else if(case_command == "redLED")
      {
          digitalWrite(redLED,HIGH);
          digitalWrite(yellowLED,LOW);
          digitalWrite(blueLED,LOW);
      }

      else if(case_command == "yellowLED")
      {
          digitalWrite(redLED,LOW);
          digitalWrite(yellowLED,HIGH);
          digitalWrite(blueLED,LOW);
      }

      else if (case_command == "blueLED")
      {
        
          digitalWrite(redLED,LOW);
          digitalWrite(yellowLED,LOW);
          digitalWrite(blueLED,HIGH);
      }
  }
  delay(10000);
}
