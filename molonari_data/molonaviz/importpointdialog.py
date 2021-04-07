import sys
import os
from PyQt5 import QtWidgets, uic

from point import Point

From_ImportPointDialog,dummy = uic.loadUiType(os.path.join(os.path.dirname(__file__),"importpointdialog.ui"))

class ImportPointDialog(QtWidgets.QDialog,From_ImportPointDialog):
    def __init__(self):
        # Call constructor of parent classes
        super(ImportPointDialog, self).__init__()
        QtWidgets.QDialog.__init__(self)
        
        self.setupUi(self)
        
        self.pushButton_BrowseRawTemperature.clicked.connect(self.browseRawTemp)
        self.pushButton_BrowseRawPressure.clicked.connect(self.browseRawPres)
        
    def browseRawTemp(self):
        dirPath = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Raw Temperature")
        if dirPath:
            self.lineEdit_RawTemperature.setText(dirPath) 
            
    def browseRawPres(self):
        dirPath = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Raw Pressure")
        if dirPath:
            self.lineEdit_RawPressure.setText(dirPath)

    def getPoint(self):
        name = self.lineEdit_PointName.text()
        rawTemp = self.lineEdit_RawTemperature.text()
        rawPressure = self.lineEdit_RawPressure.text()
        sensor = self.comboBox_Sensor.currentText()
        return Point(name,sensor,rawTemp, rawPressure)
