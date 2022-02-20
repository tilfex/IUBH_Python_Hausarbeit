import sqlalchemy as db
import csv

# creating a function to open, read, to save a csv-file into a list of dictionaries
def get_data(filename):
    result = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            result.append(row)
    return(result)

# create an engine-object
engine = db.create_engine('sqlite:///Hausarbeit_db.sqlite')

# create a connection to the database
conn = engine.connect()

# create a metadate-object
meta = db.MetaData()

# deleting the tables if they existed before the code was running
conn.execute('DROP TABLE IF EXISTS Training_Daten_Tabelle')
conn.execute('DROP TABLE IF EXISTS Ideale_Funktionen_Tabelle')

# put the location of the csv-files into al variable for easier use
train_file = 'Examples/Beispiel-Datensätze/train.csv'
ideal_file = 'Examples/Beispiel-Datensätze/ideal.csv'
test_file = 'Examples/Beispiel-Datensätze/test.csv'

# with the function get_data the data of the csv files will be putted into lists of dictionaries
train = get_data(train_file)
ideal = get_data(ideal_file)

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
train_table = create_table(create_columns(get_column_names(train)), "Training_Daten_Tabelle")
ideal_table = create_table(create_columns(get_column_names(ideal)), "Ideale_Funktionen_Tabelle")

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
insert_train = insert_data(train_table, train)
insert_ideal = insert_data(ideal_table, ideal)