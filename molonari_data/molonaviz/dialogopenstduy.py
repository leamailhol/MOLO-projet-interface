
import sys
import os
from PyQt5 import QtWidgets, uic
from study import Study

From_DialogOpenStudy,dummy = uic.loadUiType(os.path.join(os.path.dirname(__file__),"dialogopenstudy.ui"))

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

    def getStudy(self):
        name = self.lineEditName.text()
        rootDir = self.lineEditRootDir.text()
        sensorDir = self.lineEditSensorsDir.text()
        return Study(name, rootDir, sensorDir)