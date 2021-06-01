import serial
import time
import MySQLdb
import datetime
import sys
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import json
import os
from datetime import datetime

device = '/dev/ttyUSB0'
arduino = serial.Serial(device, 9600)

temperature = ''
lightIntensity = ''

THINGSBOARD_HOST = 'thingsboard.cloud'
ACCESS_TOKEN = 'F5HxNBYJ9g2H6BeikeXY'
port = 1883


def on_connect(client, data, flags, rc):
    client.subscribe("v1/devices/me/rpc/request/+")


def on_message(client, data, msg):
    print("Topic: " + msg.topic + '\nMessage: ' + str(msg.payload))
    if msg.topic.startswith('v1/devices/me/rpc/request/'):
        data = json.loads(msg.payload)
        if (data['method'] == "HighTemp_HighLightIntensity"):
            arduino.write(b'1')  # ventilator open
        elif (data['method'] == "LowTemp_LowLightIntensity_OR_LowTemp_HighLightIntensity"):
            arduino.write(b'2')  # ventilator close


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set('F5HxNBYJ9g2H6BeikeXY')
client.connect("thingsboard.cloud", 1883, 60)

while 1:
    client.loop_start()

    while arduino.in_waiting == 0:
        pass
    temperature, lightIntensity = (arduino.readline().decode('utf-8').rstrip()).split(",")

    print("Current temp: " + temperature)
    print("Current light intensity: " + lightIntensity)
    print("\n")

    publish.single(topic="v1/devices/me/telemetry",
                   payload='{"temperature":' + str(temperature) + ',"LightIntensity":' + str(lightIntensity) + '}',
                   hostname="thingsboard.cloud", auth={'username': "F5HxNBYJ9g2H6BeikeXY", "password": ""})
    time.sleep(8)




