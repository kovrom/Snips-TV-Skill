#!/usr/bin/env python
# -*-: coding utf-8 -*-

import ConfigParser
from snipsremote.snipsremote import SnipsRemote
from snipsremote.snipsremote import VolumeManip
from snipsremote.snipsremote import VocalConfig
from hermes_python.hermes import Hermes
import io
import Queue
import broadlink
import time
import re
import binascii
import os
import subprocess
from os.path import expanduser

#roku lib
from roku import Roku
roku = Roku('192.168.1.146')





CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

#MQTT connection:

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


#Config.ini file parsing:


class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section: {option_name : option for option_name, option in self.items(section)} for section in self.sections()}

def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
	    print(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()







#Skills Intents management:


class Skill:

        def __init__(self):
            config = read_configuration_file("config.ini")


#roku related	
def rokuHome():
    roku.home()
def roku_chilled_cow():
    roku.home()
    spotify = roku['Spotify Music'] 
    spotify.launch()
    time.sleep(10)
    roku.up()    
    roku.right()
    roku.select()
    time.sleep(5)
    roku.down()
    roku.select()
    time.sleep(5)
    roku.select()   	

def rokuPlay():
	roku.play()
	
def rokuBack():
	roku.back()
	
def callback(hermes, intent_message):
        pass

def remote_toggle(hermes, intent_message):
    hermes.skill.remote.toggle_on_off()

def channelup(hermes, intent_message):
    SnipsRemote.send_value("tv_chup")

def channeldown(hermes, intent_message):
    SnipsRemote.send_value("tv_chdown")

#Volume Related Skills
def volumeup(hermes, intent_message):
    SnipsRemote.send_value("audio_volup")
    VolumeManip.how_much_up(intent_message.slots.Numbers.first().value)

def volumedown(hermes, intent_message):
    SnipsRemote.send_value("audio_voldown")
    VolumeManip.how_much_down(intent_message.slots.Numbers.first().value)

def Mutebutton(hermes, intent_message):
    SnipsRemote.send_value("audio_mute")

def Advert15(hermes, intent_message):
    SnipsRemote.send_value("audio_mute")
    time.sleep(15)
    SnipsRemote.send_value("audio_mute")

def Advert30(hermes, intent_message):
    SnipsRemote.send_value("audio_mute")
    time.sleep(30)
    SnipsRemote.send_value("audio_mute")

#This Skill searches for the necessary info.  and fills it in the config file.
def entering_test_mode(hermes, intent_message):
    VocalConfig.auto_setup_BlackBeanControl_ini()

#This Skill allows relearn a button if it isn't working, or if you "mis-pressed" accidentally.  
def learningmode(hermes, intent_message):
    SnipsRemote.relearn_value(intent_message.slots.button_name.first().value) 
    sentence = "button remapped"
    hermes.publish_end_session(intent_message.session_id, sentence)

def Menu(hermes, intent_message):
    SnipsRemote.send_value("Menu")
    hermes.publish_end_session(intent_message.session_id, "Menu")
	
def SmartHub(hermes, intent_message):
    SnipsRemote.send_value("SmartHub")
    hermes.publish_end_session(intent_message.session_id, "Hello Smart World")	
    
def turnoff(hermes, intent_message):
    SnipsRemote.send_value("audio_power")
    SnipsRemote.send_value("tv_power")
    hermes.publish_end_session(intent_message.session_id, "turning off TV")	

def turnon(hermes, intent_message):
    SnipsRemote.send_value("audio_power")
    SnipsRemote.send_value("tv_power")
    hermes.publish_end_session(intent_message.session_id, "turning TV on")
	
def rightbutton(hermes, intent_message):
    SnipsRemote.send_value("rightbutton")
    hermes.publish_end_session(intent_message.session_id, "Goes right")

def leftbutton(hermes, intent_message):
    SnipsRemote.send_value("leftbutton")
    hermes.publish_end_session(intent_message.session_id, "Goes right lol")
	
def source(hermes, intent_message):
    SnipsRemote.send_value("tv_input")
    hermes.publish_end_session(intent_message.session_id, "Yup")

def factoryreset(hermes, intent_message):
    if intent_message.slots.YESNO.first().value == "Yes":
        VocalConfig.auto_setup_BlackBeanControl_ini()
        hermes.publish_end_session(intent_message.session_id, "reseted the device")
    else:
        hermes.publish_end_session(intent_message.session_id, "You succesfully cancelled factory reset")

def enterbutton(hermes, intent_message):
    SnipsRemote.send_value("Enter")
    hermes.publish_end_session(intent_message.session_id, "gotcha")
	
	
if __name__ == "__main__":
    with Hermes(MQTT_ADDR) as h:
       h.subscribe_intent("GabonV23:ChannelUP", channelup) \
        .subscribe_intent("GabonV23:ChannelDown", channeldown) \
        .subscribe_intent("kovrom:Turnon", turnon) \
	.subscribe_intent("kovrom:Turnoff", turnoff) \
        .subscribe_intent("GabonV23:volumedown", volumedown) \
        .subscribe_intent("kovrom:Mutebutton",Mutebutton ) \
        .subscribe_intent("GabonV23:volumeup", volumeup) \
        .subscribe_intent("GabonV23:volumedown", volumedown) \
        .subscribe_intent("GabonV23:EnterTestMode", entering_test_mode) \
        .subscribe_intent("GabonV23:LearningMode", learningmode) \
        .subscribe_intent("GabonV23:rightbutton", rightbutton) \
        .subscribe_intent("GabonV23:leftbutton", leftbutton) \
        .subscribe_intent("GabonV23:Menu", Menu) \
	.subscribe_intent("GabonV23:FactoryReset", factoryreset) \
        .subscribe_intent("kovrom:SourceButton", source) \
	.subscribe_intent("GabonV23:EnterButton", enterbutton) \
	.subscribe_intent("GabonV23:SmartHub", SmartHub) \
	.subscribe_intent("kovrom:Advert15", Advert15) \
	.subscribe_intent("kovrom:Advert30", Advert30) \
	.subscribe_intent("kovrom:PlayRoku", rokuPlay) \
	.subscribe_intent("kovrom:HomeRoku", rokuHome) \
	.subscribe_intent("kovrom:PauseRoku", rokuPlay) \
	.subscribe_intent("kovrom:BackRoku", rokuBack) \
	.subscribe_intent("kovrom:ChilledCowSpotify", roku_chilled_cow) \
        .loop_forever()
