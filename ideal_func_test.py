import unittest
from ideal_func import *

class TestIdealFunc(unittest.TestCase):
    def test___init__(self):
        with self.assertRaises(Exception):
            self.idealfunc = IdealFunc(
                triple=('y1', 'y1'),
                train_data_path='testdata/test_train_data.csv',
                ideal_data_path='testdata/test_ideal_data.csv',
                test_data_path='testdata/test_test_data.csv'
            )

        with self.assertRaises(SystemExit):
            self.idealfunc = IdealFunc(
                triple=('y1', 'y1', 0),
                train_data_path='noexist',
                ideal_data_path='testdata/test_ideal_data.csv',
                test_data_path='testdata/test_test_data.csv'
            )

    def test_compare_ideal_test(self):
        idealfunc1 = IdealFunc(
            triple=('y2', 'y4', 0.005),
            train_data_path='testdata/test_train_data.csv',
            ideal_data_path='testdata/test_ideal_data.csv',
            test_data_path='testdata/test_test_data.csv'
        )
        diff_df1 = idealfunc1.compare_ideal_test()
        self.assertEqual(diff_df1.shape[0], 5)

        idealfunc2 = IdealFunc(
            triple=('y1', 'y1', 0.005),
            train_data_path='testdata/test_train_data.csv',
            ideal_data_path='testdata/test_ideal_data.csv',
            test_data_path='testdata/test_test_data.csv'
        )
        diff_df2 = idealfunc2.compare_ideal_test()
        self.assertEqual(diff_df2.shape[0], 4)

        idealfunc3 = IdealFunc(
            triple=('y1', 'y2', 0.005),
            train_data_path='testdata/test_train_data.csv',
            ideal_data_path='testdata/test_ideal_data.csv',
            test_data_path='testdata/test_test_data.csv'
        )
        diff_df3 = idealfunc3.compare_ideal_test()
        self.assertEqual(diff_df3.shape[0], 0)

if __name__ == '__main__':
    unittest.main()

