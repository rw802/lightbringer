from basedb import BaseDB
from arctic.arctic import Arctic, TICK_STORE

import pymongo, pprint

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
from pytz import utc


# apsche stuff
executors = {
        'default'       : {'type': 'threadpool', 'max_workers': 20},
        'processpool'   : ProcessPoolExecutor(max_workers=5)
        }   
job_defaults = {
        'coalesce': True,
        'max_instances': 3
        }   

class Slave(Arctic):

    def __init__(self, connection = None):
        if not connection:
            connection = 'localhost'
        self.__mongo_client = connection

        # tick db
        Arctic.__init__(self, self.__mongo_client)
        # job system
        self.__job_db = self.__mongo_client.jobs
        self.__job_collection = self.__job_db.queue
        # scheduler
        self.__scheduler = BackgroundScheduler()
        self.__scheduler.configure(executors = executors, job_defaults= job_defaults, timezone=utc)
        self.__scheduler.start()

    def __del__(self):
        self.__scheduler.shutdown(wait=False)


    # TODO to have different functors query from various data sources
    def work(self, job):
        """

        :param job: a json job object contains symbol and other stuff
        :return:
        """
        pass

    def get_job(self):
        """
        Periodically query new job(s) from the master
        if running jobs is less than MAXIMUM

        @param desc : a json file of jobs
        """
	
        doc_jobs = self.__job_collection.find({"status" : {"$ne" : "removed" }})
        doc_jobs = doc_jobs.sort('add_time', pymongo.DESCENDING)
        return doc_jobs[0]


    def update_jobs(self):
        """
        Periodically check jobs' status, if job(s) from the master
        to be paused, or removed
        """
        pass


    def list_jobs(self):
        doc_jobs = self.__job_collection.find({"status" : {"$ne" : "removed"}})
        for job in doc_jobs:
            pprint.pprint(job)

