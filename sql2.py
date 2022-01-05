import pyodbc

class DataBase:
    conn = ""
    tableCreated = False
    IdIndex = 1

    def __init__(self):
        self.conn = pyodbc.connect(
            "Driver={SQL Server Native Client 11.0};"
            "Server=DESKTOP-U49AJ08\SQLEXPRESS;"
            "Database=JobFinderDB;"
            "Trusted_Connection=yes;"
        )
    
    def tableExist(self):
        try:
            self.createTable()
        except:
            # if exists continue
            return


    # getts table name and col ID
    # tableName<string>  
    def createTable(self):
        cursor = self.conn.cursor()
        cursor.execute('create table AllJobs (ID int,job_title char(100),job_id char(500),company_name char(50),company_link char(500),job_post_date char(50),job_link char(500),company_location char(500));')
        self.conn.commit()
        self.tableCreated = True


    def printData(self, data):
        for row in data:
            print(f'row = {row}')
        print()


    def AllData(self):
        cursor = self.conn.cursor()
        cursor.execute('Select * From AllJobs')
        return cursor


    def readData(self):
        dbData = []
        try:
            cursor = self.conn.cursor()
            cursor.execute('Select * From AllJobs')
            
            for index, row in enumerate(cursor):
                dbData.append(row)
                self.IdIndex += 1
            z=2
            return dbData
        except:
            # exception while reading
            emptyList = []
            return emptyList
            
    

    # insert only after read all data from db - continue writing by last ID 
    # inserts row of data to AllJobs table
    def insertData(self, dataList):
        cursor = self.conn.cursor()
        cursor.execute('Insert Into AllJobs(ID, job_title, job_id, company_name, company_link, job_post_date, job_link, company_location) Values (?,?,?,?,?,?,?,?);',
        (self.IdIndex, dataList[0][1], dataList[1][1], dataList[2][1], dataList[3][1], dataList[4][1], dataList[5][1], dataList[6][1]))
        self.conn.commit()
        self.IdIndex += 1

    
    # colName<string>  
    def addColumn(self, colName):
        cursor = self.conn.cursor()
        cursor.execute('ALTER TABLE AllData ADD (?) char(50);', (str(colName)))
        self.conn.commit()

    def closeConn(self):
        self.conn.close()

#  cant configure db in ssms this shit is not working properly

# db = DataBase()
# db.addColumn('')
# db.closeConn()


# print("finish")

    









# conn = pyodbc.connect(
#             "Driver={SQL Server Native Client 11.0};"
#             "Server=DESKTOP-U49AJ08\SQLEXPRESS;"
#             "Database=JobFinderDB;"
#             "Trusted_Connection=yes;"
# )

# cursor = conn.cursor()
# # cursor.execute('Select * from general')
# cursor.execute('Create Table test123 (ID int);')
# cursor.execute('INSERT INTO test123(ID) VALUES (?);', ('10'))
# cursor.execute('INSERT INTO test123(ID) VALUES (?);', ('11'))
# cursor.execute('INSERT INTO test123(ID) VALUES (?);', ('12'))


# cursor.execute('Select * from test123')

# for row in cursor:
#     print('row = %r' %(row,))

# conn.commit()
# conn.close()