from db_handle import NewTable
from train_data import TrainData
from ideal_func import IdealFunc
import settings


td = TrainData()
selected_ideal_funcs = td.get_selected_ideal_funcs()
for (ind, func_name) in enumerate(selected_ideal_funcs):
    func = IdealFunc(func_name)
    func.save_to_csv(f'compare_diff_{ind+1}.csv')

# Load data into database
table_train = NewTable(
    file_location=settings.TRAIN_DATA_PATH,
    tablename="Training_Daten_Tabelle")

table_ideal = NewTable(
    file_location=settings.IDEAL_DATA_PATH,
    tablename="Ideal_Daten_Tabelle")

table_test = NewTable(
    file_location=settings.TEST_DATA_PATH,
    tablename="Test_Daten_Tabelle")

# create the tables
comp_table_1 = NewTable(
    file_location="compare_diff_1.csv",
    tablename="Tabelle_Vergleich_1_Idealfunktion"
)
comp_table_2 = NewTable(
    file_location="compare_diff_2.csv",
    tablename="Tabelle_Vergleich_2_Idealfunktion"
)
comp_table_3 = NewTable(
    file_location="compare_diff_3.csv",
    tablename="Tabelle_Vergleich_3_Idealfunktion"
)
comp_table_4 = NewTable(
    file_location="compare_diff_4.csv",
    tablename="Tabelle_Vergleich_4_Idealfunktion"
)


