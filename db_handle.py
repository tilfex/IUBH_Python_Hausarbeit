import sqlalchemy as db
import csv
import settings

class ConnectDatabase(object):
    """ 
    Handles the connection with the database.

    Attributes:
        engine:     Return-value of create_engine of sqlalchemy
        conn:       A connection-handle from engine
        meta:       Meta of sqlalchemy database
    """

    def __init__(self):
        """ 
        Initializes the class.
        """
        self.engine = None
        self.conn = None
        self.meta = None

    def _connect(self):
        """
        Builds a connection to the database.
        """
        self.engine = db.create_engine('sqlite:///' + settings.DB_LOCATION)
        self.conn = self.engine.connect()
        self.meta = db.MetaData()

    def _close_connect(self):
        """
        Saves the changes and close the connection to the database.
        """
        self.meta.create_all(self.engine)
        self.conn.close()

class NewTable(ConnectDatabase):
    """
    Creates a new table from a csv-file.

    Attributes:
        file_location:  Path to the csv-file
        tablename:      Name of the table which will be loaded into the 
                        sql-database
        table:          Table in ths sql-database the data should be inserted 
                        in
    """

    def __init__(self, file_location, tablename):
        """ 
        Initializes the class.

        Arguments:
            file_location:  Path to the csv-file
            tablename:      Name of the table which will be loaded into the 
                            sql-database
        """
        super().__init__()
        self.file_location = file_location
        self.tablename = tablename
        self.table = None

        self._connect()
        self._clean_db()
        self.create_table()
        self.insert_data()
        self._close_connect()

    def _clean_db(self):
        """
        Deletes the tables if they existed before the code was running.
        """
        self.conn.execute('DROP TABLE IF EXISTS ' + self.tablename)

    def _get_data(self):
        """
        Opens the csv-file and puts the data into the list 'result'.

        Returns:
            result: list of the data from the csv-file
        """
        result = []
        with open(self.file_location, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                result.append(row)
        return(result)

    def create_table(self):
        """
        Creates a table with the needed columns.
        """
        data_list = []
        for i in self._get_data()[0]:
            data_list.append(i)
        column_list = []
        for i in data_list:
            column = db.Column(i, db.Integer, nullable=False)
            column_list.append(column)
        self.table = db.Table(
            self.tablename, self.meta,
            *column_list)
        self.meta.create_all(self.engine)

    def insert_data(self):
        """
        Inserts the data into a table in the sql-database.
        """
        data = self._get_data()
        sql_query = db.insert(self.table)
        data_dict_list = []
        for i in data[1:]:
            data_dict = {}
            for (ind, item) in enumerate(i):
                data_dict.update({data[0][ind]: item})
            data_dict_list.append(data_dict)
        self.conn.execute(sql_query, data_dict_list)