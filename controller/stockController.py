from PyQt5 import QtWidgets, QtGui, uic, QtCore
from controller import contractsController
from model.Stock import *
from PyQt5.QtWidgets import QComboBox, QMessageBox
import sys


windowNeedsUpdate = False
creatingItem = False

try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    basePath = sys._MEIPASS
except Exception:
    basePath = os.path.abspath(".")

# It loads the stockView.ui file, and then loads the stock table.
class StockUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.stock = Stock()
        self.stockWindow = uic.loadUi(basePath + "\\view\\stockView.ui", self)
        self.selectedId = None
        self.selectedRow = None
        self.changedStockContent = False

        # Event listener
        self.stockWindow.textBrand.installEventFilter(self)
        self.stockWindow.textModel.installEventFilter(self)
        self.stockWindow.textSerialNumber.installEventFilter(self)
        self.stockWindow.comboBoxEtat.activated.connect(self.comboBoxEvent)
        self.stockWindow.btnFiltrer.clicked.connect(self.filterButton)
        self.stockWindow.btnAdd.clicked.connect(self.addButton)
        self.stockWindow.tableStock.clicked.connect(self.singleClickCell)

        self.stockWindow.textBrand.setFocus()


        try:
            #Loads hole stock
            self.loadItems(self.stock.getStock())
            self.stockWindow.show()
        except Exception as error:
            # Writes an error
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText(str(error))
            msg.setIcon(QMessageBox.Critical)
            msg.exec_() 


    # Writes all the data in the table
    # Stock arg is given and table is filled thank to the arg
    def loadItems(self, stock):
        self.stockWindow.tableStock.setRowCount(0)
        self.setTableHeader()
        self.stockWindow.tableStock.verticalHeader().setVisible(False)  # Hides the row number
        for index, item in enumerate(stock):

            self.stockWindow.tableStock.insertRow(index)
            # Inserting the data into the table.
            self.stockWindow.tableStock.setItem(
                index, 0, QtWidgets.QTableWidgetItem(str(item[0])))  # ID
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

    # Updates just one row
    # row param gives the row that needs to be updated
    # item param gives the new item
    def updateItems(self, row, item):
        # Inserting the data into the table.
        self.stockWindow.tableStock.setItem(
            row, 0, QtWidgets.QTableWidgetItem(str(item.id)))  # ID
        self.stockWindow.tableStock.setItem(
            row, 1, QtWidgets.QTableWidgetItem(str(item.itemNb)))  # Code
        self.stockWindow.tableStock.setItem(
            row, 2, QtWidgets.QTableWidgetItem(str(item.brand)))  # Marque
        self.stockWindow.tableStock.setItem(
            row, 3, QtWidgets.QTableWidgetItem(str(item.model)))  # Modèle
        self.stockWindow.tableStock.setItem(
            row, 4, QtWidgets.QTableWidgetItem(str(item.articleNumber)))  # S/N
        self.stockWindow.tableStock.setItem(
            row, 5, QtWidgets.QTableWidgetItem(str(item.size)))  # Taille
        self.stockWindow.tableStock.setItem(
            row, 6, QtWidgets.QTableWidgetItem(str(item.getStateDescriptionFromId(item.state))))  # Etat
        self.stockWindow.tableStock.setItem(
            row, 7, QtWidgets.QTableWidgetItem(str(item.cost)))  # Coût
        self.stockWindow.tableStock.setItem(
            row, 8, QtWidgets.QTableWidgetItem(str(item.returned)))  # Retour
        self.stockWindow.tableStock.setItem(
            row, 9, QtWidgets.QTableWidgetItem(str(item.type)))  # Type
        self.stockWindow.tableStock.setItem(
            row, 10, QtWidgets.QTableWidgetItem(str(item.stock)))  # Stock

    # Sets the headers of the table
    def setTableHeader(self):
        headerNames = ["ID", "Code", "Marque", "Modèle", "N/S",
                       "Taille", "Etat", "Coût", "Retour", "Type", "Stock"]
        for index, header in enumerate(headerNames):
            self.stockWindow.tableStock.setHorizontalHeaderItem(
                index, QtWidgets.QTableWidgetItem(str(header)))

    # It filters the stock table based on the user input.
    def filterButton(self):
        self.fillSelectedRowColor(True)
        try:
            filter = {"code": Item.getStateIdFromDescription(self, self.stockWindow.comboBoxEtat.currentText()),
                    "brand": self.stockWindow.textBrand.text().strip(),
                    "model": self.stockWindow.textModel.text().strip(),
                    "articlenumber": self.stockWindow.textSerialNumber.text().strip()}
            self.filteredStock = self.stock.getStockByFilter(filter)

            self.loadItems(self.filteredStock)  # Loads table with filter

            self.stockWindow.tableStock.verticalScrollBar().setValue(0)  # Goes back to the top of the filter
            self.changedStockContent = True
        except Exception as error:
            # Writes an error
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText(str(error))
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()

    # When user pressed on the add button, opens the addItem window
    def addButton(self):
        try:
            self.addItemsUi = AddItemsUI()
        except Exception as error:
            # Writes an error
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText(str(error))
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
        
    # When the comboBox index changes, it will directely filter the stock
    def comboBoxEvent(self):
        self.filterButton()

    # Fills the row of a color from the row given
    # If earse = True, it will earse the current selected row
    def fillSelectedRowColor(self, earse = False):
        if self.selectedId == None:
            return
        if earse == True and self.changedStockContent == False:
            for i in range(11):
                self.stockWindow.tableStock.item(self.selectedRow, i).setBackground(QtGui.QColor(255,255,255))
            self.changedStockContent = False
            return
        if earse == False:
            for i in range(11):
                self.stockWindow.tableStock.item(self.selectedRow, i).setBackground(QtGui.QColor(51,120,210))
        self.changedStockContent = False
        return
    
    # Whenever a cell is clicked, it will earse the old selected row 
    def singleClickCell(self):
        if self.changedStockContent == False:
            self.fillSelectedRowColor(True)
    
    """
    Checks if user doubled clicked on a cell (opens the detailled view)
    Check if user pressed return on a filter field
    Checks if the variable windowNeedsUpdate is = to true

    :param object: The object that the event is being sent to
    :param event: QEvent
    """
    def eventFilter(self, object, event):
        global windowNeedsUpdate
        global creatingItem
        if self.stockWindow.tableStock.selectedIndexes() != []:  # Checks that the user clicked on a cell
            if event.type() == QtCore.QEvent.MouseButtonDblClick:  # If user double clicked
                self.selectedRow = self.stockWindow.tableStock.currentRow()  # gets row clicked
                self.selectedId = self.stockWindow.tableStock.item(self.selectedRow, 0).text()  # gets id based on click
                self.fillSelectedRowColor()
                try:
                    self.detailledUi = ItemDetailsUi()  # Prepare the second window
                    self.detailledUi.setupUi(self.selectedId)
                except Exception as error:
                    msg = QMessageBox()
                    msg.setWindowTitle("Error")
                    msg.setText(str(error))
                    msg.setIcon(QMessageBox.Critical)
                    msg.exec_()
        # Checks that it's a keypress and from a QTextEdit event
        if event.type() == QtCore.QEvent.KeyPress and object.hasSelectedText() == QtWidgets.QLineEdit(self).hasSelectedText():
            if event.key() == QtCore.Qt.Key_Return:
                self.filterButton()

        # Updates the window when the variable windowNeedsUpdate is True
        if windowNeedsUpdate == True:
            try:
                if creatingItem == True:
                    self.loadItems(self.stock.getStock())            
                else:
                    self.itemToUpdate = Item(self.selectedId)
                    self.updateItems(self.selectedRow, self.itemToUpdate)
                    self.fillSelectedRowColor()
            except Exception as error:
                    msg = QMessageBox()
                    msg.setWindowTitle("Error")
                    msg.setText(str(error))
                    msg.setIcon(QMessageBox.Critical)
                    msg.exec_()
            windowNeedsUpdate = False
            creatingItem = False
        return False
    """
        Checks if escape is pressed, if it is, it sets the focus on the textBrand. 
        Checks if escaped is pressed on different item to activate their normal behavior
        
        :param event: The event that was sent to the widget
        :return: The return value of the event handler.
    """
    def event(self,event):
        if event.type() == QtCore.QEvent.KeyPress:
            if QtCore.Qt.Key_Escape == event.key():
                self.stockWindow.textBrand.setFocus(True)
                super().event(event)
            if event.key() == QtCore.Qt.Key_Return:
                # Shows "Type" content if it has focus and enter key is pressed
                if self.stockWindow.comboBoxEtat.hasFocus():
                    self.stockWindow.comboBoxEtat.showPopup()
                    return super().event(event)
                # Filters the article if the button has focus and enter key is pressed
                if self.stockWindow.btnFiltrer.hasFocus():
                    self.filterButton()
                    return super().event(event)
                # Goes into the add article window if it has focus and enter key is pressed
                if self.stockWindow.btnAdd.hasFocus():
                    self.addButton()
                    return super().event(event)

                if self.stockWindow.tableStock.selectedIndexes():
                    self.fillSelectedRowColor(True)
                    # Opens Detailed UI
                    self.selectedRow = self.stockWindow.tableStock.currentRow()  # gets row clicked
                    self.selectedId = self.stockWindow.tableStock.item(self.selectedRow, 0).text()  # gets id based on click
                    self.fillSelectedRowColor()
                    try:
                        self.detailledUi = ItemDetailsUi()  # Prepare the second window
                        self.detailledUi.setupUi(self.selectedId)
                        super().event(event)
                    except Exception as error:
                        msg = QMessageBox()
                        msg.setWindowTitle("Error")
                        msg.setText(str(error))
                        msg.setIcon(QMessageBox.Critical)
                        msg.exec_()
        return super().event(event)


