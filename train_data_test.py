import unittest
from train_data import *

class TestTrainData(unittest.TestCase):
    def test_get_selected_ideal_funcs(self):
        self.td = TrainData(
            train_data_path='testdata/test_train_data.csv',
            ideal_data_path='testdata/test_ideal_data.csv'
        )
        list_triples = self.td.get_selected_ideal_funcs()
        list_trainfuncs = [x[0] for x in list_triples]
        list_idealfuncs = [x[1] for x in list_triples]
        # Compare with ground truth
        self.assertEqual(list_trainfuncs, ['y1', 'y2'])
        self.assertEqual(list_idealfuncs, ['y1', 'y4'])

if __name__ == '__main__':
    unittest.main()
