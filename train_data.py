import settings
from df_handle import DataframeHandle
import numpy as np

class TrainData(object):
    """
    Selects the best fitting ideal-function for each training-dataset.

    Attributes:
        df:             A dataframe containing the trainingdata
        df_wo_x:        A dataframe containing the trainingdata without the 
                        x-column
        ideal_df:       A dataframe containing the idea-functions
        ideal_df_wo_x:  A dataframe containing the idea-functions without the 
                        x-column
    """

    def __init__(self, train_data_path=settings.TRAIN_DATA_PATH, ideal_data_path=settings.IDEAL_DATA_PATH):
        """ 
        Initializes the class.

        Arguments:
            ideal_data_path: Path to ideal data csv file
            train_data_path: Path to train data csv file
        """
        self.df = DataframeHandle(train_data_path)
        self.df_wo_x = self.df.create_df_wo_x()

        self.ideal_df = DataframeHandle(ideal_data_path)
        self.ideal_df_wo_x = self.ideal_df.create_df_wo_x()

    def get_selected_ideal_funcs(self):
        """
        Selects the best fitting ideal-function for each training-dataset.

        Returns: 
            list_pairs: List of dictionarys, which contains the 
                        training-dataset as key and fitting ideal-function 
                        as value
        """
        list_triples = []
        for i in self.df_wo_x.columns:
            curr_train_col = self.df_wo_x.loc[:, i]
            curr_diff = None
            name_chosen_ideal = None
            max_diff = None
            for k in self.ideal_df_wo_x.columns:
                curr_ideal_func = self.ideal_df_wo_x.loc[:, k]
                curr_max_diff = max(np.absolute(
                                    curr_ideal_func-curr_train_col))
                new_diff = np.square(curr_ideal_func-curr_train_col).sum()
                if curr_diff is None:
                    curr_diff = new_diff
                    name_chosen_ideal = k
                    max_diff = curr_max_diff
                elif new_diff < curr_diff:
                    curr_diff = new_diff
                    name_chosen_ideal = k
                    max_diff = curr_max_diff
                else:
                    continue
            train_ideal_triple = (i, name_chosen_ideal, max_diff)
            list_triples.append(train_ideal_triple)
        return list_triples