class ItemDetailsUi(QtWidgets.QMainWindow):
    def __init__(self):
        global basePath
        super().__init__()
        self.editable = False
        self.itemDetailWindow = uic.loadUi(basePath + "\\view\\itemDetailsView.ui", self)

    # When windows closes, sets the global variable windowNeedsUpdate to true
    def closeEvent(self,event):
        global windowNeedsUpdate
        windowNeedsUpdate = True

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
        self.itemDetailWindow.comboBoxEtat.setCurrentIndex(self.item.state - 1)
        self.itemDetailWindow.textPrixAchat.setText(str(self.item.cost))
        self.itemDetailWindow.textRevenusGeneres.setText(str(incomeGenerated))
        self.itemDetailWindow.textMarque.setText(str(self.item.brand))
        self.itemDetailWindow.textModel.setText(str(self.item.model))
        self.itemDetailWindow.textStock.setText(str(self.item.stock))
        self.itemDetailWindow.textTaille.setText(str(self.item.size))
        self.itemDetailWindow.lblnbContracts.setText(str(numberOfContracts))

        
        isUnique = self.item.checkIfItemIsUnique(self.item.type)
        self.item.setItem({"unique" : isUnique})

        if self.item.unique:
            self.itemDetailWindow.lblTypeStock.setText(self.itemDetailWindow.lblTypeStock.text() + " (unique)")
        else:
            self.itemDetailWindow.lblTypeStock.setText(self.itemDetailWindow.lblTypeStock.text() + " (multiple)")

        # Accepts number only
        self.itemDetailWindow.textTaille.setValidator(QtGui.QIntValidator())
        self.itemDetailWindow.textPrixAchat.setValidator(QtGui.QIntValidator())
        self.itemDetailWindow.textStock.setValidator(QtGui.QIntValidator())

        # Sets up State comboBox 
        self.comboBoxType = QComboBox(self)

        self.gearTypes = self.item.getAllGearTypes()

        stringArray = []
        for gearType in self.gearTypes:
            stringArray.append(gearType[0])

        self.comboBoxType.addItems(stringArray)
        self.comboBoxType.setEnabled(False)
        self.comboBoxType.setGeometry(540, 90, 131, 20)
        self.comboBoxType.setCurrentIndex(self.item.type - 1)
        self.comboBoxType.currentIndexChanged.connect(self.typeIndexChanged)
        self.comboBoxType.show()
        
        self.setupTabOrder()
        self.setAllFieldsToEditable(False)

        self.itemDetailWindow.show()
    
    # Sets up the tab order 
    def setupTabOrder(self):

        tabOrder = [ self.itemDetailWindow.textMarque, self.itemDetailWindow.textModel, 
        self.comboBoxType, self.itemDetailWindow.comboBoxEtat, self.itemDetailWindow.textTaille, self.itemDetailWindow.textPrixAchat,
        self.itemDetailWindow.textRevenusGeneres, self.itemDetailWindow.textStock, self.itemDetailWindow.btnContracts, self.itemDetailWindow.btnEdit,
        self.itemDetailWindow.btnValider, self.itemDetailWindow.textCodeArticle]

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

    # When contracts button clicked, open contracts UI
    def contractsButton(self):
        contracts = contractsController.ContractsUi()
        contracts.setupUi(self.item.id, self.item.itemNb)
    
    # When edit button is clicked
    # Enables or disables fields 
    def editButton(self):
        if self.editable == False:
            self.editable = True
            self.setAllFieldsToEditable(True) # Changes all fields to editable
            
            self.itemDetailWindow.textErrorMessage.setStyleSheet("color: green; border:none;")
            self.itemDetailWindow.textErrorMessage.setText("Les champs sont désormait éditable")
        else:
            self.editable = False
            self.setAllFieldsToEditable(False) # Changes all fields to not editable
            self.itemDetailWindow.textErrorMessage.setStyleSheet("color: red; border:none;")
            self.itemDetailWindow.textErrorMessage.setText("Les champs ne sont plus éditable")

    # switches all fields availbility,
    # if bool is True, all fields are editables
    # if bool is False, all fields are not editabled
    def setAllFieldsToEditable(self, bool):
        self.itemDetailWindow.textPrixAchat.setReadOnly(not bool)
        self.itemDetailWindow.textMarque.setReadOnly(not bool)
        self.itemDetailWindow.textModel.setReadOnly(not bool)
        self.itemDetailWindow.textTaille.setReadOnly(not bool)
        self.itemDetailWindow.comboBoxEtat.setEnabled(bool)
        self.itemDetailWindow.btnValider.setEnabled(bool)
        self.itemDetailWindow.textStock.setReadOnly(not bool)
        self.comboBoxType.setEnabled(bool)

    # Checks if the fields completed are valid or not
    def checkFields(self):
        #Empty checks
        if not self.itemDetailWindow.textMarque.text():
            return {"error": True, "errorMessage": "Le champ 'Marque' est obligatoire"}

        if not self.itemDetailWindow.textTaille.text():
            return {"error": True, "errorMessage": "Le champ 'Taille' est obligatoire"}

        if not self.itemDetailWindow.textStock.text():
            return {"error": True, "errorMessage": "Le champ 'Nombre' est obligatoire"}

        if not self.itemDetailWindow.textPrixAchat.text():
            self.addItemWindow.textPrix.setText("0")

        if int(self.itemDetailWindow.textPrixAchat.text()) < 0 or int(self.itemDetailWindow.textTaille.text()) < 0 or int(self.itemDetailWindow.textStock.text()) < 0:
            return{"error" : True, "errorMessage": "Les champs ne peuvent pas être négatifs"}
        # Stock can only be 0 or 1 when its unique
        if int(self.itemDetailWindow.textStock.text()) > 1 and self.item.unique == True:
            return{"error": True, "errorMessage": "Le champ 'Nombre doit être 1 ou 0'"}

        return {"error" : False}

    # When user validates the item
    def validateButton(self):
        global windowNeedsUpdate
        res = self.checkFields()

        if res['error']:
            self.displayErrorMessage(res['errorMessage'])
        else:
            self.item.setItem({"price" : self.itemDetailWindow.textPrixAchat.text(), "brand" : self.itemDetailWindow.textMarque.text(), 
            "model" : self.itemDetailWindow.textModel.text(), "type" : self.comboBoxType.currentText(), 
            "state": self.itemDetailWindow.comboBoxEtat.currentText(), "stock" : self.itemDetailWindow.textStock.text(),
            "size" : self.itemDetailWindow.textTaille.text()})
            self.item.updateItem()
            self.itemDetailWindow.close()
            windowNeedsUpdate = True

    # Displays in a label the error given
    # Error is a string that is going to be displayed
    def displayErrorMessage(self, error):
        self.itemDetailWindow.textErrorMessage.setStyleSheet(
            "color: red; border:none;")
        self.itemDetailWindow.textErrorMessage.setText(error)

    # When the type changed, checks if it is unique or not
    def typeIndexChanged(self):
        index = self.comboBoxType.currentIndex()
        self.item.setItem({"type" : index + 1})
        self.item.setItem({"unique" : self.item.checkIfItemIsUnique(self.item.type)})

        if self.item.unique:
            self.itemDetailWindow.lblTypeStock.setText("Stock (unique)")
        else:
            self.itemDetailWindow.lblTypeStock.setText("Stock (multiple)")


    """
    Checks if the widget got pressed enter with focus, if yes it does its normal behavior
    
    :param event: The event that occurred
    """
    def event(self, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
                if self.itemDetailWindow.btnEdit.hasFocus():
                    self.editButton()
                if self.itemDetailWindow.btnValider.hasFocus():
                    self.validateButton()
                if self.itemDetailWindow.btnContracts.hasFocus():
                    self.contractsButton()
                if self.itemDetailWindow.comboBoxEtat.hasFocus():
                    self.itemDetailWindow.comboBoxEtat.showPopup()
                if self.comboBoxType.hasFocus():
                    self.comboBoxType.showPopup()
                self.focusNextPrevChild(True) # Goes to next widget
                self.window().setAttribute(QtCore.Qt.WA_KeyboardFocusChange) # Styles the border painting

        return super().event(event)


class AddItemsUI(QtWidgets.QMainWindow):
    
    def __init__(self):
        global basePath
        super().__init__()
        self.addItemWindow = uic.loadUi(basePath + "\\view\\addItemsView.ui", self)
        self.setupUi()
        self.addItemWindow.show()

    # When window closes, simulate the fact that he clicked on validate
    def closeEvent(self, event):
        self.buttonValidate()

    # Sets up the UI
    def setupUi(self):
        self.item = Item()

        self.setupComboBox()
        
        #Event listener to all buttons
        self.addItemWindow.btnValider.clicked.connect(self.buttonValidate)
        self.addItemWindow.btnEncore.clicked.connect(self.buttonAdd)
        

        # Accepts number only
        self.addItemWindow.textTaille.setValidator(QtGui.QIntValidator())
        self.addItemWindow.textPrix.setValidator(QtGui.QIntValidator())
        self.addItemWindow.textStock.setValidator(QtGui.QIntValidator())

        # Hide type choice
        self.addItemWindow.textTypeChoix.hide()

        # Disable both radioBoxes
        self.addItemWindow.radioUnique.setEnabled(False)
        self.addItemWindow.radioMultiple.setEnabled(False)

        # Setting the tab order
        tabOrder = [self.addItemWindow.textCodeArticle, self.addItemWindow.textMarque, self.addItemWindow.textModel, 
        self.comboBoxType, self.addItemWindow.textTypeChoix, self.addItemWindow.textTaille, self.addItemWindow.comboBoxEtat, self.addItemWindow.textPrix,
        self.addItemWindow.radioUnique, self.addItemWindow.radioMultiple, self.addItemWindow.textStock,
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
        self.comboBoxType = QComboBox(self)

        self.gearTypes = self.item.getAllGearTypes()
        stringArray = ["Choix", "Nouveau"]

        for gearType in self.gearTypes:
            stringArray.append(gearType[0])

        self.comboBoxType.addItems(stringArray)
        self.comboBoxType.activated.connect(self.comboBoxTypeChanged)

        self.comboBoxType.setGeometry(480, 100, 113, 20)

        self.comboBoxType.show()
    
    # When the type changed, check if "Nouveau" got choosen
    def comboBoxTypeChanged(self):
        if self.comboBoxType.currentIndex() == 1:
            # Name field visible 
            self.addItemWindow.textTypeChoix.setVisible(True)
            self.addItemWindow.textTypeChoix.setFocus(True)
            # Enables radioBoxes
            self.addItemWindow.radioUnique.setEnabled(True)
            self.addItemWindow.radioMultiple.setEnabled(True)
        if self.comboBoxType.currentIndex() > 1:
            # Name field not visible anymore
            self.addItemWindow.textTypeChoix.setVisible(False)
            # Disables radioBoxes
            self.addItemWindow.radioUnique.setEnabled(False)
            self.addItemWindow.radioMultiple.setEnabled(False)
            self.currentTypeIndex = self.comboBoxType.currentIndex() - 1
            isUnique = Item.checkIfItemIsUnique(self, self.currentTypeIndex)
            if isUnique:
                self.addItemWindow.radioUnique.setChecked(True)
            else:
                self.addItemWindow.radioMultiple.setChecked(True)

    # It returns a dictionary with the values of the fields of the add form.
    #:return: A dictionary with the values of the fields in the addItemWindow.
    def getCreatedItem(self):
        
        res = self.checkRequiredFields()

        if res['error'] == True:
            return res
        
        # If the user selected on the "Nouveau" type
        if self.comboBoxType.currentIndex() == 1:
            if self.addItemWindow.radioUnique.isChecked() == True:
                isUnique = 1
            else:
                isUnique = 0

            self.item.createType(self.addItemWindow.textTypeChoix.text(), isUnique)
            self.comboBoxType.addItems([self.addItemWindow.textTypeChoix.text()])

            itemToAdd = {
                "error": False,
                "itemNumber": self.addItemWindow.textCodeArticle.text(),
                "state": self.item.getStateIdFromDescription(self.addItemWindow.comboBoxEtat.currentText()),
                "price": self.addItemWindow.textPrix.text(),
                "brand": self.addItemWindow.textMarque.text(),
                "model": self.addItemWindow.textModel.text(),
                "type": self.item.getTypeIdFromName(self.addItemWindow.textTypeChoix.text()),
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
        
        itemToAdd = {
            "error": False,
            "itemNumber": self.addItemWindow.textCodeArticle.text(),
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

    # Leaves the window and updates it in the list of the items
    def buttonValidate(self):
        self.addItemWindow.textErrorMessage.setText("")
        self.addItemWindow.close()

    # When the button "Encore" is clicked
    # Creates a new item with the fields inputed
    def buttonAdd(self):
        global windowNeedsUpdate
        global creatingItem

        itemToAdd = self.getCreatedItem()
        if itemToAdd['error'] == True:
            self.displayErrorMessage(itemToAdd['errorMessage'])
            return
        

        self.item.setItem(itemToAdd)

        result = self.item.addItem()

        if result['error'] == True:
            self.displayErrorMessage(result['errorMessage'])
        else:
            self.addItemWindow.textErrorMessage.setStyleSheet(
                "color: green; border:none;")
            self.addItemWindow.textErrorMessage.setText("Article ajouté")
            self.addItemWindow.textCodeArticle.setText("")
            windowNeedsUpdate = True
            creatingItem = True

    # Displays in a label the error given
    def displayErrorMessage(self, error):
        self.addItemWindow.textErrorMessage.setStyleSheet("color: red; border:none;")
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

        if not self.addItemWindow.textStock.text():
            return {"error": True, "errorMessage": "Le champ 'Nombre' est obligatoire"}
        
        if not self.addItemWindow.textTypeChoix.text() and self.comboBoxType.currentIndex() == 1:
            return {"error": True, "errorMessage": "'Nom du type' est obligatoire"}

        if not self.addItemWindow.textPrix.text():
            self.addItemWindow.textPrix.setText("0")

        # Negative number checks
        if int(self.addItemWindow.textPrix.text()) < 0 or int(self.addItemWindow.textTaille.text()) < 0 or int(self.addItemWindow.textStock.text()) < 0:
            return {"error": True, "errorMessage": "Les champs ne peuvent pas être négatifs"}

        # Radio button check
        if self.addItemWindow.radioMultiple.isChecked() == False and self.addItemWindow.radioUnique.isChecked() == False:
            return {"error": True, "errorMessage": "Veuillez choisir un 'Type Stock'"}
        
        if self.addItemWindow.radioUnique.isChecked() == True and int(self.addItemWindow.textStock.text()) > 1:
            return {"error": True, "errorMessage": "Le stock doit être 1 ou 0"}

        return self.item.checkitemNumber(self.addItemWindow.textCodeArticle.text())


    # Checks if the widget got pressed enter with focus, if yes it does its normal behavior

    #:param event: The event that occurred
    def event(self, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):

                # Checks radioBox "Unique" if it hasFocus and enter key is pressed
                if self.addItemWindow.radioUnique.hasFocus(): 
                    self.addItemWindow.radioUnique.setChecked(True)

                # Checks radioBox "Multiple" if it hasFocus and enter key is pressed
                if self.addItemWindow.radioMultiple.hasFocus():
                    self.addItemWindow.radioMultiple.setChecked(True)

                # Clicks on the "Encore" Button if it has focus and enter key is pressed
                if self.addItemWindow.btnEncore.hasFocus():
                    self.buttonAdd()

                # Clicks on the "Valider" Button if it has focus and enter key is pressed
                if self.addItemWindow.btnValider.hasFocus():
                    self.buttonValidate()

                # Shows "Type" content if it has focus and enter key is pressed
                if self.addItemWindow.comboBoxType.hasFocus():
                    self.addItemWindow.comboBoxType.showPopup()

                # Shows "Etat" content if it has focus and enter key is pressed
                if self.addItemWindow.comboBoxEtat.hasFocus():
                    self.addItemWindow.comboBoxEtat.showPopup()

                self.focusNextPrevChild(True) # Goes to next widget
                self.window().setAttribute(QtCore.Qt.WA_KeyboardFocusChange) # Styles the border painting
        return super().event(event)
