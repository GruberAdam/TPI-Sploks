from model.database import *


def getStock(self):
    query ="SELECT * FROM sploks.items;"
    connection = connectToDatabase(self) # Opens a connection with the database
    stock = executeQuery(self, connection, query)

    return stock

