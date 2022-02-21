from train_data import TrainData
from test_data import TestData
from df_handle import DataframeHandle
import settings
import pandas as pd
import numpy as np

class IdealFunc(object):
    def __init__(self, name):
        self.testdata = TestData()
        self.traindata = TrainData()
        
        self.name = name
        self.df = None

        self._init_ideal_df()
        self.generate_df()

    def _init_ideal_df(self):
        self.ideal_df = DataframeHandle(settings.IDEAL_DATA_PATH)
    
    def generate_df(self):
        curr_df = pd.DataFrame()
        curr_df['x'] = self.ideal_df['x']
        curr_df[self.name] = self.ideal_df[self.name]
        self.df = curr_df
    
    def _get_diff_with_test(self):
        df_right = pd.DataFrame()
        df_right['x'] = self.testdata.df['x']
        
        df_left = pd.DataFrame()
        df_left['x'] = self.df['x']
        df_left['y'] = self.df.iloc[:, 1]
        
        df_right = df_right.merge(df_left, on='x', how='left')
        df_right_wo_x = df_right.iloc[:, 1]
        testdata_wo_x = self.testdata.df.iloc[:, 1]
        res = np.array(df_right_wo_x) - np.array(testdata_wo_x)
        return res
    
    def _get_max_diff_with_test(self):
        return max(np.absolute(self._get_diff_with_test()))
    
    def _get_diff_with_train(self):
        ideal_func = self.df.iloc[:, 1]
        diffs = []
        for j in self.traindata.df_wo_x.columns:
            train_column = self.traindata.df_wo_x.loc[:, j]
            curr_diffs = np.absolute(ideal_func - train_column)
            diffs.append(curr_diffs)
        return diffs
    
    def _get_max_diff_with_train(self):
        return np.max(self._get_diff_with_train())
    
    def is_meeting_criteria(self):
        train_ideal_diff = self._get_max_diff_with_train()
        test_ideal_diff = self._get_max_diff_with_test()
        
        if test_ideal_diff > np.sqrt(2) * train_ideal_diff:
            return False
        else:
            return True
    
    def save_to_csv(self, filename):
        if self.is_meeting_criteria() is not True:
            raise Exception("Anforderung wurde nicht erfüllt")

        df = self.testdata.df.copy(deep=True)
        df['Delya Y (Abweichung)'] = self._get_diff_with_test()

        df_right = pd.DataFrame()
        df_right['x'] = self.testdata.df['x']
        df_left = self.df.copy(deep=True)
        df_right = df_right.merge(df_left, on='x', how='left')
        df_right = df_right.reset_index()
        df = df.reset_index()
        df[self.name] = df_right[self.name]
        print(df)
        df.to_csv(filename, index=False)
