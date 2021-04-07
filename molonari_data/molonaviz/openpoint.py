import sys
import os
from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore
from point import Point

class openPoint():

    def __init__(self, name, sensor, rawTemp, rawPres):
        self.name = name
        self.sensor = sensor
        self.rawTemp = rawTemp
        self.rawPres = rawPres

    def loadPoint(self, pointName, pointSensor, pointRawTemp, pointRawPres): 
        point = Point(pointName, pointSensor, pointRawTemp, pointRawPres)
        return point.name