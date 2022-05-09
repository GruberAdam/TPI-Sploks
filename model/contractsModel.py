from model.database import *
    
# Gets all the contracts from the specified item ID
def getContractByItemId(self, id):
    query = f"SELECT sploks.renteditems.contract_id FROM sploks.renteditems WHERE item_id = {id}"
    connection = connectToDatabase(self) # Opens a connection with the database
    contractsId = executeQuery(self, connection, query)
    contracts = []

    for contractId in contractsId:
        query = f"SELECT sploks.contracts.*, sploks.customers.firstname, sploks.customers.lastname, sploks.customers.phone FROM sploks.contracts LEFT JOIN sploks.customers ON sploks.customers.id = sploks.contracts.customer_id WHERE sploks.contracts.id = {contractId[0]}"
        connection = connectToDatabase(self) # Opens a connection with the database
        contracts.append(executeQuery(self, connection, query))
    
    return contracts

#It returns the number of contracts that have been made for a specific item

#:param id: The id of the item
#:return: The number of contracts for a specific item.
def getNumberOfContractsById(self, id):

    query =f"SELECT sploks.renteditems.item_id, Count(sploks.renteditems.item_id) FROM sploks.renteditems WHERE sploks.renteditems.item_id = {id} GROUP BY sploks.renteditems.item_id"
    connection = connectToDatabase(self) # Opens a connection with the database
    numberOfContracts = executeQuery(self, connection, query)

    return numberOfContracts