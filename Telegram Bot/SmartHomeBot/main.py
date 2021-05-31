# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import telebot
from decouple import config
import paho.mqtt.publish as publish

API_KEY = config('API_KEY')
bot = telebot.TeleBot(API_KEY)


thresholdVars = {"/TemperatureGardenChange":"TemperatureThresholdVal","/SoilGardenChange":"SoilThresholdVal","/SunlightGardenChange":"SunlightThresholdVal",
"/LightVentilationChange":"thresholdLightIntensity","/TemperatureVentilationChange":"thresholdTemp",
"/SmokeFireChange":"Threshold_smoke","/TemperatureFireChange":"Threshold_temperature",
"/DistanceHomeChange":"DistanceThresholdValue","/LightHomeChange":"LightThresholdValue"}

command_dict = {}

class ActionLocation:
    def __init__(self, varname, deviceKey):
        self.varname = varname
        self.deviceKey = deviceKey


@bot.message_handler(commands=['commands'])
def commands(message):
    list_of_commands = '''
    Which command would you like to do?

    \U0001F525 Trigger actions:
    /triggers: Triggers

    \U0001F527 Change Threshold:
    /changethres
    '''
    bot.reply_to(message, list_of_commands)


@bot.message_handler(commands=['triggers'])
def TriggerCommands(message):
    list_of_commands = '''
     \U0001F331 Garden actions: 
    /waterplant : To water plants
    /openplantshade : Open garden's shade
    /closeplantshade : Close garden's shade

    \U0001F525 Fire alarm actions:
    /openbuzzer: Trigger alarm
    /watersprinkler: Turn on Water Sprinkler

    \U0001FA9F Home Ventilator actions:
    /openventilator: Open Window
    /closeventilator: Close Window

    \U0001F4A1 Home Light actions:
    /livinglights: Living Room Lights
    /bedroomlights: Bedroom Lights
    /kitchenlights: Kitchen Lights
    /dininglights: Dining Room Lights
    '''
    bot.reply_to(message, list_of_commands)

@bot.message_handler(commands=['Greet'])
def greet(message):
    bot.reply_to(message, "Hey!")


@bot.message_handler(commands=['waterplant'])
def WaterPlant(message):
    publish.single(topic="v1/devices/me/attributes",
                   payload='{"action_by_user": "low_moisture"}',hostname="thingsboard.cloud",
                   auth={'username':config('GardeningToken'),'password':""})
    bot.reply_to(message, "I have watered the plants!")

@bot.message_handler(commands=['openplantshade'])
def OpenPlantShade(message):
    publish.single(topic="v1/devices/me/attributes",
                   payload='{"action_by_user":"open_shade"}',hostname="thingsboard.cloud",
                   auth={'username':config('GardeningToken'),'password':""})
    bot.reply_to(message, "I have opened the garden's shade!")


@bot.message_handler(commands=['closeplantshade'])
def ClosePlantShade(message):
    publish.single(topic="v1/devices/me/attributes",
                   payload='{"action_by_user":"close_shade"}',hostname="thingsboard.cloud",
                   auth={'username':config('GardeningToken'),'password':""})
    bot.reply_to(message, "I have closed the garden's shade!")


@bot.message_handler(commands=['watersprinkler'])
def WaterSprinkler(message):
    publish.single(topic="v1/devices/me/attributes",
                   payload='{"action_by_user": "open_watersprinkle"}',hostname="thingsboard.cloud",
                   auth={'username':config('FireAlarmToken'),'password':""})
    bot.reply_to(message, "I have turned on the water sprinkler!")

@bot.message_handler(commands=['openbuzzer'])
def OpenBuzzer(message):
    publish.single(topic="v1/devices/me/attributes",
                   payload='{"action_by_user": "open_buzzer"}',hostname="thingsboard.cloud",
                   auth={'username':config('FireAlarmToken'),'password':""})
    bot.reply_to(message, "I have turned on the alarm!")


@bot.message_handler(commands=['livinglights'])
def TurnOnLivingLights(message):
    publish.single(topic="v1/devices/me/attributes",
                   payload='{"action_by_user": 1}',hostname="thingsboard.cloud",
                   auth={'username':config('HomeLightToken'),'password':""})
    bot.reply_to(message, "I have triggered the living room lights!")    

@bot.message_handler(commands=['bedroomlights'])
def TurnOnLivingLights(message):
    publish.single(topic="v1/devices/me/attributes",
                   payload='{"action_by_user": 2}',hostname="thingsboard.cloud",
                   auth={'username':config('HomeLightToken'),'password':""})
    bot.reply_to(message, "I have triggered the living room lights!")    

@bot.message_handler(commands=['kitchenlights'])
def TurnOnLivingLights(message):
    publish.single(topic="v1/devices/me/attributes",
                   payload='{"action_by_user": 3}',hostname="thingsboard.cloud",
                   auth={'username':config('HomeLightToken'),'password':""})
    bot.reply_to(message, "I have triggered the living room lights!")    

