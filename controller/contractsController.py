from PyQt5 import QtWidgets, QtGui, uic
from model.Contracts import *

class ContractsUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.contractsWindow = uic.loadUi("view/contractsView.ui", self)
        
    # Sets up the UI
    def setupUi(self, id, code):
        self.contractsWindow.setWindowTitle(f"Location de l'article {code}") # Article Code is set as the title

        self.contracts = Contracts() 
        #contracts = self.contracts.getContractByItemId(self, id)  # Gets all the contracts from the item ID
        contracts = self.contracts.getContractsByItemId(id)

        # Iterates over the list of contracts and inserts them into the table.
        for index, contract in enumerate(contracts):
            self.contractsWindow.tableContracts.insertRow(index) # Inserts the row


            self.contractsWindow.tableContracts.setItem(index, 0, QtWidgets.QTableWidgetItem(str(contract[0][0])))
            self.contractsWindow.tableContracts.setItem(index, 1, QtWidgets.QTableWidgetItem(str(contract[0][7])))
            self.contractsWindow.tableContracts.setItem(index, 2, QtWidgets.QTableWidgetItem(str(contract[0][13])))
            self.contractsWindow.tableContracts.setItem(index, 3, QtWidgets.QTableWidgetItem(str(contract[0][14])))
            self.contractsWindow.tableContracts.setItem(index, 4, QtWidgets.QTableWidgetItem(str(contract[0][15])))
            self.contractsWindow.tableContracts.setItem(index, 5, QtWidgets.QTableWidgetItem(str(contract[0][3])))
            self.contractsWindow.tableContracts.setItem(index, 6, QtWidgets.QTableWidgetItem(str(contract[0][2])))
            self.contractsWindow.tableContracts.setItem(index, 7, QtWidgets.QTableWidgetItem(str(contract[0][10])))

        self.contractsWindow.show()