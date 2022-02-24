import settings
from df_handle import DataframeHandle

class TestData(object):
    """
    Creates a dataframe for the test-data and a dataframe for the test-data 
    without the first column. 

    Attributes:
        df:         A dataframe for the test-data
        df_wo_x:    A dataframe for the test-data without the first column
    """

    def __init__(self, test_data_path=settings.TEST_DATA_PATH):
        """ 
        Initializes the class.

        Arguments:
            test_data_path: Path to test data csv file
        """
        self.df = DataframeHandle(test_data_path)
        self.df_wo_x = self.df.create_df_wo_x()
