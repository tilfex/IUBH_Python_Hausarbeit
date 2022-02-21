import settings
from df_handle import DataframeHandle
import pandas as pd
import numpy as np

class TestData(object):

    def __init__(self):
        self.df = DataframeHandle(settings.TEST_DATA_PATH)
        self.df_wo_x = self.df.create_df_wo_x()
    
    # define a function to get the differences between the test-data and one ideal-function
    def _get_diff_test_ideal(self, ideal_func_df):
        df_right = pd.DataFrame()
        df_right['x'] = self.df['x']
        
        df_left = pd.DataFrame()
        df_left['x'] = ideal_func_df['x']
        df_left['y'] = ideal_func_df.iloc[:, 1]
        
        df_right = df_right.merge(df_left, on='x', how='left')
        df_right_wo_x = df_right.iloc[:, 1]
        res = np.array(df_right_wo_x) - np.array(self.df_wo_x)
        return res

