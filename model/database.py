from multiprocessing import connection
import mysql.connector
from mysql.connector import errorcode
import os, sys
from dotenv import load_dotenv


try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    basePath = sys._MEIPASS
except Exception:
    basePath = os.path.abspath(".")

print(os.path.join(basePath, '.env'))
load_dotenv(dotenv_path=os.path.join(basePath, '.env')) # Loads the .env file

# Function designed to create a connection to the database
# The connection is then returned
def connectToDatabase(self):
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user= os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            raise Exception("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            raise Exception("Database does not exist")
        else:
            raise Exception(err)
            

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