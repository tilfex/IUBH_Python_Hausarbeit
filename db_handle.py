import sqlalchemy as db
import csv
import settings

class ConnectDatabase(object):
    """
    
    """
    def __init__(self):
        """
        
        """
        self.engine = None
        self.conn = None
        self.meta = None

    def _connect(self):
        """
        
        """
        # create an engine-object
        self.engine = db.create_engine('sqlite:///' + settings.DB_LOCATION)
        # create a connection to the database
        self.conn = self.engine.connect()
        # create a metadate-object
        self.meta = db.MetaData()
    
    def _close_connect(self):
        """
        
        """
        self.meta.create_all(self.engine)
        self.conn.close()

class NewTable(ConnectDatabase):
    """
    
    """
    def __init__(self, file_location, tablename):
        self.file_location = file_location
        self.tablename = tablename
        self.table = None
        self.engine = None
        self.conn = None
        self.meta = None

        self._connect()
        self._clean_db()
        self.create_table()
        self.insert_data()
        self._close_connect()
    
    def _clean_db(self):
        # deleting the tables if they existed before the code was running
        self.conn.execute('DROP TABLE IF EXISTS ' + self.tablename)
    
    def _get_data(self):
        result = []
        with open(self.file_location, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                result.append(row)
        return(result)
    
    #create a function to create a table with the needed columns
    def create_table(self):
        data_list=[]
        for i in self._get_data()[0]:
            data_list.append(i)
        column_list =[]
        for i in data_list:
            column = db.Column(i, db.Integer, nullable=False)
            column_list.append(column)
        self.table = db.Table(
            self.tablename, self.meta,
            *column_list)
        self.meta.create_all(self.engine)
    
    def insert_data(self):
        data = self._get_data()
        
        sql_query = db.insert(self.table)
        data_dict_list = []
        for i in data[1:]:
            data_dict = {}
            for (ind, item) in enumerate(i):
                data_dict.update({data[0][ind]:item})
            data_dict_list.append(data_dict)
        self.conn.execute(sql_query, data_dict_list)


    
