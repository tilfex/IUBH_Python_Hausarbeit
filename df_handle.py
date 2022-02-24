import pandas as pd
import sys

class DataframeHandle(pd.DataFrame):
    """
    Creates the dataframe of a csv-file or creates a dataframe without the 
    first column.

    Attributes:
        csv_file_location: The path to the csv-file
    """

    def __init__(self, csv_file_location):
        """ 
        Initializes the class.

        Arguments:
            csv_file_location: The path to the csv-file
        """
        super().__init__()
        self.csv_file_location = csv_file_location
        self.create_df_csv()

    def create_df_csv(self):
        """
        Creates the dataframe of a csv-file.
        """
        try:
            new_df = pd.read_csv(self.csv_file_location)
            new_df.sort_values(by=new_df.columns.values[0], inplace=True)
            self.__dict__.update(new_df.__dict__)
        except Exception as err:
            print(err)
            print('Datei ist ungültig')
            print('Das Programm wird beendet')
            sys.exit()

    def create_df_wo_x(self):
        """
        Creates a dataframe without the first column out of a already existing 
        dataframe.

        """

        # Removes the `x` column from dataframe then save
        self.df_wo_x = self.drop(['x'], axis=1)
        return self.df_wo_x