@bot.message_handler(commands=['dininglights'])
def TurnOnLivingLights(message):
    publish.single(topic="v1/devices/me/attributes",
                   payload='{"action_by_user": 4}',hostname="thingsboard.cloud",
                   auth={'username':config('HomeLightToken'),'password':""})
    bot.reply_to(message, "I have triggered the living room lights!")    

@bot.message_handler(commands=['openventilator'])
def Open_Ventilator(message):
    publish.single(topic="v1/devices/me/attributes",
                   payload='{"action_by_user": "HighTemp_HighLightIntensity"}',hostname="thingsboard.cloud",
                   auth={'username':config('HomeVentilationToken'),'password':""})
    bot.reply_to(message, "I have opened the window!")  

@bot.message_handler(commands=['closeventilator'])
def Close_Ventilator(message):
    publish.single(topic="v1/devices/me/attributes",
                   payload='{"action_by_user": "LowTemp_LowLightIntensity_OR_LowTemp_HighLightIntensity"}',hostname="thingsboard.cloud",
                   auth={'username':config('HomeVentilationToken'),'password':""})
    bot.reply_to(message, "I have closed the window!") 

@bot.message_handler(commands=['changethres'])
def ChangeThresholdRequest(message):
    bot.reply_to(message, 'Pick the Device\'s threshold to change:\n/GardenChange for Gardening System\U0001F331\n/VentilationChange for Ventilation System\U0001F4A8\n/HomeLightsChange for Home Light System\U0001F4A1\n/FireAlarmChange for Fire Alarm System\U0001F525\n')


############################

@bot.message_handler(commands=['GardenChange','VentilationChange','HomeLightsChange','FireAlarmChange'])
def ChangeGardenThreshold(message):
    if(message.text == "/GardenChange"):
        bot.reply_to(message, 'Which threshold do you wish to change?\n/TemperatureGardenChange for Temperature\n/SoilGardenChange for Soil Moisture\n/SunlightGardenChange for Sunlight\n ')
    elif(message.text == "/VentilationChange"):
        bot.reply_to(message, 'Which Threshold do you wish to change?\n/LightVentilationChange for Light\n/TemperatureVentilationChange for Temperature\n')
    elif(message.text == "/HomeLightsChange"):
        bot.reply_to(message, 'Which Threshold do you wish to change?\n/DistanceHomeChange for Distance\n/LightHomeChange for light\n')
    elif(message.text == "/FireAlarmChange"):
        bot.reply_to(message, 'Which Threshold do you wish to change?\n/SmokeFireChange for Smoke\n/TemperatureFireChange for Temperature\n')        
    

##############################

@bot.message_handler(commands=['TemperatureGardenChange','SoilGardenChange','SunlightGardenChange','LightVentilationChange','TemperatureVentilationChange','SmokeFireChange','TemperatureFireChange','DistanceHomeChange','LightHomeChange'])
def TemperatureGardenChange(message):
    if(message.text in ["/TemperatureGardenChange","/SoilGardenChange","/SunlightGardenChange"]):
        MessagetoSend = bot.send_message(message.chat.id,'\nPlease Enter your desired value:')
        command_dict[message.chat.id] = ActionLocation(message.text, config('GardeningToken'))
        bot.register_next_step_handler(MessagetoSend, ChangeThreshold)
    elif(message.text in ["/LightVentilationChange","/TemperatureVentilationChange"]):
        MessagetoSend = bot.send_message(message.chat.id,'\nPlease Enter your desired value:')
        command_dict[message.chat.id] = ActionLocation(message.text, config('HomeVentilationToken'))
        bot.register_next_step_handler(MessagetoSend, ChangeThreshold)
    elif(message.text in ["/SmokeFireChange","/TemperatureFireChange"]):
        MessagetoSend = bot.send_message(message.chat.id,'\nPlease Enter your desired value:')
        command_dict[message.chat.id] = ActionLocation(message.text, config('FireAlarmToken'))
        bot.register_next_step_handler(MessagetoSend, ChangeThreshold)
    elif(message.text in ["/DistanceHomeChange","/LightHomeChange"]):
        MessagetoSend = bot.send_message(message.chat.id,'\nPlease Enter your desired value:')
        command_dict[message.chat.id] = ActionLocation(message.text, config('HomeLightToken'))
        bot.register_next_step_handler(MessagetoSend, ChangeThreshold)           

def ChangeThreshold(message):
    try:
        int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, 'That is an invalid value')
        return

    publish.single(topic="v1/devices/me/attributes",
                   payload='{"'+ str(thresholdVars[command_dict[message.chat.id].varname]) +'":' +str(message.text) + '}',hostname="thingsboard.cloud",
                   auth={'username':command_dict[message.chat.id].deviceKey ,'password':""})
    
    del command_dict[message.chat.id]
    bot.send_message(message.chat.id, 'Value Changed!')

    

bot.polling()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
