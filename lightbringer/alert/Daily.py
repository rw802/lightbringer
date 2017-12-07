#!/usr/bin/python

import Config as cfg
from Util import *
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

from Symbol import Symbol
#check daily reversal

#read and create list
inputPath = '../scan/DailyScanIn.txt'
outputPath = '../scan/DailyScanOut_Full.txt'
symbolOutputPath = '../scan/DailyScanOut_Symbol.txt'

symbols = readIntoList(inputPath)
#clear file
open(outputPath, 'w').close()
open(symbolOutputPath, 'w').close()
#check and write to output 
f = open(outputPath, 'w')   
fSymbol = open(symbolOutputPath, 'w')   

ti = TechIndicators(key=cfg.APIKey, output_format=cfg.format)
ts = TimeSeries(key=cfg.APIKey, output_format=cfg.format)

len = symbols.__len__()
count = 1
for stock in symbols:
    print 'checking #' + stock
    print (count*100/len).__str__() + '%'
    count += 1
    symbolObj = Symbol(stock, cfg.intervalDaily, ts, ti)
    try:
        bullish, flag, info, rate = symbolObj.rate(MAMustBull=True, CandleMustBull=True)
    except:
        continue  

    if bullish:
        info = rate.__str__() + '\n' + info + '\n\n'
        print info
        f.write(info)
        fSymbol.write(stock+',')
    print '\n'
  
    
f.close()
fSymbol.close()
