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


from dialogcleanup import DialogCleanUp
from numpy import NaN


#path_point = 'C:/Users/Léa/Documents/MINES 2A/MOLONARI/INTERFACE/MOLO-projet-interface/molonari_data/study_ordiLea/Point001'
#os.chdir(path_point)
# Create processed temperatures plot

class TimeSeriesPlotCanvas(matplotlib.backends.backend_qt5agg.FigureCanvas):

    def __init__(self, title, y_name, variable):
        
        self.variable = variable
        self.fig = matplotlib.figure.Figure()
        self.title = title
        self.axes = self.fig.add_subplot(111)
        self.ylab = y_name
        

        matplotlib.backends.backend_qt5agg.FigureCanvas.__init__(self,self.fig)


    def setModel(self, model):

        self.model = model
    
    def plot(self):
        
        if self.variable == 'Temperature': 
            self.axes.title.set_text(self.title)
            self.axes.set_xlabel('Time')
            self.axes.set_ylabel(self.ylab)
            data = self.model.getData()
            self.axes.plot(data['Date'], data['T sensor 1'], label = '10cm')
            self.axes.plot(data['Date'], data['T sensor 2'], label = '20cm')
            self.axes.plot(data['Date'], data['T sensor 3'], label = '30cm')
            self.axes.plot(data['Date'], data['T sensor 4'], label = '40cm')
            self.axes.set_xticklabels(data['Date'], rotation=45)
            self.axes.legend()
            self.draw()
        
        if self.variable == 'Pressure':
            self.axes.title.set_text(self.title)
            self.axes.set_xlabel('Time')
            self.axes.set_ylabel(self.ylab)
            data = self.model.getData()
            self.axes.plot(data['Date'], data['Pressure'])
            self.axes.set_xticklabels(data['Date'], rotation=45)
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

        
        self.dataTemperature = pd.read_csv('processed_temperature.csv', encoding='utf-8', sep=',', low_memory=False, skiprows=0)
        data_to_display_temp = pandasModel(self.dataTemperature)
        self.tableViewTemperature.setModel(data_to_display_temp)
        
        
        self.dataPressure = pd.read_csv('processed_pressure.csv', encoding='utf-8', sep=',', low_memory=False, skiprows=0)
        data_to_display_press = pandasModel(self.dataPressure)
        self.tableViewPressure.setModel(data_to_display_press)


        self.plotViewTemp = TimeSeriesPlotCanvas("Temperature evolution", "Temperature (K)", 'Temperature') # Titre du grahique + indice des séries à afficher (=  colonnes dans le data frame)
        self.layoutMeasuresTemp.addWidget(self.plotViewTemp)
        self.plotViewTemp.setModel(data_to_display_temp)
        self.plotViewTemp.plot()

        self.plotViewPress = TimeSeriesPlotCanvas("Pressure evolution", "Pressure (Bar)", 'Pressure') # Titre du grahique + indice des séries à afficher (=  colonnes dans le data frame)
        self.layoutMeasuresTemp.addWidget(self.plotViewPress)
        self.plotViewPress.setModel(data_to_display_press)
        self.plotViewPress.plot()






    def reset(self):
        print('reset')
    
    def cleanup(self):
        clnp = DialogCleanUp() 
        mycleanupcode = clnp.getCode()
        res = clnp.exec()
        if (res == QtWidgets.QDialog.Accepted) :
            
            clnp.saveCleanedUpData(mycleanupcode)

    def compute(self):
        print('compute')
    

    

   
