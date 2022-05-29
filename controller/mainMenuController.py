# Author : Adam Gruber
# Date : 17.02.2022
# Version : 1.0

from PyQt5 import QtWidgets, QtGui, uic, QtCore
from controller import stockController
import sys, os

try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    basePath = sys._MEIPASS
except Exception:
    basePath = os.path.abspath(".")

class MainMenuUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        global basePath
        self.mainMenuWindow = uic.loadUi(basePath + "\\view\\menuView.ui", self)

        # Click event listener 
        self.mainMenuWindow.btnClients.clicked.connect(self.displayClients)
        self.mainMenuWindow.btnStock.clicked.connect(self.displayStock)
        self.mainMenuWindow.btnStaff.clicked.connect(self.displayStaff)
        self.mainMenuWindow.btnContracts.clicked.connect(self.displayContracts)

        self.mainMenuWindow.show()

    # Event listener when a key is pressed
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key.Key_A: # When user presses the "a" key
            self.displayClients()
        if e.key() == QtCore.Qt.Key.Key_S: # When user presses the "s" key
            self.displayStock()
        if e.key() == QtCore.Qt.Key.Key_D: # When user presses the "d" key
            self.displayStaff()
        if e.key() == QtCore.Qt.Key.Key_F: # When user presses the "f" key
            self.displayContracts()

        
    def displayClients(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Indisponible")
        msg.setText("La section client n'est pas disponible")
        msg.exec_() 

    # Redirects in the stock controller
    def displayStock(self):
        self.stockWindow = stockController.StockUi() 

    # Redirects in the staff controller
    def displayStaff(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Indisponible")
        msg.setText("La section staff n'est pas disponible")
        msg.exec_() 

    # Redirects in the contracts controller
    def displayContracts(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Indisponible")
        msg.setText("La section contrats n'est pas disponible")
        msg.exec_() 