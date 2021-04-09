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

        self.pushButton_BrowseInfo.clicked.connect(self.browseInfo)
        self.pushButton_BrowseRawTemperature.clicked.connect(self.browseRawTemp)
        self.pushButton_BrowseRawPressure.clicked.connect(self.browseRawPres)
        self.pushButton_BrowseConfig.clicked.connect(self.browseConfig)
        self.pushButton_BrowseNotice.clicked.connect(self.browseNotice)
        
    def browseInfo (self) :
        dirPath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Point Information")
        self.info = dirPath
        if dirPath:
            file = open(dirPath,"r",encoding='utf-8-sig')
            lines = file.readlines()
            for line in lines:
                parts = line.split(',')
                if parts[0].strip() == "Point_Name":
                    self.lineEdit_PointName.setText(parts[1].strip())
                if parts[0].strip() == "P_Sensor_Name":
                    self.lineEdit_Sensor.setText(parts[1].strip())
                    self.lineEdit_Sensor.setReadOnly(True)
                if parts[0].strip() == "Shaft_Name":
                    self.lineEdit_Shaft.setText(parts[1].strip())
                    self.lineEdit_Shaft.setReadOnly(True)
                    
    def browseRawTemp(self):
        dirPath = QtWidgets.QFileDialog.getOpenFileName(self, "Select Raw Temperature")
        if dirPath:
            self.lineEdit_RawTemperature.setText(dirPath[0]) 
            
    def browseRawPres(self):
        dirPath = QtWidgets.QFileDialog.getOpenFileName(self, "Select Raw Pressure")
        if dirPath:
            self.lineEdit_RawPressure.setText(dirPath[0])

    def browseConfig(self) :
        dirPath = QtWidgets.QFileDialog.getOpenFileName(self, "Select Configuration File")
        if dirPath:
            self.lineEdit_Config.setText(dirPath[0])

    def browseNotice(self) :
        dirPath = QtWidgets.QFileDialog.getOpenFileName(self, "Select Notice")
        if dirPath:
            self.lineEdit_Notice.setText(dirPath[0])

    def getPoint(self):
        name = self.lineEdit_PointName.text()
        rawTemp = self.lineEdit_RawTemperature.text()
        rawPressure = self.lineEdit_RawPressure.text()
        sensor = self.lineEdit_Sensor.text()
        shaft = self.lineEdit_Shaft.text()
        config = self.lineEdit_Config.text()
        notice = self.lineEdit_Notice.text()
        info = self.info
        return Point(name,info,sensor, shaft, rawTemp, rawPressure, config, notice)

