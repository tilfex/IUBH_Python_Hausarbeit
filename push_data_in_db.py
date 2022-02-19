import sqlalchemy as db
from data_import import get_data


# create an engine-object
engine = db.create_engine('sqlite:///test.sqlite')

# create a connection to the database
conn = engine.connect()

# create a metadate-object
meta = db.MetaData()

# with the function get_data the data of the csv files will be putted into lists of dictionaries
test = get_data('Examples/Beispiel-Datensätze/test.csv')
train = get_data('Examples/Beispiel-Datensätze/train.csv')
ideal = get_data('Examples/Beispiel-Datensätze/ideal.csv')

#create a function to get the names of the columns into a list
def get_column_names(dataset):
    res=[]
    for i in dataset [0]:
        res.append(i)
    return(res)

# create a function to create the columns in the table
def create_columns(datalist):
    res=[]
    for i in datalist:
        column = db.Column(i, db.Integer, nullable=False)
        res.append(column)
    return (res)

#create a function to create a table with the needed columns
def create_table(column_list, tablename):
    db.Table(
        tablename, meta,
        *column_list
    )

# creating all tables with the created functions
test_table = create_table(create_columns(get_column_names(test)), "Test_Tabelle")
train_table = create_table(create_columns(get_column_names(train)), "Train_Tabelle")
ideal_table = create_table(create_columns(get_column_names(ideal)), "Ideal_Tabelle")

# save the metadata-object
meta.create_all(engine)