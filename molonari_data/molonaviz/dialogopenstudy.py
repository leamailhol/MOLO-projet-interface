
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
        dirPath = QtWidgets.QFileDialog.getOpenFileName(self, "Select Study")
        if dirPath:
            self.lineEditStudy.setText(dirPath[0]) 

    def getStudy(self):
        dirs = self.lineEditStudy.text().split(sep='/')
        filename = dirs.pop()
        path =  '/'.join(dirs)
        os.chdir(path)

        f=open(filename, "r")
        lines = f.readlines()

         
        name = lines[0].rstrip('\n')
        rootDir = lines[1].rstrip('\n')
        sensorDir = lines[2].rstrip('\n')
        return Study(name, rootDir, sensorDir)