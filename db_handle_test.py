import unittest
from db_handle import *

class TestConnectDatabase(unittest.TestCase):
    """
    The class for testing ConnectDatabase class and its methods.
    """
    def setUp(self):
        """ Setting up the tests before tests start.

        Create a ConnectDatabase object and store it in self.cd.
        """
        self.cd = ConnectDatabase()

    def test__connect(self):
        """ Test _connect() method.

        The test sets up a connection with database. After connection, the 
        cd.conn.closed should be False. The test checks if it's False, and
        asserts failure if not. The connection is closed after test finishes.
        """
        self.cd._connect()
        self.assertFalse(self.cd.conn.closed)
        self.cd._close_connect()

    def test__close_connect(self):
        """ Test _connect() method.

        The test sets up a connection with database, then close it. After
        closing, cd.conn.closed should be True. The test checks if it's True,
        and asserts failure if not.
        """
        self.cd._connect()
        self.cd._close_connect()
        self.assertTrue(self.cd.conn.closed)

if __name__ == '__main__':
    unittest.main()
