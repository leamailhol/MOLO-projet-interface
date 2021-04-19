import os
from point import Point
import pandas as pd 
from study import Study
from csv import reader
from sensor import pressureSensor
import numpy as np
from pyheatmy import *
from datetime import datetime


import sys
import matplotlib.pyplot as plt
import matplotlib.backends
from matplotlib.backends import backend_qt5agg
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets, QtGui, uic, QtWidgets

From_DataPointView,dummy = uic.loadUiType(os.path.join(os.path.dirname(__file__),"datapointview.ui"))


from dialogcleanup import DialogCleanUp
from numpy import NaN
from computedialog import ComputeDialog
from pyheatmy import *


#path_point = 'C:/Users/Léa/Documents/MINES 2A/MOLONARI/INTERFACE/MOLO-projet-interface/molonari_data/study_ordiLea/Point001'
#os.chdir(path_point)
# Create processed temperatures plot

class TimeSeriesPlotCanvas(matplotlib.backends.backend_qt5agg.FigureCanvasQTAgg):

    def __init__(self, title, y_name, variable):
        
        self.variable = variable
        self.fig = matplotlib.figure.Figure()
        self.title = title
        self.axes = self.fig.add_subplot(111)
        self.ylab = y_name
        

        matplotlib.backends.backend_qt5agg.FigureCanvasQTAgg.__init__(self,self.fig)


    def setModel(self, model):

        self.model = model
    
    def plot(self):
        self.axes.cla()
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
        self.temps_from_tuple = None
        self.col = None 

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
        res = clnp.exec()
        if (res == QtWidgets.QDialog.Accepted) :
            mycleanupcode = clnp.getCode()
            print(mycleanupcode)
            clnp.saveCleanedUpData(mycleanupcode)
            
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

            

    def compute(self):
        self.compdlg = ComputeDialog()
        self.compdlg.pushButton_RunModel.clicked.connect(self.runmodel)
        self.compdlg.pushButton_Inversion.clicked.connect(self.runinversion)
        self.compdlg.exec()
            

    def runmodel(self) :
        dicParam = self.create_dicParam()
        print(dicParam)
        computeSolveTransi = self.create_computeSolveTransi()
        print(computeSolveTransi)
        self.self.col = self.column.from_dict(dicParam)
        params_tuple = computeSolveTransi[0]
        self.col.compute_solve_transi(params_tuple, computeSolveTransi[1])
        time = self.col.get_times_solve()
        dftime = pd.DataFrame(time)
        dftime.to_csv(f'{self.path_point}/res_time.csv')
        depths = self.col.get_depths_solve()
        dfdepths = pd.DataFrame(depths)
        dfdepths.to_csv(f'{self.path_point}/res_depths.csv')
        temps = self.col.get_temps_solve()
        dftemps = pd.DataFrame(temps)
        dftemps.to_csv(f'{self.path_point}/res_temps.csv')
        flows = self.col.get_flows_solve()
        dfflows = pd.DataFrame(flows)
        dfflows.to_csv(f'{self.path_point}/res_flows.csv')
        #advec = self.col.get_advec_flows_solve()
        #dfadvec = pd.DataFrame(advec)
        #dfadvec.to_csv(f'{self.path_point}/res_advec.csv')
        #conduc = self.col.get_conduc_flows_solve() 
        #dfconduc = pd.DataFrame(conduc)
        #dfconduc.to_csv(f'{self.path_point}/res_conduc.csv')
        

    def runinversion(self) :
        paramMCMC = self.create_paramMCMC()
        print(paramMCMC)
        self.col.compute_mcmc(nb_iter = paramMCMC[1], priors = paramMCMC[0], nb_cells = paramMCMC[2])
        

    def string_to_date (self, str) :
        return(datetime.strptime(str,"%Y/%m/%d %H:%M:%S"))
        

    def create_dicParam(self) :
        riv_bed = None
        depth_sensors = None
        offset = None
        dH_measures = None
        T_measures = []
        sigma_meas_P = None
        sigma_meas_T = None
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
        change_date = np.vectorize(self.string_to_date)
        dfp['Date']= change_date(dfp['Date'])
        dH_measures = list(zip(dfp['Date'].tolist(),list(zip(dfp['Pressure'].tolist(), dfp['Temperature'].tolist()))))
        #T_measures
        dft = self.dataTemperature
        dft['Date']= change_date(dft['Date'])
        T_measures = list(zip(dft['Date'].tolist(),list(zip(dft['T sensor 1'].tolist(),dft['T sensor 2'].tolist(),dft['T sensor 3'].tolist(),dft['T sensor 4'].tolist()))))
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
                'T_measures' : T_measures, 'sigma_meas_T' : sigma_meas_T, 'sigma_meas_P' : sigma_meas_P }
        return dic

    def create_computeSolveTransi(self) :
        moinslog10K = self.compdlg.doubleSpinBox_Permeability.value()
        lambda_s = self.compdlg.doubleSpinBox_Lambdas.value()
        n = self.compdlg.doubleSpinBox_Porosity.value()
        rhos_cs = self.compdlg.doubleSpinBox_ThermalCapacity.value()
        nb_cel = self.compdlg.lineEdit_CellsNumber.text()
        tuple = ((float(moinslog10K), float(lambda_s), float(n), float(rhos_cs)), int(float(nb_cel)))
        return tuple

    def create_paramMCMC(self) : 
        range_moinslog10K_min = float(self.compdlg.doubleSpinBox_PermeabilityMin.value())
        range_moinslog10K_max = float(self.compdlg.doubleSpinBox_PermeabilityMax.value())
        sigma_moinslog10K = float(self.compdlg.doubleSpinBox_PermeabilitySigma.value())

        range_lambda_s_min = float(self.compdlg.doubleSpinBox_LambdasMin.value())
        range_lambda_s_max = float(self.compdlg.doubleSpinBox_LambdasMax.value())
        sigma_lambda_s = float(self.compdlg.doubleSpinBox_LambdasSigma.value())

        range_n_min = float(self.compdlg.doubleSpinBox_PorosityMin.value())
        range_n_max = float(self.compdlg.doubleSpinBox_PorosityMax.value())
        sigma_n = float(self.compdlg.doubleSpinBox_PorositySigma.value())

        range_rhos_cs_min = float(self.compdlg.doubleSpinBox_ThermalCapacityMin.value())
        range_rhos_cs_max = float(self.compdlg.doubleSpinBox_ThermalCapacityMax.value())
        sigma_rhos_cs = float(self.compdlg.doubleSpinBox_ThermalCapacitySigma.value())

        priors = {'moinslog10K' : ((range_moinslog10K_min, range_moinslog10K_max), sigma_moinslog10K), 'lambda_s' : ((range_lambda_s_min, range_lambda_s_max), sigma_lambda_s), 'n' : ((range_n_min, range_n_max), sigma_n), 'rhos_cs' : ((range_rhos_cs_min, range_rhos_cs_max), sigma_rhos_cs)}

        nb_iter = int(float(self.compdlg.lineEdit_IterationsNumber.text()))
        nb_cel = int(float(self.compdlg.lineEdit_CellsNumberMCMC.text()))

        tuple = (priors, nb_iter, nb_cel)

        return tuple






        


    

    

   
