import unittest
from ideal_func import *

class TestIdealFunc(unittest.TestCase):
    """
    The class for testing IdealFunc class and its methods.
    """
    def test___init__(self):
        """ Test __init__() method.

        The first test passes incomplete argument (a tuple of 2 elements
        instead of 3) to __init__(). The method should raise an exception.
        The test asserts failure if no exception is raised.

        The second test passes a non-existing file as train_data_path to
        __init__(). The program is expected to end. The test asserts failure
        if program does not end.
        """
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
        """ Test compare_ideal_test() method.

        The first test calculates how many points from mock test dataset are 
        close enough to idealfunction y4 (by close enough, here the criteria
        is, distance is less than sqrt(2)*0.005). The mock test dataset is
        designed so that there should be exactly 5 points. The test checks if
        there are 5 rows in the result of compare_ideal_test(). If not, the
        test asserts failure.

        The second test is similar to first test, but it's checking about
        idealfunction y1. There should be exactly 4 points. The test checks if
        there are 4 rows in the result of compare_ideal_test(), and asserts
        asserts failure if not.

        The third test is similar to first test, but it's checking about
        idealfunction y2. There should be exactly 1 point. The test checks if
        there are 1 row in the result of compare_ideal_test(), and asserts
        asserts failure if not.
        """
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

