from PyQt5 import QtWidgets, QtGui, uic
from model.stockModel import * 

class StockUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.stockWindow = uic.loadUi("view/stockView.ui", self)

        self.stock = getStock(self)
        for item in self.stock:
            self.stockWindow.tableStock.insertRow(item[0] - 1)
           
            # Inserting the data into the table.
            self.stockWindow.tableStock.setItem(item[0] - 1, 0, QtWidgets.QTableWidgetItem(str(item[1])))  # Code
            self.stockWindow.tableStock.setItem(item[0] - 1, 1, QtWidgets.QTableWidgetItem(str(item[2])))  # Marque
            self.stockWindow.tableStock.setItem(item[0] - 1, 2, QtWidgets.QTableWidgetItem(str(item[3])))  # Modèle
            self.stockWindow.tableStock.setItem(item[0] - 1, 3, QtWidgets.QTableWidgetItem(str(item[9])))  # S/N
            self.stockWindow.tableStock.setItem(item[0] - 1, 4, QtWidgets.QTableWidgetItem(str(item[4])))  # Taille
            self.stockWindow.tableStock.setItem(item[0] - 1, 5, QtWidgets.QTableWidgetItem(str(item[11]))) # Etat
            self.stockWindow.tableStock.setItem(item[0] - 1, 6, QtWidgets.QTableWidgetItem(str(item[6])))  # Coût
            self.stockWindow.tableStock.setItem(item[0] - 1, 7, QtWidgets.QTableWidgetItem(str(item[7])))  # Retour
            self.stockWindow.tableStock.setItem(item[0] - 1, 8, QtWidgets.QTableWidgetItem(str(item[12]))) # Type
            self.stockWindow.tableStock.setItem(item[0] - 1, 9, QtWidgets.QTableWidgetItem(str(item[8])))  # Stock
        self.stockWindow.show()
