import matplotlib.pyplot as plt
from bokeh.plotting import figure, show, output_file
from df_handle import DataframeHandle
from test_data import TestData
from train_data import TrainData
from settings import TEST_DATA_PATH, TRAIN_DATA_PATH

class VisualHandle():
    """
    Handles the visualisation of the data in the Database.

    Attributes:
        csv_file_name:  The path to the csv-file
        title:          Title of the grafic
        df:             Dataframe of the data to visualize
        num_of_train:   The train-function which should be shown with its 
                        fitting ideal-function
    """

    def __init__(self, csv_file_name, title, num_of_train):
        """
        Initializes the class.

        Arguments:
            csv_file_name:  The path to the csv-file
            title:          Title of the grafic
            df:             Dataframe of the data to visualize
            num_of_train:   The train-function which should be shown with its 
                            fitting ideal-function
        """
        self.csv_file_name = csv_file_name
        self.title = title
        self.df = None
        self.num_of_train = num_of_train

    def plot_train_ideal_matplot(self):
        """
        Plots a grafic to show the pair of the trainingfunction and the fitting 
        ideal-function, with matplotlib.
        """
        td = TrainData()
        list_triples = td.get_selected_ideal_funcs()
        df_train = TrainData(TRAIN_DATA_PATH).df
        df_ideal = DataframeHandle(self.csv_file_name)
        x = df_ideal['x'].tolist()
        y_ideal = df_ideal[list_triples[(self.num_of_train-1)][1]].tolist()
        y_train = df_train[list_triples[(self.num_of_train-1)][0]].tolist()
        plt.scatter(x=x, y=y_train, color="green", label="Traingsdaten-" +
                    list_triples[(self.num_of_train-1)][0], s=2)
        plt.plot(x, y_ideal, color="orange", label="Ideale-Funktion-" +
                 list_triples[(self.num_of_train-1)][1], alpha=0.6)
        plt.title(self.title)
        plt.legend()
        plt.show()

    def plot_test_ideal_matplot(self):
        """
        Plots a grafic with one two x-y-pair with the same x-values, with 
        matplotlib.
        """
        td = TrainData()
        list_triples = td.get_selected_ideal_funcs()
        df_bestfit = DataframeHandle(
            "compare_diff_"+str(self.num_of_train)+".csv")
        df_test = TestData(TEST_DATA_PATH).df
        df_ideal = DataframeHandle(self.csv_file_name)
        x_ideal = df_ideal['x'].tolist()
        y_ideal = df_ideal[list_triples[(self.num_of_train-1)][1]].tolist()
        x_test = df_test['x'].tolist()
        y_test = df_test['y'].tolist()
        x_test_bf = df_bestfit['X - test'].tolist()
        y_test_bf = df_bestfit['Y - test'].tolist()
        y_ideal_bf = df_bestfit[df_bestfit.columns.values[3]].tolist()
        count = 0
        # the following list adds the y-scaling according to the train-ideal-plots
        ylim_list = [[0, 100], [-20, 20], [-1.5, 1.5], [0, 20]]
        for i in x_test_bf:
            point_test = []
            point_ideal = []
            point_test.append(i)
            point_ideal.append(i)
            point_test.append(y_test_bf[count])
            point_ideal.append(y_ideal_bf[count])
            count = count+1
            plt.plot([point_ideal[0], point_test[0]], [
                     point_ideal[1], point_test[1]], color="blue")

        plt.scatter(x=x_test, y=y_test, color="green", label="Testdaten", s=2)
        plt.plot(x_ideal, y_ideal, color="orange", label="Ideale-Funktion-" +
                 list_triples[(self.num_of_train-1)][1], alpha=0.6)
        plt.scatter(x=x_test_bf, y=y_test_bf, color="red",
                    label="Bestfit-Testdaten", s=5)
        plt.xlim(-20, 20)
        plt.ylim(ylim_list[self.num_of_train-1][0],
                 ylim_list[self.num_of_train-1][1])
        plt.title(self.title)
        plt.legend()
        plt.show()

    def plot_train_ideal_bokeh(self):
        """
        Plots a grafic to show the pair of the trainingfunction and the fitting 
        ideal-function, with bokeh.
        """
        td = TrainData()
        list_triples = td.get_selected_ideal_funcs()
        df_train = TrainData(TRAIN_DATA_PATH).df
        df_ideal = DataframeHandle(self.csv_file_name)
        x = df_ideal['x'].tolist()
        y_ideal = df_ideal[list_triples[(self.num_of_train-1)][1]].tolist()
        y_train = df_train[list_triples[(self.num_of_train-1)][0]].tolist()
        output_file("train_ideal-"+str(self.num_of_train)+".html")
        plot = figure(width=500, height=500, title=self.title,
                      x_axis_label="x", y_axis_label="y")
        plot.circle(x=x, y=y_train, color="green", legend_label="Traingsdaten-" +
                    list_triples[(self.num_of_train-1)][0], size=2)
        plot.line(x, y_ideal, color="orange", legend_label="Ideale-Funktion-" +
                  list_triples[(self.num_of_train-1)][1], line_width=2, line_alpha=0.6)
        show(plot)

    def plot_test_ideal_bokeh(self):
        """
        Plots a grafic with one two x-y-pair with the same x-values, with 
        bokeh.
        """
        td = TrainData()
        list_triples = td.get_selected_ideal_funcs()
        df_bestfit = DataframeHandle(
            "compare_diff_"+str(self.num_of_train)+".csv")
        df_test = TestData(TEST_DATA_PATH).df
        df_ideal = DataframeHandle(self.csv_file_name)
        x_ideal = df_ideal['x'].tolist()
        y_ideal = df_ideal[list_triples[(self.num_of_train-1)][1]].tolist()
        x_test = df_test['x'].tolist()
        y_test = df_test['y'].tolist()
        x_test_bf = df_bestfit['X - test'].tolist()
        y_test_bf = df_bestfit['Y - test'].tolist()
        y_ideal_bf = df_bestfit[df_bestfit.columns.values[3]].tolist()
        count = 0
        # the following list adds the y-scaling according to the train-ideal-plots
        ylim_list = [[0, 100], [-20, 20], [-1.5, 1.5], [0, 20]]
        output_file("test_ideal-"+str(self.num_of_train)+".html")
        plot = figure(width=500, height=500, title=self.title,
                      x_axis_label="x", y_axis_label="y", x_range=(-20, 20), y_range=(ylim_list[self.num_of_train-1][0], ylim_list[self.num_of_train-1][1]))
        for i in x_test_bf:
            point_test = []
            point_ideal = []
            point_test.append(i)
            point_ideal.append(i)
            point_test.append(y_test_bf[count])
            point_ideal.append(y_ideal_bf[count])
            count = count+1
            plot.line([point_ideal[0], point_test[0]], [
                      point_ideal[1], point_test[1]], color="blue")

        plot.circle(x=x_test, y=y_test, color="green",
                    legend_label="Testdaten", size=2)
        plot.line(x_ideal, y_ideal, color="orange", legend_label="Ideale-Funktion-" +
                  list_triples[(self.num_of_train-1)][1], line_alpha=0.6)
        plot.circle(x=x_test_bf, y=y_test_bf, color="red",
                    legend_label="Bestfit-Testdaten", size=5)
        show(plot)
