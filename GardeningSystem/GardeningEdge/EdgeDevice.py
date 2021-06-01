import serial
import sys
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json

shadeOpened = True #Shade is opened at initial state

def on_connect(client, data, flags, rc):
    client.subscribe("v1/devices/me/rpc/request/+") #Subscribe to RPC Request topic to look for actuator comands

def on_message(client, data, msg):
    global shadeOpened;
    print("Topic: " +msg.topic + '\nMessage: ' + str(msg.payload))
    if msg.topic.startswith('v1/devices/me/rpc/request/'): #Only get RPC Messages
        data = json.loads(msg.payload)
        
        #Based on received command, perform the following
        if(data['method']=='low_moisture'):
            arduino.write(b"low_moisture\n")
        elif((data['method']=='high_sunlight') and shadeOpened):
            arduino.write(b"high_sunlight\n")
            shadeOpened = False;
        elif((data['method']=='low_sunlight') and not shadeOpened):
            arduino.write(b"low_sunlight\n")
            shadeOpened = True;
        elif(data['method']=='open_shade'):
            arduino.write(b"low_sunlight\n")
            shadeOpened = True;
        elif(data['method']=='close_shade'):
            arduino.write(b"high_sunlight\n")
            shadeOpened = False;
        print("Shade:",shadeOpened)  #For Debugging  

arduino = serial.Serial('/dev/ttyACM0',9600) #Arduino serial connection
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.username_pw_set('WfWAqasNS1Aq6W4mzU3R') #Connect to thingsboard for topic subscription
client.connect("thingsboard.cloud", 1883, 60)

def main():
    client.loop_start()
    while True:
        while(arduino.in_waiting == 0):
             pass
        
        #Read Serial data sent by Arduino and split it
        line = arduino.readline()
        data = str(line).split(":")[1].split(",")
        Temp = int(data[0])
        Hum = int(data[1])
        Soil = int(data[2])
        Sunlight = int(data[3].split("\\r\\n")[0])
        print(Temp,Hum,Soil,Sunlight)# for debugging purposes
        
        
        publish.single(topic="v1/devices/me/telemetry", #publish sensor data to thingsboard
                       payload='{"Temperature":'+str(Temp)+
                       ',"Sunlight":'+str(Sunlight)+
                       ',"Humidity":'+str(Hum)+
                       ',"Soil":'+str(Soil)+
                       '}',
                   hostname="thingsboard.cloud",auth={'username':"WfWAqasNS1Aq6W4mzU3R",'password':""})
        time.sleep(8)  # Delay to compensate for internet latency
                
        
if __name__ == "__main__" :
    main()    
