import unittest
from df_handle import *


class TestDataframeHandle(unittest.TestCase):    
    def test___init__(self):
        df = DataframeHandle("nonexist")
        self.assertFalse(self.cd.conn.closed)
        self.cd._close_connect()
    

if __name__ == '__main__':
    unittest.main()