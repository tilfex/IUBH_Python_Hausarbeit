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
    def __init__(self, triple):
        """ 
        Initializes the class.

        Arguments:
            name: the name of a column
        """
        self.testdata = TestData()
        self.traindata = TrainData()
        self.triple = triple
        
        self.name = triple[1]
        self.max_diff_ideal_train = triple[2]
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
    
    def compare_ideal_test(self):
        """
        Calculates the differences between one of the chosen ideal-function and the testdata.

        x(test)  y(ideal)  y(test) diff
        Returns:
            res: An array containing the differences
        """
        df_right = pd.DataFrame()
        df_right['x'] = self.testdata.df['x']
        
        df_left = pd.DataFrame()
        df_left['x'] = self.df['x']
        df_left['Y (Ideal Funktion)'] = self.df.iloc[:, 1]
        
        df_right = df_right.merge(df_left, on='x', how='left')
        df_right['Y1 (Test Funktion)'] = self.testdata.df['y']
        df_right['Delta Y (Abweichung)'] = np.absolute(df_right['Y1 (Test Funktion)'] - df_right['Y (Ideal Funktion)'])

        # The following line add name of ideal function into the dataframe,
        # as per task description (tabelle 3)
        # df.shape[0] gets the number of rows in a dataframe
        df_right['Nummer der Idealen Funktion'] = [self.name]*df_right.shape[0]


        # The following line creates a new column in df_right, named as criteria
        # The data in this criteria column is:
        # When number in column `Delta Y (Abweichung)` is smaller than sqrt(2)*max_diff_ideal_train
        # the data in criteria column is True, else it's False
        df_right['criteria'] = df_right.loc[:, 'Delta Y (Abweichung)'] < np.sqrt(2) * self.max_diff_ideal_train

        # The following line creates another dataframe, which is a slice of df_right.
        # The new dataframe contains rows from df_right, only when:
        # The `criteria` data in this row is True
        # Here the `lambda df: df['criteria'] == True` is the same as:
        # def filter(df):
        #   return df['criteria'] == True
        # That is, it's a function that returns true, only when the criteria value is True.
        self.diff_df = df_right.loc[lambda df: df['criteria'] == True, :]
        return self.diff_df



    def save_to_csv(self, filename):
        """
        Saves the test-data, the fitting ideal-function and the difference 
        between these in a csv-file, if the criteria of 'is_meeting_criteria()'
        is satisfied.
        """
        self.diff_df.to_csv(filename, index=False)
