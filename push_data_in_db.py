import sqlalchemy as db
from data_import import get_data

# with the function get_data the data of the csv files will be putted into lists of dictionaries
test = get_data('Examples/Beispiel-Datensätze/test.csv')
train = get_data('Examples/Beispiel-Datensätze/train.csv')
ideal = get_data('Examples/Beispiel-Datensätze/ideal.csv')

engine = db.create_engine('sqlite:///test.sqlite')
conn = engine.connect()

meta = db.MetaData()

# search for tables in databse to delete them, before creating a new table
for tbl in reversed(meta.sorted_tables):
    engine.execute(tbl.delete())