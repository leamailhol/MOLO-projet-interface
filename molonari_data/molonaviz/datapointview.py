import os
from point import Point
import pandas as pd 
from study import Study
from csv import reader
from sensor import pressureSensor
import numpy as np


import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets, QtGui, uic, QtWidgets

From_DataPointView,dummy = uic.loadUiType(os.path.join(os.path.dirname(__file__),"datapointview.ui"))


#path_point = 'C:/Users/Léa/Documents/MINES 2A/MOLONARI/INTERFACE/MOLO-projet-interface/molonari_data/study_ordiLea/Point001'
#os.chdir(path_point)
# Create processed temperatures plot

class TimeSeriesPlotCanvas(matplotlib.backends.backend_qt5agg.FigureCanvas):

    def __init__(self, title, y_name, indexes, labels):

        self.fig = matplotlib.figure.Figure()
        self.title = title
        self.indexes = indexes
        self.axes = self.fig.add_subplot(111)
        self.ylab = y_name
        self.lab = labels

        matplotlib.backends.backend_qt5agg.FigureCanvas.__init__(self,self.fig)


    def setModel(self, model):

        self.model = model
    
    def plot(self):

        self.axes.title.set_text(self.title)
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel(self.ylab)
        data = self.model.getData()
        for i in self.indexes:
            header  = data.columns[i]
            print(self.lab[i-1])
            self.axes.plot(data[header], label = self.lab[i-1])
        self.axes.legend()
        self.draw()



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
    
    def getData(self):
        return self._data


class DataPointView(QtWidgets.QDialog,From_DataPointView):
    def __init__(self,point,currentStudy,sensorModel):
        # Call constructor of parent classes
        super(DataPointView, self).__init__()
        QtWidgets.QDialog.__init__(self)
        self.path_point = point.path
        self.point = point
        os.chdir(self.path_point)
        self.setupUi(self)
        self.currentStudy = currentStudy
        self.sensorModel = sensorModel

        # On paramètre le premier onglet

        ## Notice

        text_notice = ''

        with open('imp_notice.csv', 'r', encoding='utf8') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            # Iterate over each row in the csv using reader object
            for row in csv_reader:
                if len(row) > 0 and text_notice!='': 
                    # row variable is a list that represents a row in csv
                    text_notice = text_notice + '\n' + row[0]
                if len(row) > 0 and text_notice == '':
                    text_notice = row[0]


        self.plainTextEditNotice.appendPlainText(text_notice)
        self.plainTextEditNotice.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)


        ## Geometrie 

        print('')

        text_geometry = ''

        with open('imp_info.csv', 'r', encoding='utf8') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            # Iterate over each row in the csv using reader object
            for row in csv_reader:
                if len(row) > 0 and text_geometry!='': 
                    # row variable is a list that represents a row in csv
                    word1, word2 = row[0].split(';') 
                    text_geometry = text_geometry + '\n' + word1 + ' : ' + word2
                if len(row) > 0 and text_geometry == '':
                    word1, word2 = row[0].split(';') 
                    text_geometry= 'Point_Name : ' + word2
        
        self.plainTextEditGeometry.appendPlainText(text_geometry)
        self.plainTextEditGeometry.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)

        ## Info

        self.InstallationImage.setPixmap(QtGui.QPixmap('imp_config.png'))


        self.pushButtonReset.clicked.connect(self.reset)

        self.pushButtonCleanup.clicked.connect(self.cleanup)

        self.pushButtonCompute.clicked.connect(self.compute)

        
        #col_temp = ['Index','Date','Tension','Température','A','B','C']
        col_temp = ['Date','T sensor 1','T sensor 2', 'T sensor 3', 'T sensor 4']
        self.dataTemperature = pd.read_csv('imp_raw_temperature.csv', encoding='utf-8', sep=';', low_memory=False, skiprows=0)
        self.dataTemperature.columns = col_temp
        #self.dataTemperature = self.dataTemperature.drop(['A','B','C'],axis=1)
        data_to_display_temp = pandasModel(self.dataTemperature)
        self.tableViewTemperature.setModel(data_to_display_temp)
        
        col_press = ['Date','Tension','Temperature']
        self.dataPressure_unprocessed = pd.read_csv('imp_raw_pressure.csv', encoding='utf-8', sep=';', low_memory=False, skiprows=0)
        self.dataPressure_unprocessed.columns = col_press 
        sensordir = self.currentStudy.sensorDir
        dirs = os.listdir(sensordir)
        press = dirs[0]
        pathCalib = os.path.join(sensordir, press, f'{str(self.point.pressure_sensor)}.csv')
        file = open(pathCalib,"r")
        lines = file.readlines()
        intercept = None
        dudh = None 
        dudt = None 
        for line in lines:
            if line.split(';')[0].strip() == "Intercept":
                intercept = float(line.split(';')[1].strip())
            if line.split(';')[0].strip() == "dU_dH":
                dudh = float(line.split(';')[1].strip())
            if line.split(';')[0].strip() == "dU_dT":
                dudt = float(line.split(';')[1].strip())
        df = self.dataPressure_unprocessed
        df = df.dropna()
        df = df.astype({'Temperature': np.float,'Tension': np.float})
        df['Pressure'] = (df['Tension']-intercept-dudt*df['Temperature'])/dudh
        #self.dataTemperature = self.dataTemperature.drop(['A','B','C'],axis=1)
        data_to_display_press = pandasModel(df)
        self.tableViewPressure.setModel(data_to_display_press)


        self.plotViewTemp = TimeSeriesPlotCanvas("Temperature evolution", "Temperature (K)", [1,2,3,4], ['10cm', '20cm','30cm','40cm']) # Titre du grahique + indice des séries à afficher (=  colonnes dans le data frame)
        self.layoutMeasuresTemp.addWidget(self.plotViewTemp)
        self.plotViewTemp.setModel(data_to_display_temp)
        self.plotViewTemp.plot()






    def reset(self):
        print('reset')
    
    def cleanup(self):
        print('cleanup')

    def compute(self):
        print('compute')
    

    

   
