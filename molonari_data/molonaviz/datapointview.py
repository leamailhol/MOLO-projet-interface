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
from computedialog import ComputeDialog


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
        self.compdlg = None
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


        self.plotViewTemp = TimeSeriesPlotCanvas("Temperature evolution", "Temperature (K)", [1,2,3,4], ['10cm', '20cm','30cm','40cm']) # Titre du grahique + indice des séries à afficher (=  colonnes dans le data frame)
        self.layoutMeasuresTemp.addWidget(self.plotViewTemp)
        self.plotViewTemp.setModel(data_to_display_temp)
        self.plotViewTemp.plot()






    def reset(self):
        print('reset')
    
    def cleanup(self):
        clnp = DialogCleanUp() 
        mycleanupcode = clnp.getCode()
        res = clnp.exec()
        if (res == QtWidgets.QDialog.Accepted) :
            
            clnp.saveCleanedUpData(mycleanupcode)

    def compute(self):
        self.compdlg = ComputeDialog()
        res = self.compdlg.exec()
        if (res == QtWidgets.QDialog.Accepted) :
            self.runmodel()

    def runmodel(self) :
        print('coucou')
        dicParam = self.create_dicParam()
        print(dicParam)

    def create_dicParam(self) :
        riv_bed = None
        depth_sensors = None
        offset = None
        dH_measures = None
        T_measures = []
        sigma_meas_P = None
        sigma_meas_T = None
        print('coucou dic param')
        #riv_bed
        file = open(self.point.info,"r")
        lines = file.readlines()
        for line in lines:
            if line.split(';')[0].strip() == "River_Bed":
                riv_bed = float(line.split(';')[1].strip())
            if line.split(';')[0].strip() == "Delta_h":
                offset = float(line.split(';')[1].strip())
        #depth_sensors
        shaft = self.point.shaft
        item_shafts = self.sensorModel.item(2)
        shaft_sensor = None
        for row in range(item_shafts.rowCount()):
            if item_shafts.child(row).text() == shaft :
                shaft_sensor = item_shafts.child(row).data(QtCore.Qt.UserRole)
        depth_sensors = shaft_sensor.sensors_depth
        temp = shaft_sensor.t_sensor_name
        #dH_measures 
        dfp = self.dataPressure
        dH_measures = list(zip(dfp['Date'].tolist(),list(zip(dfp['Pressure'].tolist(), dfp['Temperature'].tolist())[0]))[0])
        #T_measures
        dft = self.dataTemperature
        T_measures = list(zip(dft['Date'].tolist(),dft['T sensor 1'].tolist(),dft['T sensor 2'].tolist(),dft['T sensor 3'].tolist(),dft['T sensor 4'].tolist()))
        #sigma_meas_P
        pres = self.point.pressure_sensor
        item_pres = self.sensorModel.item(0)
        pres_sensor = None
        for row in range(item_pres.rowCount()):
            if item_pres.child(row).text() == pres :
                pres_sensor = item_pres.child(row).data(QtCore.Qt.UserRole)
        sigma_meas_P = pres_sensor.sigma
        #sigma_meas_T
        item_temp = self.sensorModel.item(1)
        temp_sensor = None
        for row in range(item_temp.rowCount()):
            if item_temp.child(row).text() == temp :
                temp_sensor = item_temp.child(row).data(QtCore.Qt.UserRole)
        sigma_meas_T = temp_sensor.sigma
        dic = {'river_bed': riv_bed, 'depth_sensors' : depth_sensors, 'offset' : offset, 'dH_measures' : dH_measures, 
                'T_measures' : T_measures, 'Sigma_Meas_T' : sigma_meas_T, 'Sigma_Meas_P' : sigma_meas_P }
        return dic



        


    

    

   
