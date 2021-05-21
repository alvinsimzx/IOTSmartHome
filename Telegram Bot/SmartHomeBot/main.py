# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import telebot
from decouple import config
from beebotte import *
import paho.mqtt.client as mqtt


API_KEY = config('API_KEY')
BBotAPI = config('BBotAPI')
BBotSecret = config('BBotSecret')
bot = telebot.TeleBot(API_KEY)
bclient = BBT(BBotAPI,BBotSecret)

client = mqtt.Client()
client.username_pw_set('vzEZ7F3Hqlfp9zRByxPdXlugMRfnsk7')
client.connect("mqtt.beebotte.com", 1883, 60)

client.loop_start()

@bot.message_handler(commands=['Greet'])
def greet(message):
    bot.reply_to(message, "Hey!")

@bot.message_handler(commands=['gardeninfo'])
def showGardenInfo(message):
    temp = str(bclient.read('GardeningSystem', 'Temperature', limit=1)[0]['data'])
    hum = str(bclient.read('GardeningSystem', 'Humidity', limit=1)[0]['data'])
    soil = str(bclient.read('GardeningSystem', 'SoilMoisture', limit=1)[0]['data'])
    sun = str(bclient.read('GardeningSystem', 'Sunlight', limit=1)[0]['data'])
    info = "Here is your Garden Info:\n\n" + "Temperature: " + temp +"\n" + "Humidity: " + hum + "\n" + "Soil Moisture: " + soil + "\n" + "Sunlight: " + sun
    bot.reply_to(message, info)

@bot.message_handler(commands=['waterplant'])
def WaterPlant(message):
    bclient.publish('GardeningAction', 'Condition','Water')
    bot.reply_to(message, "I have watered the plants!")

bot.polling()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
