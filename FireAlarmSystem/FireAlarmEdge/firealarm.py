import MySQLdb
import serial
import time
import datetime
import sys
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import json

arduino = serial.Serial('/dev/ttyACM0', 9600)

def on_connect(client, data, flags, rc):
    client.subscribe("v1/devices/me/rpc/request/+")

def on_message(client, data, msg):
    print("Topic: " +msg.topic + '\nMessage: ' + str(msg.payload))
    if msg.topic.startswith('v1/devices/me/rpc/request/'):
        requestId = msg.topic[len('v1/devices/me/rpc/request/'):len(msg.topic)]
        print("requestId : ",requestId)
        data = json.loads(msg.payload)
        
        
        arduino.write(data['method'].encode())
            
        


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("Im7nj5WmL4TGY2eOwsiS")
client.connect("thingsboard.cloud",1883,60)


while 1:
    client.loop_start()
    waterspinklermotor = True;
 
            
    #Receive the data from arduino
    data = arduino.readline()
    print(data)
    temp,smoke = data.decode().split(",")
        
    temp = int(temp)
    smoke = int(smoke)     
    print(temp, smoke)
    
    publish.single(topic="v1/devices/me/telemetry",
                   payload= '{"TemperatureValue":'+str(temp)+',"SmokeValue":'+str(smoke)+'}',
                   hostname="thingsboard.cloud", auth={'username':"Im7nj5WmL4TGY2eOwsiS", 'password':""})
    
    thresholdResult = None
    
    currenttime = datetime.datetime.now()
        
    #actuator triggered
    #if(temp<=threshold_temp and smoke<=threshold_smoke): 
        #arduino.write(b"normaltemp_and_normalsmokevalue\n")
        
    
    #elif(temp<=threshold_temp and smoke>=threshold_smoke):
        #arduino.write(b"normaltemp_and_highsmokevalue\n")
        
    
    #elif(temp>=threshold_temp and smoke<=threshold_smoke):
        #arduino.write(b"hightemp_and_normalsmokevalue\n")
        
        
    #elif(temp>=threshold_temp and smoke>=threshold_smoke):
        #arduino.write(b"hightemp_and_highsmokevalue\n")
        
    time.sleep(8)
    

        
                
    


                 