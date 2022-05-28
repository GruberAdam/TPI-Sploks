from PyQt5 import QtWidgets, QtGui, uic, QtCore
from model.customersModel import *
import sys

needUpdate = False

# It loads the customers from the database and displays them in a table
class CustomersUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.customersWindow = uic.loadUi(sys.path[0] + "\\view\\customersView.ui", self)

        try:
            self.loadCustomers()
            self.customersWindow.show()
        except Exception as error:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText(str(error))
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.exec_() 

    # Method designed to load the customers from the database and fills the table with them.        
    def loadCustomers(self):
        global needUpdate
        self.customers = getCustomers(self)

        self.customersWindow.tableCustomers.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        for index, customer in enumerate(self.customers):
            self.customersWindow.tableCustomers.verticalHeader().setVisible(False) # Hides the row number
            self.customersWindow.tableCustomers.insertRow(index) # Inserts the row

            # Fills the table
            self.customersWindow.tableCustomers.setItem(index, 0, QtWidgets.QTableWidgetItem(str(customer[0]))) # Sets the ID
            self.customersWindow.tableCustomers.setItem(index, 1, QtWidgets.QTableWidgetItem(str(customer[1]))) # Sets the LastName
            self.customersWindow.tableCustomers.setItem(index, 2, QtWidgets.QTableWidgetItem(str(customer[2]))) # Sets the FirstName
            self.customersWindow.tableCustomers.setItem(index, 3, QtWidgets.QTableWidgetItem(str(customer[3]))) # Sets the Address
            self.customersWindow.tableCustomers.setItem(index, 4, QtWidgets.QTableWidgetItem(str(customer[8]))) # Sets the NPA
            self.customersWindow.tableCustomers.setItem(index, 5, QtWidgets.QTableWidgetItem(str(customer[9]))) # Sets the Locality
            self.customersWindow.tableCustomers.setItem(index, 6, QtWidgets.QTableWidgetItem(str(customer[4]))) # Sets the Phone number
            self.customersWindow.tableCustomers.setItem(index, 7, QtWidgets.QTableWidgetItem(str(customer[5]))) # Sets the email
            self.customersWindow.tableCustomers.setItem(index, 8, QtWidgets.QTableWidgetItem(str(customer[6]))) # Sets the mobile phone

        self.customersWindow.tableCustomers.viewport().installEventFilter(self) # Event listener

        needUpdate = False



    #It checks if the user double clicked on a cell in the table, if so, it gets the ID of the
    #customer and opens a new window with the details of the customer

    #:param source: The object that the event is coming from
    #:param event: The event that was triggered
    #:return: The return value is a boolean value. If the event is handled, the function should
    #return True. If the event should be propagated further, the function should return False.
    def eventFilter(self, source, event):

        global needUpdate
        if needUpdate == True:
            self.loadCustomers()
        if self.customersWindow.tableCustomers.selectedIndexes() != []: # Checks that the user clicked on a cell
            if event.type() == QtCore.QEvent.MouseButtonDblClick: # If user double clicked
                row = self.customersWindow.tableCustomers.currentRow() # gets row clicked
                id = self.customersWindow.tableCustomers.item(row, 0).text() # gets ID based on click

                self.detailledUi = CustomerDetailsUi() # Prepare the second window
                self.detailledUi.setupUi(id)                
        return False
    
    
 
#It's a class that displays a window with a customer's details
class CustomerDetailsUi(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.customerDetailWindow = uic.loadUi(sys.path[0] + "\\view\\customerDetailsView.ui", self)
        self.edit = False
        
    #Sets up the UI 
        
    #:param id: the id of the customer
    def setupUi(self, id):
        self.id = id

        # Button Listener
        self.customerDetailWindow.btnEditer.clicked.connect(self.editButton)
        self.customerDetailWindow.btnSupprimer.clicked.connect(self.deleteButton)
        self.customerDetailWindow.btnAnnuler.clicked.connect(self.cancelButton)
        self.customerDetailWindow.btnValider.clicked.connect(self.confirmButton)


        self.customer = getCustomerById(self, self.id) # Get the database data

        self.fillTheLabels()

        self.show()

    # It's filling the labels with the data from the database.
    def fillTheLabels(self):
        self.customerDetailWindow.lblPrenom.setText(str(self.customer[0][2]))
        self.customerDetailWindow.lblNom.setText(str(self.customer[0][1]))
        self.customerDetailWindow.lblAdresse.setText(str(self.customer[0][3]))
        self.customerDetailWindow.lblNPA.setText(str(self.customer[0][8])) 
        self.customerDetailWindow.lblNumero.setText(str(self.customer[0][4]))
        self.customerDetailWindow.lblTelephone.setText(str(self.customer[0][6]))
        self.customerDetailWindow.lblEmail.setText(str(self.customer[0][5]))

    
    #When the edit button is clicked, the text of the labels is set to be editable, and the buttons
    #are enabled
    
    #:param id: the id of the customer
    
    def editButton(self, id):

        if self.edit == False:
            self.edit = True
            
            # Enable text modifications
            self.customerDetailWindow.lblPrenom.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
            self.customerDetailWindow.lblNom.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)   
            self.customerDetailWindow.lblAdresse.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
            self.customerDetailWindow.lblNPA.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
            self.customerDetailWindow.lblNumero.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
            self.customerDetailWindow.lblTelephone.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
            self.customerDetailWindow.lblEmail.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)

            # Enable buttons
            self.customerDetailWindow.btnSupprimer.setEnabled(True)
            self.customerDetailWindow.btnValider.setEnabled(True)
            self.customerDetailWindow.btnAnnuler.setEnabled(True)

        elif self.edit == True:
            self.edit = False

            # Remove text modifications
            self.customerDetailWindow.lblPrenom.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
            self.customerDetailWindow.lblNom.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
            self.customerDetailWindow.lblAdresse.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
            self.customerDetailWindow.lblNPA.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
            self.customerDetailWindow.lblNumero.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
            self.customerDetailWindow.lblTelephone.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
            self.customerDetailWindow.lblEmail.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)

            # Enable buttons
            self.customerDetailWindow.btnSupprimer.setEnabled(False)
            self.customerDetailWindow.btnValider.setEnabled(False)
            self.customerDetailWindow.btnAnnuler.setEnabled(False)

    # When user clicks on the "Supprimer" Button    
    def deleteButton(self):
        print("delete")

    # When user clicks on the "Valider" Button
    def confirmButton(self):
        global needUpdate

        # Stores new value in an array
        self.updatedCustomer = {
        'firstName' :self.customerDetailWindow.lblPrenom.toPlainText(), 
        'lastName' : self.customerDetailWindow.lblNom.toPlainText(), 
        'address' : self.customerDetailWindow.lblAdresse.toPlainText(), 
        'npa' : self.customerDetailWindow.lblNPA.toPlainText(), 
        'mobile' : self.customerDetailWindow.lblNumero.toPlainText(), 
        'phone' : self.customerDetailWindow.lblTelephone.toPlainText(), 
        'email' : self.customerDetailWindow.lblEmail.toPlainText()
        }
        
        updateCustomerById(self,self.id,self.updatedCustomer)
        self.updated = True
        self.customerDetailWindow.close()
        needUpdate = True

    # When user clicks on the "Annuler" Button
    # This function basically resets all the labels to their original values
    def cancelButton(self):
        self.fillTheLabels()