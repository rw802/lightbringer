
import pandas as pd
from Robinhood import Robinhood
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.sectorperformance import SectorPerformances


import json
import pushover
import schedule
import time
import datetime
import numpy as np
from requests.exceptions import ConnectionError
import os
import logging
import argparse
import getpass
from tabulate import tabulate
import cmd

#  Parse arguments
parser = argparse.ArgumentParser(description="Command Arguments")
parser.add_argument('-u', '--username', dest='rhusername', required=False, action='store', help='Robinhood username')
parser.add_argument('-p', '--password', dest='rhpassword', required=False, action='store', help='Robinhood password')
parser.add_argument('-c', '--config', dest='configfile', required=False, action='store', default='info.json', help='path to your json file\
        which contains API informations of Pushover, AlphaVantage')
args = parser.parse_args()

# Read API infos from config
if True:
    with open(args.configfile, 'r') as f:
        info = json.load(f)
        ALPHAVANTAGE_API_TOKEN = info['alphavantage']['key']
        PUSHOVER_TOKEN = info['pushover']['token']
        PUSHOVER_USERKEY = info['pushover']['key']

po_client = pushover.Client(PUSHOVER_USERKEY, api_token=PUSHOVER_TOKEN)

g_ts = TimeSeries(key=ALPHAVANTAGE_API_TOKEN, output_format='pandas')
g_ti = TechIndicators(key=ALPHAVANTAGE_API_TOKEN, output_format='pandas')
sp = SectorPerformances(key=ALPHAVANTAGE_API_TOKEN, output_format='pandas')

g_watchlish = ['NUGT', 'UGAZ']

def unusual_volume(symbols=g_watchlish, dlen=4):
    ret = []
    for symbol in symbols:
        d = g_ts.get_intraday(symbol=sym, interval='5min')[0][-2:-1]
        o = float(d['open'])
        c = float(d['close'])
        price = min(o, c) + 0.15 * abs(o - c)
        print price

    return ret

unusual_volume()

