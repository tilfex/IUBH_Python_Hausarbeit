import pandas as pd

class DataframeHandle(pd.DataFrame):
    """
    
    """
    def __init__(self, csv_file_location):
        super().__init__()
        self.csv_file_location = csv_file_location
        self.create_df_csv()

    def create_df_csv(self):
        """
        
        """
        try:
            new_df = pd.read_csv(self.csv_file_location)
            new_df.sort_values(by='x', inplace=True)
            self.__dict__.update(new_df.__dict__)
        except Exception as err:
            print(err)
            print('Datei existiert nicht, oder es handelt sich nicht um eine .csv-Datei')
            print('Das Programm wird beendet')
    
    def create_df_wo_x(self):
        """
        
        """
        self.df_wo_x = self.iloc[:, 1:]
        return self.df_wo_x