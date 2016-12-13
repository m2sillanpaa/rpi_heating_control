# -*- coding: utf-8 -*-
"""
Created on Tue Feb  3 22:40:22 2015

SpotPriceGet  0.3.1

This is a python3 program that will fetch electricity spot prices from Nordpool
and save the data to a file. It is intended to be used in conjunction with
another program(s) for controlling electricity usage. It is associated with a
configuration file from which the settings are read. User is advised to observe
the terms and conditions of Nordpool, their website and data. 


Author: 
Arttu Huttunen
Oulu, Finland
Created in 2015

Modified by 

Matti Sillanpää

/*
 * ----------------------------------------------------------------------------
 * The MIT License (MIT)
 * Copyright (c) 2015 Arttu Huttunen 
 * Anyone is free to do whatever they want with this code, at their own risk.
 * ----------------------------------------------------------------------------
 */


"""

#config file
configFile = '/home/pi/rpi_heating_control/Settings.txt'


#Actual code starts here
#---------------------------------------------------------------------------
import sys, requests, json, configparser, datetime

# Get current time and start a log line
currentTime = datetime.datetime.now()
logLine = []
logLine.append(str (currentTime) + ' SPG: ')

#A method for writing the log file
def WriteLog(logLine, logFile = '/home/pi/rpi_heating_control/log.txt',logState = 'on'):       
    logLine.append('\n')
    logLine = ''.join(logLine)
    #print (logLine)
    if logState == 'on':
        with open(logFile, "a") as fol:
            fol.write(logLine)
    sys.exit()


try:
    # Read settings from a file
    config = configparser.ConfigParser()
    config.read(configFile)
    
    # Get settings *********************************** hardcoded stuff
    priceURL = config['Settings']['URL'] 
    outputFile = config['Settings']['OutputFile']
    outputType = config['Settings']['OutputType']
    logState = config['Settings']['Log']
    logFile = config['Settings']['LogFile']
    logPrice = config['Settings']['LogPrice']
    userTimeZone = config['Settings']['TimeZone']
    priceLimit = int(config['Settings']['PriceLimit']) 
    maxSkipped = int(config['Settings']['MaxSkipped'])
    
    
except:
    logLine.append ('Error in reading configuration file. ')
    WriteLog(logLine)
   
# Get prices from URL and parse json, then save prices to list
try:
    pricePage = requests.get(priceURL)
except:
    logLine.append ('Error in fetching data from server. ')
    WriteLog(logLine,logFile, logState )


try:
    parsedPrices = json.loads(pricePage.text)
    
    priceList =[]
    hours =[]
    priceListToday = []
    priceListYesterday = []
    
    for i in range(0,24):
        #****************************** more hardcoded stuff
        priceListToday.append(parsedPrices['data']['Rows'][i]['Columns'][0]['Value'])
        priceListYesterday.append(parsedPrices['data']['Rows'][i]['Columns'][1]['Value'])
        hours.append(i)
except:
    logLine.append ('Error in parsing the data. ')
    WriteLog(logLine,logFile, logState )


#Time zone correction
if userTimeZone == '1':
    priceList.extend(priceListToday)
    
elif userTimeZone == '2':
    priceList.extend(priceListYesterday[-1:])
    priceList.extend(priceListToday[:-1])
    
else:
    logLine.append ('Unsupported timezone! ')

# Generate output, depending on settings,
# option 'p' = write prices to file
# option 'l' = write levels to file, e.g. cheapest is 1, rest 2
# ************************ control setting keys hardcoded

outputStr = []
if outputType == 'p':
    priceFloat = []
    for i in priceList:
        priceFloat.append(float(i.replace(',','.')))
    
    maxfirst = []
    
    for i in range(0,24):
        priceMaxIndex = priceFloat.index(max(priceFloat))
        if maxSkipped > 0:
            if priceFloat[priceMaxIndex] > priceLimit:
                maxfirst.append(priceFloat[priceMaxIndex])
                maxSkipped -= 1
                
        priceFloat[priceMaxIndex] = 0

    outputStr.append('{\"values\": [')
        
    for i in range(0,24):
        try:
            if maxfirst.index(float(priceList[i].replace(',','.'))):
                mode = 'off'
        except:
            mode = 'on'

        outputStr.append('{\"hour\":'+ str(hours[i]) + ',\"price\":\"' + priceList[i] + '\",\"mode\":\"' + mode + '\"}' )
        if i < 23:
            outputStr.append(',')
        
        
    outputStr.append(']}')
try:
    #Write the output to file, first make it a string
    outputStr = ''.join(outputStr)
    with open(outputFile, "w") as fo:
        fo.write(outputStr)
except:
    logLine.append ('Error in writing output file. ')
    WriteLog(logLine,logFile, logState )


#append log with the type of output and optionally with prices 
logLine.append( "'" + outputType  + "' OK. ")
if logPrice == 'on':     
    logLine.append( ' '.join(priceList))


# Finish by writing the a line to the log file if log in 'on' 
WriteLog(logLine,logFile, logState )

# END OF PROGRAM   
