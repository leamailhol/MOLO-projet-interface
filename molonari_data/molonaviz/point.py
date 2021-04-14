import os
from PyQt5 import QtGui, QtCore
import shutil
from numpy import NaN

class Point(object):
    
    def __init__(self, name,info=NaN, sensor=NaN, shaft=NaN, rawTemp=NaN, rawPres=NaN, config=NaN, notice=NaN):
        self.name = name
        self.pressure_sensor = sensor
        self.shaft = shaft
        self.info = info
        self.rawTemp = rawTemp
        self.rawPres = rawPres
        self.config = config
        self.notice = notice 
        self.path = None 

    def loadPoint(self, pointModel) :
        item = QtGui.QStandardItem(self.name)
        pointModel.appendRow(item)
        item.setData(self, QtCore.Qt.UserRole)

    def savePoint(self, study):
        os.chdir(study.rootDir)
        os.mkdir(study.rootDir+'/'+self.name)

        shutil.copyfile(self.rawTemp, study.rootDir+'/'+self.name+'/'+'imp_raw_temperature.csv')
        shutil.copyfile(self.rawPres, study.rootDir+'/'+self.name+'/'+'imp_raw_pressure.csv')
        shutil.copyfile(self.config, study.rootDir+'/'+self.name+'/'+'imp_config.png')
        shutil.copyfile(self.notice, study.rootDir+'/'+self.name+'/'+'imp_notice.csv')
        shutil.copyfile(self.info, study.rootDir+'/'+self.name+'/'+'imp_info.csv')
