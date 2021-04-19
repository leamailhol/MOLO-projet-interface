import sys
import os
import pandas as pd
import numpy as np

from PyQt5 import QtWidgets,QtCore, uic

from point import Point

From_ImportPointDialog,dummy = uic.loadUiType(os.path.join(os.path.dirname(__file__),"importpointdialog.ui"))

class ImportPointDialog(QtWidgets.QDialog,From_ImportPointDialog):
    def __init__(self,currentStudy,sensorModel):
        # Call constructor of parent classes
        super(ImportPointDialog, self).__init__()
        QtWidgets.QDialog.__init__(self)
        
        self.setupUi(self)

        self.currentStudy = currentStudy
        self.sensorModel = sensorModel
        self.pushButton_BrowseInfo.clicked.connect(self.browseInfo)
        self.pushButton_BrowseRawTemperature.clicked.connect(self.browseRawTemp)
        self.pushButton_BrowseRawPressure.clicked.connect(self.browseRawPres)
        self.pushButton_BrowseConfig.clicked.connect(self.browseConfig)
        self.pushButton_BrowseNotice.clicked.connect(self.browseNotice)
        self.pushButtonHelp.clicked.connect(self.popup_help)

    def browseInfo (self) :
        dirPath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Point Information")
        self.info = dirPath
        if dirPath:
            file = open(dirPath,"r",encoding = 'utf-8-sig')
            lines = file.readlines()
            for line in lines:
                parts = line.split(';')
                if parts[0].strip() == "Point_Name":
                    self.lineEdit_PointName.setText(parts[1].strip())
                if parts[0].strip() == "P_Sensor_Name":
                    self.lineEdit_Sensor.setReadOnly(False)
                    self.lineEdit_Sensor.setText(parts[1].strip())
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

    def saveProcessedTemp(self):
        col_temp = ['Index','Date','T sensor 1','T sensor 2', 'T sensor 3', 'T sensor 4']
        dftemp = pd.read_csv(self.lineEdit_RawTemperature.text(), encoding='utf-8', sep=',', low_memory=False, skiprows=1)
        dftemp.columns = col_temp
        dftemp.index.name='Index'
        dftemp['Date'] = '20'+dftemp['Date']
        vect_change_date = np.vectorize(self.change_date)
        dftemp['Date'] = vect_change_date(dftemp['Date'])
        dftemp = dftemp.astype({'T sensor 1': np.float,'T sensor 2': np.float,'T sensor 3': np.float,'T sensor 4': np.float})
        for i in range(1,5) :
            dftemp[f'T sensor {i}']=dftemp[f'T sensor {i}'] + float(273.5)
        path = os.path.join(self.currentStudy.rootDir,self.lineEdit_PointName.text(), 'processed_temperature.csv')
        dftemp.to_csv(path, index = False)

    def saveProcessedPres(self):
        col_press = ['Date','Tension','Temperature']
        dfpres = pd.read_csv(self.lineEdit_RawPressure.text(), encoding='utf-8', sep=';', low_memory=False, skiprows=0)
        dfpres.columns = col_press 
        dfpres.index.name='Index'
        dfpres = dfpres.dropna()
        vect_change_date = np.vectorize(self.change_date)
        dfpres['Date'] = vect_change_date(dfpres['Date'])
        dfpres = dfpres.astype({'Temperature': np.float,'Tension': np.float})
        dfpres['Temperature'] = dfpres['Temperature'] #+float(273.5)
        pres_sensor_name = self.lineEdit_Sensor.text()
        item_pres = self.sensorModel.item(0)
        pres_sensor = None
        for row in range(item_pres.rowCount()):
            if item_pres.child(row).text() == pres_sensor_name :
                pres_sensor = item_pres.child(row).data(QtCore.Qt.UserRole)
        dfpres['Pressure'] = (dfpres['Tension']-pres_sensor.intercept-pres_sensor.dudt*dfpres['Temperature'])/pres_sensor.dudh
        path = os.path.join(self.currentStudy.rootDir, self.lineEdit_PointName.text(),'processed_pressure.csv')
        dfpres.to_csv(path)
    
    def change_date(self,str) :
        a = str.split('-')
        return '/'.join(a)

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

    def popup_help(self) :
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Help import new point")
        msg.setText("Here is a little tutorial : \n To complete the first line, browse and select info file \n Then browse the temperature file, the pressure file, the configuration and the notice" )
        msg.setIcon(QtWidgets.QMessageBox.Question)
        x = msg.exec()

