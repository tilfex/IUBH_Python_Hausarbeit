import pandas as pd
import numpy as np
from push_data_in_db import train_file, ideal_file, test_file, create_table


def create_dataframe(csv_file):
    """
    This function creates a dataframe for a csv-file. 
    It uses an exception handling to test if the file is existing or if it is a csv-file

    'new_df' is the variable for the dataframe, which gets returned.
    'csv_file' is the location of the file, which has to be entered when running the function
    """
    try:
        new_df = pd.read_csv(csv_file)
        return new_df
    except:
        print('Datei existiert nicht, oder es handelt sich nicht um eine .csv-Datei')
        print('Das Programm wird beendet')
        exit


ideal_df = create_dataframe(ideal_file)
train_df = create_dataframe(train_file)

# create dataframes without the x column and empty dataframes for next loop
ideal_df_wo_x = ideal_df.loc[:, 'y1':]
train_df_wo_x = train_df.loc[:, 'y1':]
df_sum_sq_diff = pd.DataFrame()
all_sq_diff = pd.DataFrame()
df_least_square = pd.DataFrame()

# loop through the columns of the ideal functions.
for i in ideal_df_wo_x.columns:
    ideal_col = ideal_df_wo_x.loc[:, i]
    df_sq_train = pd.DataFrame()
    # loop through the training data columns for each ideal function
    for k in train_df_wo_x.columns:
        train_col = train_df_wo_x.loc[:, k]
        # calculate the differnces to each train data column and square these
        df_sq_train[k] = np.square(ideal_col-train_col)
    # calculate sum of all squared differences
    df_sum_sq_diff[i] = df_sq_train.sum()
# calculate sum of all squared differences for each ideal function
all_sq_diff = df_sum_sq_diff.sum()
# results get sorted to find the four ideal functions with the least squared differences
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
    df_chosen_ideal_x['x'] = df_chosen_ideal['x']
    df_chosen_ideal_x[list(df_chosen_ideal.columns.values.tolist())[
        column_number]] = df_chosen_ideal.iloc[:, column_number]
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

# now we get the needed data from the ideal functions
#
#
# DO I STILL NEED THIS????
df_x_test_ideal = pd.DataFrame()
df_x_test_ideal = df_chosen_ideal[df_chosen_ideal.isin(x_values).any(1)]

# define a function to get the differences between the test-data and one ideal-function


def get_diff_test_ideal(df_ideal_num):
    df_right = pd.DataFrame()
    df_right['x'] = test_df['x']
    df_left = pd.DataFrame()
    df_left['x'] = df_ideal_num['x']
    df_left['y'] = df_ideal_num.iloc[:, 1]
    df_right = df_right.merge(df_left, on='x', how='left')
    df_right.sort_values(by='x', inplace=True)
    df_right_wo_x = df_right.iloc[:, 1]
    df_diff_test_ideal = (df_right_wo_x-test_df_wo_x)
    return (df_diff_test_ideal)


# for the criteria to check if the max of differences ideal-test is not bigger than the squareroot of 2 times the max difference
# between ideal-training we get the max difference of each pair und get the positive value of it
# first we get the max of the ideal-test pair
test_ideal_max_diff_1 = max(np.absolute((get_diff_test_ideal(df_ideal_1))))
test_ideal_max_diff_2 = max(np.absolute((get_diff_test_ideal(df_ideal_2))))
test_ideal_max_diff_3 = max(np.absolute((get_diff_test_ideal(df_ideal_3))))
test_ideal_max_diff_4 = max(np.absolute((get_diff_test_ideal(df_ideal_4))))

# now we get the max of the ideal-training pair ,therefore we define a function which gives us the searched values


def get_diff_train_ideal(df_ideal_num):
    df_diff_train_ideal = pd.DataFrame()
    df_ideal_num_wo_x = df_ideal_num.iloc[:, 1]
    max_diff = []
    for i in train_df_wo_x.columns:
        train_column = train_df_wo_x.loc[:, i]
        df_diff_train_ideal[i] = np.absolute(df_ideal_num_wo_x-train_column)
        max_diff.append(max(df_diff_train_ideal[i]))
    max_diff = max(max_diff)
    return (max_diff)


# with the defined function we get the max of the ideal_train pairs
train_ideal_max_diff_1 = get_diff_train_ideal(df_ideal_1)
train_ideal_max_diff_2 = get_diff_train_ideal(df_ideal_2)
train_ideal_max_diff_3 = get_diff_train_ideal(df_ideal_3)
train_ideal_max_diff_4 = get_diff_train_ideal(df_ideal_4)

# now we define a function, which checks if the acquirement of if the max of differences ideal-test is not bigger than
# the squareroot of 2 times the max difference between ideal-training and afterwards a table should be created with the data


def acquirement_check_create_csv(train_diff_num, test_diff_num, df_ideal_num, column_number, filename):
    if test_diff_num > np.sqrt(2)*train_diff_num:
        print("Anforderung wurde nicht erfüllt")
        return None
    df_for_csv = pd.DataFrame()
    df_for_csv = test_df.copy(deep=True)
    df_for_csv['Delya Y (Abweichung)'] = np.absolute(
        get_diff_test_ideal(df_ideal_num))
    df_right = pd.DataFrame()
    df_right['x'] = test_df['x']
    df_left = pd.DataFrame()
    df_left['x'] = df_ideal_num['x']
    df_left[df_chosen_ideal.columns.values.tolist()[
        column_number]] = df_ideal_num.iloc[:, 1]
    df_right = df_right.merge(df_left, on='x', how='left')
    df_right.sort_values(by='x', inplace=True)
    
    curr_column_name = df_chosen_ideal.columns.values.tolist()[column_number]
    
    df_for_csv[curr_column_name] = df_right[curr_column_name]
    df_for_csv.to_csv(filename)



csv_1 = acquirement_check_create_csv(
    train_ideal_max_diff_1, test_ideal_max_diff_1, df_ideal_1, 1, 'compare_diff_1.csv')
csv_2 = acquirement_check_create_csv(
    train_ideal_max_diff_2, test_ideal_max_diff_2, df_ideal_2, 2, 'compare_diff_2.csv')
csv_3 = acquirement_check_create_csv(
    train_ideal_max_diff_3, test_ideal_max_diff_3, df_ideal_3, 3, 'compare_diff_3.csv')
csv_4 = acquirement_check_create_csv(
    train_ideal_max_diff_4, test_ideal_max_diff_4, df_ideal_4, 4, 'compare_diff_4.csv')
