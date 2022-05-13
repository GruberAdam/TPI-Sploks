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
    
#It gets an item from the database by its id    
#:param id: The id of the item you want to get
#:return: A list of tuples.
def getItemById(self, id):
    query = f"SELECT sploks.items.*, sploks.geartypes.name, sploks.renteditems.price FROM sploks.items LEFT JOIN sploks.geartypes ON sploks.items.geartype_id = sploks.geartypes.id LEFT JOIN sploks.renteditems ON sploks.items.id = sploks.renteditems.item_id WHERE sploks.items.id = {id}"
    connection = connectToDatabase(self) # Opens a connection with the database
    item = executeQuery(self, connection, query)

    return item

#Gets all the gear types
#:return: A list of tuples.
    
def getAllGearTypes(self):

    query = "SELECT sploks.geartypes.name FROM sploks.geartypes"
    connection = connectToDatabase(self)
    gearTypes = executeQuery(self,connection, query)

    return gearTypes
    
#Insert the values of the dictionary into the database

#:param item: a dictionary containing the following keys:
#:return: The result of the query 
def addItem(self, item):
    print(item['type'])

    # Empty checks
    if not item['itemNumber']:
        return {"error" : True, "errorMessage" : "Le champ 'Code article' est obligatoire"}

    if not item['brand']:
        return {"error" : True, "errorMessage" : "Le champ 'Marque' est obligatoire"}

    if item['type'] == 0:
        return {"error" : True, "errorMessage" : "Faites un choix pour le type"}
    
    if not item['size']:
        return {"error" : True, "errorMessage" : "Le champ 'Taille' est obligatoire"}

    if not item['stock'] and item['multiple'] == True:
        return {"error" : True, "errorMessage" : "Le champ 'Nombre' est obligatoire"}

    # Radio button check
    if item['multiple'] == False and item['unique'] == False:
        return {"error" : True, "errorMessage" :"Veuillez choisir un 'Type Stock'"}


    # Numeric checks
    if item['size'].isnumeric() == False:
        return {"error" : True, "errorMessage" :"Le champ 'Taille' doit être un nombre"}

    if item['price'].isnumeric() == False and len(item['price'].strip()) > 0:
        return {"error" : True, "errorMessage" :"Le champ 'Prix' doit être un nombre"}

    if item['stock'].isnumeric() == False and item['multiple'] == True:
        return {"error" : True, "errorMessage" :"Le champ 'Stock' doit être un nombre"}


    query = f"INSERT INTO sploks.items (itemnb, brand, model, size, gearstate_id, cost, returned, stock, articlenumber, geartype_id) VALUES ('{item['itemNumber']}', '{item['brand']}', '{item['model']}', '{item['size']}','{item['state']}', '{item['price']}', '{0}', '{item['stock']}', '{item['serialNumber']}', '{item['type']}')"
    connection = connectToDatabase(self)
    res = executeQuery(self,connection, query)
    return {"error" : False, "res" : res}