import sys
import os
from PyQt5 import QtWidgets, uic, QtCore
from point import Point
import pandas as pd 

From_DataPointView,dummy = uic.loadUiType(os.path.join(os.path.dirname(__file__),"datapointview.ui"))

path_point = '../molonari_data/study_ordiMaëlle/point1'
os.chdir(path_point)

class pandasModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        QtCore.QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None

class DataPointView(QtWidgets.QDialog,From_DataPointView):
    def __init__(self):
        # Call constructor of parent classes
        super(DataPointView, self).__init__()
        QtWidgets.QDialog.__init__(self)
        
        self.setupUi(self)

        self.currentPoint = None


        self.pushButtonReset.clicked.connect(self.reset)

        self.pushButtonCleanup.clicked.connect(self.cleanup)

        self.pushButtonCompute.clicked.connect(self.compute)

        col_temp = ['Index','Date','Tension','Température','A','B','C']
        self.dataTemperature = pd.read_csv('rawTemp-point1.csv', encoding='latin-1', sep=',', low_memory=False, skiprows=1)
        self.dataTemperature.columns = col_temp
        self.dataTemperature = self.dataTemperature.drop(['A','B','C'],axis=1)

        print(self.dataTemperature)
        print(self.dataTemperature.columns)
        print(len(self.dataTemperature.columns))
        data_to_display = pandasModel(self.dataTemperature)

        self.tableViewTemperature.setModel(data_to_display)
        




    
    def reset(self):
        print('reset')
    
    def cleanup(self):
        print('cleanup')

    def compute(self):
        print('compute')
    
    
    





        
      





   
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = DataPointView()

    mainWin.show()
    sys.exit(app.exec_())