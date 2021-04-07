import os
from PyQt5 import QtGui, QtCore

class Point(object):
    
    def __init__(self, name, sensor, rawTemp, rawPres):
        self.name = name
        self.sensor = sensor
        self.rawTemp = rawTemp
        self.rawPres = rawPres

