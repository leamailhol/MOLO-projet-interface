import sys
import os
from PyQt5 import QtWidgets, uic
import numpy as np
From_ComputeDialog,dummy = uic.loadUiType(os.path.join(os.path.dirname(__file__),"computedialog.ui"))


class ComputeDialog(QtWidgets.QDialog,From_ComputeDialog):
    def __init__(self):
        # Call constructor of parent classes
        super(ComputeDialog, self).__init__()
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.list_quantile = []

        self.textEditQuantile.setText(f'Quantiles : {self.list_quantile}')
        self.pushButton_Quantile.clicked.connect(self.addQuantile)

    def addQuantile(self) :
        self.list_quantile.append(np.around(float(self.doubleSpinBox_Quantile.value()),2))
        self.textEditQuantile.setText(f'Quantiles : {self.list_quantile}')

     