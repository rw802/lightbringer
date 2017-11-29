import os, json

from pymongo import MongoClient 

class BaseDB(object):

    def __init__(self, config = None):
        self._database_host = None
        self._database_port = None
        self._database_db_name = None
        self._database_user = None
        self._database_pwd = None

        self._database_connection = None
        self._database_db = None
        
        if isinstance(config, str) and os.path.exists(config):
            self.load_config(config)

    def load_config(self, config):
        """ 
        load database configuration from given paht
        """

        if isinstance(config, str) and os.path.exists(config):
            with open (config, 'r') as f:
                d = json.load(f)
                d = d['mongodb']
        else:
            print ('setup database failed')
            exit(0)

        self._database_host = d['host']
        self._database_port = d['port']
        self._database_db_name = d['db']
        self._database_user = d['user']
        self._database_pwd = d['pwd']


    def connect_server(self):
        """
        connect to the server
        """

        self._database_connection = MongoClient(self._database_host, self._database_port)
        self._database_db = self._database_connection[self._database_db_name]
        auth = self._database_db.authenticate(self._database_user, self._database_pwd)
        if auth:
            # print (self._database_db.collection_names())
            return self._database_connection, self._database_db, True
        else:
            print ('mongodb authentication failed')
            return None, None, False

    def get_connection(self):
        return self._database_connection

    def get_auth(self):
        return self._database_db_name, self._database_user, self._database_pwd
