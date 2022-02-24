"""
Plots the needed bokeh-plots for the task
"""
from visual_handle import VisualHandle
from settings import IDEAL_DATA_PATH

# show the grafics for each training-data/ideal-function-pair
comp_train_ideal_1 = VisualHandle(
    IDEAL_DATA_PATH, "Vergleich Traingsdaten-Idealfunktion", 1)
comp_train_ideal_1.plot_train_ideal_bokeh()
comp_train_ideal_2 = VisualHandle(
    IDEAL_DATA_PATH, "Vergleich Traingsdaten-Idealfunktion", 2)
comp_train_ideal_2.plot_train_ideal_bokeh()
comp_train_ideal_3 = VisualHandle(
    IDEAL_DATA_PATH, "Vergleich Traingsdaten-Idealfunktion", 3)
comp_train_ideal_3.plot_train_ideal_bokeh()
comp_train_ideal_4 = VisualHandle(
    IDEAL_DATA_PATH, "Vergleich Traingsdaten-Idealfunktion", 4)
comp_train_ideal_4.plot_train_ideal_bokeh()

# show the grafics for the testdata/ideal-frunction-pair
test_to_ideal_1 = VisualHandle(
    IDEAL_DATA_PATH, "Vergleich Testdaten-Idealfunktion", 1)
test_to_ideal_1.plot_test_ideal_bokeh()
test_to_ideal_2 = VisualHandle(
    IDEAL_DATA_PATH, "Vergleich Testdaten-Idealfunktion", 2)
test_to_ideal_2.plot_test_ideal_bokeh()
test_to_ideal_3 = VisualHandle(
    IDEAL_DATA_PATH, "Vergleich Testdaten-Idealfunktion", 3)
test_to_ideal_3.plot_test_ideal_bokeh()
test_to_ideal_4 = VisualHandle(
    IDEAL_DATA_PATH, "Vergleich Testdaten-Idealfunktion", 4)
test_to_ideal_4.plot_test_ideal_bokeh()
