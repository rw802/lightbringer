import unittest

from basedb import BaseDB
from master import Master

import arctic.auth

class TestDB(unittest.TestCase):
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
        ins.load_config(self.config)
        conn, db, t = ins.connect_server()
        self.assertTrue(t)

    def test_master(self):
        ins = BaseDB()
        ins.load_config(self.config)
        conn, db, t = ins.connect_server()
        mast = Master(conn)
        self.assertGreater(len(mast.list_libraries()), 0)

    def test_slave(self):
        ins = BaseDB()
        ins.load_config(self.slave_config)
        conn, db, t = ins.connect_server()
        slave = Slave(conn)
        self.assertGreater(len(slave.list_symbols()), 0)


unittest.main()
