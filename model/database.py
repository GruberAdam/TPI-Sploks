from multiprocessing import connection
import mysql.connector
from mysql.connector import errorcode

# Function designed to create a connection to the database
# The connection is then returned
def connectToDatabase(self):
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root.1234",
        database="sploks",
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    return connection

# Function designed to execute a query
# connection param (connection with the database)
# query param (string with the SQL script)
def executeQuery(self, connection, query):
    for singleQuery in query.split(";"): # For every ";" split the execution of the query in different parts
        if len(singleQuery) > 0:
            cursor = connection.cursor()
            cursor.execute(singleQuery)
            
        
    output = cursor.fetchall() # Fetch results
    connection.commit() # Commit changes
    connection.close() # Closes connection
    return output