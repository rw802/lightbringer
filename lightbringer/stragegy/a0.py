#!/usr/bin/python3

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import time, os, sys, dateutil.parser
from collections import deque
from scipy import stats
from scipy.optimize import fsolve
import numpy as np

ts = TimeSeries(key='CKTTZCXL7LVD8BYW')
ti = TechIndicators(key='CKTTZCXL7LVD8BYW')

sym = {}

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) #Typo was here
    
    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]
    
    div = det(xdiff, ydiff)
    if div == 0:
        print ('no intersection')
        return 0, 0,

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y
                                                   
def analyze_symbol(sym):
    pass
# Get json object with the intraday data and another with  the call's metadata
# data, meta_data = ts.get_intraday('GOOGL', interval='15min')
# print (data)

# this strategy takes account of ema4/8, sma20/50, bb20, macd12/26, rsi14,
# and volume. 
# It detects abnomal activities, and suggests a potential trend base on 
# analysises from multiple time-window
count = 10
trend_period = 5
ema4his = deque(maxlen=trend_period)
ema8his = deque(maxlen=trend_period)
his_len = 5
while True:
    ema4, ema4_meta = ti.get_ema(symbol='GOOGL', interval='1min', time_period=4)
    ema8, ema8_meta = ti.get_ema(symbol='GOOGL', interval='1min', time_period=8)
#    sorted4ema = collections.OrderedDict(sorted(ema4.keys()))
    keys = sorted(ema4)[-trend_period:]
    print (keys[-1:])
    v4 = []
    v8 = []
    t = []
    for k in keys:
        v4.append(float(ema4[k]['EMA']))
        v8.append(float(ema8[k]['EMA']))
        t.append(time.mktime(dateutil.parser.parse(k).timetuple()))
    v4 = np.array(v4)
    v8 = np.array(v8)
    t = np.array(t)

    slope4, intercept4, r_value4, p_value4, std_err4 = stats.linregress(v4, t)
    slope8, intercept8, r_value8, p_value8, std_err8 = stats.linregress(v8, t)

    proj4 = intercept4 + slope4 * ( t[-1:] + 60 )
    proj8 = intercept8 + slope8 * ( t[-1:] + 60 )

    s4 = ((v4[0], t[0]), (v4[4], t[4]))
    s8 = ((v8[0], t[0]), (v8[4], t[4]))
    x = line_intersection(s4, s8)
    print (x)
#    if diff0 * diff5 < 0:
#        if diff0 > 0:
#            print ('ema change bullish')
#        else :
#            print ('ema change bearish')
#    else:
#        if diff0 > 0:
#            print ('ema up trending')
#        else:
#            print ('ema down trending')


            

    time.sleep(60)
    count -= 1
    if count <= 0:
        break

