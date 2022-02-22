from train_data import TrainData
from test_data import TestData
from df_handle import DataframeHandle
import settings
import pandas as pd
import numpy as np

class IdealFunc(object):
    """
    Does all calculations regarding one ideal-function.

    Creates a dataframe of the csv-file for the ideal-functions, to 
    calculate the difference between the ideal-functions and the training-data
    or the test-data. With the ideal-training difference it calculates the
    maximum of the differences of all training_data and the sum of
    all squared differences. With the ideal-test difference it calculates the 
    maximum of the differences and compares the result with the maximum of the
    ideal-training differences, to see if the criteria is satisfied. If the
    criteria is satisfied, the results get saved in a csv-file.


    Attributes:
        testdata: An instance of TestData-class
        traindata: An instance of TrainData-class
        name: the name of a column
        df: a dataframe for a ideal-function
    """
    def __init__(self, name):
        """ 
        Initializes the class.

        Arguments:
            name: the name of a column
        """
        self.testdata = TestData()
        self.traindata = TrainData()
        
        self.name = name
        self.df = None

        self._init_ideal_df()
        self.generate_df()

    def _init_ideal_df(self):
        """
        Creates a dataframe of all ideal-functions
        """
        self.ideal_df = DataframeHandle(settings.IDEAL_DATA_PATH)
    
    def generate_df(self):
        """
        Generates dataframes for one ideal-function.
        """
        curr_df = pd.DataFrame()
        curr_df['x'] = self.ideal_df['x']
        curr_df[self.name] = self.ideal_df[self.name]
        self.df = curr_df
    
    def _get_diff_with_test(self):
        """
        Calculates the differences between a ideal-function and the testdata.

        Returns:
            res: An array containing the differences
        """
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
        """
        Gives the max difference between an ideal-function and the 
        test-data.

        Returns:
            Max difference between an ideal-function and the 
            test-data
        """
        return max(np.absolute(self._get_diff_with_test()))
    
    def _get_diff_with_train(self):
        """
        Calculates the differences between an ideal-function and all 
        training-data.

        Returns:
            diffs: A dataframe of the differences between an ideal-function and 
            all training-data
        """
        ideal_func = self.df.iloc[:, 1]
        diffs = []
        for j in self.traindata.df_wo_x.columns:
            train_column = self.traindata.df_wo_x.loc[:, j]
            curr_diffs = np.absolute(ideal_func - train_column)
            diffs.append(curr_diffs)
        return diffs
    
    def _get_max_diff_with_train(self):
        """
        Gives the max difference between an ideal-function and all 
        training-data.

        Returns:
            Max difference between an ideal-function and all 
            training-data
        """
        return np.max(self._get_diff_with_train())
    
    def is_meeting_criteria(self):
        """
        Checks, if the criteria - the max difference between training-data and
        the ideal-function times the squareroot of two, is not allowed to be
        smaller than the max difference between test-data and the 
        ideal-function - is satisfied. 

        Returns:
            Boolean to tell if the criteria is satisfied
        """
        train_ideal_diff = self._get_max_diff_with_train()
        test_ideal_diff = self._get_max_diff_with_test()
        
        if test_ideal_diff > np.sqrt(2) * train_ideal_diff:
            return False
        else:
            return True
    
    def save_to_csv(self, filename):
        """
        Saves the test-data, the fitting ideal-function and the difference 
        between these in a csv-file, if the criteria of 'is_meeting_criteria()'
        is satisfied.
        """
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
        df.to_csv(filename, index=False)
