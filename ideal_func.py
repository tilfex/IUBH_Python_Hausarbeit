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
        testdata:               An instance of TestData-class
        traindata:              An instance of TrainData-class
        triple:                 A list of three tuples
        name:                   The name of a column
        max_diff_ideal_train:   The difference between two y-values
        df:                     A dataframe for a ideal-function
    """

    def __init__(self, triple,
                 ideal_data_path=settings.IDEAL_DATA_PATH,
                 test_data_path=settings.TEST_DATA_PATH,
                 train_data_path=settings.TRAIN_DATA_PATH):
        """ 
        Initializes the class.

        Arguments:
            triple:             A list of three tuples
            ideal_data_path:    Path to ideal data csv file
            train_data_path:    Path to train data csv file
            test_data_path:     Path to test data csv file
        """
        self.testdata = TestData(test_data_path)
        self.traindata = TrainData(train_data_path)
        self.triple = triple
        try:
            self.name = triple[1]
            self.max_diff_ideal_train = triple[2]
            self.df = None

            self._init_ideal_df(ideal_data_path)
            self.generate_df()
        except:
            raise Exception("")

    def _init_ideal_df(self, ideal_data_path):
        """
        Creates a dataframe of all ideal-functions

        Arguments:
            ideal_data_path: Path to ideal data csv file
        """
        self.ideal_df = DataframeHandle(ideal_data_path)

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
        Calculates the differences between one of the chosen ideal-function and 
        the testdata.

        Returns:
            sel.diff_df:    An dataframe which contains the values for the 
                            fitting test-data, ideal-function-values and the 
                            difference between these
        """
        df_right = pd.DataFrame()
        df_right['x'] = self.testdata.df['x']

        df_left = pd.DataFrame()
        df_left['x'] = self.df['x']
        df_left['Y (Ideal Funktion)'] = self.df.iloc[:, 1]

        df_right = df_right.merge(df_left, on='x', how='left')
        df_right['Y (Test Funktion)'] = self.testdata.df['y']
        df_right['Delta Y (Abweichung)'] = np.absolute(
            df_right['Y (Test Funktion)'] - df_right['Y (Ideal Funktion)'])

        # The following line adds name of ideal function into the dataframe,
        # as per task description (tabelle 3)
        # df.shape[0] gets the number of rows in a dataframe
        df_right['Nummer der Idealen Funktion'] = [self.name]*df_right.shape[0]

        # The following line creates a new column in df_right, named as criteria
        # The data in this criteria column is:
        # When number in column `Delta Y (Abweichung)` is smaller than sqrt(2)*max_diff_ideal_train
        # the data in criteria column is True, else it's False
        df_right['criteria'] = df_right.loc[:, 'Delta Y (Abweichung)'] < np.sqrt(
            2) * self.max_diff_ideal_train

        # The following line creates another dataframe, which is a slice of df_right.
        # The new dataframe contains rows from df_right, only when:
        # The `criteria` data in this row is True
        # Here the `lambda df: df['criteria'] == True` is the same as:
        # def filter(df):
        #   return df['criteria'] == True
        # That is, it's a function that returns true, only when the criteria value is True.
        results_df = pd.DataFrame()
        results_df = df_right.loc[lambda df: df['criteria'] == True, :]

        # In the following lines a dataframe in a wanted structure is created,
        # which will be used to create a csv file and upload the data to the
        # database into a newly created table
        self.diff_df = pd.DataFrame()
        self.diff_df['X - test'] = results_df['x']
        self.diff_df['Y - test'] = results_df['Y (Test Funktion)']
        self.diff_df['Delta Y (Abweichung)'] = results_df['Delta Y (Abweichung)']
        self.diff_df['Funktion - ' +
                     self.name] = results_df['Y (Ideal Funktion)']

        return self.diff_df

    def save_to_csv(self, filename):
        """
        Saves the test-data, the fitting ideal-function and the difference 
        between these in a csv-file, if the criteria of 'is_meeting_criteria()'
        is satisfied.
        """
        self.diff_df.to_csv(filename, index=False)
