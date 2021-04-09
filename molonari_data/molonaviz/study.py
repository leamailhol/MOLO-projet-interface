from sensor import Sensor
from point import Point

import os
from PyQt5 import QtGui, QtCore

class Study(object):
    '''
    classdocs
    '''

    def __init__(self, name, rootDir, sensorDir):
        self.name = name
        self.rootDir = rootDir
        self.sensorDir = sensorDir
    
    def loadSensors(self, sensorModel):
        # Reset the model (remove all sensors) !
        sensorModel.clear()
        # Reload all sensors from sensorDir
        sdir = self.sensorDir
        dirs = os.listdir(sdir)
        for mydir in dirs:
            sensor = self.loadSensor(mydir)
            
            item = QtGui.QStandardItem(mydir)
            item.setData(sensor, QtCore.Qt.UserRole)
            
            sensorModel.appendRow(item)
            item.appendRow(QtGui.QStandardItem("intercept = {:.2f}".format(float(sensor.intercept))))
            item.appendRow(QtGui.QStandardItem("dudh = {:.2f}".format(float(sensor.dudh))))
            item.appendRow(QtGui.QStandardItem("dudt = {:.2f}".format(float(sensor.dudt))))
    
    def loadSensor(self, sensorName):
        sensor = Sensor(sensorName)
        pathCalib = os.path.join(self.sensorDir, sensorName, "calibfit_{}.csv".format(sensorName))
        file = open(pathCalib,"r")
        lines = file.readlines()
        for line in lines:
            if line.split(';')[0].strip() == "Intercept":
                sensor.intercept = line.split(';')[1].strip()
            if line.split(';')[0].strip() == "dU/dH":
                sensor.dudh = line.split(';')[1].strip()
            if line.split(';')[0].strip() == "dU/dT":
                sensor.dudt = line.split(';')[1].strip()
        return sensor

    def loadPoint(self, pointName):
        name = pointName
        info = self.rootDir+'/'+name+'/'+'imp_notice.csv'
        rawTemp = self.rootDir+'/'+name+'/'+'imp_raw_temperature.csv'
        rawPres = self.rootDir+'/'+name+'/'+'imp_raw_pressure.csv'
        config = self.rootDir+'/'+name+'/'+'imp_config.png'
        notice = self.rootDir+'/'+name+'/'+'imp_notice.csv'
        file = open(info,"r",encoding='utf-8-sig')
        lines = file.readlines()
        for line in lines:
            parts = line.split(',')
            if parts[0].strip() == "P_Sensor_Name":
                sensor = parts[1].strip()
            if parts[0].strip() == "Shaft_Name":
                shaft = parts[1].strip()
                return Point(name,info,sensor, shaft, rawTemp, rawPres, config, notice)

    def loadPoints(self, pointModel):
        pointModel.clear()
        dirs = os.listdir(self.rootDir)
        for mydir in dirs:
            _, ext = os.path.splitext(mydir)
            if ext != '.txt' :
                item = QtGui.QStandardItem(mydir)
                pointModel.appendRow(item)
                point = self.loadPoint(mydir)
                item.setData(point, QtCore.Qt.UserRole)

    def saveStudy(self):
        os.chdir(self.rootDir)
        f = open(f"{self.name}.txt","w+")
        f.write(f"{self.name}\n{self.rootDir}\n{self.sensorDir}")

        f.close()
    

    
    