"""
Plots the needed matplotlib-plots for the task
"""
from visual_handle import VisualHandle
from settings import TRAIN_DATA_PATH, TEST_DATA_PATH

# show the grafics for each training-data x-y-pair
training_data = VisualHandle(TRAIN_DATA_PATH, "Traingsdaten")
training_data.plot_single_matplot()

# show the grafics for the test-data x-y-pair
training_data = VisualHandle(TEST_DATA_PATH, "Testdaten")
training_data.plot_single_matplot()


# show the grafics for each compare between the chisen idealfunction and the 
# test-data
compare_1 = VisualHandle("compare_diff_1.csv", "")
compare_1.plot_compare_matplot()
compare_2 = VisualHandle("compare_diff_2.csv", "")
compare_2.plot_compare_matplot()
compare_3 = VisualHandle("compare_diff_3.csv", "")
compare_3.plot_compare_matplot()
compare_4 = VisualHandle("compare_diff_4.csv", "")
compare_4.plot_compare_matplot()