import serial
import time
import json
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

device = '/dev/ttyUSB0'
arduino = serial.Serial(device, 9600)

def light_pos(pos):
    arduino.write(pos.encode())

def on_connect(client, data, flags, rc):
    client.subscribe("v1/devices/me/rpc/request/+")
    
def on_message(client, data, msg):
    print("Topic: " +msg.topic + '\nMessage: ' + str(msg.payload))
    if msg.topic.startswith('v1/devices/me/rpc/request/'):
        requestId = msg.topic[len('v1/devices/me/rpc/request/'):len(msg.topic)]
        print("requestId : ",requestId)
        data = json.loads(msg.payload)
        light_pos(data['method'])

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set('NRAtHAIhSPs87DDkrall')
client.connect("thingsboard.cloud", 1883, 60)

while 1:
    if(arduino.in_waiting > 0):
        client.loop_start()
        line = arduino.readline()
        test = line.decode("utf-8")
        lightInt = int(test[0:3])
        motionSen = int(test[4:7])
        led1 = int(test[8])
        led2 = int(test[10])
        led3 = int(test[12])
        led4 = int(test[14])
        print("Light: " + str(lightInt) + "\nDistance: " + str(motionSen))
        publish.single(topic="v1/devices/me/telemetry",
                        payload='{"LightIntensity" :'+str(lightInt)+
                        ',"Distance":'+str(motionSen)+
                        ',"LivingRoom":'+str(led1)+
                        ',"BedRoom":'+str(led2)+
                        ',"KitchenRoom":'+str(led3)+
                        ',"DiningRoom":'+str(led4)+'}',
                    hostname="thingsboard.cloud",auth={'username':"NRAtHAIhSPs87DDkrall",'password':""})
        time.sleep(8)