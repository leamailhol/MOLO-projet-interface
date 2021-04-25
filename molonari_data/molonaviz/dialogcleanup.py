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
        dft = pd.read_csv('processed_temperature.csv', encoding='utf-8', sep=',', low_memory=False, skiprows=0,index_col=[0])
        dfp = pd.read_csv('processed_pressure.csv', encoding='utf-8', sep=',', low_memory=False, skiprows=0)

        print(type(code))
        f = open("code.py","w+")
        f.write(code)
        f.close()

        dft,dfp = eval(open("code.py").read())

        print(dft)
        dft.to_csv('processed_temperature.csv', sep = ',')
        dfp.to_csv('processed_pressure.csv', sep = ',')

    def getCode(self):

        return self.textEdit.toPlainText()


    