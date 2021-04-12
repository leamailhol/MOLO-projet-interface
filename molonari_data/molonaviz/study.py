from point import Point
from sensor import pressureSensor
from sensor import temperatureSensor
from sensor import temperatureShaft
from sensor import sensorType


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

        press = dirs[0]
        temp = dirs[2]
        shaft = dirs[1]

        #capteurs de pression

        sensortype = self.loadSensorType(press) #on load le dossier "pressure"
        
        item_press = QtGui.QStandardItem(press) 
        item_press.setData(sensortype, QtCore.Qt.UserRole)
        sensorModel.appendRow(item_press) #on ajoute une ligne à l'arbre

        sdir2 = os.path.join(sdir, press)
        dirs2 = os.listdir(sdir2)

        for mydir in dirs2 :

            sensor = self.loadPressureSensor(mydir) 
            
            no_ext, ext = os.path.splitext(mydir)
            item = QtGui.QStandardItem(no_ext)
            item.setData(sensor, QtCore.Qt.UserRole)
            item_press.appendRow(item)

            item.appendRow(QtGui.QStandardItem("intercept = {:.2f}".format(float(sensor.intercept))))
            item.appendRow(QtGui.QStandardItem("dudh = {:.2f}".format(float(sensor.dudh))))
            item.appendRow(QtGui.QStandardItem("dudt = {:.2f}".format(float(sensor.dudt))))
            
        #capteurs de température

        sensortype = self.loadSensorType(temp)
            
        item_temp = QtGui.QStandardItem(temp)
        item_temp.setData(sensortype, QtCore.Qt.UserRole)
        sensorModel.appendRow(item_temp)

        sdir3 = os.path.join(sdir, temp)
        dirs3 = os.listdir(sdir3)
        for mydir in dirs3 :

            sensor = self.loadTemperatureSensor(mydir)
            no_ext, ext = os.path.splitext(mydir)
            item = QtGui.QStandardItem(no_ext) 
            item.setData(sensor, QtCore.Qt.UserRole)
            item_temp.appendRow(item)
        

        #shaft de température

        sensortype = self.loadSensorType(shaft)
        
        item_shaft = QtGui.QStandardItem(shaft)
        item_shaft.setData(sensortype, QtCore.Qt.UserRole)
        sensorModel.appendRow(item_shaft)


        sdir4 = os.path.join(sdir, shaft)
        dirs4 = os.listdir(sdir4)
        for mydir in dirs4 : 

            sensor = self.loadTemperatureShaft(mydir)
            no_ext, ext = os.path.splitext(mydir)
            item = QtGui.QStandardItem(no_ext)
            item.setData(sensor, QtCore.Qt.UserRole)
            item_shaft.appendRow(item)

            item.appendRow(QtGui.QStandardItem(f"t_sensor_name : {sensor.t_sensor_name}"))
            item.appendRow(QtGui.QStandardItem(f"sensors_depth : {sensor.sensors_depth}"))


    def loadSensorType(self, fileName):
        sensortype = sensorType(fileName)
        return sensortype


    def loadPressureSensor(self, sensorName):
        sensor = pressureSensor(sensorName)

        sdir = self.sensorDir
        dirs = os.listdir(sdir)

        press = dirs[0]
         
        pathCalib = os.path.join(self.sensorDir, press, sensorName)
        file = open(pathCalib,"r")
        lines = file.readlines()
        for line in lines:
            if line.split(';')[0].strip() == "Intercept":
                sensor.intercept = line.split(';')[1].strip()
            if line.split(';')[0].strip() == "dU_dH":
                sensor.dudh = line.split(';')[1].strip()
            if line.split(';')[0].strip() == "dU_dT":
                sensor.dudt = line.split(';')[1].strip()
        return sensor

    def loadTemperatureSensor(self, sensorName):
        sdir = self.sensorDir
        dirs = os.listdir(sdir)
        sensor = temperatureSensor(sensorName)
        return sensor

    def loadTemperatureShaft(self, sensorName):
        sensor = temperatureShaft(sensorName)

        sdir = self.sensorDir
        dirs = os.listdir(sdir)

        shaft = dirs[1]
         
        pathCalib = os.path.join(self.sensorDir, shaft, sensorName)
        file = open(pathCalib,"r")
        lines = file.readlines()
        for line in lines:
            if line.split(';')[0].strip() == "T_Sensor_Name":
                sensor.t_sensor_name = line.split(';')[1].strip()
            if line.split(';')[0].strip() == "Sensors_Depth":
                sensor.sensors_depth = line.split(';')[1].strip()
        return sensor

    def loadPoint(self, pointName):
        name = pointName
        info = self.rootDir+'/'+name+'/'+'imp_notice.csv'
        rawTemp = self.rootDir+'/'+name+'/'+'imp_raw_temperature.csv'
        rawPres = self.rootDir+'/'+name+'/'+'imp_raw_pressure.csv'
        config = self.rootDir+'/'+name+'/'+'imp_config.png'
        notice = self.rootDir+'/'+name+'/'+'imp_notice.csv'
        point = Point(name,info,rawTemp = rawTemp, rawPres = rawPres, config = config, notice = notice)
        file = open(info,"r",encoding = 'utf-8-sig')
        lines = file.readlines()
        for line in lines:
            parts = line.split(';')
            if parts[0].strip() == "P_Sensor_Name":
                point.sensor = parts[1].strip()
            if parts[0].strip() == "Shaft_Name":
                point.shaft = parts[1].strip()
        return point
        
    def loadPoints(self, pointModel):
        pointModel.clear()
        dirs = os.listdir(self.rootDir)
        for mydir in dirs:
            _, ext = os.path.splitext(mydir)
            if ext != '.txt' :
                item = QtGui.QStandardItem(mydir)
                point = self.loadPoint(mydir)
                print(point.name)
                item.setData(point, QtCore.Qt.UserRole)
                print(item.data(QtCore.Qt.UserRole))
                pointModel.appendRow(item)
                

    def saveStudy(self):
        os.chdir(self.rootDir)
        f = open(f"{self.name}.txt","w+")
        f.write(f"{self.name}\n{self.rootDir}\n{self.sensorDir}")

        f.close()
    

    
    