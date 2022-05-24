from PyQt5 import QtWidgets, QtGui, uic
import sys

class StaffUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        print("In staff")
        self.StaffWindow = uic.loadUi(sys.path[0] + "\\view\\staffsView.ui", self)
        self.StaffWindow.show()
