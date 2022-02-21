import settings
from df_handle import DataframeHandle
import pandas as pd
import numpy as np



class TrainData(object):

    def __init__(self):
        self.df = DataframeHandle(settings.TRAIN_DATA_PATH)
        self.df_wo_x = self.df.create_df_wo_x()
        self._init_ideal_df()
    
    def _init_ideal_df(self):
        self.ideal_df = DataframeHandle(settings.IDEAL_DATA_PATH)
        self.ideal_df_wo_x = self.ideal_df.create_df_wo_x()
    
    def get_selected_ideal_funcs(self):
        all_diff = pd.Series()
        for i in self.ideal_df_wo_x.columns:
            # For each ideal function
            curr_ideal_func = self.ideal_df_wo_x.loc[:, i]
            curr_diff = 0

            # Get the squared & summed difference between ideal func and each train data column
            for k in self.df_wo_x.columns:
                # For each train data column
                train_col = self.df_wo_x.loc[:, k]
                # Get the difference between ideal func and train data column
                # Then square and sum
                curr_diff += np.square(curr_ideal_func-train_col).sum()
            all_diff.loc[i] = curr_diff
        # results get sorted to find the four ideal functions with the least squared differences
        all_diff.sort_values(inplace=True)
        # after sorting them we put the four ideal function, which we want to compare with the test data into a new dataframe
        selected_func_names = all_diff.head(settings.NUM_SELECTED_IDEALS).index.tolist()
        return selected_func_names