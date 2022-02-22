import matplotlib.pyplot as plt
from bokeh.plotting import figure, show
from df_handle import DataframeHandle


class VisualHandle():
    """
    Handles the visualisation of the data in the Database.

    Attributes:
        csv_file_name: the path to the csv-file
        title: title of the grafic
        df: dataframe of the data to visualize
    """

    def __init__(self, csv_file_name, title):
        """
        Initializes the class.

        Arguments:
            csv_file_name: the path to the csv-file
            title: title of the grafic
            df: dataframe of the data to visualize
        """
        self.csv_file_name = csv_file_name
        self.title = title
        self.df = None

    def plot_single_matplot(self):
        """
        Plots a grafic for a single x-y-pair using a scatter-style, with 
        matplotlib.
        """
        df = DataframeHandle(self.csv_file_name)
        for i in df.columns[1:]:
            df.plot.scatter(x='x', y=i, s=1)
            plt.title(self.title)
        plt.show()

    def plot_compare_matplot(self):
        """
        Plots a grafic with one two x-y-pair with the same x-values using a 
        scatter-style and one x-y-pair using a bar-style, with matplotlib.
        """
        df = DataframeHandle(self.csv_file_name)
        x = df['x'].tolist()
        y_test = df[df.columns.values[1]].tolist()
        y_ideal = df[df.columns.values[3]].tolist()
        y_diff = df[df.columns.values[2]].tolist()
        plt.scatter(x, y_test, marker = ".", color="green", label= "Test")
        plt.scatter(x, y_ideal, marker = ".", color="orange", label= "Ideal")
        plt.bar(x, y_diff, width = 0.5, color = "#cccccc", alpha=0.6, \
            label= "Abweichung")
        plt.legend()
        plt.show()
    
    def plot_single_bokeh(self):
        """
        Plots a grafic for a single x-y-pair using a circle-style, with bokeh.
        """
        df = DataframeHandle(self.csv_file_name)
        
        for i in df.columns[1:]:
            plot = figure(width=500, height=500, title=self.title, \
                x_axis_label= "x axis", y_axis_label= "y axis")
            print(i)
            y = df[i].tolist()
            x = df['x'].tolist()
            plot.circle(x=x, y=y)
            show(plot)
        

    def plot_compare_bokeh(self):
        """
        
        """
        df = DataframeHandle(self.csv_file_name)
        plot = figure(width=500, height=500, title=self.title, \
        x_axis_label= "x axis", y_axis_label= "y axis")
        x = df['x'].tolist()
        y_test = df[df.columns.values[1]].tolist()
        y_ideal = df[df.columns.values[3]].tolist()
        y_diff = df[df.columns.values[2]].tolist()
        plot.circle(x=x, y=y_ideal, color= "orange", legend= "Ideal")
        plot.circle(x=x, y=y_test, color= "green", legend= "Test")
        plot.vbar(x=x, top=y_diff, width=0.5, alpha= 0.6, color= "#cccccc", legend= "Abweichung")
        show(plot)