
#include <dht.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h> 
#include <Stepper.h> 

#define STEPS 2038 

int waterSensorVal = 0;
int soilMoistureVal = 0 ;
int ldrVal = 0;

//Initialise sensor variables 
LiquidCrystal_I2C lcd(0x27,20,4);
dht DHT;
char buffer[30];
Servo servoWater;
Stepper stepper(STEPS, 8, 10, 9, 11);

void setup() {
  //Initialise servos and stepper motor
  servoWater.attach(6);
  Serial.begin (9600);
  servoWater.write(145); 
  stepper.setSpeed(10); 
  
  // Initialise LCD Screen
  lcd.init();
  lcd.clear();         
  lcd.backlight();
  lcd.setCursor(1,0);
  lcd.print("Plant Watering");
  lcd.setCursor(1,1);
  lcd.print("System");
  delay(3500);
  lcd.clear(); 
  
  
}

void loop() {
  //Get Sensor Data values and add into buffer to be outputted
  soilMoistureVal = analogRead(A1);
  ldrVal = analogRead(A3);
  soilMoistureVal = map(soilMoistureVal,550,0,0,100);
  ldrVal = map(ldrVal,0,1023,0,100);
  DHT.read11(A2);
  sprintf(buffer, "Readings: %02d, %02d, %02d, %02d",int(round(DHT.temperature)),int(round(DHT.humidity)),soilMoistureVal,ldrVal);
  Serial.println(buffer);

  //Show Sensor data values in LCD screen
    lcd.setCursor(1,0);
    lcd.print("SM:");
    lcd.print(soilMoistureVal);
    
    lcd.setCursor(1,1);
    lcd.print("H:");
    lcd.print(int(round(DHT.humidity)));
    lcd.print("%");
    
    lcd.setCursor(8,1);
    lcd.print("T:");
    lcd.print(int(round(DHT.temperature)));
    lcd.print("C");

    //Check for commands sent from Pi to activate actuators
    if (Serial.available()>0) {
      // check for incoming serial data
      String command = Serial.readStringUntil('\n');  // read command from serial port
      if (command == "low_moisture") {  // turn on watering system
          servoWater.write(0);
          delay(5000);
          servoWater.write(145);
      }else if (command == "high_sunlight"){//Open Shade
          delay(1000);
          stepper.step(-2038);
          delay(1000);
          stepper.step(-2038);
      }else if(command == "low_sunlight"){// Close Shade
          stepper.step(2038);
          delay(1000);
          stepper.step(2038);
      }
   }
   delay(10000);
}
