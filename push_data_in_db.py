import sqlalchemy as db
from data_import import get_data

# create an engine-object
engine = db.create_engine('sqlite:///Hausarbeit_db.sqlite')

# create a connection to the database
conn = engine.connect()

# create a metadate-object
meta = db.MetaData()

conn.execute('DROP TABLE IF EXISTS Test_Tabelle')
conn.execute('DROP TABLE IF EXISTS Train_Tabelle')
conn.execute('DROP TABLE IF EXISTS Ideal_Tabelle')

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
    return(res)

#create a function to create a table with the needed columns
def create_table(column_list, tablename):
    return db.Table(
        tablename, meta,
        *column_list
    )

# creating all tables with the created functions
test_table = create_table(create_columns(get_column_names(test)), "Test_Tabelle")
train_table = create_table(create_columns(get_column_names(train)), "Train_Tabelle")
ideal_table = create_table(create_columns(get_column_names(ideal)), "Ideal_Tabelle")

# save the metadata-object
meta.create_all(engine)

# create a function to insert the data into the tables
def insert_data(table, data_list):
    sql_query = db.insert(table)
    data_dict_list = []
    for i in data_list[1:]:
        data_dict = {}
        for (ind, item) in enumerate(i):
            data_dict.update({data_list[0][ind]:item})
        data_dict_list.append(data_dict)
    res = conn.execute(sql_query, data_dict_list)
    return(res)

# inserting the data into the tables with the created function
insert_test = insert_data(test_table, test)
insert_train = insert_data(train_table, train)
insert_ideal = insert_data(ideal_table, ideal)