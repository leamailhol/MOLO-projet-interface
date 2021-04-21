import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from study import Study
from dialogopenstudy import DialogOpenStudy
from dialogcreatestudy import DialogCreateStudy
from importpointdialog import ImportPointDialog
from datapointview import DataPointView

From_MainWindow,dummy = uic.loadUiType(os.path.join(os.path.dirname(__file__),"mainwindow.ui"))

class MainWindow(QtWidgets.QMainWindow,From_MainWindow):
    def __init__(self):
        # Call constructor of parent classes
        super(MainWindow, self).__init__()
        QtWidgets.QMainWindow.__init__(self)
        
        self.setupUi(self)

        self.currentStudy = None
        self.currentPoint = None
        self.clickedPoint = None

        self.actionCreate_Study.triggered.connect(self.createStudy)
        self.actionOpen_Study.triggered.connect(self.openStudy)
        self.actionImport_Point.triggered.connect(self.importPoint)
        
        self.sensorModel = QtGui.QStandardItemModel()
        self.treeViewSensors.setModel(self.sensorModel)

        self.pointModel = QtGui.QStandardItemModel()
        self.treeViewPoint.setModel(self.pointModel)
        self.treeViewPoint.doubleClicked.connect(self.openPoint)

    def createStudy(self):
        dlg = DialogCreateStudy() # Could be renamed DialogCreateStudy
        res = dlg.exec()
        if (res == QtWidgets.QDialog.Accepted) :
            self.currentStudy = dlg.getStudy()
            self.currentStudy.loadSensors(self.sensorModel)
            self.currentStudy.saveStudy()
        
    def openStudy(self):
        # TODO : create and show DialogOpenStudy, then intialiaze a new study
        dlg = DialogOpenStudy() # Could be renamed DialogCreateStudy
        res = dlg.exec()
        if (res == QtWidgets.QDialog.Accepted) :
            self.currentStudy = dlg.getStudy()
            self.currentStudy.loadSensors(self.sensorModel)
            self.currentStudy.loadPoints(self.pointModel)
            

    def importPoint(self):
        dlg = ImportPointDialog(self.currentStudy,self.sensorModel) 
        #for i in range(self.sensorModel.rowCount()) :
            #sensor_name = self.sensorModel.item(i).text() 
            #dlg.comboBox_Sensor.addItem(sensor_name)
        #for i in range(self.sensorModel.rowCount()) :
            #shaft_name = self.sensorModel.item(i).tcdext() 
            #dlg.comboBox_Shaft.addItem(shaft_name)
        res = dlg.exec()
        if (res == QtWidgets.QDialog.Accepted) :
            self.currentPoint = dlg.getPoint()
            self.currentPoint.loadPoint(self.pointModel)
            self.currentPoint.savePoint(self.currentStudy)
            dlg.saveProcessedPres()
            dlg.saveProcessedTemp()

    def openPoint(self,index):
        item = self.pointModel.itemFromIndex(index)
        self.clickedPoint = item.data(QtCore.Qt.UserRole)
        self.clickedPoint.path = f'{self.currentStudy.rootDir}/{self.clickedPoint.name}'
        datapointview = DataPointView(self.clickedPoint,self.currentStudy,self.sensorModel)
        datapointview.setWindowTitle(self.clickedPoint.name)
        self.mdiArea.addSubWindow(datapointview)    
        datapointview.show()

        
    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())