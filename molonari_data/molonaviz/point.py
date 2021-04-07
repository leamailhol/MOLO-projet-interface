import os
from PyQt5 import QtGui, QtCore
import shutil

class Point(object):
    
    def __init__(self, name, sensor, rawTemp, rawPres):
        self.name = name
        self.sensor = sensor
        self.rawTemp = rawTemp
        self.rawPres = rawPres

    def loadPoint(self, pointModel) :
        item = QtGui.QStandardItem(self.name)
        pointModel.appendRow(item)

    def savePoint(self, study):
        os.chdir(study.rootDir)
        os.mkdir(study.rootDir+'/'+self.name)

        shutil.copyfile(self.rawTemp, study.rootDir+'/'+self.name+'/'+'rawTemp-'+self.name+'.csv')
        shutil.copyfile(self.rawPres, study.rootDir+'/'+self.name+'/'+'rawPres-'+self.name+'.csv')

