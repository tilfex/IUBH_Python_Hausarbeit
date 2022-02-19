import unittest
from data_import import get_data as gd

class UnitTestCsvFile(unittest.TestCase):
    def test_get_data(self):
        with self.assertRaises(FileNotFoundError) as fnfe:
            result = gd('filename.txt')

if __name__ == '__main__':
    unittest.main()