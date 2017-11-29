from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.sectorperformance import SectorPerformances

from pymongo import MongoClient

from arctic import Arctic, TICK_STORE

import logging, os, sys 
import pandas, json


class Slave(object):
    def __init__(self, config=None):
        """ 
        Every slave must be instantiated with a path to a configuration file,
        which minimumly contain master connection and data feed
        """

        self.datafeed_carrier = None
        self.datafeed_entry = None
        self.datafeed_api_token = None
        self.datafeed_api_secret = None # optional
        self.df_ts, self.df_ti, self.df_sp = None, None, None

        self.database_host = None
        self.database_port = None
        self.database_db = None
        self.database_user = None
        self.database_pwd = None
        self.database_connection = None


        if isinstance(config, str) and os.path.exists(config):
            with open (config, 'r') as f:
                self.config = json.load(f)

    def connect_datafeed(self, config=None):
        d = None
        if isinstance(config, str) and os.path.exists(config):
            with open (config, 'r') as f:
                d = json.load(f)
        # use config stored in the instance
        else:
            d = self.config

        self.datafeed_carrier = d['name']
        self.datafeed_entry = d['entry']
        self.datafeed_api_token = d['key']

        if d['secret']:
            self.datafeed_api_secret = d['secret']

        self.df_ts = TimeSeries(key=ALPHAVANTAGE_API_TOKEN, output_format='pandas') 
        self.df_ti = TechIndicators(key=ALPHAVANTAGE_API_TOKEN, output_format='pandas') 
        self.df_sp = SectorPerformances(key=ALPHAVANTAGE_API_TOKEN, output_format='pandas') 

    def test_connect_datafeed(self):
        try:
            d = self.df_ti.get_ema(symbol='AMD', interval='1min', time_period=8)
        except ValueError as e:
            print ('Failed to connect to Alpha Vantage')
            exit(0)

    def connect_master(self, config=None):
        if isinstance(config, str) and os.path.exists(config):
            with open (config, 'r') as f:
                d = json.load(f)
                d = d['mongodb']
        else:
            print ('setup database failed')
            exit(0)

        self.database_host = d['host']
        self.database_port = d['port']
        self.database_db = d['db']
        self.database_user = d['user']
        self.database_pwd = d['pwd']

        self.database_connection = MongoClient(self.database_host, self.database_port)
        db = self.database_connection[self.database_db]
        auth = db.authenticate(self.database_user, self.database_pwd)
        if auth:
            print (db.collection_names())    
        else:
            print ('mongodb authentication failed')


if __name__ == '__main__':
    Slave().connect_master('config/my_slave.json')
