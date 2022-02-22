import pandas as pd

class DataframeHandle(pd.DataFrame):
    """
    Creates the dataframe of a csv-file or creates a dataframe without the first column.

    Attributes:
        csv_file_location: the path to the csv-file
    """
    def __init__(self, csv_file_location):
        """ 
        Initializes the class.

        Arguments:
            csv_file_location: the path to the csv-file
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
            new_df.sort_values(by='x', inplace=True)
            self.__dict__.update(new_df.__dict__)
        except Exception as err:
            print(err)
            print('Datei existiert nicht, oder es handelt sich nicht um eine .csv-Datei')
            print('Das Programm wird beendet')
            exit()
    
    def create_df_wo_x(self):
        """
        Creates a dataframe without the first column out of a already existing dataframe.
        """
        self.df_wo_x = self.iloc[:, 1:]
        return self.df_wo_x