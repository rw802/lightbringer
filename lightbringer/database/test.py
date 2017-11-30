import unittest

from basedb import BaseDB
from master import Master
from slave import Slave

import pprint

class TestBadeDB(unittest.TestCase):
    """
    Tests for class BaseDB
    """

    def setUp(self):
        """
        var setups
        """

        self.master_config = '../../docs/config/my_master.json'
        self.slave_config = '../../docs/config/my_slave.json'

    def test_connection(self):
        ins = BaseDB()
        ins.load_config(self.master_config)
        conn, db, t = ins.connect_server()
        self.assertTrue(t)


class TestMaster(unittest.TestCase):
    """
    Tests for class Master, Jez I'm getting tired of writting
    this shit
    """

    def setUp(self):
        """
        var setups
        """

        self.master_config = '../../docs/config/my_master.json'
        self.slave_config = '../../docs/config/my_slave.json'
        self.base =  None
        self.conn = None
        self.mast = None

        self.base= BaseDB()
        self.base.load_config(self.master_config)
        self.conn, db, t = self.base.connect_server()
        self.mast = Master(self.conn)

    def test_master(self):
        self.assertGreater(len(self.mast.list_libraries()), 0)

    def test_add_job(self):
        self.mast.clear_jobs()
        self.assertEqual(self.mast.count_jobs(), 0)
        jobs = [{
                  "symbol" : "AMD",
                  'time_start' : 'N/A',
                  'time_end' : 'N/A',
                  'interval' : '15min',
                  'field' : 'price'
                  }
                  ]
        self.mast.add_jobs(jobs)
        self.assertEqual(self.mast.count_jobs(), 1)


class TestSlave(unittest.TestCase):
    """
    Tests for class Slave, Jez I'm getting tired of writting
    this shit
    """

    def setUp(self):
        """
        var setups
        """

        self.master_config = '../../docs/config/my_master.json'
        self.slave_config = '../../docs/config/my_slave.json'
        self.base =  None
        self.conn = None
        self.ins = None

        self.base= BaseDB()
        self.base.load_config(self.slave_config)
        self.conn, db, t = self.base.connect_server()
        self.ins = Slave(self.conn)

    def test_slave(self):
        self.assertIsNotNone(self.ins.get_job())

    # def test_get_job(self):
    #     j = self.ins.get_job()
    #     pprint.pprint(ins.list_jobs())

unittest.main()
