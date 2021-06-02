int LED1 = 4;
int LED2 = 5;
int LED3 = 6;
int LED4 = 7;
int trigPin = 10;    // Trigger
int echoPin = 9;    // Echo
char buffer[30];
int diningRoom, kitchen, bedRoom, livingRoom;
long duration, cm, inches;
int photoResistor = A0;
int analogValue = 0;
int datafromUser = 0;

void setup() {
  Serial.begin(9600);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);
  pinMode(LED4, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  analogValue = analogRead(photoResistor);
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  cm = duration*0.034/2;
  livingRoom = digitalRead(LED1);
  bedRoom = digitalRead(LED2);
  kitchen = digitalRead(LED3);
  diningRoom = digitalRead(LED4);
  sprintf(buffer,"%03d %03ld %d %d %d %d", analogValue, cm, livingRoom, bedRoom, kitchen, diningRoom);
  if(Serial.available() > 0){
    datafromUser = Serial.read();
    if(datafromUser == '1'){
      digitalWrite(LED1, !digitalRead(LED1));
    }
    if(datafromUser == '2'){
      digitalWrite(LED2, !digitalRead(LED2));
    }
    if(datafromUser == '3'){
      digitalWrite(LED3, !digitalRead(LED3));
    }
    if(datafromUser == '4'){
      digitalWrite(LED4, !digitalRead(LED4));
    }
    if(datafromUser == '0'){
      digitalWrite(LED1, LOW);
      digitalWrite(LED2, LOW);
      digitalWrite(LED3, LOW);
      digitalWrite(LED4, LOW);
    }
    if(datafromUser == '5'){
      digitalWrite(LED1, HIGH);
      digitalWrite(LED2, HIGH);
      digitalWrite(LED3, HIGH);
      digitalWrite(LED4, HIGH);
    }
  }
  Serial.println(buffer);
  delay(10000);
}
