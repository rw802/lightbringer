from basedb import BaseDB
from arctic.arctic import Arctic, TICK_STORE


class Master(Arctic):

    def __init__(self, connection = None):
        if not connection:
            connection = 'localhost'
        Arctic.__init__(self, connection)

    def add_jobs(self, job_description):
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

        lib_jobs = self.get_library('jobs')
        for each in lib_job:
            metadata= {
                    'time':str(datetime.datetime.now())[:-7],
                    'source':each['source'],
                    'status': 'wait',
                    'slave' : 'N/A'
                    }
            lib_jobs.write(each['pair'], each, metadata)


    def list_jobs(self):
        """
        Return jobs that are being run on slaves, and 
        corresponding slaves' status
        """

        lib_jobs = self.get_library('jobs')
        # TODO sort jobs by 1. active, 2. added time, then
        # print as a table


