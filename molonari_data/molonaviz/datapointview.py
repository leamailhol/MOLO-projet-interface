import sys
import os
from PyQt5 import QtWidgets, uic, QtCore
from point import Point
import pandas as pd 
from study import Study
From_DataPointView,dummy = uic.loadUiType(os.path.join(os.path.dirname(__file__),"datapointview.ui"))

#path_point = 'C:/Users/Léa/Documents/MINES 2A/MOLONARI/INTERFACE/MOLO-projet-interface/molonari_data/study_ordiLea/Point001'
#os.chdir(path_point)

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
    def __init__(self,path_point):
        # Call constructor of parent classes
        super(DataPointView, self).__init__()
        QtWidgets.QDialog.__init__(self)
        self.path_point = path_point
        os.chdir(path_point)
        self.setupUi(self)

        self.pushButtonReset.clicked.connect(self.reset)

        self.pushButtonCleanup.clicked.connect(self.cleanup)

        self.pushButtonCompute.clicked.connect(self.compute)

        #col_temp = ['Index','Date','Tension','Température','A','B','C']
        col_temp = ['Date','Tension','Température']
        self.dataTemperature = pd.read_csv('imp_raw_pressure.csv', encoding='latin-1', sep=';', low_memory=False, skiprows=1)
        self.dataTemperature.columns = col_temp
        #self.dataTemperature = self.dataTemperature.drop(['A','B','C'],axis=1)

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
    

    

   
