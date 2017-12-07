import datetime
from Util import *
from Message import Message
import sched, time
from Symbol import Symbol

now = datetime.datetime.now()
# set to 21 to match time of google cloud
time3pm = now.replace(hour=21, minute=0, second=0, microsecond=0) 

class IntraDay:
    
    def checkBullish(self, MAMustBull = False, CandleMustBull = False, MACDMustBull = False, RSIMustBull = False, BBandMustBull = False):
        now = datetime.datetime.now()
        if now > time3pm:
            print 'market close'
            return
        for symbol in self.symbolList:
            symbol = symbol.rstrip()
            print self.inqueryInterval + ' checking #' + symbol + ' if bullish\n'
            
            symbolObj = Symbol(symbol, self.inqueryInterval, self.avTimeSeriesObj, self.avTechIndicatorObj)
            try:
                bullish, flag, text, rate = symbolObj.checkBullish(
                    CandleMustBull=CandleMustBull,
                    MACDMustBull = MACDMustBull,
                    RSIMustBull = RSIMustBull,
                    BBandMustBull = BBandMustBull,
                    MAMustBull = MAMustBull)
            except:
                continue  
        
            if bullish:
                self.msg.sendSlack(text,channel =self.msgChannel, bullish = True)
                
                   
        self.scheduler.enter(self.schedulerInterval, 1, self.checkBullish, 
                             (
                                 MAMustBull, 
                                 CandleMustBull, 
                                 MACDMustBull, 
                                 RSIMustBull, 
                                 BBandMustBull
                                 )
                             )
        pass
    
    
    def checkBearish(self, MAMustBear = False, CandleMustBear = False, MACDMustBear = False, RSIMustBear = False, BBandMustBear = False):
        now = datetime.datetime.now()
        if now > time3pm:
            print 'market close'
            return
        for symbol in self.symbolList:
            symbol = symbol.rstrip()
            print self.inqueryInterval + ' checking #' + symbol + ' if bearish\n'
            
            symbolObj = Symbol(symbol, self.inqueryInterval, self.avTimeSeriesObj, self.avTechIndicatorObj)
            try:
                bearish, flag, text, rate = symbolObj.checkBearish(
                    CandleMustBear=CandleMustBear,
                    MACDMustBear = MACDMustBear,
                    RSIMustBear = RSIMustBear,
                    BBandMustBear = BBandMustBear,
                    MAMustBear = MAMustBear)
            except:
                continue  
        
            if bearish:
                self.msg.sendSlack(text, channel = self.msgChannel ,bullish = False)
                
                   
        self.scheduler.enter(self.schedulerInterval, 1, self.checkBearish, 
                             (
                                 MAMustBear, 
                                 CandleMustBear, 
                                 MACDMustBear, 
                                 RSIMustBear, 
                                 BBandMustBear
                                 )
                             )
        pass
    
    def runBullishCheck(self, MAMustBull = False, CandleMustBull = False, MACDMustBull = False, RSIMustBull = False, BBandMustBull = False):
        self.scheduler.enter(self.schedulerInterval, 1, self.checkBullish, 
                             (
                                 MAMustBull, 
                                 CandleMustBull, 
                                 MACDMustBull, 
                                 RSIMustBull, 
                                 BBandMustBull
                                 )
                             )
        self.scheduler.run()
        
        pass
    
    def runBearishCheck(self, MAMustBear = False, CandleMustBear = False, MACDMustBear = False, RSIMustBear = False, BBandMustBear = False):
        self.scheduler.enter(self.schedulerInterval, 1, self.checkBearish, 
                             (
                                 MAMustBear, 
                                 CandleMustBear, 
                                 MACDMustBear, 
                                 RSIMustBear, 
                                 BBandMustBear
                                 )
                             )
        self.scheduler.run()
        
        pass
    
    def __init__(self, symbolFilePath, avTimeSeriesObj, avTechIndicatorObj, inqueryInterval, schedulerInterval, channel):
        self.path = symbolFilePath
        self.inqueryInterval = inqueryInterval
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.msg = Message()
        self.avTimeSeriesObj = avTimeSeriesObj
        self.avTechIndicatorObj = avTechIndicatorObj
        self.schedulerInterval = schedulerInterval
        self.msgChannel = channel
        self.symbolList = list(set(readIntoList(symbolFilePath)))

