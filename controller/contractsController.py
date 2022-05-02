from PyQt5 import QtWidgets, QtGui, uic

class ContractsUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        print("In Contracts")
        self.StaffWindow = uic.loadUi("view/contractsView.ui", self)
        self.StaffWindow.show()
