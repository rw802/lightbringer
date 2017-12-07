from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from CandleStickPattern import *
from Util import *
import Config as cfg
from MAStrategy import MAStrategy
from BBandStrategy import BBandStrategy
from MACDStrategy import MACDStrategy
from RSIStrategy import RSIStrategy

class Symbol:
    def __init__(self, symbol, interval,avTimeSeriesObj, avTechIndicatorObj):
        self.symbol = symbol
        self.interval = interval
        self.avTimeSeriesObj = avTimeSeriesObj
        self.avTechIndicatorObj = avTechIndicatorObj
        self.maShort = 50
        self.maLong = 150

    # check if stock is bullish. 
    def checkBullish(self, MAMustBull = False, CandleMustBull = False, MACDMustBull = False, RSIMustBull = False, BBandMustBull = False):
        info = '#'+self.symbol + ' ' + self.interval
        flag = 0
        rate = 0
        
        # candle
        if self.interval == cfg.intervalDaily: #daily
            dataTS, meta_data = self.avTimeSeriesObj.get_daily(symbol=self.symbol)
        else:
            dataTS, meta_data = self.avTimeSeriesObj.get_intraday(symbol=self.symbol,interval=self.interval)
            
        sample = [dict() for x in range(3)]
        
        for i in range(1,4):
            sample[i-1] = {'close':dataTS['close'][-i],'high':dataTS['high'][-i],'low':dataTS['low'][-i],'open':dataTS['open'][-i]}
                    
        csp = CandleStickPattern(sample[2],sample[1],sample[0])
        if csp.bullishPattern():
            info += '\nCandle Bull'
            setBullish(flag, CandleBull)
            rate += 1
        elif CandleMustBull:
            return False, 0, info, 0
        
        #MA   
        ma = MAStrategy(self.avTechIndicatorObj)
        if ma.verify(self.symbol, self.interval, self.maShort, self.maLong):
            info += '\nMA Up Trend'
            rate += 1
            setBullish(flag, MABull)
        elif MAMustBull:
            return False, 0, info, 0
        
        #MACD
        macd = MACDStrategy(self.avTechIndicatorObj)    
        if macd.verify(self.symbol, self.interval):
            info += '\nMACD Cross'
            rate += 1
            setBullish(flag, MACDBull)
        elif MACDMustBull:
            return False, 0, info, 0
          
        #RSI  
        rsi = RSIStrategy(self.avTechIndicatorObj)
        if rsi.verify(self.symbol, self.interval):
            info += '\nRSI Over Bought'
            rate += 1
            setBullish(flag, RSIBull)
        elif RSIMustBull:
            return False, 0, info, 0
        
        #BBand    
        bband = BBandStrategy(self.avTechIndicatorObj)
        if bband.verify(dataTS['close'][-3:], 3, self.symbol, self.interval):
            info += '\nBBand Low Tested'
            rate += 1
            setBullish(flag, BBandBull)
        elif BBandMustBull:
            return False, 0, info, 0
        
        info += '\nVol ' + printInK(dataTS['volume'][-1]) +" "+ printInK(dataTS['volume'][-2]) +" "+ printInK(dataTS['volume'][-3])   
        return (rate != 0), flag, info, rate
    
    def checkBearish(self, MAMustBear = False, CandleMustBear = False, MACDMustBear = False, RSIMustBear = False, BBandMustBear = False):
        info = '#'+self.symbol + ' ' + self.interval
        flag = 0
        rate = 0
        
        # candle
        if self.interval == cfg.intervalDaily: #daily
            dataTS, meta_data = self.avTimeSeriesObj.get_daily(symbol=self.symbol)
        else:
            dataTS, meta_data = self.avTimeSeriesObj.get_intraday(symbol=self.symbol,interval=self.interval)
            
        sample = [dict() for x in range(3)]
        
        for i in range(1,4):
            sample[i-1] = {'close':dataTS['close'][-i],'high':dataTS['high'][-i],'low':dataTS['low'][-i],'open':dataTS['open'][-i]}
                    
        csp = CandleStickPattern(sample[2],sample[1],sample[0])
        if csp.bearishPatter():
            info += '\nCandle Bear'
            rate += 1
        elif CandleMustBear:
            return False, 0, info, 0
        
        info += '\nVol ' + printInK(dataTS['volume'][-1]) +" "+ printInK(dataTS['volume'][-2]) +" "+ printInK(dataTS['volume'][-3])   
        return (rate != 0), flag, info, rate
            