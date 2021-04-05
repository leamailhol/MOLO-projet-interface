import sys
import os
from PyQt5 import QtWidgets, uic
from study import Study

From_DialogCreateStudy,dummy = uic.loadUiType(os.path.join(os.path.dirname(__file__),"dialogcreatestudy.ui"))
From_DialogOpenStudy,dummy = uic.loadUiType(os.path.join(os.path.dirname(__file__),"dialogopenstudy.ui"))


class DialogCreateStudy(QtWidgets.QDialog,From_DialogCreateStudy):
    def __init__(self):
        # Call constructor of parent classes
        super(DialogCreateStudy, self).__init__()
        QtWidgets.QDialog.__init__(self)
        
        self.setupUi(self)
        
        self.pushButtonBrowseRootDir.clicked.connect(self.browseRootDir)
        self.pushButtonBrowseSensorsDir.clicked.connect(self.browseSensorDir)
        
    def browseRootDir(self):
        dirPath = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Study Root Directory")
        if dirPath:
            self.lineEditRootDir.setText(dirPath) 
            
    def browseSensorDir(self):
        dirPath = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Sensor Directory")
        if dirPath:
            self.lineEditSensorsDir.setText(dirPath) 

    def getStudy(self):
        name = self.lineEditName.text()
        rootDir = self.lineEditRootDir.text()
        sensorDir = self.lineEditSensorsDir.text()
        return Study(name, rootDir, sensorDir)

class DialogOpenStudy(QtWidgets.QDialog,From_DialogOpenStudy):
    def __init__(self):
        # Call constructor of parent classes
        super(DialogOpenStudy, self).__init__()
        QtWidgets.QDialog.__init__(self)
        
        self.setupUi(self)
        
        self.pushButtonBrowseStudy.clicked.connect(self.browseStudy)
        
        
    def browseStudy(self):
        dirPath = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Study")
        if dirPath:
            self.lineEditRootDir.setText(dirPath) 
            
    def browseSensorDir(self):
        dirPath = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Sensor Directory")
        if dirPath:
            self.lineEditSensorsDir.setText(dirPath) 

    def getStudy(self):
        name = self.lineEditName.text()
        rootDir = self.lineEditRootDir.text()
        sensorDir = self.lineEditSensorsDir.text()
        return Study(name, rootDir, sensorDir)