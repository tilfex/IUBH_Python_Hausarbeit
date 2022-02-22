"""
Calls all classes which are needed to sovle the Python Tasks.
"""
from db_handle import NewTable
from train_data import TrainData
from ideal_func import IdealFunc
import settings

# Create tables in db, insert training-data, test-data and ideal-functions
table_train = NewTable(
    file_location=settings.TRAIN_DATA_PATH,
    tablename="Training_Daten_Tabelle")

table_ideal = NewTable(
    file_location=settings.IDEAL_DATA_PATH,
    tablename="Ideal_Daten_Tabelle")

table_test = NewTable(
    file_location=settings.TEST_DATA_PATH,
    tablename="Test_Daten_Tabelle")

# Create csv-files with the results of the compare of test- and ideal-data
td = TrainData()
list_triples = td.get_selected_ideal_funcs()
for (ind, triple) in enumerate(list_triples):
    func = IdealFunc(triple)
    func.compare_ideal_test()
    func.save_to_csv(f'compare_diff_{ind+1}.csv')

# Create tables in db, insert results of the compare of test- and ideal-datas
# comp_table_1 = NewTable(
#     file_location="compare_diff_1.csv",
#     tablename="Tabelle_Vergleich_1_Idealfunktion"
# )
# comp_table_2 = NewTable(
#     file_location="compare_diff_2.csv",
#     tablename="Tabelle_Vergleich_2_Idealfunktion"
# )
# comp_table_3 = NewTable(
#     file_location="compare_diff_3.csv",
#     tablename="Tabelle_Vergleich_3_Idealfunktion"
# )
# comp_table_4 = NewTable(
#     file_location="compare_diff_4.csv",
#     tablename="Tabelle_Vergleich_4_Idealfunktion"
# )