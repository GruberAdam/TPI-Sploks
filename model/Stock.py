from model.database import *

class Stock():    
    #Gets all the stock from the database and returns them.
    #:return: A list of tuples.
    def getStock(self):
        query ="SELECT sploks.items.*, sploks.gearstates.code, sploks.geartypes.name FROM sploks.items LEFT JOIN sploks.gearstates ON sploks.items.gearstate_id = sploks.gearstates.id LEFT JOIN sploks.geartypes ON sploks.items.geartype_id = sploks.geartypes.id"
        connection = connectToDatabase(self) # Opens a connection with the database
        res = executeQuery(self, connection, query)

        return res
        
    #Filters the stock based on the filter parameter given.
    
    #:param filter: a dictionary with the filter information
    #:return: A list of tuples.
    def getStockByFilter(self, filter):
        filteredQuery = "WHERE"
        isFilterEmpty = True

        for key, value in filter.items():
            if value != "":
                filteredQuery = filteredQuery + f" {key} LIKE '%{value}%' AND"
                isFilterEmpty = False
        
        if isFilterEmpty == True:
            return self.getStock()

        filteredQuery = filteredQuery[:-3] # Removes the last "AND"

        query ="SELECT sploks.items.*, sploks.gearstates.code, sploks.geartypes.name FROM sploks.items LEFT JOIN sploks.gearstates ON sploks.items.gearstate_id = sploks.gearstates.id LEFT JOIN sploks.geartypes ON sploks.items.geartype_id = sploks.geartypes.id " + filteredQuery
        connection = connectToDatabase(self) # Opens a connection with the database
        res = executeQuery(self, connection, query)

        return res

    def checkItem(self, item):
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

    #Gets all the gear types
    #:return: A list of tuples.
    def getAllGearTypes(self):
        query = "SELECT sploks.geartypes.name FROM sploks.geartypes"
        connection = connectToDatabase(self)
        gearTypes = executeQuery(self,connection, query)

        return gearTypes

class Item(Stock):
    def __init__(self, id=None):
        if id != None:
            self.item = self.getItemById(id)
            self.id = id
            self.itemNb = self.item[0][1]
            self.brand = self.item[0][2]
            self.model = self.item[0][3]
            self.size = self.item[0][4]
            self.state = self.item[0][5]
            self.cost = self.item[0][6]
            self.returned = self.item[0][7]
            self.stock = self.item[0][8]
            self.articlenumber = self.item[0][9]
            self.type = self.item[0][10]
            

    #It gets an item from the database by its id    
    #:param id: The id of the item you want to get
    #:return: A list of tuples.
    def getItemById(self, id):
        query = f"SELECT sploks.items.*, sploks.geartypes.name, sploks.renteditems.price FROM sploks.items LEFT JOIN sploks.geartypes ON sploks.items.geartype_id = sploks.geartypes.id LEFT JOIN sploks.renteditems ON sploks.items.id = sploks.renteditems.item_id WHERE sploks.items.id = {id}"
        connection = connectToDatabase(self) # Opens a connection with the database
        item = executeQuery(self, connection, query)

        return item

    #It returns the number of contracts that have been made for a specific item
    #:param id: The id of the item
    #:return: The number of contracts for a specific item.
    def getNumberOfContracts(self):
        query =f"SELECT Count(sploks.renteditems.item_id) FROM sploks.renteditems WHERE sploks.renteditems.item_id = {self.id}"
        connection = connectToDatabase(self) # Opens a connection with the database
        res = executeQuery(self, connection, query)

        return res[0][0]


    #Returns the sum of the generated income by the item
    #:return: The total income generated by the item.
    def getIncomeGenerated(self):
        query = f"SELECT SUM(sploks.renteditems.price) FROM sploks.renteditems WHERE sploks.renteditems.item_id = {self.id}"
        connection = connectToDatabase(self) # Opens a connection with the database
        res = executeQuery(self, connection, query)

        return res[0][0]
    
    #Sets all the properties of the item thanks to the properties param
    #:param properties: a list of tuples, each tuple containing a key and a value
    def setItem(self, properties):
        print(properties)
        for key, property in properties.items():
            if key == "itemNumber":
                self.itemNb = property
            if key == "serialNumber":
                self.articleNumber = property
            if key == "state":
                self.state = property
            if key == "price":
                self.cost = property
            if key == "brand":
                self.brand = property
            if key == "model":
                self.model = property            
            if key == "type":
                self.type = property 
            if key == "stock":
                self.stock = property 
            if key == "size":
                self.size = property

    #Insert the values of the dictionary into the database
    #:param item: a dictionary containing the following keys:
    #:return: The result of the query 
    def addItem(self, item):

        res = self.checkItem(item)

        if res['error'] == True:
            return res

        query = f"INSERT INTO sploks.items (itemnb, brand, model, size, gearstate_id, cost, returned, stock, articlenumber, geartype_id) VALUES ('{item['itemNumber']}', '{item['brand']}', '{item['model']}', '{item['size']}','{item['state']}', '{item['price']}', '{0}', '{item['stock']}', '{item['serialNumber']}', '{item['type']}')"
        connection = connectToDatabase(self)
        res = executeQuery(self,connection, query)
        return {"error" : False, "res" : res}
