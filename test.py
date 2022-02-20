import unittest
from push_data_in_db import get_data as gd

class UnitTestCsvFile(unittest.TestCase):
    def test_get_data(self):
        with self.assertRaises(FileNotFoundError) as fnfe:
            result = gd('filename.txt')

if __name__ == '__main__':
    unittest.main()