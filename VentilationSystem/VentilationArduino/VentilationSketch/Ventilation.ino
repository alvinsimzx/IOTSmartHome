#include <Servo.h>
#include <Wire.h>
#include <dht.h>
#include <DHT.h>
#include <LiquidCrystal_I2C.h>
#define dht_apin A0 //Pin A0 to DHT11

LiquidCrystal_I2C lcd(0x27, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);
dht DHT;

Servo myservo;

int servoPin = 6;
const int pResistor = A2;

unsigned int pinStatus = 0;


//void setup
void setup() {
  lcd.begin(20, 4); // Initializes the interface to the LCD screen, and specifies the dimensions (width and height) of the display (20,4)
  lcd.backlight();

  Serial.begin(9600);

  myservo.attach(servoPin);

  pinMode(pResistor, INPUT); //for Photoresistor

  //pin for micro servo motor
  pinMode(6, OUTPUT);

}


void loop() {
  //Start of Program

  int sensorData = DHT.read11(dht_apin);
  int temperature = DHT.temperature;
  int lightIntensity = analogRead(pResistor);

  if (Serial.available() > 0)
  
  {
    pinStatus = Serial.parseInt();
    switch (pinStatus)
    {

      case 1:
        myservo.write(0); //tells servo to go back to 0 (open window)
        lcd.setCursor(0, 2);
        lcd.print("Ventilator Opened");
        break;
        
      case 2:
        myservo.write(180); //tells servo to go 180  (close window)
        lcd.setCursor(0, 2);
        lcd.print("Ventilator Closed");
        break;

    }
 
  }

  //Print temperature
  lcd.setCursor(0, 0);
  lcd.print("Temperature:");
  lcd.print(temperature);
  lcd.print(" C");

  lcd.setCursor(0, 1);
  lcd.print("Light indicator:");
  lcd.print(lightIntensity);

   //transmit data to be printed in the raspberry pi or to show at Serial Monitor

  Serial.println(String(temperature) + "," + String(lightIntensity));
  
  delay(10000);
 
}// end loop()
