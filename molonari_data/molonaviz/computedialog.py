import sys
import os
from PyQt5 import QtWidgets, uic

From_ComputeDialog,dummy = uic.loadUiType(os.path.join(os.path.dirname(__file__),"computedialog.ui"))


class ComputeDialog(QtWidgets.QDialog,From_ComputeDialog):
    def __init__(self):
        # Call constructor of parent classes
        super(ComputeDialog, self).__init__()
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
     