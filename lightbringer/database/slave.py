from basedb import BaseDB
from arctic.arctic import Arctic, TICK_STORE



class Slave(Arctic):

    def __init__(self, connection = None):
        # number of jobs currently running on this slave
        self.__jobscount__ = 0
        self.__max_jobscount__ = 3

        if not connection:
            connection = 'localhost'
        Arctic.__init__(self, connection)

    def get_job(self):
        """
        Periodically query new job(s) from the master
        if running jobs is less than MAXIMUM

        @param desc : a json file of jobs
        """

        lib_jobs = self.get_library('jobs')
        for each in lib_job:
            metadata= {
                    'time':str(datetime.datetime.now())[:-7],
                    'source':each['source'],
                    'slave' : 'N/A'
                    }
            lib_jobs.write(each['pair'], each, metadata)


    def update_jobs(self):
        """
        Periodically check jobs' status, if job(s) from the master
        to be paused, or removed
        """

        pass

