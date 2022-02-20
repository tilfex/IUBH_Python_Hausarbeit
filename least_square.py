from cmath import sqrt
from more_itertools import difference
import pandas as pd
import numpy as np
from push_data_in_db import train_file, ideal_file, test_file

# create function to create a dataframe with an user defined exception handling
def create_dataframe(csv_file):
    try:
        new_df = pd.read_csv(csv_file)
        return new_df
    except:
        print('Datei existiert nicht, oder es handelt sich nicht um eine .csv-Datei')
        print('Das Programm wird beendet')
        exit
    

ideal_df = create_dataframe(ideal_file)
train_df = create_dataframe(train_file)

# change dataframe for calculation. X column gets removed
ideal_df_wo_x = ideal_df.loc[:, 'y1':]
train_df_wo_x = train_df.loc[:, 'y1':]


# calculate the sum of the square difference to get the four ideal function with the least squre difference
# define the needed datdaframes
df_sum_sq_diff = pd.DataFrame()
all_sq_diff = pd.DataFrame()
df_least_square = pd.DataFrame()

# loop through the columns of the ideal function
for i in ideal_df_wo_x.columns:
    ideal_col = ideal_df_wo_x.loc[:,i]
    df_sq_train = pd.DataFrame()
    # for each ideal function we loop through the training data columns
    for k in train_df_wo_x.columns:
        train_col = train_df_wo_x.loc[:,k]
        # for each column of the ideal functions, we calculate the differnces to each training data clolumn and square these
        df_sq_train[k]= np.square(ideal_col-train_col)
    # in the following the sum of all squared differences are calculated, so we get one number for each ideal-training-pair
    df_sum_sq_diff[i] = df_sq_train.sum()
# afterwards the sum of all training-data results is calculated,
# so we get to see the sum of all squared differences for each ideal function
all_sq_diff = df_sum_sq_diff.sum()
# to find the four ideal functions with the least squared differences the results get sorted, so the first four rows show the ideal 
# functions, which have the least squared differences
all_sq_diff.sort_values(inplace=True)
# after sorting them we put the four ideal function, which we want to compare with the test data into a new dataframe
df_least_square = all_sq_diff.head(4)
    
# now we do the same for the chosen four ideal functions and the test data. Therefore we put the chosen four functions into a new dataframe
df_chosen_ideal = pd.DataFrame()

# create a list with the names of the four ideal function
list_four_ideal = ['x'] + df_least_square.index.tolist()

# now put the ideal function with the help of the list into the newly created dataframe and separate them in a new dateframe for each
df_chosen_ideal = ideal_df.loc[:, list_four_ideal]
# create a function to create the dataframes
def push_ideal_function_in_df(column_number):
    df_chosen_ideal_x = pd.DataFrame()
    df_chosen_ideal_x ['x'] = df_chosen_ideal ['x']
    df_chosen_ideal_x ['y'] = df_chosen_ideal.iloc[:, column_number]
    return(df_chosen_ideal_x)

df_ideal_1 = push_ideal_function_in_df(1)
df_ideal_2 = push_ideal_function_in_df(2)
df_ideal_3 = push_ideal_function_in_df(3)
df_ideal_4 = push_ideal_function_in_df(4)

# now we get the data from the test.csv file unto a dataframe and sort it by x for easier usage, also we create a dataset without the x 
# value for calculations
test_df = create_dataframe(test_file) 
test_df.sort_values(by='x', inplace=True)
test_df_wo_x = test_df.iloc[:, 1]

# create a list of the x-values to filter the needed x-values from the ideal-functions
x_values = {'x': list(test_df['x'])}

#now we get the needed data from the ideal functions
df_x_test_ideal = pd.DataFrame()
df_x_test_ideal = df_chosen_ideal[df_chosen_ideal.isin(x_values).any(1)]

# define a function to get the sum of the squared difference betweet the test-data and one ideal-function
def get_squared_diff_test_ideal(df_ideal_num):
    df_right = pd.DataFrame()
    df_right['x']=test_df['x']
    df_left = pd.DataFrame()
    df_left['x']=df_ideal_num['x']
    df_left['y']=df_ideal_num.iloc[:, 1]
    df_right = df_right.merge(df_left, on='x', how='left')
    df_right.sort_values(by='x', inplace=True)
    df_right_wo_x = df_right.iloc[:, 1]
    df_sq_test_ideal= np.square(df_right_wo_x-test_df_wo_x)
    df_sq_test_ideal_sum_diff = df_sq_test_ideal.sum()
    return (df_sq_test_ideal_sum_diff)

sq_diff_test_ideal_1 = get_squared_diff_test_ideal(df_ideal_1)
sq_diff_test_ideal_2 = get_squared_diff_test_ideal(df_ideal_2)
sq_diff_test_ideal_3 = get_squared_diff_test_ideal(df_ideal_3)
sq_diff_test_ideal_4 = get_squared_diff_test_ideal(df_ideal_4)

print(sq_diff_test_ideal_1*sqrt(2))
print(sq_diff_test_ideal_2*sqrt(2))
print(sq_diff_test_ideal_3*sqrt(2))
print(sq_diff_test_ideal_4*sqrt(2))
print(df_least_square)