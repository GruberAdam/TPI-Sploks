from PyQt5.QtCore import Qt

from controller import mainMenuController

# Redirects to the right function based on the key pressed
def keyPressEvent(self, e):
    if e.key() == Qt.Key.Key_A: # When user presses the "a" key
        mainMenuController.displayClients(self)
    if e.key() == Qt.Key.Key_S: # When user presses the "s" key
        mainMenuController.displayStock(self)
    if e.key() == Qt.Key.Key_D: # When user presses the "d" key
        mainMenuController.displayStaff(self)
    if e.key() == Qt.Key.Key_F: # When user presses the "f" key
        mainMenuController.displayContracts(self)