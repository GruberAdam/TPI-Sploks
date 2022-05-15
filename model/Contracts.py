from model.database import *


class Contracts():

    # Gets all the contracts from the specified item ID
    def getContractsByItemId(self, id):
        query = f"SELECT sploks.renteditems.contract_id FROM sploks.renteditems WHERE item_id = {id}"
        # Opens a connection with the database
        connection = connectToDatabase(self)
        contractsId = executeQuery(self, connection, query)
        contracts = []

        for contractId in contractsId:
            query = f"SELECT sploks.contracts.*, sploks.customers.firstname, sploks.customers.lastname, sploks.customers.phone FROM sploks.contracts LEFT JOIN sploks.customers ON sploks.customers.id = sploks.contracts.customer_id WHERE sploks.contracts.id = {contractId[0]}"
            # Opens a connection with the database
            connection = connectToDatabase(self)
            contracts.append(executeQuery(self, connection, query))

        return contracts
