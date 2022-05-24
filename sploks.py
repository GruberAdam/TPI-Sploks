# Author : Adam Gruber
# Date : 17.02.2022
# Version : 1.0

import sys

sys.path.append(sys.path[0] + "\\packages") # Importing packages file
from PyQt5 import QtWidgets

from controller import mainMenuController, keyPressController

# It's a class that displays the main menu and listens for key presses.
class Sploks(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        mainMenuController.displayMainMenu(self) # Calls function in controller

    # Event listener when a key is pressed
    def keyPressEvent(self, e):
        keyPressController.keyPressEvent(self, e)


app = QtWidgets.QApplication(sys.argv)
window = Sploks()
app.exec_()