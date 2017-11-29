#!/usr/bin/python

import cmd, datetime, time
from apscheduler.schedulers.background import BackgroundScheduler
import logging
logging.basicConfig()

bs = BackgroundScheduler()
bsstart = False
class InteractiveShell(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.trader = 'trader'

    def do_s(self, args):
        print ('pressed s')

    def do_bb(self, args):
        print ('pressed b')

    def do_q(self, args):
        exit(0)

    def do_t(self, args):
        global bsstart
        if bsstart:
            bs.pause()
        else:
            bs.start()
        bsstart = not bsstart

def say():
    print datetime.datetime.now()

bs.add_job(say, 'interval', seconds=2, id='my_job_id')

if __name__ == '__main__':
    InteractiveShell().cmdloop()
