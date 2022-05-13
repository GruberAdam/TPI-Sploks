from PyQt5 import QtWidgets, QtGui, uic, QtCore
from PyQt5.QtWidgets import QCheckBox 
from packages.PyQt5.ExtendedCombo import ExtendedComboBox
from controller import contractsController
from model.contractsModel import getNumberOfContractsById 
from model.stockModel import *

windowNeedsUpdate = False

class StockUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.stockWindow = uic.loadUi("view/stockView.ui", self)
        
        self.stockWindow.textBrand.installEventFilter(self)
        self.stockWindow.textModel.installEventFilter(self)
        self.stockWindow.textSerialNumber.installEventFilter(self)
        self.stockWindow.textState.installEventFilter(self)

        self.stockWindow.btnFiltrer.clicked.connect(self.filterButton)
        self.stockWindow.btnAdd.clicked.connect(self.addButton)
        self.stock = getStock(self)
        self.loadItems(self.stock)
        self.stockWindow.show()

    # Writes all the data in the table
    def loadItems(self, stock):

        self.stockWindow.tableStock.setRowCount(0)
        self.setTableHeader()
        
        self.stockWindow.tableStock.verticalHeader().setVisible(False) # Hides the row number
        for index, item in enumerate(stock):
            
            self.stockWindow.tableStock.insertRow(index)
            # Inserting the data into the table.
            self.stockWindow.tableStock.setItem(index, 0, QtWidgets.QTableWidgetItem(str(item[0])))  # Code
            self.stockWindow.tableStock.setItem(index, 1, QtWidgets.QTableWidgetItem(str(item[1])))  # Code
            self.stockWindow.tableStock.setItem(index, 2, QtWidgets.QTableWidgetItem(str(item[2])))  # Marque
            self.stockWindow.tableStock.setItem(index, 3, QtWidgets.QTableWidgetItem(str(item[3])))  # Modèle
            self.stockWindow.tableStock.setItem(index, 4, QtWidgets.QTableWidgetItem(str(item[9])))  # S/N
            self.stockWindow.tableStock.setItem(index, 5, QtWidgets.QTableWidgetItem(str(item[4])))  # Taille
            self.stockWindow.tableStock.setItem(index, 6, QtWidgets.QTableWidgetItem(str(item[11]))) # Etat
            self.stockWindow.tableStock.setItem(index, 7, QtWidgets.QTableWidgetItem(str(item[6])))  # Coût
            self.stockWindow.tableStock.setItem(index, 8, QtWidgets.QTableWidgetItem(str(item[7])))  # Retour
            self.stockWindow.tableStock.setItem(index, 9, QtWidgets.QTableWidgetItem(str(item[12]))) # Type
            self.stockWindow.tableStock.setItem(index, 10, QtWidgets.QTableWidgetItem(str(item[8])))  # Stock
        
        self.stockWindow.tableStock.viewport().installEventFilter(self) # Event listener
    
    # Sets the headers of the table
    def setTableHeader(self):
        headerNames = ["ID", "Code", "Marque", "Modèle", "N/S", "Taille", "Etat", "Coût", "Retour", "Type", "Stock"]
        for index, header in enumerate(headerNames):
            self.stockWindow.tableStock.setHorizontalHeaderItem(index, QtWidgets.QTableWidgetItem(str(header)))
    
    
    #Resets the text in the filters in the stock window.    
    def resetTextEdits(self):
        self.stockWindow.textBrand.setText("")
        self.stockWindow.textModel.setText("")
        self.stockWindow.textSerialNumber.setText("")
        self.stockWindow.textState.setText("")


    # It filters the stock table based on the user input.
    def filterButton(self):
        filteredQuery = "WHERE"
        filters = [self.stockWindow.textState.text().strip(), self.stockWindow.textBrand.text().strip(), self.stockWindow.textModel.text().strip(),self.stockWindow.textSerialNumber.text().strip()]
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

        self.loadItems(self.filteredStock) # Loads table with filter

        self.stockWindow.tableStock.verticalScrollBar().setValue(0) # Goes back to the top of the filter

        self.resetTextEdits()
    
    def addButton(self):
        self.addItemsUi = AddItemsUI()


    #If the user double clicks on a cell in the table, get the row and the id of the item, then open the
    #second window and pass the id to it.
    
    #:param source: The object that the event is coming from
    #:param event: The event that was triggered
    #:return: The return value is a boolean value. If the event is handled, the function should return
    #True. If the event should be propagated further, the function should return False.

    def eventFilter(self, object, event):
        global windowNeedsUpdate
        if self.stockWindow.tableStock.selectedIndexes() != []: # Checks that the user clicked on a cell
            if event.type() == QtCore.QEvent.MouseButtonDblClick: # If user double clicked
                row = self.stockWindow.tableStock.currentRow() # gets row clicked
                id = self.stockWindow.tableStock.item(row, 0).text() # gets id based on click

                self.detailledUi = ItemDetailsUi() # Prepare the second window
                self.detailledUi.setupUi(id)         
        if event.type() == QtCore.QEvent.KeyPress and object.hasSelectedText() == QtWidgets.QLineEdit(self).hasSelectedText(): # Checks that it's a keypress and from a QTextEdit event
            if event.key() == QtCore.Qt.Key_Return:
                self.filterButton()

        if windowNeedsUpdate == True:
            self.stock = getStock(self)
            self.loadItems(self.stock)
            windowNeedsUpdate = False
        return False

