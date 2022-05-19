# It loads the stockView.ui file, and then loads the stock table.
from pickle import FALSE
from PyQt5 import QtWidgets, QtGui, uic, QtCore
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import Qt
from packages.PyQt5.ExtendedCombo import ExtendedComboBox
from controller import contractsController
from model.Stock import *

windowNeedsUpdate = False


class StockUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.stock = Stock()
        self.stockWindow = uic.loadUi("view/stockView.ui", self)

        self.stockWindow.textBrand.installEventFilter(self)
        self.stockWindow.textModel.installEventFilter(self)
        self.stockWindow.textSerialNumber.installEventFilter(self)
        self.stockWindow.textState.installEventFilter(self)
        self.stockWindow.btnFiltrer.clicked.connect(self.filterButton)
        self.stockWindow.btnAdd.clicked.connect(self.addButton)

        self.loadItems(self.stock.getStock())

        self.stockWindow.show()

    # Writes all the data in the table
    def loadItems(self, stock):

        self.stockWindow.tableStock.setRowCount(0)
        self.setTableHeader()

        self.stockWindow.tableStock.verticalHeader(
        ).setVisible(False)  # Hides the row number
        for index, item in enumerate(stock):

            self.stockWindow.tableStock.insertRow(index)
            # Inserting the data into the table.
            self.stockWindow.tableStock.setItem(
                index, 0, QtWidgets.QTableWidgetItem(str(item[0])))  # Code
            self.stockWindow.tableStock.setItem(
                index, 1, QtWidgets.QTableWidgetItem(str(item[1])))  # Code
            self.stockWindow.tableStock.setItem(
                index, 2, QtWidgets.QTableWidgetItem(str(item[2])))  # Marque
            self.stockWindow.tableStock.setItem(
                index, 3, QtWidgets.QTableWidgetItem(str(item[3])))  # Modèle
            self.stockWindow.tableStock.setItem(
                index, 4, QtWidgets.QTableWidgetItem(str(item[9])))  # S/N
            self.stockWindow.tableStock.setItem(
                index, 5, QtWidgets.QTableWidgetItem(str(item[4])))  # Taille
            self.stockWindow.tableStock.setItem(
                index, 6, QtWidgets.QTableWidgetItem(str(item[11])))  # Etat
            self.stockWindow.tableStock.setItem(
                index, 7, QtWidgets.QTableWidgetItem(str(item[6])))  # Coût
            self.stockWindow.tableStock.setItem(
                index, 8, QtWidgets.QTableWidgetItem(str(item[7])))  # Retour
            self.stockWindow.tableStock.setItem(
                index, 9, QtWidgets.QTableWidgetItem(str(item[12])))  # Type
            self.stockWindow.tableStock.setItem(
                index, 10, QtWidgets.QTableWidgetItem(str(item[8])))  # Stock

        self.stockWindow.tableStock.viewport().installEventFilter(self)  # Event listener

    # Sets the headers of the table
    def setTableHeader(self):
        headerNames = ["ID", "Code", "Marque", "Modèle", "N/S",
                       "Taille", "Etat", "Coût", "Retour", "Type", "Stock"]
        for index, header in enumerate(headerNames):
            self.stockWindow.tableStock.setHorizontalHeaderItem(
                index, QtWidgets.QTableWidgetItem(str(header)))

    # Resets the text in the filters in the stock window.

    def resetTextEdits(self):
        self.stockWindow.textBrand.setText("")
        self.stockWindow.textModel.setText("")
        self.stockWindow.textSerialNumber.setText("")
        self.stockWindow.textState.setText("")

    # It filters the stock table based on the user input.

    def filterButton(self):
        filter = {"description": self.stockWindow.textState.text().strip(),
                  "brand": self.stockWindow.textBrand.text().strip(),
                  "model": self.stockWindow.textModel.text().strip(),
                  "articlenumber": self.stockWindow.textSerialNumber.text().strip()}
        self.filteredStock = self.stock.getStockByFilter(filter)

        self.loadItems(self.filteredStock)  # Loads table with filter

        self.stockWindow.tableStock.verticalScrollBar().setValue(
            0)  # Goes back to the top of the filter

        self.resetTextEdits()

    def addButton(self):
        self.addItemsUi = AddItemsUI()

    # If the user double clicks on a cell in the table, get the row and the id of the item, then open the
    # second window and pass the id to it.

    #:param source: The object that the event is coming from
    #:param event: The event that was triggered
    #:return: The return value is a boolean value. If the event is handled, the function should return
    # True. If the event should be propagated further, the function should return False.

    def eventFilter(self, object, event):
        global windowNeedsUpdate
        if self.stockWindow.tableStock.selectedIndexes() != []:  # Checks that the user clicked on a cell
            if event.type() == QtCore.QEvent.MouseButtonDblClick:  # If user double clicked
                row = self.stockWindow.tableStock.currentRow()  # gets row clicked
                id = self.stockWindow.tableStock.item(
                    row, 0).text()  # gets id based on click

                self.detailledUi = ItemDetailsUi()  # Prepare the second window
                self.detailledUi.setupUi(id)
        # Checks that it's a keypress and from a QTextEdit event
        if event.type() == QtCore.QEvent.KeyPress and object.hasSelectedText() == QtWidgets.QLineEdit(self).hasSelectedText():
            if event.key() == QtCore.Qt.Key_Return:
                self.filterButton()

        if windowNeedsUpdate == True:
            self.loadItems(self.stock.getStock())
            windowNeedsUpdate = False
        return False

