import sys
import os
from numpy import NaN
from PyQt5 import QtWidgets, uic
from study import Study

import pandas as pd
import numpy as np

From_DialogCleanUp,dummy = uic.loadUiType(os.path.join(os.path.dirname(__file__),"dialogcleanup.ui"))

class DialogCleanUp(QtWidgets.QDialog,From_DialogCleanUp):
    def __init__(self):
        # Call constructor of parent classes
        super(DialogCleanUp, self).__init__()
        QtWidgets.QDialog.__init__(self)
        
        self.setupUi(self)


    def saveCleanedUpData(self, code):
        dft = pd.read_csv('processed_temperature.csv', encoding='utf-8', sep=',', low_memory=False, skiprows=0)
        dfp = pd.read_csv('processed_pressure.csv', encoding='utf-8', sep=',', low_memory=False, skiprows=0)

        
        f = open("test.py","w+")
        text = code
        f.write(code)
        f.close()

        exec(open("test.py").read())

    def getCode(self):
        return self.textEdit.toPlainText()

        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = DialogCleanUp()
    mainWin.show()
    sys.exit(app.exec_())