# Loads the ui file and creates a window.
class ItemDetailsUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.itemDetailWindow = uic.loadUi("view/itemDetailsView.ui", self)

    # Setting up the UI of the inspector window.
    #:param id: the id of the customer
    def setupUi(self, id):
        self.id = id
        self.item = getItemById(self,self.id)

        self.itemDetailWindow.setWindowTitle(f"Article {self.item[0][1]}") # Article Code is set as the title
        numberOfContracts = getNumberOfContractsById(self, self.id)

        if not numberOfContracts:
            numberOfContracts = 0
        else :
            numberOfContracts = numberOfContracts[0][1]

        incomeGenerated = 0

        self.itemDetailWindow.btnContracts.clicked.connect(self.contractsButton)
        # Counting the number of contracts and the income generated by the item.
        for index, instance in enumerate(self.item):
            if instance[12] != None:
                incomeGenerated += instance[12]


        # Setting the text of the labels 
        self.itemDetailWindow.lblCodeArticle.setText(str(self.item[0][1]))
        self.itemDetailWindow.lblNumeroSerie.setText(str(self.item[0][9]))
        self.itemDetailWindow.lblPrixAchat.setText(str(self.item[0][6]))
        self.itemDetailWindow.lblRevenusGeneres.setText(str(incomeGenerated))
        self.itemDetailWindow.lblMarque.setText(str(self.item[0][2]))
        self.itemDetailWindow.lblModel.setText(str(self.item[0][3]))
        self.itemDetailWindow.lblType.setText(str(self.item[0][11]))
        self.itemDetailWindow.lblStock.setText(str(self.item[0][8]))
        self.itemDetailWindow.lblTaille.setText(str(self.item[0][4]))
        self.itemDetailWindow.lblnbContracts.setText(str(numberOfContracts))

        self.itemDetailWindow.show()

    # When contracts button clicked, open contracts UI
    def contractsButton(self):
        contracts = contractsController.ContractsUi()
        contracts.setupUi(self.id, self.item[0][1])


class AddItemsUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.addItemWindow = uic.loadUi("view/addItemsView.ui", self)
        self.setupUi()
        self.addItemWindow.show()

    #Sets up the UI
    def setupUi(self):
        self.setupComboBox()
        self.addItemWindow.btnValider.clicked.connect(self.buttonValidate)
        self.addItemWindow.btnEncore.clicked.connect(self.buttonAdd)
        self.addItemWindow.radioUnique.clicked.connect(self.radioButtonChecked)
        self.addItemWindow.radioMultiple.clicked.connect(self.radioButtonChecked)
        self.addItemWindow.textNumeroSerie.hide()
        self.addItemWindow.textStock.hide()

    # Sets up the comboBox
    def setupComboBox(self):
        self.comboBoxType = ExtendedComboBox(self)
        
        self.gearTypes = getAllGearTypes(self)
        stringArray = ["Choix"]

        for gearType in self.gearTypes:
            stringArray.append(gearType[0])

        self.comboBoxType.addItems(stringArray)

        self.comboBoxType.setGeometry(530, 100, 113, 20)

        self.comboBoxType.show()

    #It returns a dictionary with the values of the fields of the add form.
    #:return: A dictionary with the values of the fields in the addItemWindow.
    def getCreatedItem(self):

        if not self.addItemWindow.textPrix.text():
            self.addItemWindow.textPrix.setText("0")

        if not self.addItemWindow.textStock.text():
            self.addItemWindow.textStock.setText("1")

        return {
            "itemNumber" : self.addItemWindow.textCodeArticle.text(),
            "serialNumber" : self.addItemWindow.textNumeroSerie.text(),
            "state" : self.addItemWindow.comboBoxEtat.currentIndex() + 1,
            "price" : self.addItemWindow.textPrix.text(),
            "brand" : self.addItemWindow.textMarque.text(),
            "model" : self.addItemWindow.textModel.text(),
            "type" : self.comboBoxType.currentIndex(),
            "stock" : self.addItemWindow.textStock.text(),
            "size" : self.addItemWindow.textTaille.text(),
            "unique" : self.addItemWindow.radioUnique.isChecked(),
            "multiple" : self.addItemWindow.radioMultiple.isChecked()
        }

    def buttonValidate(self):
        global windowNeedsUpdate
        self.addItemWindow.textErrorMessage.setText("")
        self.addItemWindow.close()
        windowNeedsUpdate = True

    
    def buttonAdd(self):
        self.itemToAdd = self.getCreatedItem()

        result = addItem(self, self.itemToAdd)

        if result['error'] == True:
            self.addItemWindow.textErrorMessage.setStyleSheet("color: red; border:none;")
            self.addItemWindow.textErrorMessage.setText(result['errorMessage'])
        else:
            self.addItemWindow.textErrorMessage.setStyleSheet("color: green; border:none;")
            self.addItemWindow.textErrorMessage.setText("Contrat ajouté")

    def radioButtonChecked(self):
        if self.addItemWindow.radioUnique.isChecked():
            self.addItemWindow.textNumeroSerie.setVisible(True)
            self.addItemWindow.textStock.hide()
        if self.addItemWindow.radioMultiple.isChecked():
            self.addItemWindow.textStock.setVisible(True)
            self.addItemWindow.textNumeroSerie.hide()
