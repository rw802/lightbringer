from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from CandleStickPattern import *
from Util import *
import Config as cfg

def checkSymbol(symbol, interval, msgInterval, mustCandleBullish = False):
    
    bullish = False
    rate = 0
    gMsg = '#'+symbol + ' '+msgInterval
    
    ts = TimeSeries(key=cfg.APIKey, output_format=cfg.format)
    if interval == cfg.intervalDaily: #daily
        dataTS, meta_data = ts.get_daily(symbol=symbol)
    else:
        dataTS, meta_data = ts.get_intraday(symbol=symbol,interval=interval)
        
    sample = [dict() for x in range(3)]
    
    for i in range(1,4):
        sample[i-1] = {'close':dataTS['close'][-i],'high':dataTS['high'][-i],'low':dataTS['low'][-i],'open':dataTS['open'][-i]}
                
    csp = CandleStickPattern(sample[2],sample[1],sample[0])
    if csp.bullishPattern():
        bullish = True
        rate += 1
        gMsg += '\nCandle Bull'
    else:
        if mustCandleBullish:
            return False, gMsg, rate
    
    ti = TechIndicators(key=cfg.APIKey, output_format=cfg.format)
    ##### bband
    data, meta_data = ti.get_bbands(symbol=symbol, interval=interval)
    # data.plot()
    bbLower = data['Real Lower Band'][-1]
    if sample[0]['low'] < bbLower:
        bullish = True
        rate += 1
        gMsg += '\nBB lower band tested'
    
    ##### MACD
    data, meta_data = ti.get_macd(symbol=symbol, interval=interval, fastperiod=12, slowperiod = 26, signalperiod = 9)
    #print data.keys()
    if data['MACD_Hist'][-1] > 0:
        for i in range(2,6):
            if data['MACD_Hist'][-i] < 0:
                gMsg += '\nMACD cross'
                bullish = True
                rate += 1
                break
    
    if bullish:
        data, meta_data = ti.get_rsi(symbol=symbol, interval = interval)
        if data['RSI'][-1] < 50:
            rate += 1
        gMsg += '\nRSI ' + round(data['RSI'][-1]).__str__()
        gMsg += '\nVol ' + printInK(dataTS['volume'][-1]) +" "+ printInK(dataTS['volume'][-2]) +" "+ printInK(dataTS['volume'][-3])
    
    
    return bullish, gMsg, rate

