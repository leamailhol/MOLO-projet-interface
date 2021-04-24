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

        self.lineEdit_Config.setText(os.path.join(self.currentStudy.rootDir,'..','measures','pt2pourtest','config.png'))
        self.lineEdit_Notice.setText(os.path.join(self.currentStudy.rootDir,'..','measures','pt2pourtest','imp_notice.csv'))
        self.lineEdit_RawTemperature.setText(os.path.join(self.currentStudy.rootDir,'..','measures','pt2pourtest','p41_t_11_07_17.csv'))
        self.lineEdit_RawPressure.setText(os.path.join(self.currentStudy.rootDir,'..','measures','pt2pourtest','p41_p_11_07_17.csv'))

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

    def replace_date_temp_fabien(self, str) :
        if str[-2:]=='PM':
            str = str.replace('PM','')
            mois,jour,an_etc = str.split('/')
            an = an_etc[:2]
            rest = an_etc[2:]
            print(rest)
            if rest[1:3] !='12':
                if rest[1] == '0' :
                    rest = rest.replace(rest[1:3],f'{int(rest[2])+12}')
                else : 
                    rest = rest.replace(rest[1:3],f'{int(rest[1:3])+12}')
        if str[-2:] == 'AM':
            str = str.replace('AM','')
            mois,jour,an_etc = str.split('/')
            an = an_etc[:2]
            rest = an_etc[2:]
            if rest[1:3] =='12':
                rest = rest.replace(rest[1:3],'00')
        str = '20' + an +'/'+mois+'/'+jour+rest
        return str[:-1]

    def replace_date_pres_fabien(self, str) :
        mois,jour,an_etc = str.split('/')
        an = an_etc[:2]
        rest = an_etc[2:]
        str = '20' + an +'/'+mois+'/'+jour+rest
        return str

    def saveProcessedTemp(self):
        col_temp = ['Index','Date','T sensor 1','T sensor 2', 'T sensor 3', 'T sensor 4','A','B','C','D','E']
        dftemp = pd.read_csv(self.lineEdit_RawTemperature.text(), skiprows=1)
        dftemp.columns = col_temp
        dftemp = dftemp.drop(axis = 1, columns = ['Index','A','B','C','D','E'])
        dftemp.index.name='Index'
        rep = np.vectorize(self.replace_date_temp_fabien)
        dftemp['Date'] = rep(dftemp['Date'])
        dftemp = dftemp.iloc[:2237] #specifique fichier fabien 
        dftemp = dftemp.astype({'T sensor 1': np.float,'T sensor 2': np.float,'T sensor 3': np.float,'T sensor 4': np.float})
        for i in range(1,5) :
            dftemp[f'T sensor {i}']=dftemp[f'T sensor {i}'] + float(273.5)
            dftemp[f'T sensor {i}'] = dftemp[f'T sensor {i}'].round(2)
        path = os.path.join(self.currentStudy.rootDir,self.lineEdit_PointName.text(), 'processed_temperature.csv')
        dftemp.to_csv(path, index = False)

    def saveProcessedPres(self):
        col_press = ['Index','Date','Tension','Temperature','A','B','C']
        dfpres = pd.read_csv(self.lineEdit_RawPressure.text(), skiprows=1)
        dfpres.columns = col_press 
        dfpres = dfpres.drop(axis = 1, columns = ['Index','A','B','C'])
        dfpres.index.name='Index'
        dfpres = dfpres.dropna()
        rep = np.vectorize(self.replace_date_pres_fabien)
        dfpres['Date'] = rep(dfpres['Date'])
        dfpres = dfpres.iloc[1:2238]
        dfpres = dfpres.astype({'Temperature': np.float,'Tension': np.float})
        dfpres['Temperature'] = dfpres['Temperature'] + float(273.5)
        pres_sensor_name = self.lineEdit_Sensor.text()
        item_pres = self.sensorModel.item(0)
        pres_sensor = None
        for row in range(item_pres.rowCount()):
            if item_pres.child(row).text() == pres_sensor_name :
                pres_sensor = item_pres.child(row).data(QtCore.Qt.UserRole)
        dfpres['Pressure'] = (dfpres['Tension']-pres_sensor.intercept-pres_sensor.dudt*dfpres['Temperature'])/pres_sensor.dudh
        dfpres['Pressure'] = dfpres['Pressure'].round(2)
        dfpres['Temperature'] = dfpres['Temperature'].round(2)
        dfpres['Tension'] = dfpres['Tension'].round(2)
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
        msg.exec()

