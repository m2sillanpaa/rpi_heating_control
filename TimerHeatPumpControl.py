# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 22:13:42 2016

TimerHeatPumpControl 0.2

uses hours.txt values to control gpio and turn off the heating element if price is above
desired.

Requires python 3.

Author: 
Matti Sillanpää
maash.1.bridge@gmail.com

Original file:
Arttu Huttunen

/*
 * ----------------------------------------------------------------------------
 * The MIT License (MIT)
 * Copyright (c) 2016 Matti Sillanpää
 * Anyone is free to do whatever they want with this code, at their own risk.
 * ----------------------------------------------------------------------------
 */

INSTRUCTIONS:
1. Set to run hourly e.g. with cron
2. Set the desired temperature values below in deg Celcius,
'hour00' start at midnight. 

Cron example:
# sudo crontab -e

and edit a line in crontab to:
0 * * * * python3 /home/pi/rpi_heating_control/TimerHeatPumpControl.py

"""

#**********************************************************
#ACTUAL PROGRAM STARTS HERE, DO NOT EDIT

import datetime
import RPi.GPIO as GPIO
import json, configparser
from pprint import pprint

configFile = '/home/pi/rpi_heating_control/Settings.txt'
try:
    # Read settings from a file
    config = configparser.ConfigParser()
    config.read(configFile)
    
    pin = int(config['Settings']['GPIOPin'])
except:
    print("failed to load settings")


controlList =[]

try:
    with open('/home/pi/rpi_heating_control/hours.txt', encoding='utf-8') as hours:
        hourlyInfo = json.loads(hours.read())
    
        for i in range(0,24):
            controlList.append(hourlyInfo["values"][i]["mode"])
except:
    print("failed to parse")
# Get current time

currentHour = datetime.datetime.now().hour

if currentHour == 0:
    currentHour = 23
else:
    currentHour-=1
    
print('current hour',  currentHour)
gpioState = 1

if controlList[currentHour] == "off":
    gpioState = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

GPIO.output(pin,gpioState)

# END OF PROGRAM
