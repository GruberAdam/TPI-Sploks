from model.database import *


# Function designed to get all the items from the database
# :return: A list of tuples.
def getStock(self):
    query ="SELECT sploks.items.*, sploks.gearstates.code, sploks.geartypes.name FROM sploks.items LEFT JOIN sploks.gearstates ON sploks.items.gearstate_id = sploks.gearstates.id LEFT JOIN sploks.geartypes ON sploks.items.geartype_id = sploks.geartypes.id"
    connection = connectToDatabase(self) # Opens a connection with the database
    stock = executeQuery(self, connection, query)

    return stock
    
#It gets the filtered stock from the database.
#:param filter: A string containing the filter to be applied to the query
#:return: A list of tuples.   
def getFilteredStock(self, filter):

    query ="SELECT sploks.items.*, sploks.gearstates.code, sploks.geartypes.name FROM sploks.items LEFT JOIN sploks.gearstates ON sploks.items.gearstate_id = sploks.gearstates.id LEFT JOIN sploks.geartypes ON sploks.items.geartype_id = sploks.geartypes.id " + filter
    connection = connectToDatabase(self) # Opens a connection with the database
    filteredStock = executeQuery(self, connection, query)

    return filteredStock
