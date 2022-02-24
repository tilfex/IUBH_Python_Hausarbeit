import unittest
from db_handle import *

class TestConnectDatabase(unittest.TestCase):
    def setUp(self):
        self.cd = ConnectDatabase()

    def test__connect(self):
        self.cd._connect()
        self.assertFalse(self.cd.conn.closed)
        self.cd._close_connect()

    def test__close_connect(self):
        self.cd._connect()
        self.cd._close_connect()
        self.assertTrue(self.cd.conn.closed)

if __name__ == '__main__':
    unittest.main()
