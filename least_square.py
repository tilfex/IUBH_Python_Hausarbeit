from more_itertools import difference
import pandas as pd
import numpy as np
from push_data_in_db import train_file, ideal_file, test_file

# create dataframes of the ideal- and train dataset
ideal_df=pd.read_csv(ideal_file)
train_df = pd.read_csv(train_file)

# change dataframe for calculation. X column gets removed
ideal_df_wo_x = ideal_df.loc[:, 'y1':]
train_df_wo_x = train_df.loc[:, 'y1':]

# define function to calculate the sum of the square difference
def get_all_sq_diff():
    df_sum_sq_diff = pd.DataFrame()
    all_sq_diff = pd.DataFrame()
    df_least_square = pd.DataFrame()
    for i in ideal_df_wo_x.columns:
        ideal_col = ideal_df_wo_x.loc[:,i]
        df_sq_train = pd.DataFrame()
        for k in train_df_wo_x.columns:
            train_col = train_df_wo_x.loc[:,k]
            df_sq_train[k]= np.square(ideal_col-train_col)
        df_sum_sq_diff[i] = df_sq_train.sum()
    all_sq_diff = df_sum_sq_diff.sum()
    all_sq_diff.sort_values(inplace=True)
    

#     print(all_sq_diff)
# c = get_all_sq_diff()

