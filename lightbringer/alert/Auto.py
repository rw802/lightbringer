#!/usr/bin/python

import Checker as checker
import Config as cfg
import sched, time
from Util import *
import datetime
from slackclient import SlackClient
import os

inputPath60 = '/code/stock/scan/ScanIn60Min.txt'
inputPath5 = '/code/stock/scan/ScanIn5Min.txt'
symbol60 = list(set(readIntoList(inputPath60))) # read and remove duplicates
symbol5 = list(set(readIntoList(inputPath5))) # read and remove duplicates

now = datetime.datetime.now()    
today3pm = now.replace(hour=15, minute=0, second=0, microsecond=0) 

def sendMsg(msg):
    msg = ':o:\n'+msg+'\n:tada:'
    sc.api_call(
      "chat.postMessage",
      channel="alert-bot",
      username='ALERTBOT',
      text=msg,
      icon_emoji=':ninja:'
    )
#Hourly 
def task60min():
    now = datetime.datetime.now()
    if now > today3pm:
        print 'market close'
        exit()
    for symbol in symbol60:
        time.sleep(0.9) 
        symbol = symbol.rstrip()
        print '60min checking #' + symbol + '\n'
        try:
            send, msg, rate = checker.checkSymbol(symbol, cfg.interval60, 'Hourly', True)
        except:
            continue
        if send and rate > 2:
            sendMsg(msg)
            
               
    s.enter(cfg.timeInterval60min, 1, task60min, ())
    pass

#5min    
def task5min():   
    if now > today3pm:
        print 'market close'
        exit() 
    for symbol in symbol5:
        time.sleep(0.9) 
        symbol = symbol.rstrip()
        print '30min checking #' + symbol + '\n'
        try:
            send, msg, rate = checker.checkSymbol(symbol, cfg.interval5, '30min', True)
        except:
            continue
        if send and rate > 2:
            sendMsg(msg)
            
                  
    s.enter(cfg.timeInterval5min, 1, task5min, ())
    pass



slack_token = os.environ['SLACK_API_TOKEN']

sc = SlackClient(slack_token)

#gSMS = GoogleVoice(cfg.smsEmail,cfg.smsPassword)  
s = sched.scheduler(time.time, time.sleep)    
s.enter(cfg.timeInterval5min, 1, task5min, ())
s.enter(cfg.timeInterval60min, 1, task60min, ())
s.run()