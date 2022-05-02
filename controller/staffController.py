from PyQt5 import QtWidgets, QtGui, uic

class StaffUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        print("In staff")
        self.StaffWindow = uic.loadUi("view/staffsView.ui", self)
        self.StaffWindow.show()
