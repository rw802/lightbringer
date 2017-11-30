from basedb import BaseDB
from arctic.arctic import Arctic, TICK_STORE

import datetime, pprint


class Job(object):
    def __init__(self):
        pass



class Master(Arctic):

    def __init__(self, connection = None):
        if not connection:
            connection = 'localhost'
        self.__mongo_client = connection

        # tick db
        Arctic.__init__(self, self.__mongo_client)
        # job system
        self.__job_db = self.__mongo_client.jobs
        self.__job_collection = self.__job_db.queue

    def add_jobs(self, job_list):
        """
        Add job(s) to the server job pool for slaves
        to fetch.
        job status:
        wait, waiting for a slave to pick up, slave = N/A
        pause, remain active but paused on slave, slave not N/A
        remove, indicates this job is to be deleted, once slave
            becomes N/A, remove this job from database

        @param desc : a json file of jobs
        """

        for each in job_list:
            job = {
                    'add_time':str(datetime.datetime.now())[:-7],
                    'status': 'wait',
                    'slave' : 'N/A',
                    'symbol':each['symbol'],
                    'time_start' : each['time_start'],
                    'time_end' : each['time_end'],
                    'interval' : each['interval'],
                    'field'    : each['field']
                    }
            self.__job_collection.insert_one(job)


    def list_jobs(self):
        """
        Return jobs that are being run on slaves, and 
        corresponding slaves' status
        """

        doc_jobs = self.__job_collection.find({"status" : {"$ne" : "removed"}})
        for job in doc_jobs:
            pprint.pprint(job)

    def clear_jobs(self):
        self.__job_collection.delete_many({})

    def count_jobs(self):
        return self.__job_collection.find({}).count()


