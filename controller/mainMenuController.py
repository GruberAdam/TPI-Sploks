# Author : Adam Gruber
# Date : 17.02.2022
# Version : 1.0

from PyQt5 import QtWidgets, QtGui, uic
from controller import customersController, stockController, staffController, contractsController
import sys

# Displays the main menu
def displayMainMenu(self):
    mainMenuWindow = uic.loadUi(sys.path[0] + "\\view\\menuView.ui", self)

    # Click event listener 
    mainMenuWindow.btnClients.clicked.connect(displayClients)
    mainMenuWindow.btnStock.clicked.connect(displayStock)
    mainMenuWindow.btnStaff.clicked.connect(displayStaff)
    mainMenuWindow.btnContracts.clicked.connect(displayContracts)

    mainMenuWindow.show()

# Redirects in the customers controller
def displayClients(self):
    customersController.CustomersUi()

# Redirects in the stock controller
def displayStock(self):
    stockController.StockUi() 

# Redirects in the staff controller
def displayStaff(self):
    staffController.StaffUi()

# Redirects in the contracts controller
def displayContracts(self):
    contractsController.ContractsUi()