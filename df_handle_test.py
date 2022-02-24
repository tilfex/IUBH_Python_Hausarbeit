import unittest
from df_handle import *

class TestDataframeHandle(unittest.TestCase):
    def test_create_df_csv(self):
        with self.assertRaises(SystemExit):
            df = DataframeHandle("nonexist")

    def test_create_df_wo_x(self):
        df = DataframeHandle("testdata/test_df_1.csv")
        df.create_df_wo_x()
        self.assertEqual(df.df_wo_x.shape[1], 1)

        df = DataframeHandle("testdata/test_df_2.csv")
        df.create_df_wo_x()
        self.assertEqual(df.df_wo_x.shape[1], 0)

if __name__ == '__main__':
    unittest.main()