# Loads the ui file and creates a window.


class ItemDetailsUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.editable = False
        self.itemDetailWindow = uic.loadUi("view/itemDetailsView.ui", self)

    # Setting up the UI of the inspector window.
    #:param id: the id of the customer
    def setupUi(self, id):
        self.item = Item(id)

        # Article Code is set as the title
        self.itemDetailWindow.setWindowTitle(f"Article {self.item.itemNb}")
        numberOfContracts = self.item.getNumberOfContracts()
        incomeGenerated = self.item.getIncomeGenerated()

        # Button Listener
        self.itemDetailWindow.btnContracts.clicked.connect(self.contractsButton)
        self.itemDetailWindow.btnEdit.clicked.connect(self.editButton)
        self.itemDetailWindow.btnValider.clicked.connect(self.validateButton)

        # Setting the text of the labels
        self.itemDetailWindow.textCodeArticle.setText(str(self.item.itemNb))
        self.itemDetailWindow.textNumeroSerie.setText(str(self.item.articleNumber))
        self.itemDetailWindow.comboBoxEtat.setCurrentIndex(self.item.state - 1)
        self.itemDetailWindow.textPrixAchat.setText(str(self.item.cost))
        self.itemDetailWindow.textRevenusGeneres.setText(str(incomeGenerated))
        self.itemDetailWindow.textMarque.setText(str(self.item.brand))
        self.itemDetailWindow.textModel.setText(str(self.item.model))
        self.itemDetailWindow.textType.setText(str(self.item.type))
        self.itemDetailWindow.textStock.setText(str(self.item.stock))
        self.itemDetailWindow.textTaille.setText(str(self.item.size))
        self.itemDetailWindow.lblnbContracts.setText(str(numberOfContracts))

        self.itemDetailWindow.show()

    # When contracts button clicked, open contracts UI
    def contractsButton(self):
        contracts = contractsController.ContractsUi()
        contracts.setupUi(self.item.id, self.item.itemNb)
    
    def editButton(self):
        if self.editable == False:
            self.itemDetailWindow.textStock.setReadOnly(False)
            self.editable = True
            self.itemDetailWindow.btnValider.setEnabled(True)
            self.itemDetailWindow.textErrorMessage.setStyleSheet("color: green; border:none;")
            self.itemDetailWindow.textErrorMessage.setText("Les champs sont désormait éditable")
        else:
            self.itemDetailWindow.textStock.setReadOnly(True)
            self.editable = False
            self.itemDetailWindow.btnValider.setEnabled(False)
            self.itemDetailWindow.textErrorMessage.setStyleSheet("color: red; border:none;")
            self.itemDetailWindow.textErrorMessage.setText("Les champs ne sont plus éditable")

    def checkFields(self):
        newStock = self.itemDetailWindow.textStock.text()

        if not newStock:
            return {"error" : True, "errorMessage" : "Le stock ne peux pas être vide"}
        if newStock.isnumeric() == False:
            return {"error" : True, "errorMessage" : "Le stock doit être un numbre"}

        return {"error" : False}

    def validateButton(self):
        global windowNeedsUpdate
        res = self.checkFields()

        if res['error']:
            self.displayErrorMessage(res['errorMessage'])
        else:
            self.item.setItem({"stock" : self.itemDetailWindow.textStock.text()})
            self.item.updateItem()
            self.itemDetailWindow.close()
            windowNeedsUpdate = True

    #Displays in a label the error given
    def displayErrorMessage(self, error):
        self.itemDetailWindow.textErrorMessage.setStyleSheet(
            "color: red; border:none;")
        self.itemDetailWindow.textErrorMessage.setText(error)

    def event(self, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
                if self.itemDetailWindow.btnEdit.hasFocus():
                    self.editButton()
                if self.itemDetailWindow.btnValider.hasFocus():
                    self.validateButton()
                if self.itemDetailWindow.btnContracts.hasFocus():
                    self.contractsButton()
                self.focusNextPrevChild(True) # Goes to next widget
                self.window().setAttribute(Qt.WA_KeyboardFocusChange) # Styles the border painting

        return super().event(event)


class AddItemsUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.addItemWindow = uic.loadUi("view/addItemsView.ui", self)
        self.setupUi()
        self.addItemWindow.show()

    # Sets up the UI
    def setupUi(self):
        self.item = Item()

        self.setupComboBox()
        
        #Event listener to all buttons
        self.addItemWindow.btnValider.clicked.connect(self.buttonValidate)
        self.addItemWindow.btnEncore.clicked.connect(self.buttonAdd)
        self.addItemWindow.radioUnique.clicked.connect(self.radioButtonChecked)
        self.addItemWindow.radioMultiple.clicked.connect(
            self.radioButtonChecked)
        
        # Hides text behind both radioBoxes
        self.addItemWindow.textNumeroSerie.hide()
        self.addItemWindow.textStock.hide()

        # Setting the tab order
        tabOrder = [self.addItemWindow.textCodeArticle, self.addItemWindow.textMarque, self.addItemWindow.textModel, 
        self.comboBoxType, self.addItemWindow.textTaille, self.addItemWindow.comboBoxEtat, self.addItemWindow.textPrix,
        self.addItemWindow.radioUnique, self.addItemWindow.textNumeroSerie,self.addItemWindow.radioMultiple, self.addItemWindow.textStock,
        self.addItemWindow.btnEncore, self.addItemWindow.btnValider]

        self.setTabOrder(tabOrder[0], tabOrder[1])
        self.setTabOrder(tabOrder[1], tabOrder[2])
        self.setTabOrder(tabOrder[2], tabOrder[3])
        self.setTabOrder(tabOrder[3], tabOrder[4])
        self.setTabOrder(tabOrder[4], tabOrder[5])
        self.setTabOrder(tabOrder[5], tabOrder[6])
        self.setTabOrder(tabOrder[6], tabOrder[7])
        self.setTabOrder(tabOrder[7], tabOrder[8])
        self.setTabOrder(tabOrder[8], tabOrder[9])
        self.setTabOrder(tabOrder[9], tabOrder[10])
        self.setTabOrder(tabOrder[10], tabOrder[11])
        self.setTabOrder(tabOrder[11], tabOrder[12])

    # Sets up the comboBox
    def setupComboBox(self):
        self.comboBoxType = ExtendedComboBox(self)

        self.gearTypes = self.item.getAllGearTypes()
        stringArray = ["Choix"]

        for gearType in self.gearTypes:
            stringArray.append(gearType[0])

        self.comboBoxType.addItems(stringArray)

        self.comboBoxType.setGeometry(530, 100, 113, 20)

        self.comboBoxType.show()

    # It returns a dictionary with the values of the fields of the add form.
    #:return: A dictionary with the values of the fields in the addItemWindow.
    def getCreatedItem(self):
        res = self.checkRequiredFields()

        if res['error'] == True:
            return res

        if self.addItemWindow.radioMultiple.isChecked():  # If mlultiple articles are added
            itemToAdd = {
                "error": False,
                "itemNumber": self.addItemWindow.textCodeArticle.text(),
                "serialNumber": "-",
                "state": self.item.getStateIdFromDescription(self.addItemWindow.comboBoxEtat.currentText()),
                "price": self.addItemWindow.textPrix.text(),
                "brand": self.addItemWindow.textMarque.text(),
                "model": self.addItemWindow.textModel.text(),
                "type": self.item.getTypeIdFromName(self.comboBoxType.currentText()),
                "stock": self.addItemWindow.textStock.text(),
                "size": self.addItemWindow.textTaille.text(),
            }

            try:
                if itemToAdd['type']['error']:
                    return {"error" : True, "errorMessage" : itemToAdd['type']['errorMessage']}

                if itemToAdd['state']['error']:
                    return {"error" : True, "errorMessage" : itemToAdd['state']['errorMessage']}
            except:
                return itemToAdd
            

        if self.addItemWindow.radioUnique.isChecked():  # If a unique article is added
            itemToAdd = {
                "error": False,
                "itemNumber": self.addItemWindow.textCodeArticle.text(),
                "serialNumber": self.addItemWindow.textNumeroSerie.text(),
                "state": self.item.getStateIdFromDescription(self.addItemWindow.comboBoxEtat.currentText()),
                "price": self.addItemWindow.textPrix.text(),
                "brand": self.addItemWindow.textMarque.text(),
                "model": self.addItemWindow.textModel.text(),
                "type": self.item.getTypeIdFromName(self.comboBoxType.currentText()),
                "stock": "1",
                "size": self.addItemWindow.textTaille.text(),
            }

            try:
                if itemToAdd['type']['error']:
                    return {"error" : True, "errorMessage" : itemToAdd['type']['errorMessage']}

                if itemToAdd['state']['error']:
                    return {"error" : True, "errorMessage" : itemToAdd['state']['errorMessage']}
            except:
                return itemToAdd


    # Leaves the window and updates it in the list of the items
    def buttonValidate(self):
        global windowNeedsUpdate
        self.addItemWindow.textErrorMessage.setText("")
        self.addItemWindow.close()
        windowNeedsUpdate = True

    # When the button "Encore" is clicked
    # Creates a new item with the fields inputed

    def buttonAdd(self):
        global windowNeedsUpdate
        itemToAdd = self.getCreatedItem()
        if itemToAdd['error'] == True:
            self.displayErrorMessage(itemToAdd['errorMessage'])
            return
        

        result = self.item.setItem(itemToAdd)

        result = self.item.addItem()

        if result['error'] == True:
            self.displayErrorMessage(result['errorMessage'])
        else:
            self.addItemWindow.textErrorMessage.setStyleSheet(
                "color: green; border:none;")
            self.addItemWindow.textErrorMessage.setText("Contrat ajouté")
            self.addItemWindow.textCodeArticle.setText("")
            windowNeedsUpdate = True

    # Displays the right widget according to the radioBox clicked
    def radioButtonChecked(self):
        if self.addItemWindow.radioUnique.isChecked():
            self.addItemWindow.textNumeroSerie.setVisible(True)
            self.addItemWindow.textStock.hide()
        if self.addItemWindow.radioMultiple.isChecked():
            self.addItemWindow.textStock.setVisible(True)
            self.addItemWindow.textNumeroSerie.hide()

    # Displays in a label the error given
    def displayErrorMessage(self, error):
        self.addItemWindow.textErrorMessage.setStyleSheet(
            "color: red; border:none;")
        self.addItemWindow.textErrorMessage.setText(error)

    # Checks the requirement of each fields
    def checkRequiredFields(self):
        # Empty checks
        if not self.addItemWindow.textCodeArticle.text():
            return {"error": True, "errorMessage": "Le champ 'Code article' est obligatoire"}

        if not self.addItemWindow.textMarque.text():
            return {"error": True, "errorMessage": "Le champ 'Marque' est obligatoire"}

        if self.comboBoxType.currentIndex() == 0:
            return {"error": True, "errorMessage": "Faites un choix pour le type"}

        if not self.addItemWindow.textTaille.text():
            return {"error": True, "errorMessage": "Le champ 'Taille' est obligatoire"}

        if not self.addItemWindow.textStock.text() and self.addItemWindow.radioMultiple.isChecked() == True:
            return {"error": True, "errorMessage": "Le champ 'Nombre' est obligatoire"}

        # Radio button check
        if self.addItemWindow.radioMultiple.isChecked() == False and self.addItemWindow.radioUnique.isChecked() == False:
            return {"error": True, "errorMessage": "Veuillez choisir un 'Type Stock'"}

        # Numeric checks
        if self.addItemWindow.textTaille.text().isnumeric() == False:
            return {"error": True, "errorMessage": "Le champ 'Taille' doit être un nombre"}

        if self.addItemWindow.textPrix.text().isnumeric() == False and len(self.addItemWindow.textPrix.text().strip()) > 0:
            return {"error": True, "errorMessage": "Le champ 'Prix' doit être un nombre"}

        if self.addItemWindow.textStock.text().isnumeric() == False and self.addItemWindow.radioMultiple.isChecked() == True:
            return {"error": True, "errorMessage": "Le champ 'Nombre' doit être un nombre"}

        if not self.addItemWindow.textPrix.text():
            self.addItemWindow.textPrix.setText("0")

        return {"error": False}


    # Every kind of events come in this function

    #:param event: The event that occurred
    #:return: The event is being returned.
    def event(self, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):

                # Checks radioBox "Unique" if it hasFocus and enter key is pressed
                if self.addItemWindow.radioUnique.hasFocus(): 
                    self.addItemWindow.radioUnique.setChecked(True)
                    self.radioButtonChecked()

                # Checks radioBox "Multiple" if it hasFocus and enter key is pressed
                if self.addItemWindow.radioMultiple.hasFocus():
                    self.addItemWindow.radioMultiple.setChecked(True)
                    self.radioButtonChecked()

                # Clicks on the "Encore" Button if it has focus and enter key is pressed
                if self.addItemWindow.btnEncore.hasFocus():
                    self.buttonAdd()

                # Clicks on the "Valider" Button if it has focus and enter key is pressed
                if self.addItemWindow.btnValider.hasFocus():
                    self.buttonValidate()

                self.focusNextPrevChild(True) # Goes to next widget
                self.window().setAttribute(Qt.WA_KeyboardFocusChange) # Styles the border painting
        return super().event(event)
