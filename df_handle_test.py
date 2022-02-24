import unittest
from df_handle import *

class TestDataframeHandle(unittest.TestCase):
    """
    The class for testing DataframeHandle class and its methods.
    """
    def test_create_df_csv(self):
        """ Test create_df_csv() method.

        The test creates a DataframeHandle object with a non-existing csv file.
        The program is expected to exit since the file path is invalid. The
        test checks if the program exits, and asserts failure if not.
        """
        with self.assertRaises(SystemExit):
            df = DataframeHandle("nonexist")

    def test_create_df_wo_x(self):
        """ Test create_df_wo_x() method.

        First test creates a DataframeHandle object with "testdata/test_df_1.csv"
        a mock dataset. The dataset has 2 columns: 'x' and 'y'. After
        create_df_wo_x(), the 'x' column is removed and there should be only
        one column left. The test checks if the number of columns is 1, and
        asserts failure if not.

        Second test is similar but uses data from "testdata/test_df_2.csv". The
        dataset has only 1 column, and should have 0 column after calling
        create_df_wo_x(). The test checks if the number of columns is 0, and
        asserts failure if not.
        """
        df = DataframeHandle("testdata/test_df_1.csv")
        df.create_df_wo_x()
        self.assertEqual(df.df_wo_x.shape[1], 1)

        df = DataframeHandle("testdata/test_df_2.csv")
        df.create_df_wo_x()
        self.assertEqual(df.df_wo_x.shape[1], 0)

if __name__ == '__main__':
    unittest.main()
