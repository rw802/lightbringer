

import os, sys, time, logging

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.sectorperformance import SectorPerformances

import pandas, json

# Read API infos from config 
config_paht = 'myinfo.json'
if os.path.exists(config_paht):
    with open(config_paht, 'r') as f:
        info = json.load(f)
        ALPHAVANTAGE_API_TOKEN = info['alphavantage']['key']

g_ts = TimeSeries(key=ALPHAVANTAGE_API_TOKEN, output_format='pandas') 
g_ti = TechIndicators(key=ALPHAVANTAGE_API_TOKEN, output_format='pandas') 
g_sp = SectorPerformances(key=ALPHAVANTAGE_API_TOKEN, output_format='pandas') 
 
# global constants
MAX_API_RETRIES = 3

# ti params 
g_intervals = ['1min', '5min', '15min', '60min']
slow_interval = '1min' 
fast_interval = '1min' 
ema_fast_period = 4
ema_slow_period = 8
series_type = 'close' 
track_interval = '1min'

def abnormaly(symbol):
    retry_count = 0
    while retry_count <= MAX_API_RETRIES:
        pass


def ema_short(symbol):
    logging.info("processing {}".format(symbol))
    retry_count = 0
    while (retry_count <= MAX_API_RETRIES):
        score = 0
        try:
            fast_ema = g_ti.get_ema(
                symbol=symbol, interval=fast_interval, time_period=ema_fast_period, series_type=series_type)
            slow_ema = g_ti.get_ema(
                symbol=symbol, interval=slow_interval, time_period=ema_slow_period, series_type=series_type)
            price = g_ts.get_intraday(
                symbol=symbol, interval=track_interval, outputsize='compact')
            
            sema_t0 = fast_ema[0].tail(2)['EMA'][1]
            lema_t0 = slow_ema[0].tail(2)['EMA'][1]
            sema_t1 = fast_ema[0].tail(2)['EMA'][0]
            lema_t1 = slow_ema[0].tail(2)['EMA'][0]
            last_quote = price[0].tail(1)
            last_price = last_quote['close'][0]


            diff = sema_t0 - lema_t0
            thresh = 0.001 * last_price 
            
            print (last_quote)
            ss = ''
            if diff > thresh:
                ss += 'uptrending '
                score += 2
                if sema_t0 > sema_t1:
                    ss += 'heating'
                    score += 1
                else :
                    ss += 'cooling'
            elif diff < -thresh:
                ss -= 2
                ss += 'downtrending '
                if lema_t0 < lema_t1:
                    ss += 'heating'
                else:
                    ss += 'cooling'
                    score -= 1
            else:  # EMA crossing!!!
                ss += 'sidewaying'
                msg = "[{}] EMAs crossing, must BUY/SELL now!".format(symbol)
                logging.info(msg)

            time.sleep(30)
            print (ss, ' score = ', score)

        except KeyError as e:
            logging.error(
                "[{}] is not supported by Alpha Vantage.".format(symbol))
            break

        except urllib.error.HTTPError:  # Alpha Vantage API has high failure rate - retry 3 times
            logging.error("[{}] - Exception HTTPError - Retry: {}/{}".format(
                symbol, retry_count, MAX_API_RETRIES))
            retry_count = retry_count + 1
            sleep(5)  # Time in seconds.


if __name__ == '__main__':
    ema_short('TOPS')
