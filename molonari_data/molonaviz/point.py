import os
from PyQt5 import QtGui, QtCore

class Point(object):
    
    def __init__(self, name, sensor, rawTemp, rawPres):
        self.name = name
        self.sensor = sensor
        self.rawTemp = rawTemp
        self.rawPres = rawPres

    def savePoint(self, study):

        os.chdir(study.rootDir)
        os.mkdir(study.rootDir+'/'+self.name)

        shutil.copyfile(self.rawTemp, study.rootDir+'rawTemp-'+self.name+'.csv')
        shutil.copyfile(self.rawPres, study.rootDir+'rawPres-'+self.name+'.csv')

