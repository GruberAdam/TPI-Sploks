from PyQt5 import QtWidgets, QtGui, uic
from model.stockModel import * 

class StockUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.stockWindow = uic.loadUi("view/stockView.ui", self)
        self.stockWindow.btnFiltrer.clicked.connect(self.filterButton)
        self.stock = getStock(self)
        self.loadItems(self.stock)
        self.stockWindow.show()

    # Writes all the data in the table
    def loadItems(self, stock):

        self.stockWindow.tableStock.clear()
        self.setTableHeader()
        

        for index, item in enumerate(stock):
            
            self.stockWindow.tableStock.insertRow(index)
            # Inserting the data into the table.
            self.stockWindow.tableStock.setItem(index, 0, QtWidgets.QTableWidgetItem(str(item[1])))  # Code
            self.stockWindow.tableStock.setItem(index, 1, QtWidgets.QTableWidgetItem(str(item[2])))  # Marque
            self.stockWindow.tableStock.setItem(index, 2, QtWidgets.QTableWidgetItem(str(item[3])))  # Modèle
            self.stockWindow.tableStock.setItem(index, 3, QtWidgets.QTableWidgetItem(str(item[9])))  # S/N
            self.stockWindow.tableStock.setItem(index, 4, QtWidgets.QTableWidgetItem(str(item[4])))  # Taille
            self.stockWindow.tableStock.setItem(index, 5, QtWidgets.QTableWidgetItem(str(item[11]))) # Etat
            self.stockWindow.tableStock.setItem(index, 6, QtWidgets.QTableWidgetItem(str(item[6])))  # Coût
            self.stockWindow.tableStock.setItem(index, 7, QtWidgets.QTableWidgetItem(str(item[7])))  # Retour
            self.stockWindow.tableStock.setItem(index, 8, QtWidgets.QTableWidgetItem(str(item[12]))) # Type
            self.stockWindow.tableStock.setItem(index, 9, QtWidgets.QTableWidgetItem(str(item[8])))  # Stock
    
    # Sets the headers of the table
    def setTableHeader(self):
        headerNames = ["Code", "Marque", "Modèle", "N/S", "Taille", "Etat", "Coût", "Retour", "Type", "Stock"]
        for index, header in enumerate(headerNames):
            self.stockWindow.tableStock.setHorizontalHeaderItem(index, QtWidgets.QTableWidgetItem(str(header)))
    
    # It filters the stock table based on the user input.
    def filterButton(self):
        
        filteredQuery = "WHERE"
        filters = [self.stockWindow.textState.toPlainText().strip(), self.stockWindow.textBrand.toPlainText().strip(), self.stockWindow.textModel.toPlainText().strip(),self.stockWindow.textSerialNumber.toPlainText().strip()]
        filterText = ["code", "brand", "model", "articlenumber"]
        checkFilter = False

        for index, value in enumerate(filters):
            if value != "":
                filteredQuery = filteredQuery + f" {filterText[index]} LIKE '%{filters[index]}%' AND"
                checkFilter = True
        
        if checkFilter == False:
             filteredQuery = ""
        filteredQuery = filteredQuery[:-3]
        self.filteredStock = getFilteredStock(self, filteredQuery)
        self.loadItems(self.filteredStock)