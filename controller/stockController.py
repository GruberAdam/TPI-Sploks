from PyQt5 import QtWidgets, QtGui, uic
from model.stockModel import * 

class StockUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.stockWindow = uic.loadUi("view/stockView.ui", self)

        self.stock = getStock(self)

        for item in self.stock:
            self.stockWindow.tableStock.insertRow(item[0] - 1)
           
            self.stockWindow.tableStock.setItem(item[0] - 1, 0, QtWidgets.QTableWidgetItem(str(item[9])))
            self.stockWindow.tableStock.setItem(item[0] - 1, 1, QtWidgets.QTableWidgetItem(str(item[2])))
            self.stockWindow.tableStock.setItem(item[0] - 1, 2, QtWidgets.QTableWidgetItem(str(item[3])))
            self.stockWindow.tableStock.setItem(item[0] - 1, 3, QtWidgets.QTableWidgetItem(str("???")))
            self.stockWindow.tableStock.setItem(item[0] - 1, 4, QtWidgets.QTableWidgetItem(str(item[4])))
            self.stockWindow.tableStock.setItem(item[0] - 1, 5, QtWidgets.QTableWidgetItem(str("???")))
            self.stockWindow.tableStock.setItem(item[0] - 1, 6, QtWidgets.QTableWidgetItem(str(item[8])))
        self.stockWindow.show()
