import settings
from df_handle import DataframeHandle
import pandas as pd
import numpy as np

class TestData(object):
    """
    Creates a dataframe for the test-data and a dataframe for the test-data 
    without the first column. 

    Attributes:
        df: a dataframe for the test-data
        df_wo_x: a dataframe for the test-data without the first column
    """

    def __init__(self):
        self.df = DataframeHandle(settings.TEST_DATA_PATH)
        self.df_wo_x = self.df.create_df_wo_x()